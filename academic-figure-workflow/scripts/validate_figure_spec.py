#!/usr/bin/env python3
"""Validate Academic FigureSpec v1 JSON without third-party dependencies.

Field shapes come from the sibling ``figure-spec.schema.json``, checked by a
small interpreter for the JSON Schema keywords that file uses.  This script
adds the cross-field invariants a schema cannot express: unique ids, declared
connection endpoints, group membership, absolute artifact paths, and the
render-ready gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from dataclasses import asdict, dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable, Iterator


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "figure-spec.schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
SHA256_PATTERN = re.compile(SCHEMA["properties"]["prompt_reviewed_sha256"]["pattern"])
SCHEMA_KEYWORDS = frozenset(
    {
        "$schema", "$id", "$defs", "title", "description",
        "$ref", "oneOf", "type", "const", "enum",
        "minLength", "pattern", "minimum", "maximum", "exclusiveMinimum",
        "items", "minItems", "properties", "required", "additionalProperties", "minProperties",
    }
)
JSON_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class ValidationReport:
    source: str = "<memory>"
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def error(self, code: str, path: str, message: str) -> None:
        self.diagnostics.append(Diagnostic("error", code, path, message))

    def warning(self, code: str, path: str, message: str) -> None:
        self.diagnostics.append(Diagnostic("warning", code, path, message))

    @property
    def errors(self) -> list[Diagnostic]:
        return [item for item in self.diagnostics if item.severity == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [item for item in self.diagnostics if item.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "ok": self.ok,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "diagnostics": [asdict(item) for item in self.diagnostics],
        }


def _is_json_type(value: Any, name: str) -> bool:
    if isinstance(value, bool) and name in {"integer", "number"}:
        return False
    return isinstance(value, JSON_TYPES[name])


def _schema_errors(value: Any, schema: dict[str, Any], path: str) -> Iterator[tuple[str, str, str]]:
    """Yield ``(keyword, path, message)`` for each schema violation."""

    unsupported = schema.keys() - SCHEMA_KEYWORDS
    if unsupported:
        raise ValueError(f"{SCHEMA_PATH.name} uses unsupported keyword(s): {sorted(unsupported)}")
    if "$ref" in schema:
        yield from _schema_errors(value, SCHEMA["$defs"][schema["$ref"].rsplit("/", 1)[-1]], path)
    if "oneOf" in schema:
        results = [list(_schema_errors(value, branch, path)) for branch in schema["oneOf"]]
        matches = sum(not errors for errors in results)
        if matches > 1:
            yield "oneOf", path, "matches more than one allowed shape"
        elif not matches:
            # Explain the closest branch: its type matched and it has the fewest violations.
            yield from min(results, key=lambda errors: (errors[0][:2] == ("type", path), len(errors)))
    names = schema.get("type")
    if names is not None:
        names = [names] if isinstance(names, str) else names
        if not any(_is_json_type(value, name) for name in names):
            yield "type", path, f"must be {' or '.join(names)}"
            return
    if "const" in schema and value != schema["const"]:
        yield "const", path, f"must be {schema['const']!r}"
    if "enum" in schema and value not in schema["enum"]:
        yield "enum", path, f"must be one of: {', '.join(map(str, schema['enum']))}"
    if isinstance(value, str):
        # minLength counts non-whitespace content so blank strings are rejected.
        if len(value.strip()) < schema.get("minLength", 0):
            yield "minLength", path, f"needs at least {schema['minLength']} non-blank character(s)"
        if "pattern" in schema and not re.search(schema["pattern"], value):
            yield "pattern", path, f"must match {schema['pattern']}"
    if _is_json_type(value, "number"):
        if "minimum" in schema and value < schema["minimum"]:
            yield "minimum", path, f"must be >= {schema['minimum']}"
        if "maximum" in schema and value > schema["maximum"]:
            yield "maximum", path, f"must be <= {schema['maximum']}"
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            yield "exclusiveMinimum", path, f"must be > {schema['exclusiveMinimum']}"
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            yield "minItems", path, f"needs at least {schema['minItems']} item(s)"
        if "items" in schema:
            for index, item in enumerate(value):
                yield from _schema_errors(item, schema["items"], f"{path}[{index}]")
    if isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            yield "minProperties", path, f"needs at least {schema['minProperties']} property(ies)"
        for key in schema.get("required", ()):
            if key not in value:
                yield "required", f"{path}.{key}", "is required"
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                yield from _schema_errors(item, properties[key], f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                yield "additionalProperties", f"{path}.{key}", "is not allowed here"


def _is_absolute_path(value: str) -> bool:
    return Path(value).is_absolute() or PureWindowsPath(value).is_absolute()


def _is_within_path(value: str, root: str) -> bool:
    """Return whether an absolute output path is contained by an absolute root."""

    windows_value = PureWindowsPath(value)
    windows_root = PureWindowsPath(root)
    if windows_value.is_absolute() or windows_root.is_absolute():
        if not (windows_value.is_absolute() and windows_root.is_absolute()):
            return False
        try:
            windows_value.relative_to(windows_root)
        except ValueError:
            return False
        return True
    try:
        Path(value).resolve(strict=False).relative_to(Path(root).resolve(strict=False))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def _resolved_native_path(value: str | Path) -> Path:
    """Return a native absolute path without requiring the leaf to exist."""

    return Path(value).expanduser().resolve(strict=False)


def _has_symlink_component(path: Path) -> bool:
    """Return whether an existing component of *path* is a symbolic link."""

    candidate = path if path.is_absolute() else path.absolute()
    for component in (candidate, *candidate.parents):
        try:
            if component.is_symlink():
                return True
        except (OSError, RuntimeError, ValueError):
            # Filesystem failures are handled by later existence/type checks.
            # They must not turn malformed or racy input into a crash.
            continue
    return False


def _objects(value: Any) -> list[tuple[int, dict[str, Any]]]:
    if not isinstance(value, list):
        return []
    return [(index, item) for index, item in enumerate(value) if isinstance(item, dict)]


def _declared_ids(
    report: ValidationReport,
    items: list[tuple[int, dict[str, Any]]],
    base: str,
    kind: str,
) -> set[str]:
    seen: set[str] = set()
    for index, item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            report.error(f"{kind}.id_duplicate", f"{base}[{index}].id", f"duplicate {kind} id {item_id!r}")
        seen.add(item_id)
    return seen


def _check_declared(
    report: ValidationReport,
    value: Any,
    path: str,
    declared: set[str],
    code: str,
    kind: str,
) -> None:
    if isinstance(value, str) and value not in declared:
        report.error(code, path, f"{value!r} does not name a declared {kind}")


def _validate_topology_references(report: ValidationReport, spec: dict[str, Any]) -> None:
    topology = spec.get("topology") if isinstance(spec.get("topology"), dict) else {}
    components = _objects(topology.get("components"))
    groups = _objects(topology.get("groups"))
    connections = _objects(topology.get("connections"))
    component_ids = _declared_ids(report, components, "$.topology.components", "component")
    group_ids = _declared_ids(report, groups, "$.topology.groups", "group")
    _declared_ids(report, connections, "$.topology.connections", "connection")

    for index, connection in connections:
        for key in ("from", "to"):
            _check_declared(
                report,
                connection.get(key),
                f"$.topology.connections[{index}].{key}",
                component_ids,
                "connection.endpoint_unknown",
                "component",
            )
    for index, component in components:
        _check_declared(
            report,
            component.get("group_id"),
            f"$.topology.components[{index}].group_id",
            group_ids,
            "component.group_unknown",
            "group",
        )
    for index, group in groups:
        members = group.get("component_ids")
        for member_index, member in enumerate(members if isinstance(members, list) else []):
            _check_declared(
                report,
                member,
                f"$.topology.groups[{index}].component_ids[{member_index}]",
                component_ids,
                "group.member_unknown",
                "component",
            )
    for index, item in _objects(spec.get("visible_text")):
        _check_declared(
            report,
            item.get("component_id"),
            f"$.visible_text[{index}].component_id",
            component_ids,
            "visible_text.component_unknown",
            "component",
        )
    layout = spec.get("layout") if isinstance(spec.get("layout"), dict) else {}
    _check_declared(
        report,
        layout.get("hero"),
        "$.layout.hero",
        component_ids | group_ids,
        "layout.hero_unknown",
        "component or group",
    )
    reading_order = layout.get("reading_order")
    for index, item in enumerate(reading_order if isinstance(reading_order, list) else []):
        _check_declared(
            report,
            item,
            f"$.layout.reading_order[{index}]",
            component_ids,
            "layout.reading_order_unknown",
            "component",
        )


def _validate_local_reference_path(
    report: ValidationReport,
    value: Any,
    path: str,
    *,
    render_ready: bool,
) -> None:
    if not isinstance(value, str):
        return
    if not _is_absolute_path(value):
        report.error(
            "reference_image.not_absolute",
            path,
            "local reference image path must be absolute",
        )
        return
    if not render_ready:
        return

    candidate = Path(value)
    try:
        if _has_symlink_component(candidate):
            report.error(
                "reference_image.symlink",
                path,
                "render-ready local reference must not contain a symbolic-link component",
            )
            return
        mode = candidate.lstat().st_mode
        candidate.resolve(strict=True)
        if not stat.S_ISREG(mode):
            report.error(
                "reference_image.not_file",
                path,
                "render-ready local reference must be a regular file",
            )
    except FileNotFoundError:
        report.error(
            "reference_image.missing",
            path,
            "render-ready local reference does not exist",
        )
    except (OSError, RuntimeError, ValueError) as exc:
        report.error(
            "reference_image.inaccessible",
            path,
            f"cannot inspect render-ready local reference: {exc}",
        )


def _validate_artifacts(report: ValidationReport, spec: dict[str, Any], *, render_ready: bool) -> None:
    workspace_root = spec.get("workspace_root")
    output_path = spec.get("output_path")
    for key, value in (("workspace_root", workspace_root), ("output_path", output_path)):
        if isinstance(value, str) and value.strip() and not _is_absolute_path(value):
            report.error(f"{key}.not_absolute", f"$.{key}", f"{key} must be absolute")
    if (
        isinstance(output_path, str)
        and isinstance(workspace_root, str)
        and _is_absolute_path(output_path)
        and _is_absolute_path(workspace_root)
        and not _is_within_path(output_path, workspace_root)
    ):
        report.error(
            "output_path.outside_workspace",
            "$.output_path",
            "output_path must be inside workspace_root",
        )

    references = spec.get("reference_images")
    mechanisms: set[str] = set()
    for index, reference in enumerate(references if isinstance(references, list) else []):
        path = f"$.reference_images[{index}]"
        kind = reference.get("kind") if isinstance(reference, dict) else None
        if isinstance(reference, str):
            mechanisms.add("local_path")
            _validate_local_reference_path(report, reference, path, render_ready=render_ready)
        elif kind == "local_path":
            mechanisms.add("local_path")
            _validate_local_reference_path(
                report, reference.get("path"), f"{path}.path", render_ready=render_ready
            )
        elif kind == "recent_conversation":
            mechanisms.add("recent_conversation")
            if render_ready:
                report.warning(
                    "reference_image.nonreproducible",
                    path,
                    "recent-conversation ordinals are call-relative; persist a stable asset id or local copy for reproducibility",
                )
    if len(mechanisms) > 1:
        report.error(
            "reference_image.mixed_mechanisms",
            "$.reference_images",
            "local paths and recent-conversation images cannot be sent in one native image call",
        )

    profile = spec.get("style_profile")
    if isinstance(profile, dict):
        profile = profile.get("id")
    if profile == "reference-led" and not references:
        report.error(
            "style_profile.reference_missing",
            "$.reference_images",
            "reference-led style requires at least one local or recent-conversation reference image",
        )


def _validate_workspace_trust(
    report: ValidationReport,
    spec: dict[str, Any],
    *,
    trusted_workspace_root: str | Path | None,
    required: bool,
) -> None:
    if trusted_workspace_root is None:
        if required:
            report.error(
                "workspace_root.trusted_required",
                "$.workspace_root",
                "render-ready validation requires a trusted workspace root from the caller",
            )
        return
    if not isinstance(trusted_workspace_root, (str, Path)):
        report.error(
            "workspace_root.trusted_invalid",
            "$.workspace_root",
            "trusted workspace root must be a filesystem path",
        )
        return

    try:
        trusted = _resolved_native_path(trusted_workspace_root)
        if not trusted.exists() or not trusted.is_dir():
            report.error(
                "workspace_root.trusted_not_directory",
                "$.workspace_root",
                f"trusted workspace root must resolve to an existing directory: {trusted}",
            )
            return
    except (OSError, RuntimeError, ValueError) as exc:
        report.error(
            "workspace_root.trusted_inaccessible",
            "$.workspace_root",
            f"cannot inspect trusted workspace root {trusted_workspace_root}: {exc}",
        )
        return
    declared = spec.get("workspace_root")
    if not isinstance(declared, str) or not Path(declared).is_absolute():
        report.error(
            "workspace_root.trusted_mismatch",
            "$.workspace_root",
            f"declared workspace_root must equal trusted native root {trusted}",
        )
        return
    try:
        declared_root = _resolved_native_path(declared)
    except (OSError, RuntimeError, ValueError) as exc:
        report.error(
            "workspace_root.invalid",
            "$.workspace_root",
            f"cannot resolve declared workspace_root: {exc}",
        )
        return
    if declared_root != trusted:
        report.error(
            "workspace_root.trusted_mismatch",
            "$.workspace_root",
            f"declared workspace_root must equal trusted root {trusted}",
        )

    output = spec.get("output_path")
    if not isinstance(output, str) or not Path(output).is_absolute():
        return
    output_candidate = Path(output)
    try:
        if output_candidate.is_symlink():
            report.error(
                "output_path.symlink",
                "$.output_path",
                "render-ready output_path must not itself be a symbolic link",
            )
    except (OSError, RuntimeError, ValueError) as exc:
        report.error(
            "output_path.inaccessible",
            "$.output_path",
            f"cannot inspect render-ready output_path: {exc}",
        )
        return
    try:
        resolved_output = output_candidate.resolve(strict=False)
        resolved_output.relative_to(trusted)
    except (OSError, RuntimeError, ValueError):
        report.error(
            "output_path.outside_trusted_workspace",
            "$.output_path",
            f"output_path must be inside trusted workspace root {trusted}",
        )


def _validate_render_readiness(
    report: ValidationReport,
    spec: dict[str, Any],
    *,
    trusted_workspace_root: str | Path | None,
) -> None:
    selection = spec.get("style_selection")
    if selection not in {"confirmed", "waived"}:
        report.error(
            "style_selection.render_blocked",
            "$.style_selection",
            "style selection is missing or pending; rendering is blocked until the user chooses a style",
        )
    elif selection == "confirmed":
        preset = spec.get("style_preset")
        profile = spec.get("style_profile")
        if isinstance(profile, dict):
            profile = profile.get("id")
        references = spec.get("reference_images")
        has_preset = isinstance(preset, str) and bool(preset.strip())
        has_reference = isinstance(references, list) and len(references) > 0
        if not has_preset and not (profile == "reference-led" and has_reference):
            report.error(
                "style_selection.unconfirmed",
                "$.style_selection",
                "confirmed style selection requires a non-empty style_preset, or reference-led with a reference image",
            )

    review = spec.get("prompt_review")
    if review in {"requested", "waived"} and "prompt_reviewed_sha256" in spec:
        report.error(
            "prompt_reviewed_sha256.unexpected",
            "$.prompt_reviewed_sha256",
            "prompt_reviewed_sha256 is permitted only when prompt_review is confirmed",
        )
    if review == "requested":
        report.error(
            "prompt_review.render_blocked",
            "$.prompt_review",
            "prompt review is requested; rendering is blocked until confirmation",
        )
    elif review == "confirmed":
        prompt = spec.get("prompt")
        reviewed_digest = spec.get("prompt_reviewed_sha256")
        if reviewed_digest is None:
            report.error(
                "prompt_reviewed_sha256.required",
                "$.prompt_reviewed_sha256",
                "confirmed prompt review requires the reviewed prompt SHA-256 digest",
            )
        elif (
            isinstance(prompt, str)
            and isinstance(reviewed_digest, str)
            and SHA256_PATTERN.search(reviewed_digest)
        ):
            try:
                current_digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            except UnicodeEncodeError as exc:
                report.error(
                    "prompt.utf8_invalid",
                    "$.prompt",
                    f"confirmed prompt cannot be encoded as UTF-8: {exc}",
                )
            else:
                if reviewed_digest != current_digest:
                    report.error(
                        "prompt_reviewed_sha256.mismatch",
                        "$.prompt_reviewed_sha256",
                        "reviewed digest does not match the current UTF-8 prompt",
                    )

    _validate_workspace_trust(
        report,
        spec,
        trusted_workspace_root=trusted_workspace_root,
        required=True,
    )


def validate_spec(
    spec: Any,
    *,
    render_ready: bool = False,
    trusted_workspace_root: str | Path | None = None,
    source: str = "<memory>",
) -> ValidationReport:
    """Validate a decoded figure spec and return all diagnostics."""

    report = ValidationReport(source=source)
    for keyword, path, message in _schema_errors(spec, SCHEMA, "$"):
        report.error(f"schema.{keyword}", path, message)
    if not isinstance(spec, dict):
        return report
    _validate_topology_references(report, spec)
    _validate_artifacts(report, spec, render_ready=render_ready)
    if render_ready:
        _validate_render_readiness(
            report,
            spec,
            trusted_workspace_root=trusted_workspace_root,
        )
    elif trusted_workspace_root is not None:
        _validate_workspace_trust(
            report,
            spec,
            trusted_workspace_root=trusted_workspace_root,
            required=False,
        )
    return report


def validate_path(
    path: Path,
    *,
    render_ready: bool = False,
    trusted_workspace_root: str | Path | None = None,
) -> ValidationReport:
    """Load and validate one JSON file."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        report = ValidationReport(source=str(path))
        report.error("json.invalid", "$", str(exc))
        return report
    return validate_spec(
        data,
        render_ready=render_ready,
        trusted_workspace_root=trusted_workspace_root,
        source=str(path),
    )


def print_reports(reports: Iterable[ValidationReport]) -> None:
    for report in reports:
        status = "PASS" if report.ok else "FAIL"
        print(f"{status} {report.source} ({len(report.errors)} error(s), {len(report.warnings)} warning(s))")
        for item in report.diagnostics:
            print(f"  {item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="figure spec JSON file(s)")
    parser.add_argument(
        "--render-ready",
        action="store_true",
        help="enforce prompt-review, trusted-workspace, and local-reference render gates",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="trusted native workspace boundary (required with --render-ready)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable diagnostics")
    # Separately installed skills of older pack versions still pass this retired flag.
    parser.add_argument("--strict-v1", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    reports = [
        validate_path(
            path,
            render_ready=args.render_ready,
            trusted_workspace_root=args.workspace_root,
        )
        for path in args.paths
    ]
    if args.json:
        print(json.dumps([report.to_dict() for report in reports], indent=2, ensure_ascii=False))
    else:
        print_reports(reports)
    return 0 if all(report.ok for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
