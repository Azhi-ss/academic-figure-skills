#!/usr/bin/env python3
"""Validate a RenderAudit@2 record against an exact spec and image artifact.

This checker validates record completeness, consistency, and byte-level binding.
It does not inspect pixels and cannot prove that human/agent assertions are true.
Use alongside actual image inspection and the separate FigureSpec validator.

Exit codes: 0 = complete passing record; 1 = valid but failed/unverified record;
2 = malformed, incomplete, incorrectly bound, or inconsistent record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SCHEMA = "academic-figure/RenderAudit@2"
STATUSES = frozenset({"pass", "fail", "unverified"})
CHECKS = (
    "semantic_topology", "visible_text", "background", "layout",
    "style_fidelity", "accessibility",
)
EDGE_FIELDS = ("from", "to", "kind", "direction", "line", "label")


@dataclass
class AuditReport:
    errors: list[str] = field(default_factory=list)
    nonpassing: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.nonpassing else 0)

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _read_json(path: Path, name: str, report: AuditReport) -> tuple[Any, bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        report.errors.append(f"{name}: cannot read JSON: {exc}")
        return None, b""
    if not isinstance(value, dict):
        report.errors.append(f"{name}: root must be an object")
        return None, raw
    return value, raw


def _status_record(value: Any, name: str, report: AuditReport, *, evidence: bool = True) -> None:
    if not isinstance(value, dict):
        report.errors.append(f"{name}: must be a status object")
        return
    status = value.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        report.errors.append(f"{name}.status: must be pass, fail, or unverified")
    elif status != "pass":
        report.nonpassing.append(f"{name}: {status}")
    if evidence and not _text(value.get("evidence")):
        report.errors.append(f"{name}.evidence: must be a nonempty string")


def _expected_topology(spec: dict, report: AuditReport) -> tuple[set[str], dict[str, dict]]:
    topology = spec.get("topology")
    if not isinstance(topology, dict):
        report.errors.append("spec.topology: must be an object")
        return set(), {}
    components = topology.get("components")
    connections = topology.get("connections")
    if not isinstance(components, list) or not components:
        report.errors.append("spec.topology.components: must be a nonempty list")
        components = []
    if not isinstance(connections, list):
        report.errors.append("spec.topology.connections: must be a list")
        connections = []
    nodes: set[str] = set()
    for index, component in enumerate(components):
        node_id = component.get("id") if isinstance(component, dict) else None
        if not _text(node_id):
            report.errors.append(f"spec.components[{index}].id: must be a nonempty string")
        elif node_id in nodes:
            report.errors.append(f"spec.components: duplicate id {node_id!r}")
        else:
            nodes.add(node_id)
    edges: dict[str, dict] = {}
    for index, connection in enumerate(connections):
        name = f"spec.connections[{index}]"
        if not isinstance(connection, dict):
            report.errors.append(f"{name}: must be an object")
            continue
        edge_id = connection.get("id", f"edge_{index + 1:03d}")
        if not _text(edge_id):
            report.errors.append(f"{name}.id: must be a nonempty string")
            continue
        if edge_id in edges:
            report.errors.append(f"spec.connections: duplicate id {edge_id!r}")
            continue
        expected = {key: connection.get(key) for key in EDGE_FIELDS}
        expected["line"] = connection.get("line", "unspecified")
        expected["direction"] = connection.get("direction", "unspecified")
        expected["label"] = connection.get("label", "")
        for key in ("from", "to", "kind", "line"):
            if not _text(expected[key]):
                report.errors.append(f"{name}.{key}: must be a nonempty string")
        for endpoint in ("from", "to"):
            if isinstance(expected[endpoint], str) and expected[endpoint] not in nodes:
                report.errors.append(f"{name}.{endpoint}: unknown node {expected[endpoint]!r}")
        if expected["direction"] not in ("forward", "backward", "bidirectional", "unspecified"):
            report.errors.append(f"{name}.direction: invalid direction")
        if not isinstance(expected["label"], str):
            report.errors.append(f"{name}.label: must be a string")
        edges[edge_id] = expected
    return nodes, edges


def _coverage(value: Any, expected: set[str], name: str, report: AuditReport) -> dict[str, dict]:
    if not isinstance(value, list):
        report.errors.append(f"{name}: must be a list")
        value = []
    records: dict[str, dict] = {}
    for index, record in enumerate(value):
        location = f"{name}[{index}]"
        _status_record(record, location, report)
        item_id = record.get("id") if isinstance(record, dict) else None
        if not _text(item_id):
            report.errors.append(f"{location}.id: must be a nonempty string")
        elif item_id in records:
            report.errors.append(f"{name}: duplicate id {item_id!r}")
        else:
            records[item_id] = record
            if item_id not in expected:
                report.errors.append(f"{name}: unknown id {item_id!r}")
    missing = expected - records.keys()
    if missing:
        report.errors.append(f"{name}: missing ids: {', '.join(sorted(missing))}")
    return records


def validate_paths(spec_path: Path, image_path: Path, audit_path: Path) -> AuditReport:
    """Check a saved audit; no computer-vision or renderer is invoked."""
    report = AuditReport()
    spec, spec_raw = _read_json(Path(spec_path), "spec", report)
    audit, _ = _read_json(Path(audit_path), "audit", report)
    if spec is None or audit is None:
        return report
    if spec.get("schema") != "academic-figure/FigureSpec@1":
        report.errors.append("spec.schema: expected academic-figure/FigureSpec@1")
    if audit.get("schema") != SCHEMA:
        report.errors.append(f"audit.schema: expected {SCHEMA}")
    if not _text(spec.get("figure_id")):
        report.errors.append("spec.figure_id: must be a nonempty string")
    if audit.get("figure_id") != spec.get("figure_id"):
        report.errors.append("audit.figure_id: does not match spec")
    if not _text(audit.get("render_revision")):
        report.errors.append("audit.render_revision: must be a nonempty string")

    declared_image = audit.get("image_path")
    if not _text(declared_image):
        report.errors.append("audit.image_path: must be a nonempty string")
    else:
        try:
            candidate = Path(declared_image)
            if not candidate.is_absolute():
                report.errors.append("audit.image_path: must be an absolute path")
            elif candidate.resolve() != Path(image_path).resolve():
                report.errors.append("audit.image_path: does not match --image")
        except (OSError, ValueError, RuntimeError) as exc:
            report.errors.append(f"audit.image_path: cannot resolve: {exc}")

    expected_hashes = {"spec_sha256": hashlib.sha256(spec_raw).hexdigest()}
    try:
        expected_hashes["image_sha256"] = hashlib.sha256(Path(image_path).read_bytes()).hexdigest()
    except (OSError, ValueError) as exc:
        report.errors.append(f"image: cannot hash file: {exc}")
    for name in ("image_sha256", "spec_sha256"):
        supplied = audit.get(name)
        if not isinstance(supplied, str) or re.fullmatch(r"[0-9a-f]{64}", supplied) is None:
            report.errors.append(f"audit.{name}: must be a lowercase SHA256 digest")
        elif name in expected_hashes and supplied != expected_hashes[name]:
            report.errors.append(f"audit.{name}: does not match artifact bytes")

    _status_record(audit.get("spec_validation"), "spec_validation", report, evidence=False)
    _status_record(audit.get("image_inspection"), "image_inspection", report)
    expected_nodes, expected_edges = _expected_topology(spec, report)
    _coverage(audit.get("nodes"), expected_nodes, "nodes", report)
    edges = _coverage(audit.get("edges"), set(expected_edges), "edges", report)
    for edge_id, record in edges.items():
        if edge_id not in expected_edges:
            continue
        for key in EDGE_FIELDS:
            if key not in record or record[key] != expected_edges[edge_id][key]:
                report.errors.append(f"edges[{edge_id!r}].{key}: does not match spec")

    checks = audit.get("checks")
    if not isinstance(checks, dict):
        report.errors.append("checks: must be an object")
        checks = {}
    for name in CHECKS:
        _status_record(checks.get(name), f"checks.{name}", report)
    # Additional named checks are allowed but cannot hide fail/unverified statuses.
    for name in sorted(set(checks) - set(CHECKS)):
        _status_record(checks[name], f"checks.{name}", report)

    defects = audit.get("defects", [])
    if not isinstance(defects, list):
        report.errors.append("defects: must be a list")
        defects = []
    for index, defect in enumerate(defects):
        if not isinstance(defect, dict):
            report.errors.append(f"defects[{index}]: must be an object")
            continue
        severity = defect.get("severity")
        if severity not in ("minor", "major", "critical"):
            report.errors.append(f"defects[{index}].severity: invalid severity")
        elif severity in ("major", "critical"):
            report.nonpassing.append(f"defects[{index}]: {severity}")
        if not (_text(defect.get("description")) or _text(defect.get("observed"))):
            report.errors.append(f"defects[{index}]: description or observed must be a nonempty string")

    overall = audit.get("pass")
    if not isinstance(overall, bool):
        report.errors.append("audit.pass: must be a boolean")
    elif not report.errors and overall != (not report.nonpassing):
        report.errors.append("audit.pass: inconsistent with statuses and defect severity")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("audit", type=Path)
    args = parser.parse_args(argv)
    report = validate_paths(args.spec, args.image, args.audit)
    label = {0: "PASS", 1: "NOT ACCEPTED", 2: "INVALID"}[report.exit_code]
    print(f"{label}: audit record ({len(report.errors)} error(s), {len(report.nonpassing)} nonpassing item(s))")
    for error in report.errors:
        print(f"  ERROR: {error}")
    for item in report.nonpassing:
        print(f"  NOT PASSING: {item}")
    print("Record validation only: this does not inspect pixels or verify the truth of inspection evidence.")
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
