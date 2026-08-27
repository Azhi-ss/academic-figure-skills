#!/usr/bin/env python3
"""Synchronize shared documentation into installable skill directories.

The repository keeps authoritative shared documents under ``docs/``.  Skill
installers may copy a single skill directory without the repository-level docs,
so every skill needs vendored copies of the references it consumes.  This script
is the only writer for those copies.

Run without arguments to update copies, or with ``--check`` in CI to make drift
an error without changing the working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXPECTED_SKILL_IDS = frozenset(
    {
        "academic-figure-workflow",
        "academic-repo-analyzer",
        "academic-figure-draft-analyzer",
        "academic-figure-architecture-extractor",
        "academic-figure-designer",
    }
)
RENDER_AUDIT_SKILLS = frozenset(
    {
        "academic-figure-workflow",
        "academic-figure-designer",
    }
)
STYLE_LIBRARY_SKILLS = frozenset(
    {
        "academic-figure-workflow",
        "academic-figure-designer",
    }
)


@dataclass(frozen=True)
class SyncItem:
    source: Path
    target: Path

    @property
    def in_sync(self) -> bool:
        return (
            not self.target.is_symlink()
            and self.target.is_file()
            and file_digest(self.source) == file_digest(self.target)
        )


def file_digest(path: Path) -> str:
    """Return a stable SHA-256 digest for *path*."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inside(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _absolute(path: Path) -> Path:
    """Return a normalized absolute path without resolving symlinks."""

    return Path(os.path.abspath(os.fspath(path)))


def contains_symlink_component(root: Path, path: Path) -> bool:
    """Return whether any existing component from *root* to *path* is a symlink."""

    root = root.resolve()
    try:
        relative = _absolute(path).relative_to(root)
    except ValueError:
        return True
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def validate_sync_target(root: Path, target: Path) -> None:
    """Reject a destination outside *root* or containing any symlink component."""

    root = root.resolve()
    lexical_target = _absolute(target)
    if not _inside(root, lexical_target):
        raise ValueError(f"refusing to write outside repository: {target}")

    has_symlink = contains_symlink_component(root, lexical_target)
    resolved_target = lexical_target.resolve(strict=False)
    if not _inside(root, resolved_target):
        qualifier = " through symlink path" if has_symlink else ""
        raise ValueError(
            f"refusing to write outside repository{qualifier}: {target}"
        )
    if has_symlink:
        raise ValueError(f"refusing to write through symlink path: {target}")


def load_skill_paths(root: Path) -> dict[str, Path]:
    """Load safe skill id -> directory mappings from the pack manifest."""

    root = root.resolve()
    manifest_path = root / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError(f"{manifest_path}: 'skills' must be a list")

    result: dict[str, Path] = {}
    for index, entry in enumerate(skills):
        if not isinstance(entry, dict):
            raise ValueError(f"{manifest_path}: skills[{index}] must be an object")
        skill_id = entry.get("id")
        raw_path = entry.get("path")
        if not isinstance(skill_id, str) or not skill_id:
            raise ValueError(f"{manifest_path}: skills[{index}].id must be a string")
        if skill_id in result:
            raise ValueError(f"{manifest_path}: duplicate skill id {skill_id!r}")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"{manifest_path}: skills[{index}].path must be a string")
        lexical_skill_dir = _absolute(root / raw_path)
        if not _inside(root, lexical_skill_dir):
            raise ValueError(f"{manifest_path}: skill path escapes repository: {raw_path!r}")
        if contains_symlink_component(root, lexical_skill_dir):
            raise ValueError(f"{manifest_path}: skill path contains a symlink: {raw_path!r}")
        skill_dir = lexical_skill_dir.resolve(strict=False)
        if not _inside(root, skill_dir):
            raise ValueError(f"{manifest_path}: skill path escapes repository: {raw_path!r}")
        result[skill_id] = skill_dir
    return result


