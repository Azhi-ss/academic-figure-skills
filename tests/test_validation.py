from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "academic-figure-workflow" / "scripts"))

from validate_figure_spec import ValidationReport, validate_spec  # noqa: E402
from validate_skill_pack import validate_skills  # noqa: E402


def valid_spec() -> dict:
    return {
        "schema": "academic-figure/FigureSpec@1",
        "figure_id": "figure_1",
        "plan_revision": "r1",
        "sources": [
            {
                "kind": "repository",
                "uri_or_path": "/tmp/repository",
                "revision_or_page": "abc123",
                "evidence": "src/controller.py:run",
            }
        ],
        "prompt": "A grounded academic figure showing a typed scientific loop.",
        "aspect_ratio": "16:9",
        "final_width_mm": 183,
        "visible_text": ["Evidence", "Policy", "Harness"],
        "layout": {
            "composition": "pipeline",
            "hero": "policy",
            "reading_order": ["evidence", "policy", "harness"],
        },
        "topology": {
            "components": [
                {"id": "evidence", "label": "Evidence"},
                {"id": "policy", "label": "Policy"},
                {"id": "harness", "label": "Harness"},
            ],
            "connections": [
                {
                    "from": "evidence",
                    "to": "policy",
                    "kind": "executed",
                    "direction": "forward",
                },
                {
                    "from": "policy",
                    "to": "harness",
                    "kind": "advisory",
                    "direction": "forward",
                },
            ],
        },
        "style_profile": "classic-technical",
        "style_grammar": {"composition": "pipeline", "marks": "flat-vector"},
        "semantic_color_roles": {"evidence": "#0072B2"},
        "reference_images": [],
        "must_not_claim": ["Autonomous wet-lab execution"],
        "forbidden_connections": ["policy -> numeric_prediction"],
        "negative_constraints": ["No invented components"],
        "prompt_review": "waived",
        "workspace_root": "/tmp",
        "output_path": "/tmp/figure_1.png",
    }


def diagnostic_codes(report) -> set[str]:
    return {item.code for item in report.diagnostics}


def diagnostics(report) -> set[tuple[str, str]]:
    return {(item.code, item.path) for item in report.diagnostics}


