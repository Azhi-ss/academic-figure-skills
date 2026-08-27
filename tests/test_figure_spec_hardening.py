from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_DIR = ROOT / "academic-figure-designer" / "scripts"
sys.path.insert(0, str(VALIDATOR_DIR))

from validate_figure_spec import main, validate_path, validate_spec  # noqa: E402


def valid_spec(workspace: Path, *, prompt_review: str = "waived") -> dict:
    return {
        "schema": "academic-figure/FigureSpec@1",
        "figure_id": "figure_1",
        "plan_revision": "r1",
        "sources": [
            {
                "kind": "repository",
                "uri_or_path": str(workspace),
                "revision_or_page": "abc123",
                "evidence": "src/controller.py:run",
            }
        ],
        "prompt": "A grounded academic figure showing a typed scientific loop.",
        "aspect_ratio": "16:9",
        "final_width_mm": 183,
        "visible_text": [
            {"text": "Evidence", "component_id": "evidence", "priority": "primary"},
            "Policy",
        ],
        "layout": {
            "composition": "pipeline",
            "hero": "policy",
            "reading_order": ["evidence", "policy"],
        },
        "topology": {
            "components": [
                {"id": "evidence", "label": "Evidence"},
                {"id": "policy", "label": "Policy"},
            ],
            "connections": [
                {
                    "from": "evidence",
                    "to": "policy",
                    "kind": "executed",
                    "direction": "forward",
                    "label": "evidence flow",
                }
            ],
        },
        "style_profile": "classic-technical",
        "style_preset": None,
        "style_source": "default",
        "style_grammar": {"composition": "pipeline"},
        "semantic_color_roles": {"evidence": "#0072B2"},
        "reference_images": [],
        "must_not_claim": ["Autonomous wet-lab execution"],
        "forbidden_connections": ["policy -> numeric_prediction"],
        "negative_constraints": ["No invented components"],
        "prompt_review": prompt_review,
        "workspace_root": str(workspace),
        "output_path": str(workspace / "figure_1.png"),
        "caption_notes": ["Keep the caption evidence-grounded."],
    }


def codes(report) -> set[str]:
    return {item.code for item in report.diagnostics}


class MalformedTypeTests(unittest.TestCase):
    def test_all_json_types_return_diagnostics_instead_of_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            mutations = {
                "prompt_review": lambda spec: spec.__setitem__("prompt_review", []),
                "aspect_ratio": lambda spec: spec.__setitem__("aspect_ratio", {}),
                "style_profile": lambda spec: spec.__setitem__("style_profile", []),
                "style_profile_id": lambda spec: spec.__setitem__("style_profile", {"id": []}),
                "composition": lambda spec: spec["layout"].__setitem__("composition", []),
                "direction": lambda spec: spec["topology"]["connections"][0].__setitem__("direction", []),
                "style_source": lambda spec: spec.__setitem__("style_source", []),
            }
            for name, mutate in mutations.items():
                with self.subTest(name=name):
                    spec = valid_spec(workspace)
                    mutate(spec)
                    report = validate_spec(spec, strict_v1=True)
                    self.assertFalse(report.ok, report.to_dict())


