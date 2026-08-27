# Legacy Real-repo Structural Smoke Test

These legacy goldens were derived from real public repositories cloned into the
git-ignored `ref_repos/` directory. The scorer checks required sections, selected
keywords, evidence labels, and legacy handoff lines in manually produced Markdown.

It does **not** execute an image backend, verify semantic topology against source
code, compare generated pixels, assess typography or color, measure reference-style
fidelity, or run RenderAudit v1. A passing report is a structural/keyword smoke-test
result only; it is never evidence of image quality or publication readiness.

| id | repo | category | license | tests |
|----|------|----------|---------|-------|
| stable-diffusion | CompVis/stable-diffusion | DL/CV | CreativeML Open RAIL-M | diffusion baseline; anchors fictional example 01 |
| nanogpt | karpathy/nanoGPT | DL/NLP | MIT | minimal transformer vocabulary and handoff shape |
| esm | facebookresearch/esm | protein/AI4Science | MIT | protein classification row |
| alphafold | google-deepmind/alphafold | protein/JAX | Apache-2.0 | protein + non-PyTorch stack |
| graphcast | google-deepmind/graphcast | GNN/scientific | Apache-2.0 | GNN/weather outside DL taxonomy |
| transformers | huggingface/transformers | huge-repo | Apache-2.0 | sampling cap; no keyword-scan leak |
| cyclegan | junyanz/pytorch-CycleGAN-and-pix2pix | GAN/image translation | BSD-3-Clause | generators, discriminators, and paired/unpaired flow terms |
| nerf | bmild/nerf | 3D neural rendering | MIT | MLP, ray sampling, and volume-rendering terms |
| detr | facebookresearch/detr | object detection | Apache-2.0 | Transformer, queries, and matching terms |
| whisper | openai/whisper | speech/ASR | MIT | audio encoder-decoder and mel front-end terms |
| fixture-sparse | synthetic (scripts/create_sparse_fixture.py) | sparse-input | — | simulate.py entry; no model files; evidence-insufficient |

## Reproduce

```bash
# 1. clone (shallow, git-ignored)
python3 academic-repo-analyzer/scripts/fetch_benchmark_repos.py --manifest examples/benchmarks/manifest.json
# 2. create the sparse fixture
python3 academic-repo-analyzer/scripts/create_sparse_fixture.py
# 3. manually run academic-repo-analyzer for each repo and write
#    ref_repos/<id>/analysis/<id>-analysis.md
# 4. score
python3 academic-repo-analyzer/scripts/run_repo_benchmarks.py --manifest examples/benchmarks/manifest.json
```

Report: `ref_repos/benchmark-report.md`. Exit code 0 = all checks pass.
Repository URLs/licenses: `manifest.json`. Actual fetched commits: `ref_repos/fetch-log.json`; committed golden headers record the derived short SHA.

Treat older `module_count` expectations as compatibility fixtures for the legacy
Markdown contract, not as the 3.1.0 semantic architecture definition. Release
acceptance for rendered figures requires evidence-backed FigurePlan/FigureSpec
artifacts plus a successful RenderAudit; that coverage is outside this smoke test.
