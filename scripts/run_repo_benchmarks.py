#!/usr/bin/env python3
"""Score analyzer outputs against examples/benchmarks/manifest expectations.

Writes ref_repos/benchmark-report.md. Exit 0 iff every check passes.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ANALYSIS_DIR = "analysis"
LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "NOTICE", "LICENCE")
KEYWORD_EXPECTATIONS = ("framework", "task_any", "paths_any", "architecture_any", "entry_script")
REQUIRED_SECTIONS = {
    "completeness block": ["信息完整度", "completeness"],
    "figure suggestions": ["配图建议", "figure suggestion"],
}
FLAG_NEEDLES = {
    "limited_sample": ["抽样", "limited sample", "huge repo"],
    "evidence_insufficient": ["证据不足", "evidence insufficient"],
}

EXPECTED = {
    "stable-diffusion": {
        "framework": ["PyTorch"],
        "task_any": ["diffusion", "latent diffusion", "text-to-image"],
        "paths_any": ["ldm/", "models/"],
        "architecture_any": ["U-Net", "UNet", "autoencoder", "VAE", "CLIP"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 4},
    },
    "nanogpt": {
        "framework": ["PyTorch"],
        "task_any": ["GPT", "transformer", "language model"],
        "paths_any": ["model.py"],
        "architecture_any": ["GPT", "transformer", "attention"],
        "module_count": {"source": ["top_level_dirs"], "value": 1},
    },
    "esm": {
        "framework": ["PyTorch"],
        "task_any": ["protein", "esm"],
        "paths_any": ["esm/"],
        "architecture_any": ["transformer"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 2},
    },
    "alphafold": {
        "framework": ["JAX", "Haiku"],
        "task_any": ["protein"],
        "paths_any": ["alphafold/", "alphafold/model/"],
        "architecture_any": ["Evoformer", "structure module", "MSA"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 4},
    },
    "graphcast": {
        "framework": ["JAX", "Haiku"],
        "task_any": ["weather", "forecast"],
        "paths_any": ["graphcast/"],
        "architecture_any": ["GNN", "graph neural", "message passing", "GraphCast"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 2},
    },
    "transformers": {
        "framework": ["PyTorch"],
        "task_any": ["transformer", "language model", "LLM"],
        "limited_sample": True,
        "no_keyword_scan_mention": True,
        "module_count": {"source": ["top_level_dirs"], "value_min": 10},
    },
    "fixture-sparse": {
        "entry_script": ["simulate.py"],
        "evidence_insufficient": True,
        "no_keyword_scan_mention": True,
        "module_count": {"source": ["component_scan"], "value": 2},
    },
    "cyclegan": {
        "framework": ["PyTorch"],
        "task_any": ["GAN", "image translation", "image-to-image", "unpaired"],
        "paths_any": ["models/", "data/"],
        "architecture_any": ["generator", "discriminator", "PatchGAN", "ResNet", "cycle"],
        "module_count": {"source": ["top_level_dirs"], "value_min": 4},
    },
    "nerf": {
        "framework": ["TensorFlow", "tensorflow"],
        "task_any": ["NeRF", "neural radiance", "volume rendering", "3D", "view synthesis"],
        "paths_any": ["run_nerf.py", "run_nerf_helpers.py"],
        "architecture_any": ["MLP", "positional encoding", "ray", "volume rendering", "render_rays"],
        "module_count": {"source": ["component_scan"], "value_min": 3},
    },
    "detr": {
        "framework": ["PyTorch"],
        "task_any": ["detection", "object detection", "DETR", "transformer"],
        "paths_any": ["models/", "datasets/", "engine.py", "main.py"],
        "architecture_any": ["transformer", "backbone", "object quer", "bipartite", "Hungarian", "matcher", "encoder", "decoder"],
        "module_count": {"source": ["top_level_dirs"], "value_min": 4},
    },
    "whisper": {
        "framework": ["PyTorch"],
        "task_any": ["speech", "ASR", "transcrib", "audio", "Whisper"],
        "paths_any": ["whisper/", "whisper/model.py", "whisper/audio.py", "whisper/decoding.py"],
        "architecture_any": ["encoder", "decoder", "transformer", "attention", "mel", "convolution"],
        "module_count": {"source": ["top_level_dirs"], "value_min": 1},
    },
}

LICENSE_BY_ID = {
    "stable-diffusion": "CreativeML Open RAIL-M",
    "nanogpt": "MIT",
    "esm": "MIT",
    "alphafold": "Apache",
    "graphcast": "Apache",
    "transformers": "Apache",
    "fixture-sparse": None,
    "cyclegan": "Redistribution",
    "nerf": "MIT",
    "detr": "Apache",
    "whisper": "MIT",
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def has_any(text: str, needles) -> bool:
    low = text.lower()
    return any(needle.lower() in low for needle in needles)


def check(repo_id: str, manifest_root: Path) -> list[str]:
    errs = []
    exp = EXPECTED[repo_id]
    repo_dir = manifest_root / repo_id
    analysis = load_text(repo_dir / ANALYSIS_DIR / f"{repo_id}-analysis.md")
    if not analysis:
        return [f"{repo_id}: missing {ANALYSIS_DIR}/{repo_id}-analysis.md"]
    for key in KEYWORD_EXPECTATIONS:
        if key in exp and not has_any(analysis, exp[key]):
            errs.append(f"{repo_id}: {key} {exp[key]} not found")
    for label, needles in REQUIRED_SECTIONS.items():
        if not has_any(analysis, needles):
            errs.append(f"{repo_id}: {label} missing")
    for key, needles in FLAG_NEEDLES.items():
        if exp.get(key) and not has_any(analysis, needles):
            errs.append(f"{repo_id}: {key} note missing")
    if exp.get("no_keyword_scan_mention") and re.search(r"keyword.scan", analysis, re.I):
        errs.append(
            f"{repo_id}: analysis mentions keyword-scan (internal method, must not leak)"
        )
    module_count = exp.get("module_count")
    if module_count:
        match = re.search(
            r"module_count[^\n]*?source:\s*([A-Za-z_]+)[^\n]*?value:\s*(\d+)",
            analysis,
        )
        if not match:
            errs.append(
                f"{repo_id}: handoff module_count line missing "
                "(need 'module_count' + 'source:' + 'value:')"
            )
        else:
            source, value = match.group(1), int(match.group(2))
            if source not in module_count["source"]:
                errs.append(
                    f"{repo_id}: module_count source={source} not in {module_count['source']}"
                )
            if "value" in module_count and value != module_count["value"]:
                errs.append(
                    f"{repo_id}: module_count value={value} != {module_count['value']}"
                )
            if "value_min" in module_count and value < module_count["value_min"]:
                errs.append(
                    f"{repo_id}: module_count value={value} < {module_count['value_min']}"
                )
    license_name = LICENSE_BY_ID[repo_id]
    if license_name:
        license_files = [repo_dir / name for name in LICENSE_FILES if (repo_dir / name).exists()]
        if not license_files:
            errs.append(f"{repo_id}: no LICENSE-like file found in clone")
        elif not has_any("\n".join(load_text(path) for path in license_files), [license_name]):
            errs.append(f"{repo_id}: license text does not contain '{license_name}'")
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--repos", nargs="+", default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    base = root / data["clone_root"]
    repo_ids = [repo["id"] for repo in data["repos"]] + [
        fixture["id"] for fixture in data.get("synthetic_fixtures", [])
    ]
    if args.repos:
        repo_ids = [repo_id for repo_id in repo_ids if repo_id in set(args.repos)]
    all_errs = []
    for repo_id in repo_ids:
        all_errs.extend(check(repo_id, base))
    report = base / "benchmark-report.md"
    lines = [
        "# Repo Benchmark Report",
        f"- generated: {datetime.now(timezone.utc).isoformat()}",
        f"- repos: {len(repo_ids)}",
        f"- result: {'PASS' if not all_errs else 'FAIL'}",
        "",
    ]
    lines += [f"- [FAIL] {error}" for error in all_errs] or ["- all checks passed"]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if not all_errs else 1


if __name__ == "__main__":
    sys.exit(main())
