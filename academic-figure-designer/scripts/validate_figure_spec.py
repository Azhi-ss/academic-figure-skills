#!/usr/bin/env python3
"""Validate Academic FigureSpec JSON without third-party dependencies.

Default mode accepts historical benchmark specs and emits migration warnings.
``--strict-v1`` requires the versioned ``academic-figure/FigureSpec@1`` handoff.
JSON Schema handles local field shapes; this validator additionally enforces
cross-field invariants: unique component ids, valid connection endpoints, known
style profiles, group membership, and absolute artifact paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from dataclasses import asdict, dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable


SCHEMA_V1 = "academic-figure/FigureSpec@1"
ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")
ASPECT_RATIOS = frozenset({"16:9", "3:2", "4:3", "1:1"})
CONNECTION_DIRECTIONS = frozenset({"forward", "backward", "bidirectional"})
PROMPT_REVIEW_STATES = frozenset({"requested", "confirmed", "waived"})
VISIBLE_TEXT_PRIORITIES = frozenset({"primary", "secondary", "optional"})
STYLE_SOURCES = frozenset({"user", "reference", "scene", "default"})
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
LAYOUT_COMPOSITIONS = frozenset(
    {
        "pipeline",
        "loop",
        "storyboard",
        "layered_boundary",
        "central_mechanism",
        "modular_collage",
        "comparison_grid",
        "custom",
    }
)
STYLE_PROFILE_IDS = frozenset(
    {
        "classic-technical",
        "modern-technical-vector",
        "pastel-airy-ui",
        "illustrated-modular",
        "reference-led",
    }
)
STYLE_PROFILE_ALIASES = {
    "Classic technical": "classic-technical",
    "Pastel airy UI": "pastel-airy-ui",
    "Illustrated modular": "illustrated-modular",
    "Reference-led": "reference-led",
    "classic-academic-border": "classic-technical",
    "modern-technical-vector": "classic-technical",
    "modern-pastel-airy": "pastel-airy-ui",
    "nature-blue-minimal": "classic-technical",
    "okabe-ito-universal": "classic-technical",
    "purple-green-comparison": "classic-technical",
    "print-safe-grayscale": "classic-technical",
    "reference-derived": "reference-led",
    "custom": "reference-led",
    "经典学术框线风": "classic-technical",
    "现代前沿技术框线风": "classic-technical",
    "现代柔彩空气风": "pastel-airy-ui",
    "有色语义分区图示风": "illustrated-modular",
    "编辑手绘模块风": "illustrated-modular",
    "顶刊蓝调极简风": "classic-technical",
    "通用色盲友好风": "classic-technical",
    "对比消融实验风": "classic-technical",
    "严谨黑白印刷风": "classic-technical",
    "Classic academic": "classic-technical",
    "Pastel airy": "pastel-airy-ui",
}
V1_REQUIRED = (
    "schema",
    "figure_id",
    "plan_revision",
    "sources",
    "prompt",
    "aspect_ratio",
    "final_width_mm",
    "visible_text",
    "layout",
    "topology",
    "style_profile",
    "style_grammar",
    "semantic_color_roles",
    "reference_images",
    "must_not_claim",
    "forbidden_connections",
    "negative_constraints",
    "prompt_review",
    "workspace_root",
    "output_path",
)


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class ValidationReport:
    source: str = "<memory>"
    mode: str = "compatible"
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
            "mode": self.mode,
            "ok": self.ok,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "diagnostics": [asdict(item) for item in self.diagnostics],
        }


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


def _is_id(value: Any) -> bool:
    return isinstance(value, str) and bool(ID_PATTERN.fullmatch(value))


def _expect_type(
    report: ValidationReport,
    value: Any,
    expected: type | tuple[type, ...],
    path: str,
    label: str,
) -> bool:
    if isinstance(value, expected):
        return True
    names = (
        "/".join(item.__name__ for item in expected)
        if isinstance(expected, tuple)
        else expected.__name__
    )
    report.error("type.invalid", path, f"{label} must be {names}")
    return False


def _style_profile_value(spec: dict[str, Any]) -> tuple[Any, str]:
    if "style_profile" in spec:
        return spec["style_profile"], "$.style_profile"
    style = spec.get("style")
    if isinstance(style, dict):
        if "profile" in style:
            return style["profile"], "$.style.profile"
        if "name" in style:
            return style["name"], "$.style.name"
    return None, "$.style_profile"


def _validate_style_profile(
    report: ValidationReport, spec: dict[str, Any], *, required: bool
) -> str | None:
    value, path = _style_profile_value(spec)
    if value is None:
        if required:
            report.error("style_profile.required", path, "strict FigureSpec v1 requires a style profile")
        else:
            report.warning(
                "legacy.style_profile_missing",
                path,
                "legacy spec has no machine-checkable style profile",
            )
        return None
    if isinstance(value, dict):
        value = value.get("id")
        path += ".id"
    if not isinstance(value, str):
        report.error("style_profile.type", path, "style profile must be a string or an object with string id")
        return None

    canonical = STYLE_PROFILE_ALIASES.get(value, value)
    if canonical not in STYLE_PROFILE_IDS:
        allowed = ", ".join(sorted(STYLE_PROFILE_IDS))
        report.error(
            "style_profile.invalid",
            path,
            f"unknown style profile {value!r}; expected one of: {allowed}",
        )
        return None
    if value in STYLE_PROFILE_ALIASES:
        message = f"use canonical profile id {canonical!r} in FigureSpec v1"
        if required:
            report.error("style_profile.noncanonical", path, message)
        else:
            report.warning("style_profile.alias", path, message)
    return canonical


def _extract_topology(
    spec: dict[str, Any], *, v1: bool
) -> tuple[Any, Any, Any, str]:
    topology = spec.get("topology")
    if isinstance(topology, dict):
        return (
            topology.get("components"),
            topology.get("connections"),
            topology.get("groups", []),
            "$.topology",
        )

    if "content_blocks" in spec:
        visual = spec.get("visual_elements")
        connections = visual.get("connections") if isinstance(visual, dict) else None
        return spec.get("content_blocks"), connections, [], "$.content_blocks"

    if "components" in spec or "connections" in spec:
        return spec.get("components"), spec.get("connections"), spec.get("groups", []), "$"

    if "layout_and_content_blocks" in spec:
        return spec.get("layout_and_content_blocks"), None, [], "$.layout_and_content_blocks"

    return None, None, None, "$.topology" if v1 else "$"


def _validate_topology(report: ValidationReport, spec: dict[str, Any], *, v1: bool) -> None:
    components, connections, groups, base = _extract_topology(spec, v1=v1)
    if components is None:
        if v1:
            report.error("topology.components_required", "$.topology.components", "components list is required")
        else:
            report.warning("legacy.topology_missing", base, "legacy spec has no machine-checkable components")
        return
    if not isinstance(components, list):
        report.error("topology.components_type", f"{base}.components" if base == "$.topology" else base, "components must be a list")
        return
    if v1 and not components:
        report.error("topology.components_empty", "$.topology.components", "strict FigureSpec v1 needs at least one component")

    component_ids: set[str] = set()
    component_group_refs: list[tuple[str, str]] = []
    id_path = "$.topology.components" if base == "$.topology" else base
    missing_ids = 0
    for index, component in enumerate(components):
        path = f"{id_path}[{index}]"
        if not isinstance(component, dict):
            report.error("component.type", path, "component must be an object")
            continue
        component_id = component.get("id")
        if component_id is None:
            missing_ids += 1
            if v1 or connections:
                report.error("component.id_required", f"{path}.id", "component id is required")
            continue
        if not _is_id(component_id):
            report.error(
                "component.id_invalid",
                f"{path}.id",
                "component id must start with a letter and contain only letters, digits, '.', '_' or '-'",
            )
            continue
        if component_id in component_ids:
            report.error("component.id_duplicate", f"{path}.id", f"duplicate component id {component_id!r}")
        component_ids.add(component_id)
        if v1 and not (
            isinstance(component.get("label"), str) and component["label"].strip()
        ):
            report.error("component.label_required", f"{path}.label", "strict v1 component requires a label")
        group_id = component.get("group_id")
        if group_id is not None:
            if not _is_id(group_id):
                report.error(
                    "component.group_id_invalid",
                    f"{path}.group_id",
                    "component group_id must be a valid id",
                )
            else:
                component_group_refs.append((f"{path}.group_id", group_id))

    if missing_ids and not v1 and not connections:
        report.warning(
            "legacy.component_ids_missing",
            id_path,
            f"{missing_ids} legacy component(s) have no ids; endpoints cannot be checked",
        )

    if connections is None:
        if v1:
            report.error("topology.connections_required", "$.topology.connections", "connections list is required")
        else:
            report.warning(
                "legacy.connections_unstructured",
                "$",
                "legacy prose flow cannot be checked for endpoint integrity",
            )
        connections = []
    elif not isinstance(connections, list):
        report.error("topology.connections_type", "$.topology.connections", "connections must be a list")
        connections = []

    connection_ids: set[str] = set()
    for index, connection in enumerate(connections):
        path = f"$.topology.connections[{index}]" if base == "$.topology" else f"$.connections[{index}]"
        if not isinstance(connection, dict):
            report.error("connection.type", path, "connection must be an object")
            continue
        connection_id = connection.get("id")
        if connection_id is not None:
            if not _is_id(connection_id):
                report.error("connection.id_invalid", f"{path}.id", "connection id has invalid syntax")
            elif connection_id in connection_ids:
                report.error("connection.id_duplicate", f"{path}.id", f"duplicate connection id {connection_id!r}")
            else:
                connection_ids.add(connection_id)

        source_key = "from" if "from" in connection else "source_id"
        target_key = "to" if "to" in connection else "target_id"
        source = connection.get(source_key)
        target = connection.get(target_key)
        for key, endpoint in ((source_key, source), (target_key, target)):
            endpoint_path = f"{path}.{key}"
            if not _is_id(endpoint):
                report.error("connection.endpoint_invalid", endpoint_path, "connection endpoint must be a valid component id")
            elif endpoint not in component_ids:
                report.error(
                    "connection.endpoint_unknown",
                    endpoint_path,
                    f"connection endpoint {endpoint!r} does not name a declared component",
                )
        if v1 and not (
            isinstance(connection.get("kind"), str)
            and connection["kind"].strip()
        ):
            report.error(
                "connection.kind_required",
                f"{path}.kind",
                "strict v1 connection requires a non-empty kind",
            )
        label = connection.get("label")
        if "label" in connection and not isinstance(label, str):
            report.error(
                "connection.label_type",
                f"{path}.label",
                "connection label must be a string",
            )
        direction = connection.get("direction")
        if v1 and direction is None:
            report.error(
                "connection.direction_required",
                f"{path}.direction",
                "strict v1 connection requires an explicit direction",
            )
        elif direction is not None and (
            not isinstance(direction, str)
            or direction not in CONNECTION_DIRECTIONS
        ):
            report.error(
                "connection.direction_invalid",
                f"{path}.direction",
                f"direction must be one of {sorted(CONNECTION_DIRECTIONS)}",
            )

    if groups is None:
        groups = []
    if not isinstance(groups, list):
        report.error("topology.groups_type", "$.topology.groups", "groups must be a list")
        return
    group_ids: set[str] = set()
    for index, group in enumerate(groups):
        path = f"$.topology.groups[{index}]"
        if not isinstance(group, dict):
            report.error("group.type", path, "group must be an object")
            continue
        group_id = group.get("id")
        if not _is_id(group_id):
            report.error("group.id_invalid", f"{path}.id", "group id is required and must be valid")
        elif group_id in group_ids:
            report.error("group.id_duplicate", f"{path}.id", f"duplicate group id {group_id!r}")
        else:
            group_ids.add(group_id)
        members = group.get("component_ids", [])
        if not isinstance(members, list):
            report.error("group.members_type", f"{path}.component_ids", "component_ids must be a list")
            continue
        for member_index, member in enumerate(members):
            if not _is_id(member):
                report.error(
                    "group.member_invalid",
                    f"{path}.component_ids[{member_index}]",
                    "group member must be a valid component id",
                )
            elif member not in component_ids:
                report.error(
                    "group.member_unknown",
                    f"{path}.component_ids[{member_index}]",
                    f"group member {member!r} does not name a declared component",
                )

    for path, group_id in component_group_refs:
        if group_id not in group_ids:
            report.error(
                "component.group_unknown",
                path,
                f"component group_id {group_id!r} does not name a declared group",
            )

    visible_text = spec.get("visible_text")
    if isinstance(visible_text, list):
        for index, item in enumerate(visible_text):
            if not isinstance(item, dict) or "component_id" not in item:
                continue
            component_id = item.get("component_id")
            if not _is_id(component_id):
                report.error(
                    "visible_text.component_invalid",
                    f"$.visible_text[{index}].component_id",
                    "visible-text component_id must be a valid id",
                )
            elif component_id not in component_ids:
                report.error(
                    "visible_text.component_unknown",
                    f"$.visible_text[{index}].component_id",
                    f"visible-text component_id {component_id!r} does not name a declared component",
                )

    layout = spec.get("layout")
    if isinstance(layout, dict):
        hero = layout.get("hero")
        if hero is not None:
            if not _is_id(hero):
                report.error(
                    "layout.hero_invalid",
                    "$.layout.hero",
                    "layout hero must be a valid component or group id",
                )
            elif hero not in component_ids | group_ids:
                report.error(
                    "layout.hero_unknown",
                    "$.layout.hero",
                    f"layout hero {hero!r} does not name a declared component or group",
                )
        reading_order = layout.get("reading_order")
        if isinstance(reading_order, list):
            for index, item in enumerate(reading_order):
                if not _is_id(item):
                    report.error(
                        "layout.reading_order_invalid",
                        f"$.layout.reading_order[{index}]",
                        "reading-order item must be a valid component id",
                    )
                elif item not in component_ids:
                    report.error(
                        "layout.reading_order_unknown",
                        f"$.layout.reading_order[{index}]",
                        f"reading-order item {item!r} does not name a declared component",
                    )


def _validate_local_reference_path(
    report: ValidationReport,
    value: Any,
    path: str,
    *,
    render_ready: bool,
) -> None:
    if not isinstance(value, str) or not value:
        report.error(
            "reference_image.path_required",
            path,
            "local reference image requires a non-empty path",
        )
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


def _validate_v1_fields(
    report: ValidationReport,
    spec: dict[str, Any],
    *,
    render_ready: bool,
) -> None:
    for key in V1_REQUIRED:
        if key not in spec:
            report.error("v1.required", f"$.{key}", f"strict FigureSpec v1 requires {key!r}")

    figure_id = spec.get("figure_id")
    if "figure_id" in spec and not _is_id(figure_id):
        report.error("figure_id.invalid", "$.figure_id", "figure_id has invalid syntax")
    revision = spec.get("plan_revision")
    if "plan_revision" in spec and not (
        (isinstance(revision, str) and bool(revision))
        or (isinstance(revision, int) and not isinstance(revision, bool) and revision >= 0)
    ):
        report.error("plan_revision.invalid", "$.plan_revision", "plan_revision must be a non-empty string or non-negative integer")
    prompt = spec.get("prompt")
    if "prompt" in spec and not (isinstance(prompt, str) and prompt.strip()):
        report.error("prompt.invalid", "$.prompt", "prompt must be a non-empty string")
    prompt_review = spec.get("prompt_review")
    if "prompt_review" in spec and (
        not isinstance(prompt_review, str)
        or prompt_review not in PROMPT_REVIEW_STATES
    ):
        report.error(
            "prompt_review.invalid",
            "$.prompt_review",
            "prompt_review must be requested, confirmed, or waived",
        )
    reviewed_digest = spec.get("prompt_reviewed_sha256")
    if "prompt_reviewed_sha256" in spec and not (
        isinstance(reviewed_digest, str)
        and SHA256_PATTERN.fullmatch(reviewed_digest)
    ):
        report.error(
            "prompt_reviewed_sha256.invalid",
            "$.prompt_reviewed_sha256",
            "prompt_reviewed_sha256 must be a lowercase 64-character SHA-256 hex digest",
        )
    ratio = spec.get("aspect_ratio")
    if "aspect_ratio" in spec and (
        not isinstance(ratio, str) or ratio not in ASPECT_RATIOS
    ):
        report.error("aspect_ratio.invalid", "$.aspect_ratio", f"aspect_ratio must be one of {sorted(ASPECT_RATIOS)}")
    final_width = spec.get("final_width_mm")
    if "final_width_mm" in spec and not (
        isinstance(final_width, (int, float))
        and not isinstance(final_width, bool)
        and final_width > 0
    ):
        report.error(
            "final_width_mm.invalid",
            "$.final_width_mm",
            "final_width_mm must be a positive number",
        )

    for key in (
        "sources",
        "visible_text",
        "reference_images",
        "must_not_claim",
        "forbidden_connections",
        "negative_constraints",
    ):
        value = spec.get(key)
        if key in spec:
            _expect_type(report, value, list, f"$.{key}", key)
    for key in ("layout", "topology", "style_grammar", "semantic_color_roles"):
        value = spec.get(key)
        if key in spec:
            if _expect_type(report, value, dict, f"$.{key}", key) and key not in {
                "semantic_color_roles",
                "topology",
            } and not value:
                report.error(f"{key}.empty", f"$.{key}", f"{key} must not be empty")

    layout = spec.get("layout")
    if isinstance(layout, dict):
        for key in ("composition", "hero", "reading_order"):
            if key not in layout:
                report.error(
                    "layout.field_required",
                    f"$.layout.{key}",
                    f"strict FigureSpec v1 requires layout.{key}",
                )
        composition = layout.get("composition")
        if composition is not None and (
            not isinstance(composition, str)
            or composition not in LAYOUT_COMPOSITIONS
        ):
            report.error(
                "layout.composition_invalid",
                "$.layout.composition",
                f"composition must be one of {sorted(LAYOUT_COMPOSITIONS)}",
            )
        reading_order = layout.get("reading_order")
        if reading_order is not None and not isinstance(reading_order, list):
            report.error(
                "layout.reading_order_type",
                "$.layout.reading_order",
                "layout.reading_order must be a list of component ids",
            )
        elif isinstance(reading_order, list) and not reading_order:
            report.error(
                "layout.reading_order_empty",
                "$.layout.reading_order",
                "layout.reading_order must not be empty",
            )

    visible_text = spec.get("visible_text")
    if isinstance(visible_text, list):
        for index, item in enumerate(visible_text):
            path = f"$.visible_text[{index}]"
            if isinstance(item, str):
                if not item.strip():
                    report.error("visible_text.empty", path, "visible text must not be empty")
            elif isinstance(item, dict):
                if not isinstance(item.get("text"), str) or not item["text"].strip():
                    report.error("visible_text.text_required", f"{path}.text", "visible text object requires non-empty text")
                priority = item.get("priority")
                if "priority" in item and (
                    not isinstance(priority, str)
                    or priority not in VISIBLE_TEXT_PRIORITIES
                ):
                    report.error(
                        "visible_text.priority_invalid",
                        f"{path}.priority",
                        f"visible-text priority must be one of {sorted(VISIBLE_TEXT_PRIORITIES)}",
                    )
            else:
                report.error("visible_text.item_type", path, "visible text item must be a string or object")

    caption_notes = spec.get("caption_notes")
    if "caption_notes" in spec:
        if not isinstance(caption_notes, list):
            report.error(
                "caption_notes.type",
                "$.caption_notes",
                "caption_notes must be an array of strings",
            )
        else:
            for index, note in enumerate(caption_notes):
                if not isinstance(note, str):
                    report.error(
                        "caption_notes.item_type",
                        f"$.caption_notes[{index}]",
                        "caption note must be a string",
                    )

    style_preset = spec.get("style_preset")
    if (
        "style_preset" in spec
        and style_preset is not None
        and not isinstance(style_preset, str)
    ):
        report.error(
            "style_preset.type",
            "$.style_preset",
            "style_preset must be a string or null",
        )
    style_source = spec.get("style_source")
    if "style_source" in spec and (
        not isinstance(style_source, str) or style_source not in STYLE_SOURCES
    ):
        report.error(
            "style_source.invalid",
            "$.style_source",
            f"style_source must be one of {sorted(STYLE_SOURCES)}",
        )

    for key in ("must_not_claim", "forbidden_connections", "negative_constraints"):
        constraints = spec.get(key)
        if not isinstance(constraints, list):
            continue
        for index, constraint in enumerate(constraints):
            if not isinstance(constraint, str) or not constraint.strip():
                report.error(
                    f"{key}.invalid",
                    f"$.{key}[{index}]",
                    f"{key} item must be a non-empty string",
                )

    sources = spec.get("sources")
    if isinstance(sources, list):
        if not sources:
            report.error(
                "source.empty",
                "$.sources",
                "strict FigureSpec v1 requires at least one evidence source",
            )
        for index, source in enumerate(sources):
            path = f"$.sources[{index}]"
            if not isinstance(source, dict):
                report.error("source.type", path, "source must be an object")
                continue
            for key in ("kind", "uri_or_path", "evidence"):
                value = source.get(key)
                if not isinstance(value, str) or not value.strip():
                    report.error(
                        "source.field_required",
                        f"{path}.{key}",
                        f"source requires non-empty string {key!r}",
                    )

    output_path = spec.get("output_path")
    if "output_path" in spec:
        if not isinstance(output_path, str) or not output_path:
            report.error("output_path.invalid", "$.output_path", "output_path must be a non-empty string")
        elif not _is_absolute_path(output_path):
            report.error("output_path.not_absolute", "$.output_path", "output_path must be absolute")

    workspace_root = spec.get("workspace_root")
    if "workspace_root" in spec:
        if not isinstance(workspace_root, str) or not workspace_root:
            report.error(
                "workspace_root.invalid",
                "$.workspace_root",
                "workspace_root must be a non-empty string",
            )
        elif not _is_absolute_path(workspace_root):
            report.error(
                "workspace_root.not_absolute",
                "$.workspace_root",
                "workspace_root must be absolute",
            )
        elif (
            isinstance(output_path, str)
            and _is_absolute_path(output_path)
            and not _is_within_path(output_path, workspace_root)
        ):
            report.error(
                "output_path.outside_workspace",
                "$.output_path",
                "output_path must be inside workspace_root",
            )

    references = spec.get("reference_images")
    if isinstance(references, list):
        local_references = False
        conversation_references = False
        for index, reference in enumerate(references):
            path = f"$.reference_images[{index}]"
            if isinstance(reference, str):
                local_references = True
                _validate_local_reference_path(
                    report,
                    reference,
                    path,
                    render_ready=render_ready,
                )
                continue
            if not isinstance(reference, dict):
                report.error(
                    "reference_image.invalid",
                    path,
                    "reference image must be an absolute path or a supported descriptor",
                )
                continue
            kind = reference.get("kind")
            if kind == "local_path":
                local_references = True
                unexpected = sorted(set(reference) - {"kind", "path"})
                if unexpected:
                    report.error(
                        "reference_image.extra_keys",
                        path,
                        f"local_path reference has unsupported key(s): {', '.join(unexpected)}",
                    )
                _validate_local_reference_path(
                    report,
                    reference.get("path"),
                    f"{path}.path",
                    render_ready=render_ready,
                )
            elif kind == "recent_conversation":
                conversation_references = True
                unexpected = sorted(
                    set(reference) - {"kind", "ordinal_from_latest"}
                )
                if unexpected:
                    report.error(
                        "reference_image.extra_keys",
                        path,
                        "recent_conversation reference has unsupported key(s): "
                        + ", ".join(unexpected),
                    )
                ordinal = reference.get("ordinal_from_latest")
                if not (
                    isinstance(ordinal, int)
                    and not isinstance(ordinal, bool)
                    and 1 <= ordinal <= 5
                ):
                    report.error(
                        "reference_image.ordinal_invalid",
                        f"{path}.ordinal_from_latest",
                        "recent conversation ordinal must be an integer from 1 to 5",
                    )
                elif render_ready:
                    report.warning(
                        "reference_image.nonreproducible",
                        path,
                        "recent-conversation ordinals are call-relative; persist a stable asset id or local copy for reproducibility",
                    )
            else:
                report.error(
                    "reference_image.kind_invalid",
                    f"{path}.kind",
                    "reference kind must be local_path or recent_conversation",
                )
        if local_references and conversation_references:
            report.error(
                "reference_image.mixed_mechanisms",
                "$.reference_images",
                "local paths and recent-conversation images cannot be sent in one native image call",
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
            f"cannot inspect trusted workspace root {trusted}: {exc}",
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
    review = spec.get("prompt_review")
    if (
        isinstance(review, str)
        and review in {"requested", "waived"}
        and "prompt_reviewed_sha256" in spec
    ):
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
            and SHA256_PATTERN.fullmatch(reviewed_digest)
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
    strict_v1: bool = False,
    render_ready: bool = False,
    trusted_workspace_root: str | Path | None = None,
    source: str = "<memory>",
) -> ValidationReport:
    """Validate a decoded figure spec and return all diagnostics."""

    mode = "render-ready" if render_ready else "strict-v1" if strict_v1 else "compatible"
    report = ValidationReport(source=source, mode=mode)
    if not isinstance(spec, dict):
        report.error("document.type", "$", "figure spec must be a JSON object")
        return report

    schema = spec.get("schema")
    is_v1 = schema == SCHEMA_V1
    if schema is not None and not is_v1:
        report.error("schema.unsupported", "$.schema", f"unsupported schema {schema!r}")
    if (strict_v1 or render_ready) and not is_v1:
        report.error("schema.v1_required", "$.schema", f"strict mode requires {SCHEMA_V1!r}")
    elif not is_v1:
        report.warning(
            "legacy.spec",
            "$.schema",
            "legacy unversioned spec accepted in compatibility mode; migrate to FigureSpec v1",
        )

    enforce_v1 = is_v1 or strict_v1 or render_ready
    if enforce_v1:
        _validate_v1_fields(report, spec, render_ready=render_ready)
    canonical_profile = _validate_style_profile(report, spec, required=enforce_v1)
    _validate_topology(report, spec, v1=enforce_v1)

    if canonical_profile == "reference-led" and not spec.get("reference_images"):
        report.error(
            "style_profile.reference_missing",
            "$.reference_images",
            "reference-led style requires at least one local or recent-conversation reference image",
        )
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
    strict_v1: bool = False,
    render_ready: bool = False,
    trusted_workspace_root: str | Path | None = None,
) -> ValidationReport:
    """Load and validate one JSON file."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        mode = "render-ready" if render_ready else "strict-v1" if strict_v1 else "compatible"
        report = ValidationReport(source=str(path), mode=mode)
        report.error("json.invalid", "$", str(exc))
        return report
    return validate_spec(
        data,
        strict_v1=strict_v1,
        render_ready=render_ready,
        trusted_workspace_root=trusted_workspace_root,
        source=str(path),
    )


def _print_human(reports: Iterable[ValidationReport]) -> None:
    for report in reports:
        status = "PASS" if report.ok else "FAIL"
        print(f"{status} {report.source} ({len(report.errors)} error(s), {len(report.warnings)} warning(s))")
        for item in report.diagnostics:
            print(f"  {item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="figure spec JSON file(s)")
    parser.add_argument("--strict-v1", action="store_true", help="reject legacy specs and require FigureSpec v1")
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
    args = parser.parse_args(argv)

    reports = [
        validate_path(
            path,
            strict_v1=args.strict_v1,
            render_ready=args.render_ready,
            trusted_workspace_root=args.workspace_root,
        )
        for path in args.paths
    ]
    if args.json:
        print(json.dumps([report.to_dict() for report in reports], indent=2, ensure_ascii=False))
    else:
        _print_human(reports)
    return 0 if all(report.ok for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