class FigureSpecValidationTests(unittest.TestCase):
    def test_valid_spec_passes(self) -> None:
        report = validate_spec(valid_spec())
        self.assertTrue(report.ok, report.to_dict())

    def test_bad_connection_endpoint_fails(self) -> None:
        spec = valid_spec()
        spec["topology"]["connections"][1]["to"] = "missing_component"
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn("connection.endpoint_unknown", diagnostic_codes(report))

    def test_missing_connection_direction_fails(self) -> None:
        spec = valid_spec()
        del spec["topology"]["connections"][0]["direction"]
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn(("schema.required", "$.topology.connections[0].direction"), diagnostics(report))

    def test_duplicate_component_id_fails(self) -> None:
        spec = valid_spec()
        spec["topology"]["components"][2]["id"] = "policy"
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn("component.id_duplicate", diagnostic_codes(report))

    def test_invalid_style_profile_fails(self) -> None:
        spec = valid_spec()
        spec["style_profile"] = "enterprise-neon-dashboard"
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn(("schema.enum", "$.style_profile"), diagnostics(report))

    def test_style_aliases_are_not_profile_ids(self) -> None:
        for alias in ("classic-academic-border", "modern-technical-vector"):
            with self.subTest(alias=alias):
                spec = valid_spec()
                spec["style_profile"] = alias
                report = validate_spec(spec)
                self.assertIn(("schema.enum", "$.style_profile"), diagnostics(report))

    def test_invalid_prompt_review_fails(self) -> None:
        spec = valid_spec()
        spec["prompt_review"] = "assumed-from-unrelated-chat"
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn(("schema.enum", "$.prompt_review"), diagnostics(report))

    def test_recent_conversation_reference_is_valid(self) -> None:
        spec = valid_spec()
        spec["style_profile"] = "reference-led"
        spec["reference_images"] = [
            {"kind": "recent_conversation", "ordinal_from_latest": 1}
        ]
        report = validate_spec(spec)
        self.assertTrue(report.ok, report.to_dict())

    def test_recent_conversation_reference_is_limited_to_five(self) -> None:
        spec = valid_spec()
        spec["reference_images"] = [
            {"kind": "recent_conversation", "ordinal_from_latest": 6}
        ]
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn(
            ("schema.maximum", "$.reference_images[0].ordinal_from_latest"),
            diagnostics(report),
        )

    def test_mixed_reference_mechanisms_fail(self) -> None:
        spec = valid_spec()
        spec["reference_images"] = [
            "/tmp/reference.png",
            {"kind": "recent_conversation", "ordinal_from_latest": 1},
        ]
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn("reference_image.mixed_mechanisms", diagnostic_codes(report))

    def test_output_outside_workspace_fails(self) -> None:
        spec = valid_spec()
        spec["workspace_root"] = "/tmp/workspace"
        spec["output_path"] = "/tmp/outside/figure.png"
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn("output_path.outside_workspace", diagnostic_codes(report))

    def test_empty_sources_fail(self) -> None:
        spec = valid_spec()
        spec["sources"] = []
        report = validate_spec(spec)
        self.assertFalse(report.ok)
        self.assertIn(("schema.minItems", "$.sources"), diagnostics(report))

    def test_legacy_unversioned_spec_fails(self) -> None:
        legacy = {
            "diagram_type": "Overall Framework",
            "layout_and_content_blocks": [
                {"exact_title_to_render_inside": "Input", "flow": "right"}
            ],
        }
        report = validate_spec(legacy)
        self.assertFalse(report.ok)
        self.assertIn(("schema.required", "$.schema"), diagnostics(report))


def write_skill(root: Path, skill_id: str) -> None:
    skill_dir = root / skill_id
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"""---
name: {skill_id}
description: Validate the isolated {skill_id} fixture.
metadata:
  version: "1.0.0"
---

# Fixture
""",
        encoding="utf-8",
    )


def write_pack(root: Path, skill_ids: list[str]) -> None:
    for skill_id in skill_ids:
        write_skill(root, skill_id)
    entries = [
        {"id": skill_id, "path": f"./{skill_id}", "version": "1.0.0"}
        for skill_id in skill_ids
    ]
    (root / "manifest.json").write_text(
        json.dumps({"version": "1.0.0", "skills": entries}),
        encoding="utf-8",
    )


class PackValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def test_manifest_metadata_version_drift_fails(self) -> None:
        write_pack(self.root, ["example-skill"])
        skill_file = self.root / "example-skill" / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace('"1.0.0"', '"1.1.0"'),
            encoding="utf-8",
        )
        report = ValidationReport()
        validate_skills(self.root, report)
        self.assertFalse(report.ok)
        self.assertIn("manifest.version_drift", diagnostic_codes(report))

    def test_unregistered_top_level_skill_is_rejected(self) -> None:
        write_pack(self.root, ["registered-skill"])
        write_skill(self.root, "rogue-skill")
        report = ValidationReport()
        validate_skills(self.root, report)
        rogue = [item for item in report.diagnostics if item.code == "manifest.skill_unregistered"]
        self.assertEqual(1, len(rogue), report.to_dict())
        self.assertTrue(rogue[0].path.endswith("rogue-skill/SKILL.md"))

    def test_worker_prompt_keeps_bounded_contract_fields(self) -> None:
        prompt = (ROOT / "academic-figure-workflow" / "prompts" / "figure-worker.md").read_text(
            encoding="utf-8"
        )
        for field in (
            "- task kind:",
            "- owned output paths:",
            "- acceptance criteria:",
            "- status: success | blocked | failed",
            "- summary:",
            "- artifacts:",
            "- evidence:",
            "- validation:",
            "- residual risks:",
            "- next action:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, prompt)


if __name__ == "__main__":
    unittest.main()
