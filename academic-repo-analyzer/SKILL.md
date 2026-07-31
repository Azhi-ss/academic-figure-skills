---
id: academic-repo-analyzer
name: Academic Repo Analyzer
version: 1.1.0
description: Quick-understanding doc for ML/DL, AI4Science, and research codebases — task type, stack, architecture, and figure-worthy innovations. Use when the user wants repo analysis, 仓库分析, or to understand a codebase before figure planning.
stages: [research, review]
tools: [bash]
---

# Academic Repo Analyzer

Produce a **仓库快速理解文档** for ML/DL, AI4Science, and general research codebases, for downstream figure planning.

Keywords: → `keywords.md`  
Missing info: → `references/missing-info-policy.md`

## Input Contract

- Prefer: repo path, README, deps, entry scripts, model files, configs
- Minimum: any one of README / entry script / model file
- Missing: partial analysis with 推断 / 待确认

## Output Contract — Quick Understanding Doc

- overview (name, task, framework, architecture one-liner)
- completeness block
- stack details
- model / algorithm notes
- train / inference flow (or “evidence insufficient”)
- figure suggestions for paper-analyzer

## Steps

### Step 1: Scan structure

Locate README, dependency files, entry scripts (`train|main|eval|inference|predict|run|simulate|benchmark|demo|app|serve`), `configs/`, `models|networks|src/`, data loaders. Notebooks (`*.ipynb`) count as entry evidence when no scripts exist.

For huge repos, sampling is top-level + 3–5 core files ONLY; never run broad keyword scans on huge repos; state "抽样 / limited sample" in the completeness block.

Done when: tree of key paths exists and each must-read class is read **or** marked missing.

### Step 2: Task + stack

Use `keywords.md`. Classify task type and framework from imports, deps, and paths.

Done when: task type + primary framework are stated with file evidence.

### Step 3: Architecture + algorithms

From model files: backbone family, key modules, losses, training tricks. Prefer evidence over naming guesses.

Done when: architecture summary cites concrete classes/files, or is marked 推断.

### Step 3.5: Module inventory & count

Produce the module inventory for the Handoff block:

- `source`: `top_level_dirs` (top-level package/module dirs, e.g. `ldm/`, `alphafold/`) when the repo is a library/monorepo, else `component_scan` (named components found inside the 3–5 sampled core files, e.g. `lennard_jones.py` + `integrator.py`).
- `value`: integer count. Never infer from keyword matches alone.

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
domain: <CV|NLP|RL|Robotics|Multimodal|TimeSeries|Generative|Protein/AI4Science|GNN/ScientificComputing|ScientificComputing(non-ML)|Other>
figure_types: <comma-separated suggested types>
evidence: <high|partial|sparse>
```

Done when: Output Contract fields are filled; figure suggestions list concrete types (framework / arch / module / …).

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

Prefer the environment’s file/search tools. Typical digs: dependency files, `class.*Model|Network|Transformer`, `loss|criterion`, model package entrypoints.

## Stop

Stop when the quick-understanding doc is delivered. Suggest paper-analyzer only if the user wants figure planning next.