def load_style_sources(root: Path) -> list[Path]:
    """Load canonical Markdown styles and reject ambiguous portable filenames."""

    root = root.resolve()
    styles_dir = root / "docs" / "styles"
    if contains_symlink_component(root, styles_dir):
        raise ValueError(f"canonical style directory contains a symlink: {styles_dir}")
    if not styles_dir.is_dir():
        raise FileNotFoundError(f"canonical style library missing: {styles_dir}")

    by_portable_name: dict[str, Path] = {}
    sources: list[Path] = []
    for candidate in styles_dir.iterdir():
        if candidate.suffix.casefold() != ".md":
            continue
        if candidate.is_symlink():
            raise ValueError(f"canonical style must be a real file, not a symlink: {candidate}")
        if not candidate.is_file():
            continue
        portable_name = unicodedata.normalize("NFC", candidate.name).casefold()
        previous = by_portable_name.get(portable_name)
        if previous is not None:
            raise ValueError(
                "canonical style filename collision after Unicode NFC + casefold: "
                f"{previous.name!r} and {candidate.name!r}"
            )
        by_portable_name[portable_name] = candidate
        sources.append(candidate)

    if not sources:
        raise FileNotFoundError(f"canonical style library is empty: {styles_dir}")
    return sorted(
        sources,
        key=lambda path: (unicodedata.normalize("NFC", path.name).casefold(), path.name),
    )


def build_sync_plan(root: Path) -> list[SyncItem]:
    """Return every canonical source and vendored destination pair."""

    root = root.resolve()
    skill_paths = load_skill_paths(root)
    # Keep all shipped skill directories synchronized even while a manifest
    # edit is in progress.  A missing manifest entry must not leave a stale
    # standalone installation behind.
    for skill_id in EXPECTED_SKILL_IDS:
        skill_dir = root / skill_id
        if skill_dir.is_symlink():
            raise ValueError(f"shipped skill path contains a symlink: {skill_dir}")
        if skill_dir.is_dir():
            resolved = skill_dir.resolve()
            if not _inside(root, resolved):
                raise ValueError(
                    f"shipped skill path escapes repository: {skill_dir} -> {resolved}"
                )
            skill_paths.setdefault(skill_id, resolved)
    sources = {
        "palettes.md": root / "docs" / "palettes.md",
        "missing-info-policy.md": root / "docs" / "missing-info-policy.md",
    }
    render_audit = root / "docs" / "render-audit.md"
    codex_image_workflow = root / "docs" / "codex-image-workflow.md"
    style_sources = load_style_sources(root)

    for source in (*sources.values(), render_audit, codex_image_workflow):
        if contains_symlink_component(root, source):
            raise ValueError(f"canonical shared reference contains a symlink: {source}")
        if not source.is_file():
            raise FileNotFoundError(f"canonical shared reference missing: {source}")

    plan: list[SyncItem] = []
    for skill_id, skill_dir in sorted(skill_paths.items()):
        for filename, source in sources.items():
            plan.append(SyncItem(source, skill_dir / "references" / filename))
        if skill_id in RENDER_AUDIT_SKILLS:
            plan.append(SyncItem(render_audit, skill_dir / "references" / "render-audit.md"))
        if skill_id == "academic-figure-workflow":
            plan.append(
                SyncItem(
                    codex_image_workflow,
                    skill_dir / "references" / "codex-image-workflow.md",
                )
            )
        if skill_id in STYLE_LIBRARY_SKILLS:
            for source in style_sources:
                plan.append(
                    SyncItem(source, skill_dir / "references" / "styles" / source.name)
                )
    return plan


def _atomic_copy(root: Path, source: Path, target: Path) -> None:
    """Copy bytes atomically while refusing a symlink destination."""

    root = root.resolve()
    validate_sync_target(root, target)
    target.parent.mkdir(parents=True, exist_ok=True)
    validate_sync_target(root, target)
    payload = source.read_bytes()
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, source.stat().st_mode & 0o777)
        validate_sync_target(root, target)
        os.replace(temporary, target)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def synchronize(root: Path, *, check: bool = False) -> list[SyncItem]:
    """Check or update the sync plan and return items that were out of sync."""

    root = root.resolve()
    plan = build_sync_plan(root)
    for item in plan:
        validate_sync_target(root, item.target)
    stale = [item for item in plan if not item.in_sync]
    if not check:
        for item in stale:
            _atomic_copy(root, item.source, item.target)
    return stale


def _relative_lines(items: Iterable[SyncItem], root: Path) -> list[str]:
    root = root.resolve()
    lines = []
    for item in items:
        try:
            target = item.target.relative_to(root)
        except ValueError:
            target = item.target
        lines.append(str(target))
    return lines


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

    try:
        stale = synchronize(args.root, check=args.check)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if not stale:
        print("shared references are in sync")
        return 0

    verb = "out of sync" if args.check else "synchronized"
    print(f"{verb}: {len(stale)} shared reference(s)")
    for target in _relative_lines(stale, args.root):
        print(f"- {target}")
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
