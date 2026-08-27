from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "academic-figure-prompt" / "scripts"))

from sync_shared_refs import SyncItem, synchronize  # noqa: E402
from validate_figure_spec import validate_spec  # noqa: E402
from validate_skill_pack import (  # noqa: E402
    PackReport,
    validate_reference_items,
    validate_skills,
)


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


class FigureSpecValidationTests(unittest.TestCase):
    def test_valid_strict_v1_spec_passes(self) -> None:
        report = validate_spec(valid_spec(), strict_v1=True)
        self.assertTrue(report.ok, report.to_dict())

    def test_bad_connection_endpoint_fails(self) -> None:
        spec = valid_spec()
        spec["topology"]["connections"][1]["to"] = "missing_component"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("connection.endpoint_unknown", diagnostic_codes(report))

    def test_missing_connection_direction_fails(self) -> None:
        spec = valid_spec()
        del spec["topology"]["connections"][0]["direction"]
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("connection.direction_required", diagnostic_codes(report))

    def test_duplicate_component_id_fails(self) -> None:
        spec = valid_spec()
        spec["topology"]["components"][2]["id"] = "policy"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("component.id_duplicate", diagnostic_codes(report))

    def test_invalid_style_profile_fails(self) -> None:
        spec = valid_spec()
        spec["style_profile"] = "enterprise-neon-dashboard"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("style_profile.invalid", diagnostic_codes(report))

    def test_legacy_style_profile_is_noncanonical_in_strict_mode(self) -> None:
        spec = valid_spec()
        spec["style_profile"] = "classic-academic-border"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("style_profile.noncanonical", diagnostic_codes(report))

    def test_invalid_prompt_review_fails(self) -> None:
        spec = valid_spec()
        spec["prompt_review"] = "assumed-from-unrelated-chat"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("prompt_review.invalid", diagnostic_codes(report))

    def test_recent_conversation_reference_is_valid(self) -> None:
        spec = valid_spec()
        spec["style_profile"] = "reference-led"
        spec["reference_images"] = [
            {"kind": "recent_conversation", "ordinal_from_latest": 1}
        ]
        report = validate_spec(spec, strict_v1=True)
        self.assertTrue(report.ok, report.to_dict())

    def test_recent_conversation_reference_is_limited_to_five(self) -> None:
        spec = valid_spec()
        spec["reference_images"] = [
            {"kind": "recent_conversation", "ordinal_from_latest": 6}
        ]
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("reference_image.ordinal_invalid", diagnostic_codes(report))

    def test_mixed_reference_mechanisms_fail(self) -> None:
        spec = valid_spec()
        spec["reference_images"] = [
            "/tmp/reference.png",
            {"kind": "recent_conversation", "ordinal_from_latest": 1},
        ]
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("reference_image.mixed_mechanisms", diagnostic_codes(report))

    def test_output_outside_workspace_fails(self) -> None:
        spec = valid_spec()
        spec["workspace_root"] = "/tmp/workspace"
        spec["output_path"] = "/tmp/outside/figure.png"
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("output_path.outside_workspace", diagnostic_codes(report))

    def test_empty_sources_fail(self) -> None:
        spec = valid_spec()
        spec["sources"] = []
        report = validate_spec(spec, strict_v1=True)
        self.assertFalse(report.ok)
        self.assertIn("source.empty", diagnostic_codes(report))

    def test_legacy_spec_warns_in_compatible_mode_and_fails_strict(self) -> None:
        legacy = {
            "diagram_type": "Overall Framework",
            "layout_and_content_blocks": [
                {"exact_title_to_render_inside": "Input", "flow": "right"}
            ],
        }
        compatible = validate_spec(legacy)
        self.assertTrue(compatible.ok)
        self.assertIn("legacy.spec", diagnostic_codes(compatible))
        strict = validate_spec(legacy, strict_v1=True)
        self.assertFalse(strict.ok)
        self.assertIn("schema.v1_required", diagnostic_codes(strict))


