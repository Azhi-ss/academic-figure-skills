---
id: academic-figure-workflow
name: Academic Figure Workflow Orchestrator
version: 1.3.0
description: Entry-point router for academic figure generation. Two independent entry paths — repository analysis (code-first) or paper analysis (document-first) — that converge only at the color/prompt stage. Use when unsure which skill to start with, or for a full pipeline.
stages: [research, writing, review]
tools: [bash]
---

# Academic Figure Workflow Orchestrator

Pack entrypoint. Detect which input the user has, route to the right skill, and **stop at each stage unless the user explicitly asks to continue**. Do not force the full chain.

Shared refs:

- palettes → `references/palettes.md`
- missing info → `references/missing-info-policy.md`

## Two independent entry paths

### Path A — Repo-first (code input)

User gives a repository path or URL. The goal is understanding **what the code actually does**.

```
repo-analyzer
  → Quick Understanding Doc + Handoff
  → STOP. Ask: analyze only, or plan figures?
    → if plan figures: figure type selection (from repo Handoff)
      → STOP. Ask: proceed to color + prompt?
        → color-expert → figure-prompt → image
```

| Stage | Skill | Output | Can stop here? |
|-------|-------|--------|----------------|
| Analyze code | `repo-analyzer` | Quick Understanding Doc + Handoff (module_count, domain, figure_types, evidence) | Yes |
| Select figures | `repo-analyzer` Handoff → choose 1–2 types | Figure type + aspect ratio | Yes |
| Pick colors | `color-expert` | Palette Decision (hex) | Yes |
| Generate spec | `figure-prompt` / `figure-prompt-pastel` | JSON figure spec or prompt | Yes |

**Repo path characteristics:**
- module_count comes from real code structure (drives Nature Blue vs Okabe-Ito)
- figure types suited to code: Network Architecture, Module Detail, Overall Framework
- no paper narrative; evidence level is sparse/partial/high based on code read

### Path B — Paper-first (document input)

User gives a PDF, paper text, outline, or existing figure. The goal is understanding **what the paper says and what figures it needs**.

```
PDF / existing figure?
  → yes: architecture-extractor (extract structure)
  → no:  paper-analyzer directly
    → Figure Plan (count, types, priorities, aspect ratios)
    → STOP. Ask: plan only, or generate figures?
      → color-expert → figure-prompt → image
```

| Stage | Skill | Output | Can stop here? |
|-------|-------|--------|----------------|
| Extract from PDF/image | `architecture-extractor` | Extracted structure + redraw params | Yes |
| Analyze paper | `paper-analyzer` | Figure Plan (section → figure map, priorities) | Yes |
| Pick colors | `color-expert` | Palette Decision (hex) | Yes |
| Generate spec | `figure-prompt` / `figure-prompt-pastel` | JSON figure spec or prompt | Yes |

**Paper path characteristics:**
- no module_count unless a repo is also provided
- figure types suited to papers: Overall Framework, Comparison/Ablation, Data Behavior, Module Detail
- venue and domain drive color; module_count may be unknown (use Okabe-Ito default)

### When both repo and paper are present

Analyze paper first (it defines the narrative), use repo to fill technical gaps. module_count from repo feeds into color decision.

## Sibling routing

Read a sibling file only when that stage runs:

| skill | when |
|-------|------|
| `../academic-repo-analyzer/SKILL.md` | Path A: repository / codebase input |
| `../academic-figure-paper-analyzer/SKILL.md` | Path B: paper/section text input |
| `../academic-figure-architecture-extractor/SKILL.md` | Path B: PDF or existing image input |
| `../academic-figure-color-expert/SKILL.md` | either path, when user wants colors |
| `../academic-figure-prompt/SKILL.md` | either path, when user wants classic JSON spec |
| `../academic-figure-prompt-pastel/SKILL.md` | either path, when user wants pastel/airy style |

## Color routing (convergence point)

Both paths converge at color selection but carry different inputs:

| Input present | Decision rule |
|---------------|---------------|
| module_count ≥ 4 (from repo) | Nature Blue monochrome |
| module_count < 4 or unknown | Okabe-Ito, or scene-based palette |
| venue: NeurIPS/ICML/ICLR classic | ML TopConf Colorblind |
| venue: NeurIPS/ICML/ICLR pastel/airy | route to `figure-prompt-pastel` |
| venue: Nature/Science | Okabe-Ito or Journal Standard |
| user specifies palette | use it, state the branch |

Always state which rule produced the choice and offer one alternate.

## Style family first

Before picking any palette, decide **classic vs pastel** based on user language:

| User says | Style family | Skill |
|-----------|-------------|-------|
| box-border, JSON spec, classic, 顶刊, CVPR/Nature | Classic academic | `figure-prompt` |
| airy, pastel, soft, 现代ML, token flow, ICLR那种 | Pastel airy | `figure-prompt-pastel` |

## Handoffs (carry forward, don't re-narrate)

- **Repo path:** Quick Understanding Doc → Handoff (module_count, domain, figure_types, evidence) → Palette Decision → Figure Spec
- **Paper path:** Figure Plan (types, counts, priorities, aspect ratios, venue) → Palette Decision → Figure Spec

## Output shape

1. Which path (repo / paper / direct)
2. Current stage result
3. Next action or stop point
4. Handoff artifact or final deliverable

## Stop rules

- Stop after each stage and state what the user can do next
- Do not auto-advance: analysis → plan → color → prompt requires explicit user intent
- If user only asked "what does this repo do", stop after repo-analyzer
- If user only asked "what figures should my paper have", stop after paper-analyzer
- If user only asked "what palette", stop after color-expert
