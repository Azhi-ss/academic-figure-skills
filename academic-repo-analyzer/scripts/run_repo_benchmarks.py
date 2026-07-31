#!/usr/bin/env python3
"""Score repo-analyzer outputs against examples/benchmarks/manifest expectations.

Writes ref_repos/benchmark-report.md. Exit 0 iff every check passes.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List

ANALYSIS_DIR = "analysis"
LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "NOTICE", "LICENCE")

EXPECTED = {
    "stable-diffusion": {
        "framework": ["PyTorch"],
        "task_any": ["diffusion", "latent diffusion", "text-to-image"],
        "paths_any": ["ldm/", "models/"],
        "architecture_any": ["U-Net", "UNet", "autoencoder", "VAE", "CLIP"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 4},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "nanogpt": {
        "framework": ["PyTorch"],
        "task_any": ["GPT", "transformer", "language model"],
        "paths_any": ["model.py"],
        "architecture_any": ["GPT", "transformer", "attention"],
        "module_count": {"source": ["top_level_dirs"], "value": 1},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "esm": {
        "framework": ["PyTorch"],
        "task_any": ["protein", "esm"],
        "paths_any": ["esm/"],
        "architecture_any": ["transformer"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 2},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "alphafold": {
        "framework_any": ["JAX", "Haiku"],
        "task_any": ["protein"],
        "paths_any": ["alphafold/", "alphafold/model/"],
        "architecture_any": ["Evoformer", "structure module", "MSA"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 4},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "graphcast": {
        "framework_any": ["JAX", "Haiku"],
        "task_any": ["weather", "forecast"],
        "paths_any": ["graphcast/"],
        "architecture_any": ["GNN", "graph neural", "message passing", "GraphCast"],
        "module_count": {"source": ["top_level_dirs", "component_scan"], "value_min": 2},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "transformers": {
        "framework": ["PyTorch"],
        "task_any": ["transformer", "language model", "LLM"],
        "limited_sample": True,
        "no_keyword_scan_mention": True,
        "module_count": {"source": ["top_level_dirs"], "value_min": 10},
        "completeness_block": True,
        "figure_suggestions": True,
    },
    "fixture-sparse": {
        "entry_script": ["simulate.py"],
        "evidence_insufficient": True,
        "no_keyword_scan_mention": True,
        "module_count": {"source": ["component_scan"], "value": 2},
        "completeness_block": True,
        "figure_suggestions": True,
    },
}

LICENSE_BY_ID = {
    "stable-diffusion": "MIT",
    "nanogpt": "MIT",
    "esm": "MIT",
    "alphafold": "Apache",
    "graphcast": "Apache",
    "transformers": "Apache",
    "fixture-sparse": None,
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def has_any(text: str, needles) -> bool:
    low = text.lower()
    return any(needle.lower() in low for needle in needles)


def check(repo_id: str, root: Path, manifest_root: Path) -> List[str]:
    errs = []
    exp = EXPECTED[repo_id]
    repo_dir = manifest_root / repo_id
    analysis = load_text(repo_dir / ANALYSIS_DIR / f"{repo_id}-analysis.md")
    if not analysis:
        return [f"{repo_id}: missing {ANALYSIS_DIR}/{repo_id}-analysis.md"]
    if exp.get("framework") and not has_any(analysis, exp["framework"]):
        errs.append(f"{repo_id}: framework {exp['framework']} not found")
    if exp.get("framework_any") and not has_any(analysis, exp["framework_any"]):
        errs.append(f"{repo_id}: none of {exp['framework_any']} found")
    if exp.get("task_any") and not has_any(analysis, exp["task_any"]):
        errs.append(f"{repo_id}: task keywords {exp['task_any']} not found")
    if exp.get("paths_any") and not has_any(analysis, exp["paths_any"]):
        errs.append(f"{repo_id}: paths {exp['paths_any']} not found")
    if exp.get("architecture_any") and not has_any(analysis, exp["architecture_any"]):
        errs.append(f"{repo_id}: architecture {exp['architecture_any']} not found")
    if exp.get("entry_script") and not has_any(analysis, exp["entry_script"]):
        errs.append(f"{repo_id}: entry script {exp['entry_script']} not found")
    if exp.get("completeness_block") and not has_any(analysis, ["信息完整度", "completeness"]):
        errs.append(f"{repo_id}: completeness block missing")
    if exp.get("figure_suggestions") and not has_any(analysis, ["配图建议", "figure suggestion"]):
        errs.append(f"{repo_id}: figure suggestions missing")
    if exp.get("limited_sample") and not has_any(analysis, ["抽样", "limited sample", "huge repo"]):
        errs.append(f"{repo_id}: limited-sample note missing")
    if exp.get("evidence_insufficient") and not has_any(
        analysis, ["证据不足", "evidence insufficient"]
    ):
        errs.append(f"{repo_id}: evidence-insufficient label missing")
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
        if not any((repo_dir / filename).exists() for filename in LICENSE_FILES):
            errs.append(f"{repo_id}: no LICENSE-like file found in clone")
        elif not has_any(
            "\n".join(
                load_text(repo_dir / filename)
                for filename in LICENSE_FILES
                if (repo_dir / filename).exists()
            ),
            [license_name],
        ):
            errs.append(f"{repo_id}: license text does not contain '{license_name}'")
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--repos", nargs="+", default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    base = root / data["clone_root"]
    repo_ids = [repo["id"] for repo in data["repos"]] + [
        fixture["id"] for fixture in data.get("synthetic_fixtures", [])
    ]
    if args.repos:
        repo_ids = [repo_id for repo_id in repo_ids if repo_id in set(args.repos)]
    all_errs = []
    for repo_id in repo_ids:
        all_errs.extend(check(repo_id, root, base))
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