class ManualSchemaParityTests(unittest.TestCase):
    def test_visible_text_priority_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            spec["visible_text"][0]["priority"] = "decorative"
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("visible_text.priority_invalid", codes(report))

    def test_connection_kind_must_be_nonempty_and_label_must_be_string(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            connection = spec["topology"]["connections"][0]
            connection["kind"] = "  "
            connection["label"] = 7
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("connection.kind_required", codes(report))
            self.assertIn("connection.label_type", codes(report))

    def test_caption_notes_shape_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            spec["caption_notes"] = "not an array"
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("caption_notes.type", codes(report))

            spec = valid_spec(Path(temporary))
            spec["caption_notes"] = ["valid", 1]
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("caption_notes.item_type", codes(report))

    def test_reference_descriptor_rejects_extra_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            reference = workspace / "reference.png"
            reference.write_bytes(b"image fixture")
            spec = valid_spec(workspace)
            spec["reference_images"] = [
                {"kind": "local_path", "path": str(reference), "ordinal_from_latest": 1}
            ]
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("reference_image.extra_keys", codes(report))

    def test_style_preset_and_source_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            spec["style_preset"] = []
            spec["style_source"] = "guess"
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("style_preset.type", codes(report))
            self.assertIn("style_source.invalid", codes(report))

    def test_reviewed_digest_shape_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            spec["prompt_reviewed_sha256"] = "ABC"
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("prompt_reviewed_sha256.invalid", codes(report))

    def test_explicit_null_is_rejected_where_schema_does_not_allow_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec = valid_spec(Path(temporary))
            spec["visible_text"][0]["priority"] = None
            spec["topology"]["connections"][0]["label"] = None
            spec["caption_notes"] = None
            spec["style_source"] = None
            spec["prompt_reviewed_sha256"] = None
            report = validate_spec(spec, strict_v1=True)
            self.assertIn("visible_text.priority_invalid", codes(report))
            self.assertIn("connection.label_type", codes(report))
            self.assertIn("caption_notes.type", codes(report))
            self.assertIn("style_source.invalid", codes(report))
            self.assertIn("prompt_reviewed_sha256.invalid", codes(report))


class RenderReadyTests(unittest.TestCase):
    def test_requested_review_blocks_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace, prompt_review="requested")
            structural = validate_spec(spec, strict_v1=True)
            self.assertTrue(structural.ok, structural.to_dict())
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("prompt_review.render_blocked", codes(report))

    def test_confirmed_review_requires_digest_matching_exact_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace, prompt_review="confirmed")
            missing = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("prompt_reviewed_sha256.required", codes(missing))

            spec["prompt_reviewed_sha256"] = "0" * 64
            mismatch = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("prompt_reviewed_sha256.mismatch", codes(mismatch))

            spec["prompt_reviewed_sha256"] = hashlib.sha256(
                spec["prompt"].encode("utf-8")
            ).hexdigest()
            matching = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertTrue(matching.ok, matching.to_dict())

    def test_unencodable_confirmed_prompt_returns_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace, prompt_review="confirmed")
            spec["prompt"] = "\ud800"
            spec["prompt_reviewed_sha256"] = "0" * 64
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("prompt.utf8_invalid", codes(report))

    def test_waived_review_is_render_ready_without_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            report = validate_spec(
                valid_spec(workspace),
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertTrue(report.ok, report.to_dict())

    def test_review_digest_is_forbidden_unless_review_is_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            for review in ("requested", "waived"):
                with self.subTest(review=review):
                    spec = valid_spec(workspace, prompt_review=review)
                    spec["prompt_reviewed_sha256"] = hashlib.sha256(
                        spec["prompt"].encode("utf-8")
                    ).hexdigest()
                    report = validate_spec(
                        spec,
                        render_ready=True,
                        trusted_workspace_root=workspace,
                    )
                    self.assertIn(
                        "prompt_reviewed_sha256.unexpected",
                        codes(report),
                    )
                    if review == "requested":
                        self.assertIn("prompt_review.render_blocked", codes(report))

    def test_render_ready_requires_trusted_matching_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace)
            missing = validate_spec(spec, render_ready=True)
            self.assertIn("workspace_root.trusted_required", codes(missing))

            other = workspace / "other"
            other.mkdir()
            mismatch = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=other,
            )
            self.assertIn("workspace_root.trusted_mismatch", codes(mismatch))
            self.assertIn("output_path.outside_trusted_workspace", codes(mismatch))

    def test_trusted_workspace_must_be_an_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace)

            missing_root = workspace / "missing"
            missing = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=missing_root,
            )
            self.assertIn("workspace_root.trusted_not_directory", codes(missing))

            file_root = workspace / "not-a-directory"
            file_root.write_text("fixture", encoding="utf-8")
            regular_file = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=file_root,
            )
            self.assertIn("workspace_root.trusted_not_directory", codes(regular_file))

    def test_output_parent_symlink_cannot_escape_trusted_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            workspace = Path(temporary)
            link = workspace / "linked-output"
            try:
                link.symlink_to(Path(outside), target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            spec = valid_spec(workspace)
            spec["output_path"] = str(link / "figure.png")
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("output_path.outside_trusted_workspace", codes(report))

    def test_output_path_itself_must_not_be_a_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            target = workspace / "existing.png"
            target.write_bytes(b"existing artifact")
            link = workspace / "figure-link.png"
            try:
                link.symlink_to(target)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            spec = valid_spec(workspace)
            spec["output_path"] = str(link)
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("output_path.symlink", codes(report))

    def test_cli_render_ready_and_workspace_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec_path = workspace / "figure.figure-spec.json"
            spec_path.write_text(json.dumps(valid_spec(workspace)), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(
                    [
                        "--render-ready",
                        "--workspace-root",
                        str(workspace),
                        "--json",
                        str(spec_path),
                    ]
                )
            self.assertEqual(0, status, output.getvalue())

    def test_validate_path_exposes_render_ready_api(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec_path = workspace / "figure.figure-spec.json"
            spec_path.write_text(json.dumps(valid_spec(workspace)), encoding="utf-8")
            report = validate_path(
                spec_path,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertTrue(report.ok, report.to_dict())


class RenderReferenceTests(unittest.TestCase):
    def test_render_ready_local_reference_must_exist_and_be_regular(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace)
            spec["reference_images"] = [str(workspace / "missing.png")]
            missing = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("reference_image.missing", codes(missing))

            spec["reference_images"] = [str(workspace)]
            directory = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("reference_image.not_file", codes(directory))

    def test_invalid_filesystem_string_returns_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace)
            spec["reference_images"] = ["/invalid/\x00/reference.png"]
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("reference_image.inaccessible", codes(report))

    def test_render_ready_rejects_symlink_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            target = workspace / "target.png"
            target.write_bytes(b"image fixture")
            link = workspace / "link.png"
            try:
                link.symlink_to(target)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            spec = valid_spec(workspace)
            spec["reference_images"] = [str(link)]
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertIn("reference_image.symlink", codes(report))

    def test_regular_local_reference_passes_render_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            reference = workspace / "reference.png"
            reference.write_bytes(b"image fixture")
            spec = valid_spec(workspace)
            spec["reference_images"] = [
                {"kind": "local_path", "path": str(reference)}
            ]
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertTrue(report.ok, report.to_dict())

    def test_recent_conversation_reference_warns_as_nonreproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            spec = valid_spec(workspace)
            spec["style_profile"] = "reference-led"
            spec["reference_images"] = [
                {"kind": "recent_conversation", "ordinal_from_latest": 1}
            ]
            report = validate_spec(
                spec,
                render_ready=True,
                trusted_workspace_root=workspace,
            )
            self.assertTrue(report.ok, report.to_dict())
            self.assertIn("reference_image.nonreproducible", codes(report))


if __name__ == "__main__":
    unittest.main()
