---
id: academic-figure-workflow
name: Academic Figure Workflow Orchestrator
version: 1.0.0
description: Use this skill whenever the user wants an end-to-end academic figure workflow, wants to go from a repository or paper to a figure prompt, is unsure which academic-figure skill to start with, or says "帮我从仓库到配图走一遍", "完整论文配图工作流", "academic figure workflow", "end-to-end figure pipeline", "from paper to figure prompt", or "which skill should I use first".
stages: [research, writing, review]
tools: [bash]
---

# Academic Figure Workflow Orchestrator

Use this skill as the pack entrypoint. Route the task to the minimum set of sibling skills needed to get the user from raw inputs to a usable academic figure prompt.

Do not dump every sub-skill at once. Identify the user's current stage, load only the relevant sibling skill files, and move the workflow forward with the fewest necessary steps.

## Sibling Skill Routing

Read the sibling skill files only when their stage is needed:

- `../academic-repo-analyzer/SKILL.md`: Use when the user provides a repository, asks what a codebase does, or needs a quick understanding document before figure planning.
- `../academic-figure-paper-analyzer/SKILL.md`: Use when the user provides a paper, section draft, abstract, or method description and needs figure planning.
- `../academic-figure-architecture-extractor/SKILL.md`: Use when the user provides a PDF, wants to extract architecture diagrams, analyze diagram structure, or get color scheme recommendations for existing diagrams.
- `../academic-figure-color-expert/SKILL.md`: Use when the user asks for palette selection, venue-specific style advice, or accessibility-safe colors.
- `../academic-figure-prompt/SKILL.md`: Use when the user wants a classic academic figure prompt.
- `../academic-figure-prompt-pastel/SKILL.md`: Use when the user explicitly wants a modern ML / ICLR / NeurIPS 2024-2025 airy pastel style.

## Stage Detection

Classify the request into one of these entry states:

1. **Repo-first**
   The user has a repository or codebase and wants to understand it before planning figures.
2. **Paper-first**
   The user has a paper, PDF, outline, or section text and wants figure planning directly.
3. **Architecture-extraction-first**
   The user has a PDF and wants to extract architecture diagrams, analyze diagram structure, or get color recommendations for existing diagrams.
4. **Prompt-first**
   The user already knows the target figure and wants a prompt now.
5. **Color-first**
   The user mainly wants palette selection or venue-specific visual style guidance.

If the user is ambiguous, infer the most likely entry state from the artifacts they provided. Ask only for missing information that blocks the next step.

## Default Workflow

Use the lightest valid path:

- **Repo-first**: repo analyzer -> paper analyzer if figure planning is requested -> color expert if palette is unspecified -> prompt skill
- **Paper-first**: paper analyzer -> color expert if palette is unspecified -> prompt skill
- **Architecture-extraction-first**: architecture extractor -> paper analyzer if figure planning is requested -> color expert if palette is unspecified -> prompt skill
- **Prompt-first**: choose prompt style -> collect only the minimum missing figure details -> generate prompt
- **Color-first**: color expert -> optionally continue into prompt generation

Do not force the full chain when the user wants only one stage.

## Minimal Input Checklist

Before generating a final prompt, make sure you know:

- figure type
- subject or method being visualized
- target venue or style preference, if any
- palette choice, or a safe default
- any mandatory labels, modules, equations, or comparisons

If one or two details are missing, proceed with explicit assumptions. If core content is missing, ask targeted questions instead of hallucinating the figure structure.

## Default Decisions

- If no palette is specified, prefer a safe default and say so explicitly. Default to `Okabe-Ito` unless the user's venue or requested style strongly suggests otherwise.
- If the user mentions ICLR / NeurIPS / ICML 2024-2025 airy pastel aesthetics, route to `academic-figure-prompt-pastel`.
- Otherwise route to `academic-figure-prompt`.
- If the user has both a repo and a paper, prioritize the paper for figure planning and use the repo only to fill technical gaps.

## Handoff Artifacts

When moving between stages, carry forward compact structured artifacts instead of re-explaining everything.

### Quick Understanding Doc

Include:

- task type
- model family or method category
- input/output summary
- core modules
- training or inference flow
- likely figure-worthy innovations

### Figure Plan

Include:

- recommended figure count
- figure types
- section-to-figure mapping
- priority ranking
- notes on what must appear visually

### Palette Decision

Include:

- selected palette
- 2-3 core hex colors
- why it fits the venue or task
- accessibility notes if relevant

### Prompt Package

Include:

- final English image prompt
- short Chinese explanation of what the prompt is optimizing for
- any explicit assumptions made due to missing input

## Output Contract

When acting as the orchestrator, respond in this order:

1. **Current stage**
2. **Next action**
3. **Result or required clarification**
4. **Handoff artifact or final prompt**

Keep the orchestration visible but concise. The user should be able to see where they are in the pipeline without reading an essay.

## Stop Conditions

Stop when one of these is true:

- the user received the requested deliverable for the current stage
- the next step requires missing source material the user has not provided
- the user explicitly wants evaluation instead of generation

Do not continue into downstream stages unless the user asked for them or the request clearly implies an end-to-end workflow.
