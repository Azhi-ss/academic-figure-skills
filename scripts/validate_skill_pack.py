#!/usr/bin/env python3
"""Validate skill-pack metadata, shared references, and figure specs.

The checker is intentionally standard-library-only so it can run in a fresh
checkout and in lightweight CI.  It validates the subset of SKILL.md frontmatter
supported by Codex/Agent Skills, checks manifest versions against
``metadata.version``, detects vendored-reference drift by SHA-256, and delegates
figure topology checks to ``validate_figure_spec.py``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(PACK_ROOT / "academic-figure-designer" / "scripts"))

from sync_shared_refs import (  # noqa: E402
    SyncItem,
    build_sync_plan,
    contains_symlink_component,
    file_digest,
    validate_sync_target,
)
from validate_figure_spec import (  # noqa: E402
    SCHEMA_V1,
    STYLE_PROFILE_IDS,
    V1_REQUIRED,
    ValidationReport as FigureValidationReport,
    validate_path as validate_figure_path,
)


CODEX_FRONTMATTER_KEYS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
FRONTMATTER_KEY_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")


@dataclass(frozen=True)
class PackDiagnostic:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class PackReport:
    root: str
    diagnostics: list[PackDiagnostic] = field(default_factory=list)

    def error(self, code: str, path: str | Path, message: str) -> None:
        self.diagnostics.append(PackDiagnostic("error", code, str(path), message))

    def warning(self, code: str, path: str | Path, message: str) -> None:
        self.diagnostics.append(PackDiagnostic("warning", code, str(path), message))

    @property
    def errors(self) -> list[PackDiagnostic]:
        return [item for item in self.diagnostics if item.severity == "error"]

    @property
    def warnings(self) -> list[PackDiagnostic]:
        return [item for item in self.diagnostics if item.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "ok": self.ok,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "diagnostics": [asdict(item) for item in self.diagnostics],
        }


class FrontmatterError(ValueError):
    pass


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_skill_frontmatter(path: Path) -> dict[str, Any]:
    """Parse the simple frontmatter shape used by Codex SKILL.md files.

    A full YAML parser is deliberately unnecessary: Codex top-level fields are
    scalar values plus a shallow ``metadata`` mapping.  Block scalar bodies are
    retained as joined text so folded descriptions remain valid.
    """

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise FrontmatterError(str(exc)) from exc
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("SKILL.md must start with a YAML frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise FrontmatterError("frontmatter closing delimiter is missing") from exc

    result: dict[str, Any] = {}
    current_block: str | None = None
    block_lines: list[str] = []

    def finish_block() -> None:
        nonlocal current_block, block_lines
        if current_block is not None:
            result[current_block] = " ".join(part.strip() for part in block_lines if part.strip())
        current_block = None
        block_lines = []

    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_block is not None:
                block_lines.append(line)
                continue
            metadata = result.get("metadata")
            if not isinstance(metadata, dict):
                raise FrontmatterError(f"line {line_number}: unexpected indentation")
            match = FRONTMATTER_KEY_PATTERN.match(line.strip())
            if not match:
                raise FrontmatterError(f"line {line_number}: malformed metadata entry")
            key, raw = match.group(1), match.group(2) or ""
            if key in metadata:
                raise FrontmatterError(f"line {line_number}: duplicate metadata key {key!r}")
            metadata[key] = _scalar(raw)
            continue

        finish_block()
        match = FRONTMATTER_KEY_PATTERN.match(line)
        if not match:
            raise FrontmatterError(f"line {line_number}: malformed top-level entry")
        key, raw = match.group(1), match.group(2) or ""
        if key in result:
            raise FrontmatterError(f"line {line_number}: duplicate top-level key {key!r}")
        if key == "metadata" and not raw:
            result[key] = {}
        elif raw in {"|", "|-", ">", ">-"}:
            current_block = key
        else:
            result[key] = _scalar(raw)
    finish_block()
    return result


def load_manifest(root: Path, report: PackReport) -> dict[str, Any] | None:
    path = root / "manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        report.error("manifest.invalid", path, str(exc))
        return None
    if not isinstance(data, dict):
        report.error("manifest.type", path, "manifest must be a JSON object")
        return None
    if not isinstance(data.get("skills"), list):
        report.error("manifest.skills_type", path, "manifest 'skills' must be a list")
        return None
    version = data.get("version")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        report.error("manifest.version_invalid", path, "manifest version must be semantic versioning")
    return data


def _safe_skill_dir(root: Path, raw_path: Any) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path:
        return None
    root = root.resolve()
    candidate = Path(os.path.abspath(os.fspath(root / raw_path)))
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if contains_symlink_component(root, candidate):
        return None
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return None
    return resolved


def _discover_top_level_skill_files(root: Path) -> list[Path]:
    """Return lexical ``*/SKILL.md`` paths without traversing directory symlinks."""

    files: list[Path] = []
    for directory in root.iterdir():
        if directory.is_symlink() or not directory.is_dir():
            continue
        skill_file = directory / "SKILL.md"
        if skill_file.is_symlink() or skill_file.is_file():
            files.append(skill_file)
    return sorted(files, key=lambda path: path.as_posix())


def validate_skills(root: Path, report: PackReport, manifest: dict[str, Any] | None = None) -> None:
    """Validate manifest entries and Codex-compatible SKILL.md frontmatter."""

    root = root.resolve()
    manifest = manifest if manifest is not None else load_manifest(root, report)
    if manifest is None:
        return
    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for index, entry in enumerate(manifest["skills"]):
        manifest_path = f"manifest.json:skills[{index}]"
        if not isinstance(entry, dict):
            report.error("manifest.skill_type", manifest_path, "skill entry must be an object")
            continue
        skill_id = entry.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            report.error("manifest.skill_id", manifest_path, "skill id must be a non-empty string")
            continue
        if skill_id in seen_ids:
            report.error("manifest.skill_id_duplicate", manifest_path, f"duplicate skill id {skill_id!r}")
        seen_ids.add(skill_id)

        skill_dir = _safe_skill_dir(root, entry.get("path"))
        if skill_dir is None:
            report.error(
                "manifest.skill_path",
                manifest_path,
                "skill path is missing, escapes the repository, or contains a symlink",
            )
            continue
        if skill_dir in seen_paths:
            report.error("manifest.skill_path_duplicate", manifest_path, f"duplicate skill path {skill_dir}")
        seen_paths.add(skill_dir)
        skill_file = skill_dir / "SKILL.md"
        if contains_symlink_component(root, skill_file):
            report.error(
                "frontmatter.path_symlink",
                skill_file,
                "SKILL.md and each parent path must be real paths, not symlinks",
            )
            continue
        try:
            frontmatter = parse_skill_frontmatter(skill_file)
        except FrontmatterError as exc:
            report.error("frontmatter.invalid", skill_file, str(exc))
            continue

        unknown = sorted(set(frontmatter) - CODEX_FRONTMATTER_KEYS)
        if unknown:
            report.error(
                "frontmatter.keys_unsupported",
                skill_file,
                f"unsupported Codex frontmatter key(s): {', '.join(unknown)}",
            )
        for required in ("name", "description"):
            if not isinstance(frontmatter.get(required), str) or not frontmatter[required].strip():
                report.error("frontmatter.required", skill_file, f"required field {required!r} is missing or empty")

        name = frontmatter.get("name")
        if isinstance(name, str):
            if len(name) > 64 or not SKILL_NAME_PATTERN.fullmatch(name):
                report.error(
                    "frontmatter.name_invalid",
                    skill_file,
                    "name must be <=64 characters of lowercase letters, digits, and single hyphens",
                )
            if name != skill_dir.name:
                report.error(
                    "frontmatter.name_path_mismatch",
                    skill_file,
                    f"frontmatter name {name!r} must equal directory name {skill_dir.name!r}",
                )
            if name != skill_id:
                report.error(
                    "frontmatter.name_manifest_mismatch",
                    skill_file,
                    f"frontmatter name {name!r} must equal manifest id {skill_id!r}",
                )
        description = frontmatter.get("description")
        if isinstance(description, str) and len(description) > 1024:
            report.error("frontmatter.description_too_long", skill_file, "description exceeds 1024 characters")

        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict):
            report.error("frontmatter.metadata_required", skill_file, "metadata mapping is required")
            continue
        skill_version = metadata.get("version")
        if not isinstance(skill_version, str) or not SEMVER_PATTERN.fullmatch(skill_version):
            report.error(
                "frontmatter.version_invalid",
                skill_file,
                "metadata.version must be a semantic-version string",
            )
            continue
        manifest_version = entry.get("version")
        if manifest_version != skill_version:
            report.error(
                "manifest.version_drift",
                skill_file,
                f"manifest version {manifest_version!r} != metadata.version {skill_version!r}",
            )

    try:
        actual_skill_files = _discover_top_level_skill_files(root)
    except OSError as exc:
        report.error("manifest.skill_scan_failed", root, str(exc))
        return
    for skill_file in actual_skill_files:
        if skill_file.parent.resolve() not in seen_paths:
            report.error(
                "manifest.skill_unregistered",
                skill_file,
                f"skill directory {skill_file.parent.name!r} is missing from manifest.json",
            )

    worker_prompt = root / "academic-figure-workflow" / "prompts" / "figure-worker.md"
    try:
        worker_text = worker_prompt.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error("worker_prompt.missing", worker_prompt, str(exc))
    else:
        required_worker_fields = (
            "- task kind:",
            "- owned output paths:",
            "- acceptance criteria:",
            "- status: success | blocked | failed",
            "- artifacts:",
            "- summary:",
            "- validation:",
            "- residual risks:",
            "- evidence:",
            "- next action:",
        )
        for required_field in required_worker_fields:
            if required_field not in worker_text:
                report.error(
                    "worker_prompt.contract",
                    worker_prompt,
                    f"required worker contract field is missing: {required_field}",
                )


def validate_reference_items(
    root: Path,
    items: Iterable[SyncItem],
    report: PackReport,
) -> None:
    """Compare canonical and vendored reference hashes."""

    root = root.resolve()
    for item in items:
        try:
            display = item.target.relative_to(root)
        except ValueError:
            display = item.target
        try:
            validate_sync_target(root, item.target)
        except ValueError as exc:
            code = (
                "reference.target_symlink"
                if contains_symlink_component(root, item.target)
                else "reference.target_unsafe"
            )
            report.error(code, display, str(exc))
            continue
        if not item.source.is_file():
            report.error("reference.source_missing", item.source, "canonical shared reference is missing")
            continue
        if not item.target.is_file():
            report.error("reference.target_missing", display, "vendored shared reference is missing; run sync_shared_refs.py")
            continue
        if item.target.is_symlink():
            report.error(
                "reference.target_symlink",
                display,
                "vendored reference must be a real self-contained file, not a symlink",
            )
            continue
        if file_digest(item.source) != file_digest(item.target):
            report.error("reference.drift", display, f"vendored copy differs from {item.source.relative_to(root)}")


def validate_vendored_style_sets(
    root: Path,
    items: Iterable[SyncItem],
    report: PackReport,
) -> None:
    """Reject vendored style Markdown files absent from the canonical library."""

    root = root.resolve()
    canonical_style_dir = root / "docs" / "styles"
    expected_by_directory: dict[Path, set[str]] = {}
    for item in items:
        if item.source.parent != canonical_style_dir:
            continue
        expected_by_directory.setdefault(item.target.parent, set()).add(item.target.name)

    for style_dir, expected_names in sorted(
        expected_by_directory.items(), key=lambda pair: pair[0].as_posix()
    ):
        if not style_dir.exists():
            continue
        try:
            validate_sync_target(root, style_dir / ".style-scan-sentinel")
            entries = list(style_dir.iterdir())
        except (OSError, ValueError) as exc:
            report.error("reference.style_directory_unsafe", style_dir, str(exc))
            continue
        for entry in sorted(entries, key=lambda path: path.name):
            if entry.suffix.casefold() != ".md" or entry.name in expected_names:
                continue
            try:
                display = entry.relative_to(root)
            except ValueError:
                display = entry
            report.error(
                "reference.style_extra",
                display,
                "vendored style is not present in docs/styles; remove the stale copy",
            )


def validate_shared_refs(root: Path, report: PackReport) -> None:
    try:
        plan = build_sync_plan(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.error("reference.plan_invalid", root, str(exc))
        return
    validate_reference_items(root, plan, report)
    validate_vendored_style_sets(root, plan, report)


def validate_schema_file(root: Path, report: PackReport) -> None:
    path = root / "academic-figure-designer" / "figure-spec.schema.json"
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        report.error("figure_schema.invalid", path, str(exc))
        return
    if schema.get("properties", {}).get("schema", {}).get("const") != SCHEMA_V1:
        report.error("figure_schema.version", path, f"schema const must be {SCHEMA_V1!r}")
    required = schema.get("required")
    if not isinstance(required, list) or set(required) != set(V1_REQUIRED):
        report.error(
            "figure_schema.required_fields",
            path,
            "schema required fields and validator V1_REQUIRED differ",
        )
    enum = (
        schema.get("$defs", {})
        .get("styleProfileId", {})
        .get("enum")
    )
    if not isinstance(enum, list) or set(enum) != set(STYLE_PROFILE_IDS):
        report.error("figure_schema.style_profiles", path, "style profile enum and validator constants differ")
    connection_required = (
        schema.get("$defs", {}).get("connection", {}).get("required")
    )
    if not isinstance(connection_required, list) or "direction" not in connection_required:
        report.error(
            "figure_schema.connection_direction",
            path,
            "strict connection schema must require direction",
        )


def _figure_spec_paths(root: Path) -> list[Path]:
    paths = set((root / "examples" / "benchmarks").glob("*/prompt-spec.json"))
    paths.update(root.rglob("*.figure-spec.json"))
    return sorted(path for path in paths if path.is_file())


def _merge_figure_report(pack_report: PackReport, figure_report: FigureValidationReport) -> None:
    for item in figure_report.diagnostics:
        message = f"{item.path}: {item.message}"
        if item.severity == "error":
            pack_report.error(f"figure.{item.code}", figure_report.source, message)
        else:
            pack_report.warning(f"figure.{item.code}", figure_report.source, message)


def validate_figure_specs(root: Path, report: PackReport, *, strict_v1: bool = False) -> None:
    paths = _figure_spec_paths(root)
    if not paths:
        report.warning("figure.none", root, "no figure specs found")
        return
    for path in paths:
        _merge_figure_report(report, validate_figure_path(path, strict_v1=strict_v1))


def validate_pack(root: Path, *, strict_v1: bool = False) -> PackReport:
    root = root.resolve()
    report = PackReport(root=str(root))
    manifest = load_manifest(root, report)
    validate_skills(root, report, manifest)
    validate_shared_refs(root, report)
    validate_schema_file(root, report)
    validate_figure_specs(root, report, strict_v1=strict_v1)
    return report


def _print_human(report: PackReport) -> None:
    status = "PASS" if report.ok else "FAIL"
    print(f"{status} {report.root} ({len(report.errors)} error(s), {len(report.warnings)} warning(s))")
    for item in report.diagnostics:
        print(f"  {item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=PACK_ROOT,
        help="skill-pack root (default: repository containing this script)",
    )
    parser.add_argument(
        "--strict-v1",
        action="store_true",
        help="require every discovered figure spec to use FigureSpec v1",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable diagnostics")
    args = parser.parse_args(argv)

    report = validate_pack(args.root, strict_v1=args.strict_v1)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        _print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
