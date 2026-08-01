---
id: academic-repo-analyzer
name: Academic Repo Analyzer
version: 1.3.0
description: Quick-understanding doc for ML/DL, AI4Science, and research codebases — task type, stack, architecture, and figure-worthy innovations. Use when the user wants repo analysis, 仓库分析, or to understand a codebase before figure planning.
stages: [research, review]
tools: [bash]
---

# Academic Repo Analyzer

Produce a concise **仓库快速理解文档** for downstream figure planning.

Keywords: → `keywords.md`  
Missing info: → `references/missing-info-policy.md`

## Input Contract

- Prefer: repo path, README, deps, entry scripts, model files, configs
- Minimum: any one of README / entry script / model file
- Missing: partial analysis with 推断 / 待确认

## Output Contract — Quick Understanding Doc

- **Length: 30–60 lines.** Be concise. This is a summary for figure planning, not a code audit.
- overview (name, task, framework, architecture one-liner)
- completeness block (evidence level + what was read)
- stack details (table, ≤8 rows)
- architecture analysis (numbered, cite file/class names)
- workflow (train/inference flow, or "evidence insufficient")
- figure suggestions (2–4 concrete figures with type labels)
- Handoff block

## Steps

### Step 1: Scan structure

Locate README, dependency files, entry scripts (`train|main|eval|inference|predict|run|simulate|benchmark|demo|app|serve`), `configs/`, `models|networks|src/`, data loaders. Notebooks (`*.ipynb`) count as entry evidence when no scripts exist.

For huge repos, sampling is top-level + 3–5 core files ONLY; never run broad keyword scans; state "抽样 / limited sample" in the completeness block.

Done when: tree of key paths exists and each must-read class is read **or** marked missing.

### Step 2: Task + stack

Use `keywords.md`. Classify task type and framework from imports, deps, and paths.

Done when: task type + primary framework are stated with file evidence.

### Step 3: Architecture + algorithms

From model files: backbone family, key modules, losses, training tricks. Prefer evidence over naming guesses.

Done when: architecture summary cites concrete classes/files, or is marked 推断.

### Step 3.5: Module inventory & count

Count **architectural modules** — the major named components that would appear as boxes in a figure. Use this decision order:

1. **`top_level_dirs`** — count top-level Python package directories that contain model/algorithm code (e.g. `models/`, `ldm/`, `whisper/`, `datasets/`). Do NOT count: `tests/`, `docs/`, `scripts/`, `configs/`, `data/` download helpers, `assets/`, `.github/`.
   - Example: nanoGPT is flat (no package dirs) → do NOT use top_level_dirs.
   - Example: Whisper has one package `whisper/` → top_level_dirs = 1.
   - Example: CycleGAN has `models/`, `data/`, `util/`, `options/`, `datasets/` → top_level_dirs = 5 (count only architecture-relevant dirs).

2. **`component_scan`** — use ONLY when there are no architecture package dirs (flat repo). Count **named functional components** that a figure would show as boxes:
   - Count: distinct model/algorithm components (e.g. "Coarse NeRF MLP", "Fine NeRF MLP", "Ray sampler", "Volume renderer").
   - Do NOT count: every `nn.Module` class (LayerNorm is not a figure box), data loader scripts, config files, utility scripts, test files.
   - Do NOT count files — count the functional components those files implement.
   - A single `model.py` containing one neural network = 1 component, even if it defines 5 helper classes.

- `value`: integer count. Never infer from keyword matches alone.
- State the counting rationale in one line after the Handoff block.

### Step 4: Emit quick-understanding doc

```markdown
# 仓库快速理解文档
## 仓库概览
| 项目 | 内容 |
| 仓库名称 / 任务类型 / 核心框架 / 主要架构 / 一句话描述 | ... |
## 信息完整度说明
## 技术栈详情
## 模型架构分析
## 工作流程
## 配图建议（→ paper-analyzer）
## Handoff (→ paper-analyzer)
module_count: source: top_level_dirs|component_scan; value: <int>
domain: <controlled_enum>
figure_types: <controlled_figure_types>
evidence: <high|partial|sparse>
```

**Controlled domain enum** (pick exactly one):
`CV`, `NLP`, `Speech/Audio`, `RL`, `Robotics`, `Multimodal`, `TimeSeries`, `Generative`, `Protein/AI4Science`, `GNN/ScientificComputing`, `ScientificComputing(non-ML)`, `Other`

**Controlled figure_types** (pick 2–4 from this list, comma-separated):
`Overall Framework`, `Network Architecture`, `Module Detail`, `Comparison/Ablation`, `Data Behavior`

- **Overall Framework** — end-to-end pipeline / data flow between components
- **Network Architecture** — internal layer structure, module hierarchy, skip connections
- **Module Detail** — zoom into one mechanism (attention, loss, sampling)
- **Comparison/Ablation** — variants, baselines, result grids
- **Data Behavior** — curves, heatmaps, embeddings, qualitative results

Done when: Output Contract fields are filled; figure suggestions use controlled type names and explain what each figure shows.

## Sparse-input cases

| gap | action |
|-----|--------|
| no README | infer from code; label as structure-inferred |
| no entry scripts | module-level understanding only |
| no model files | stack/task only; soft architecture language |
| huge repo | sample top-level + 3–5 core files ONLY; never run broad keyword scans; state 抽样 / limited sample in the completeness block |
| non-ML / scientific code | use entry scripts + component_scan; architecture language soft; flows marked 证据不足 / evidence insufficient when no train/inference loop exists |
| almost nothing | pre-analysis + minimum materials list (README → deps → entry → model → config) |

## Tooling cues

Prefer the environment's file/search tools. Typical digs: dependency files, `class.*Model|Network|Transformer`, `loss|criterion`, model package entrypoints.

## Stop

Stop when the quick-understanding doc is delivered. Suggest paper-analyzer only if the user wants figure planning next.
