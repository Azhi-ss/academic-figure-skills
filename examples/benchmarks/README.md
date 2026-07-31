# Real-repo Benchmarks

Goldens derived from real public repos (cloned into git-ignored `ref_repos/`).

| id | repo | category | license | tests |
|----|------|----------|---------|-------|
| stable-diffusion | CompVis/stable-diffusion | DL/CV | CreativeML Open RAIL-M | diffusion baseline; anchors fictional example 01 |
| nanogpt | karpathy/nanoGPT | DL/NLP | MIT | minimal transformer; module_count=1 via top_level_dirs |
| esm | facebookresearch/esm | protein/AI4Science | MIT | protein classification row |
| alphafold | google-deepmind/alphafold | protein/JAX | Apache-2.0 | protein + non-PyTorch stack |
| graphcast | google-deepmind/graphcast | GNN/scientific | Apache-2.0 | GNN/weather outside DL taxonomy |
| transformers | huggingface/transformers | huge-repo | Apache-2.0 | sampling cap; no keyword-scan leak |
| fixture-sparse | synthetic (scripts/create_sparse_fixture.py) | sparse-input | — | simulate.py entry; no model files; evidence-insufficient |

## Reproduce

# 1. clone (shallow, git-ignored)
python3 academic-repo-analyzer/scripts/fetch_benchmark_repos.py --manifest examples/benchmarks/manifest.json
# 2. create the sparse fixture
python3 academic-repo-analyzer/scripts/create_sparse_fixture.py
# 3. for each repo, run academic-repo-analyzer and write ref_repos/<id>/analysis/<id>-analysis.md
# 4. score
python3 academic-repo-analyzer/scripts/run_repo_benchmarks.py --manifest examples/benchmarks/manifest.json

Report: `ref_repos/benchmark-report.md`. Exit code 0 = all checks pass.
Pinned commits + license per repo: `manifest.json`.
