from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sync_shared_refs import (  # noqa: E402
    STYLE_LIBRARY_SKILLS,
    build_sync_plan,
    synchronize,
)
from validate_skill_pack import (  # noqa: E402
    PackReport,
    validate_shared_refs,
    validate_skills,
)


def _write_skill(root: Path, skill_id: str) -> None:
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


def _write_pack(
    root: Path,
    skill_ids: list[str],
    *,
    style_names: tuple[str, ...] = ("style.md",),
) -> None:
    docs = root / "docs"
    styles = docs / "styles"
    styles.mkdir(parents=True)
    (docs / "palettes.md").write_text("palette\n", encoding="utf-8")
    (docs / "missing-info-policy.md").write_text("missing\n", encoding="utf-8")
    (docs / "render-audit.md").write_text("audit\n", encoding="utf-8")
    (docs / "codex-image-workflow.md").write_text("codex\n", encoding="utf-8")
    for name in style_names:
        (styles / name).write_text(f"style: {name}\n", encoding="utf-8")

    entries = []
    for skill_id in skill_ids:
        _write_skill(root, skill_id)
        entries.append(
            {
                "id": skill_id,
                "path": f"./{skill_id}",
                "version": "1.0.0",
            }
        )
    (root / "manifest.json").write_text(
        json.dumps({"version": "1.0.0", "skills": entries}),
        encoding="utf-8",
    )


def _diagnostic_codes(report: PackReport) -> set[str]:
    return {item.code for item in report.diagnostics}


class PackHardeningTests(unittest.TestCase):
    def test_sync_refuses_target_symlink_even_inside_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_pack(root, ["example-skill"])
            decoy = root / "decoy.md"
            decoy.write_text("do not overwrite\n", encoding="utf-8")
            target = root / "example-skill" / "references" / "palettes.md"
            target.parent.mkdir()
            target.symlink_to(decoy)

            report = PackReport(root=str(root))
            validate_shared_refs(root, report)
            self.assertIn("reference.target_symlink", _diagnostic_codes(report))
            with self.assertRaisesRegex(ValueError, "symlink path"):
                synchronize(root, check=True)
            with self.assertRaisesRegex(ValueError, "symlink path"):
                synchronize(root)

            self.assertTrue(target.is_symlink())
            self.assertEqual("do not overwrite\n", decoy.read_text(encoding="utf-8"))

    def test_sync_refuses_parent_symlink_even_inside_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_pack(root, ["example-skill"])
            real_references = root / "real-references"
            real_references.mkdir()
            (root / "example-skill" / "references").symlink_to(
                real_references,
                target_is_directory=True,
            )

            report = PackReport(root=str(root))
            validate_shared_refs(root, report)
            self.assertIn("reference.target_symlink", _diagnostic_codes(report))
            with self.assertRaisesRegex(ValueError, "symlink path"):
                synchronize(root)
            self.assertEqual([], list(real_references.iterdir()))

    def test_unregistered_top_level_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_pack(root, ["registered-skill"])
            _write_skill(root, "rogue-skill")

            report = PackReport(root=str(root))
            validate_skills(root, report)

            self.assertFalse(report.ok)
            self.assertIn("manifest.skill_unregistered", _diagnostic_codes(report))
            rogue = [
                item
                for item in report.diagnostics
                if item.code == "manifest.skill_unregistered"
            ]
            self.assertEqual(1, len(rogue))
            self.assertTrue(rogue[0].path.endswith("rogue-skill/SKILL.md"))

    def test_stale_vendored_style_is_rejected_for_every_style_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill_ids = sorted(STYLE_LIBRARY_SKILLS)
            _write_pack(root, skill_ids)
            synchronize(root)

            for skill_id in skill_ids:
                style_dir = root / skill_id / "references" / "styles"
                self.assertTrue((style_dir / "style.md").is_file())
                (style_dir / "deleted-style.md").write_text(
                    "stale\n",
                    encoding="utf-8",
                )

            report = PackReport(root=str(root))
            validate_shared_refs(root, report)
            extras = [
                item
                for item in report.diagnostics
                if item.code == "reference.style_extra"
            ]

            self.assertEqual(len(STYLE_LIBRARY_SKILLS), len(extras))
            self.assertEqual(
                set(skill_ids),
                {Path(item.path).parts[0] for item in extras},
            )

    def test_unicode_normalization_collision_in_style_names_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            composed = "Caf\N{LATIN SMALL LETTER E WITH ACUTE}.md"
            decomposed = "Cafe\N{COMBINING ACUTE ACCENT}.md"
            _write_pack(
                root,
                ["example-skill"],
                style_names=(composed, decomposed),
            )
            if len(list((root / "docs" / "styles").iterdir())) != 2:
                self.skipTest("filesystem normalizes Unicode filenames")

            with self.assertRaisesRegex(ValueError, r"Unicode NFC \+ casefold"):
                build_sync_plan(root)

    def test_casefold_collision_in_style_names_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_pack(
                root,
                ["example-skill"],
                style_names=("Diagram.md", "diagram.md"),
            )
            if len(list((root / "docs" / "styles").iterdir())) != 2:
                self.skipTest("filesystem folds filename case")

            with self.assertRaisesRegex(ValueError, r"Unicode NFC \+ casefold"):
                build_sync_plan(root)


if __name__ == "__main__":
    unittest.main()