class PackValidationTests(unittest.TestCase):
    def test_manifest_metadata_version_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                """---
name: example-skill
description: Validate a temporary example skill.
metadata:
  version: "1.1.0"
---

# Example
""",
                encoding="utf-8",
            )
            manifest = {
                "version": "1.0.0",
                "skills": [
                    {
                        "id": "example-skill",
                        "name": "Example Skill",
                        "version": "1.0.0",
                        "path": "./example-skill",
                    }
                ],
            }
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            prompt = root / "academic-figure-workflow" / "prompts"
            prompt.mkdir(parents=True)
            (prompt / "figure-worker.md").write_text(
                "\n".join(
                    (
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
                    )
                ),
                encoding="utf-8",
            )
            report = PackReport(root=str(root))
            validate_skills(root, report)
            self.assertFalse(report.ok)
            self.assertIn("manifest.version_drift", diagnostic_codes(report))

    def test_worker_prompt_requires_every_bounded_contract_field(self) -> None:
        required_fields = (
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
        )
        complete_prompt = "\n".join(required_fields)
        for missing_field in required_fields:
            with self.subTest(missing_field=missing_field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                skill = root / "example-skill"
                skill.mkdir()
                (skill / "SKILL.md").write_text(
                    """---
name: example-skill
description: Validate a temporary example skill.
metadata:
  version: "1.0.0"
---
""",
                    encoding="utf-8",
                )
                (root / "manifest.json").write_text(
                    json.dumps(
                        {
                            "version": "1.0.0",
                            "skills": [
                                {
                                    "id": "example-skill",
                                    "name": "Example Skill",
                                    "version": "1.0.0",
                                    "path": "./example-skill",
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                prompt = root / "academic-figure-workflow" / "prompts"
                prompt.mkdir(parents=True)
                (prompt / "figure-worker.md").write_text(
                    complete_prompt.replace(missing_field, "", 1),
                    encoding="utf-8",
                )
                report = PackReport(root=str(root))
                validate_skills(root, report)
                self.assertIn("worker_prompt.contract", diagnostic_codes(report))

    def test_shared_reference_hash_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "docs" / "palettes.md"
            target = root / "example-skill" / "references" / "palettes.md"
            source.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            source.write_text("canonical\n", encoding="utf-8")
            target.write_text("stale\n", encoding="utf-8")
            report = PackReport(root=str(root))
            validate_reference_items(root, [SyncItem(source, target)], report)
            self.assertFalse(report.ok)
            self.assertIn("reference.drift", diagnostic_codes(report))

    def test_sync_shared_references_in_temporary_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "palettes.md").write_text("palette\n", encoding="utf-8")
            (docs / "missing-info-policy.md").write_text("missing\n", encoding="utf-8")
            (docs / "render-audit.md").write_text("audit\n", encoding="utf-8")
            (docs / "codex-image-workflow.md").write_text(
                "codex image workflow\n", encoding="utf-8"
            )
            styles = docs / "styles"
            styles.mkdir()
            (styles / "illustrated.md").write_text(
                "illustrated style\n", encoding="utf-8"
            )
            skill_ids = [
                "academic-figure-workflow",
                "academic-figure-prompt",
                "other-skill",
            ]
            manifest = {"skills": []}
            for skill_id in skill_ids:
                (root / skill_id).mkdir()
                manifest["skills"].append(
                    {"id": skill_id, "path": f"./{skill_id}"}
                )
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            stale = synchronize(root)
            self.assertEqual(11, len(stale))
            self.assertEqual([], synchronize(root, check=True))
            for skill_id in skill_ids:
                self.assertEqual(
                    "palette\n",
                    (root / skill_id / "references" / "palettes.md").read_text(encoding="utf-8"),
                )
            self.assertTrue(
                (root / "academic-figure-workflow" / "references" / "render-audit.md").is_file()
            )
            self.assertFalse((root / "other-skill" / "references" / "render-audit.md").exists())
            for skill_id in (
                "academic-figure-workflow",
                "academic-figure-prompt",
            ):
                self.assertEqual(
                    "illustrated style\n",
                    (
                        root
                        / skill_id
                        / "references"
                        / "styles"
                        / "illustrated.md"
                    ).read_text(encoding="utf-8"),
                )
            self.assertFalse(
                (root / "other-skill" / "references" / "styles").exists()
            )

            codex_target = (
                root
                / "academic-figure-workflow"
                / "references"
                / "codex-image-workflow.md"
            )
            self.assertEqual("codex image workflow\n", codex_target.read_text(encoding="utf-8"))
            codex_target.write_text("drifted workflow\n", encoding="utf-8")
            drift = synchronize(root, check=True)
            self.assertEqual(1, len(drift))
            self.assertEqual(docs / "codex-image-workflow.md", drift[0].source)
            self.assertEqual(codex_target, drift[0].target)

    def test_sync_refuses_reference_directory_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary)
            docs = root / "docs"
            styles = docs / "styles"
            styles.mkdir(parents=True)
            (docs / "palettes.md").write_text("palette\n", encoding="utf-8")
            (docs / "missing-info-policy.md").write_text("missing\n", encoding="utf-8")
            (docs / "render-audit.md").write_text("audit\n", encoding="utf-8")
            (docs / "codex-image-workflow.md").write_text("codex\n", encoding="utf-8")
            (styles / "style.md").write_text("style\n", encoding="utf-8")

            skill = root / "academic-figure-workflow"
            skill.mkdir()
            (skill / "references").symlink_to(Path(outside), target_is_directory=True)
            (root / "manifest.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "id": "academic-figure-workflow",
                                "path": "./academic-figure-workflow",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "outside repository"):
                synchronize(root)
            self.assertEqual([], list(Path(outside).iterdir()))


if __name__ == "__main__":
    unittest.main()
