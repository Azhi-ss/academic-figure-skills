#!/usr/bin/env python3
"""Validate skill-pack metadata, shared references, and figure specs.

The checker is intentionally standard-library-only so it can run in a fresh
checkout and in lightweight CI.  It validates the subset of SKILL.md frontmatter
supported by Codex/Agent Skills, checks manifest versions against
``metadata.version``, detects vendored-copy drift, and delegates the example
FigureSpecs in ``docs/prompts/`` to ``validate_figure_spec.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(PACK_ROOT / "academic-figure-designer" / "scripts"))

from sync_shared_refs import SyncItem, build_sync_plan, load_skill_paths  # noqa: E402
from validate_figure_spec import ValidationReport, print_reports, validate_path  # noqa: E402


CODEX_FRONTMATTER_KEYS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
FRONTMATTER_KEY_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")


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


def validate_skills(root: Path, report: ValidationReport) -> None:
    """Validate manifest entries and Codex-compatible SKILL.md frontmatter."""

    root = root.resolve()
    manifest_path = root / "manifest.json"
    try:
        skill_paths = load_skill_paths(root)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        report.error("manifest.invalid", str(manifest_path), str(exc))
        return
    pack_version = manifest.get("version")
    if not (isinstance(pack_version, str) and SEMVER_PATTERN.fullmatch(pack_version)):
        report.error("manifest.version_invalid", str(manifest_path), "manifest version must be semantic versioning")
    manifest_versions = {entry["id"]: entry.get("version") for entry in manifest["skills"]}

    for skill_id, skill_dir in skill_paths.items():
        skill_file = skill_dir / "SKILL.md"
        display = str(skill_file)
        try:
            frontmatter = parse_skill_frontmatter(skill_file)
        except FrontmatterError as exc:
            report.error("frontmatter.invalid", display, str(exc))
            continue

        unknown = sorted(set(frontmatter) - CODEX_FRONTMATTER_KEYS)
        if unknown:
            report.error(
                "frontmatter.keys_unsupported",
                display,
                f"unsupported Codex frontmatter key(s): {', '.join(unknown)}",
            )
        for required in ("name", "description"):
            if not isinstance(frontmatter.get(required), str) or not frontmatter[required].strip():
                report.error("frontmatter.required", display, f"required field {required!r} is missing or empty")

        name = frontmatter.get("name")
        if isinstance(name, str):
            if len(name) > 64 or not SKILL_NAME_PATTERN.fullmatch(name):
                report.error(
                    "frontmatter.name_invalid",
                    display,
                    "name must be <=64 characters of lowercase letters, digits, and single hyphens",
                )
            if name != skill_dir.name:
                report.error(
                    "frontmatter.name_path_mismatch",
                    display,
                    f"frontmatter name {name!r} must equal directory name {skill_dir.name!r}",
                )
            if name != skill_id:
                report.error(
                    "frontmatter.name_manifest_mismatch",
                    display,
                    f"frontmatter name {name!r} must equal manifest id {skill_id!r}",
                )
        description = frontmatter.get("description")
        if isinstance(description, str) and len(description) > 1024:
            report.error("frontmatter.description_too_long", display, "description exceeds 1024 characters")

        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict):
            report.error("frontmatter.metadata_required", display, "metadata mapping is required")
            continue
        skill_version = metadata.get("version")
        if not isinstance(skill_version, str) or not SEMVER_PATTERN.fullmatch(skill_version):
            report.error(
                "frontmatter.version_invalid",
                display,
                "metadata.version must be a semantic-version string",
            )
            continue
        manifest_version = manifest_versions[skill_id]
        if manifest_version != skill_version:
            report.error(
                "manifest.version_drift",
                display,
                f"manifest version {manifest_version!r} != metadata.version {skill_version!r}",
            )

    registered = set(skill_paths.values())
    for skill_file in sorted(root.glob("*/SKILL.md")):
        if skill_file.parent.resolve() not in registered:
            report.error(
                "manifest.skill_unregistered",
                str(skill_file),
                f"skill directory {skill_file.parent.name!r} is missing from manifest.json",
            )


def validate_reference_items(
    root: Path,
    items: Iterable[SyncItem],
    report: ValidationReport,
) -> None:
    """Compare canonical sources with their vendored copies."""

    for item in items:
        target = str(item.target.relative_to(root))
        if not item.source.is_file():
            report.error("reference.source_missing", str(item.source.relative_to(root)), "canonical shared file is missing")
        elif not item.target.is_file():
            report.error("reference.target_missing", target, "vendored copy is missing; run sync_shared_refs.py")
        elif not item.in_sync:
            report.error("reference.drift", target, f"vendored copy differs from {item.source.relative_to(root)}")


def validate_vendored_style_sets(
    root: Path,
    items: Iterable[SyncItem],
    report: ValidationReport,
) -> None:
    """Reject vendored style Markdown files absent from the canonical library."""

    expected: dict[Path, set[str]] = {}
    for item in items:
        if item.source.parent == root / "docs" / "styles":
            expected.setdefault(item.target.parent, set()).add(item.target.name)
    for style_dir, names in sorted(expected.items()):
        for entry in sorted(style_dir.glob("*.md")):
            if entry.name not in names:
                report.error(
                    "reference.style_extra",
                    str(entry.relative_to(root)),
                    "vendored style is not present in docs/styles; remove the stale copy",
                )


def validate_shared_refs(root: Path, report: ValidationReport) -> None:
    root = root.resolve()
    try:
        plan = build_sync_plan(root)
    except (OSError, ValueError) as exc:
        report.error("reference.plan_invalid", str(root), str(exc))
        return
    validate_reference_items(root, plan, report)
    validate_vendored_style_sets(root, plan, report)


def validate_figure_specs(root: Path, report: ValidationReport) -> None:
    paths = sorted((root / "docs" / "prompts").glob("*.spec.json"))
    if not paths:
        report.warning("figure.none", str(root), "no figure specs found in docs/prompts")
    for path in paths:
        for item in validate_path(path).diagnostics:
            add = report.error if item.severity == "error" else report.warning
            add(f"figure.{item.code}", str(path.relative_to(root)), f"{item.path}: {item.message}")


def validate_pack(root: Path) -> ValidationReport:
    root = root.resolve()
    report = ValidationReport(source=str(root))
    validate_skills(root, report)
    validate_shared_refs(root, report)
    validate_figure_specs(root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=PACK_ROOT,
        help="skill-pack root (default: repository containing this script)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable diagnostics")
    args = parser.parse_args(argv)

    report = validate_pack(args.root)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print_reports([report])
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
