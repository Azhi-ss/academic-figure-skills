#!/usr/bin/env python3
"""Synchronize shared files into installable skill directories.

The repository keeps authoritative shared documents under ``docs/`` and the
FigureSpec schema, validator, and metadata cleaner under
``academic-figure-designer/``.  Skill installers may copy a single skill
directory without the rest of the repository, so every skill needs vendored
copies of the files it consumes.  This script is the only writer for those
copies.

Run without arguments to update copies, or with ``--check`` in CI to make drift
an error without changing the working tree.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


FIGURE_SKILLS = frozenset({"academic-figure-designer", "academic-figure-workflow"})
WORKFLOW_FILES_FROM_DESIGNER = (
    "figure-spec.schema.json",
    "scripts/validate_figure_spec.py",
    "scripts/clean_image_metadata.py",
)


@dataclass(frozen=True)
class SyncItem:
    source: Path
    target: Path

    @property
    def in_sync(self) -> bool:
        return self.target.is_file() and filecmp.cmp(self.source, self.target, shallow=False)


def load_skill_paths(root: Path) -> dict[str, Path]:
    """Load skill id -> directory mappings from the pack manifest."""

    root = root.resolve()
    manifest_path = root / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(skills, list):
        raise ValueError(f"{manifest_path}: 'skills' must be a list")

    result: dict[str, Path] = {}
    for index, entry in enumerate(skills):
        skill_id = entry.get("id") if isinstance(entry, dict) else None
        raw_path = entry.get("path") if isinstance(entry, dict) else None
        if not (isinstance(skill_id, str) and skill_id and isinstance(raw_path, str) and raw_path):
            raise ValueError(f"{manifest_path}: skills[{index}] needs non-empty string 'id' and 'path'")
        if skill_id in result:
            raise ValueError(f"{manifest_path}: duplicate skill id {skill_id!r}")
        skill_dir = (root / raw_path).resolve()
        if not skill_dir.is_relative_to(root):
            raise ValueError(f"{manifest_path}: skill path escapes repository: {raw_path!r}")
        result[skill_id] = skill_dir
    return result


def build_sync_plan(root: Path) -> list[SyncItem]:
    """Return every canonical source and vendored destination pair."""

    root = root.resolve()
    skills = load_skill_paths(root)
    docs = root / "docs"
    styles = sorted((docs / "styles").glob("*.md"))
    plan: list[SyncItem] = []
    for skill_id, skill_dir in sorted(skills.items()):
        references = skill_dir / "references"
        plan.append(SyncItem(docs / "missing-info-policy.md", references / "missing-info-policy.md"))
        if skill_id in FIGURE_SKILLS:
            plan += [SyncItem(docs / name, references / name) for name in ("palettes.md", "render-audit.md")]
            plan += [SyncItem(style, references / "styles" / style.name) for style in styles]
    if FIGURE_SKILLS <= skills.keys():
        designer = skills["academic-figure-designer"]
        workflow = skills["academic-figure-workflow"]
        plan += [SyncItem(designer / name, workflow / name) for name in WORKFLOW_FILES_FROM_DESIGNER]
    return plan


def synchronize(root: Path, *, check: bool = False) -> list[SyncItem]:
    """Check or update the sync plan and return items that were out of sync."""

    stale = [item for item in build_sync_plan(root) if not item.in_sync]
    if not check:
        for item in stale:
            item.target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item.source, item.target)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="skill-pack root (default: repository containing this script)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without writing files",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        stale = synchronize(root, check=args.check)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if not stale:
        print("shared references are in sync")
        return 0

    verb = "out of sync" if args.check else "synchronized"
    print(f"{verb}: {len(stale)} shared reference(s)")
    for item in stale:
        print(f"- {item.target.relative_to(root)}")
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
