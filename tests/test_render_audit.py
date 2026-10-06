from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fig1-draw" / "scripts" / "validate_render_audit.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_render_audit", SCRIPT)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
MODULE = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = MODULE
MODULE_SPEC.loader.exec_module(MODULE)

# A one-pixel PNG is only a byte-binding fixture. These tests do not inspect art.
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP4/x8AAwAB/2+Bq7YAAAAASUVORK5CYII="
)


def status(value: str = "pass") -> dict:
    return {"status": value, "evidence": "Synthetic test assertion; no visual inspection performed."}


class RenderAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.spec_path = self.root / "figure.spec.json"
        self.image_path = self.root / "figure.png"
        self.audit_path = self.root / "figure.audit.json"
        self.image_path.write_bytes(PNG)
        self.spec = {
            "schema": "academic-figure/FigureSpec@1", "figure_id": "figure_2",
            "topology": {
                "components": [{"id": "policy"}, {"id": "review"}, {"id": "fusion"}],
                "connections": [
                    {"id": "proposal", "from": "policy", "to": "fusion", "kind": "executed",
                     "direction": "forward", "line": "solid", "label": "proposal"},
                    {"from": "review", "to": "fusion", "kind": "advisory", "direction": "forward"},
                ],
            },
        }
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
        self.audit = {
            "schema": MODULE.SCHEMA, "figure_id": "figure_2", "render_revision": "r1",
            "image_path": str(self.image_path), "image_sha256": hashlib.sha256(PNG).hexdigest(),
            "spec_sha256": hashlib.sha256(self.spec_path.read_bytes()).hexdigest(),
            "pass": True, "spec_validation": {"status": "pass"}, "image_inspection": status(),
            "nodes": [{"id": name, **status()} for name in ("policy", "review", "fusion")],
            "edges": [
                {**self.spec["topology"]["connections"][0], **status()},
                {"id": "edge_002", **self.spec["topology"]["connections"][1],
                 "line": "unspecified", "label": "", **status()},
            ],
            "checks": {name: status() for name in MODULE.CHECKS}, "defects": [],
        }

    def check(self, audit: dict | None = None):
        self.audit_path.write_text(json.dumps(self.audit if audit is None else audit), encoding="utf-8")
        return MODULE.validate_paths(self.spec_path, self.image_path, self.audit_path)

    def assertInvalid(self, report, text: str) -> None:
        self.assertEqual(2, report.exit_code, report)
        self.assertTrue(any(text in error for error in report.errors), report.errors)

    def test_complete_record_passes_with_explicit_and_fallback_edge_ids(self) -> None:
        report = self.check()
        self.assertEqual(0, report.exit_code, report)
        self.assertTrue(report.passed)

    def test_image_path_must_be_absolute(self) -> None:
        self.audit["image_path"] = "figure.png"
        self.assertInvalid(self.check(), "image_path: must be an absolute path")

    def test_omitted_spec_direction_is_unspecified_not_guessed(self) -> None:
        del self.spec["topology"]["connections"][1]["direction"]
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
        self.audit["spec_sha256"] = hashlib.sha256(self.spec_path.read_bytes()).hexdigest()
        self.audit["edges"][1]["direction"] = "unspecified"
        self.assertEqual(0, self.check().exit_code)
        self.audit["edges"][1]["direction"] = "forward"
        self.assertInvalid(self.check(), "].direction: does not match spec")

    def test_missing_expected_edge_is_invalid_even_with_overall_pass(self) -> None:
        self.audit["edges"].pop()
        self.assertInvalid(self.check(), "missing ids: edge_002")

    def test_empty_node_and_edge_ledgers_cannot_pass(self) -> None:
        self.audit["nodes"] = []
        self.audit["edges"] = []
        self.assertInvalid(self.check(), "missing ids")

    def test_known_missing_arrow_record_fails_delivery(self) -> None:
        self.audit["edges"][1].update(status("fail"))
        self.audit["pass"] = False
        self.assertEqual(1, self.check().exit_code)

    def test_unverified_inspection_fails_delivery(self) -> None:
        self.audit["image_inspection"] = status("unverified")
        self.audit["pass"] = False
        self.assertEqual(1, self.check().exit_code)

    def test_old_image_hash_rejected(self) -> None:
        self.image_path.write_bytes(PNG + b"changed-render-bytes")
        self.assertInvalid(self.check(), "image_sha256: does not match")

    def test_spec_hash_binds_raw_bytes_even_if_json_meaning_unchanged(self) -> None:
        self.spec_path.write_bytes(self.spec_path.read_bytes() + b"\n")
        self.assertInvalid(self.check(), "spec_sha256: does not match")

    def test_changed_spec_cannot_choose_old_coverage_after_rebinding_hash(self) -> None:
        self.spec["topology"]["connections"].append({
            "id": "extra", "from": "policy", "to": "review", "kind": "advisory", "direction": "forward",
        })
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
        self.audit["spec_sha256"] = hashlib.sha256(self.spec_path.read_bytes()).hexdigest()
        self.assertInvalid(self.check(), "missing ids: extra")

    def test_image_path_must_match_even_if_same_bytes(self) -> None:
        alternate = self.root / "other.png"
        alternate.write_bytes(PNG)
        self.audit["image_path"] = str(alternate)
        self.assertInvalid(self.check(), "image_path: does not match")

    def test_unknown_and_duplicate_ids_are_invalid_for_nodes_and_edges(self) -> None:
        for ledger in ("nodes", "edges"):
            for variant in ("unknown", "duplicate"):
                with self.subTest(ledger=ledger, variant=variant):
                    audit = copy.deepcopy(self.audit)
                    item = copy.deepcopy(audit[ledger][0])
                    if variant == "unknown":
                        item["id"] = "not_in_spec"
                    audit[ledger].append(item)
                    self.assertInvalid(self.check(audit), f"{ledger}: {variant} id")

    def test_every_edge_semantic_field_must_match_spec(self) -> None:
        for name in MODULE.EDGE_FIELDS:
            with self.subTest(field=name):
                audit = copy.deepcopy(self.audit)
                audit["edges"][0][name] = "changed"
                self.assertInvalid(self.check(audit), f"].{name}: does not match spec")

    def test_each_edge_field_is_required_including_empty_label(self) -> None:
        for name in MODULE.EDGE_FIELDS:
            with self.subTest(field=name):
                audit = copy.deepcopy(self.audit)
                del audit["edges"][1][name]
                self.assertInvalid(self.check(audit), f"].{name}: does not match spec")

    def test_overall_pass_cannot_hide_failed_or_unverified_statuses(self) -> None:
        for value in ("fail", "unverified"):
            for target in ("spec_validation", "image_inspection", "node", "edge", "check"):
                with self.subTest(status=value, target=target):
                    audit = copy.deepcopy(self.audit)
                    record = {"node": audit["nodes"][0], "edge": audit["edges"][0],
                              "check": audit["checks"]["layout"]}.get(target, audit.get(target))
                    record["status"] = value
                    self.assertInvalid(self.check(audit), "audit.pass: inconsistent")

    def test_false_overall_pass_with_all_pass_records_is_inconsistent(self) -> None:
        self.audit["pass"] = False
        self.assertInvalid(self.check(), "audit.pass: inconsistent")

    def test_missing_image_inspection_and_each_required_check_are_invalid(self) -> None:
        audit = copy.deepcopy(self.audit)
        del audit["image_inspection"]
        self.assertInvalid(self.check(audit), "image_inspection: must be a status object")
        for name in MODULE.CHECKS:
            with self.subTest(check=name):
                audit = copy.deepcopy(self.audit)
                del audit["checks"][name]
                self.assertInvalid(self.check(audit), f"checks.{name}: must be a status object")

    def test_blank_evidence_and_missing_revision_are_invalid(self) -> None:
        self.audit["nodes"][0]["evidence"] = "  "
        self.assertInvalid(self.check(), "evidence: must be a nonempty string")
        self.audit["nodes"][0].update(status())
        self.audit["render_revision"] = ""
        self.assertInvalid(self.check(), "render_revision: must be a nonempty string")

    def test_figure_id_and_schema_are_bound(self) -> None:
        self.audit["figure_id"] = "other"
        self.assertInvalid(self.check(), "figure_id: does not match")
        self.audit["figure_id"] = "figure_2"
        self.audit["schema"] = "academic-figure/RenderAudit@1"
        self.assertInvalid(self.check(), "audit.schema: expected")

    def test_major_and_critical_defects_block_pass_but_minor_does_not(self) -> None:
        for severity in ("minor", "major", "critical"):
            with self.subTest(severity=severity):
                audit = copy.deepcopy(self.audit)
                audit["defects"] = [{"severity": severity, "description": "Synthetic defect."}]
                if severity == "minor":
                    self.assertEqual(0, self.check(audit).exit_code)
                else:
                    self.assertInvalid(self.check(audit), "audit.pass: inconsistent")
                    audit["pass"] = False
                    self.assertEqual(1, self.check(audit).exit_code)

    def test_additional_checks_cannot_hide_failure(self) -> None:
        self.audit["checks"]["caption_match"] = status("fail")
        self.assertInvalid(self.check(), "audit.pass: inconsistent")

    def test_existing_observed_defect_record_shape_is_accepted(self) -> None:
        self.audit["defects"] = [{
            "check": "semantic_topology", "severity": "major", "observed": "Required arrow absent.",
            "expected": "Complete expected edge set.", "evidence": "Synthetic fixture assertion.",
            "edit_instruction": "Restore the arrow and recheck the whole image.",
        }]
        self.audit["pass"] = False
        self.assertEqual(1, self.check().exit_code)

    def test_duplicate_spec_ids_are_invalid(self) -> None:
        self.spec["topology"]["components"].append({"id": "policy"})
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
        self.audit["spec_sha256"] = hashlib.sha256(self.spec_path.read_bytes()).hexdigest()
        self.assertInvalid(self.check(), "spec.components: duplicate id")

    def test_malformed_records_return_diagnostics_instead_of_crashing(self) -> None:
        for field in ("nodes", "edges", "checks", "image_inspection", "spec_validation", "defects"):
            with self.subTest(field=field):
                audit = copy.deepcopy(self.audit)
                audit[field] = None
                self.assertEqual(2, self.check(audit).exit_code)
        self.audit["nodes"][0]["id"] = []
        self.assertEqual(2, self.check().exit_code)

    def test_cli_exit_codes_and_truthful_scope_notice(self) -> None:
        for expected in (0, 1, 2):
            with self.subTest(exit_code=expected):
                audit = copy.deepcopy(self.audit)
                if expected == 1:
                    audit["image_inspection"] = status("unverified")
                    audit["pass"] = False
                elif expected == 2:
                    audit["edges"] = []
                self.check(audit)
                process = subprocess.run(
                    [sys.executable, str(SCRIPT), "--spec", str(self.spec_path),
                     "--image", str(self.image_path), str(self.audit_path)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(expected, process.returncode, process.stdout + process.stderr)
                self.assertIn("does not inspect pixels", process.stdout)


if __name__ == "__main__":
    unittest.main()
