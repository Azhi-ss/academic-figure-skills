---
id: academic-figure-workflow
name: Academic Figure Workflow Orchestrator
version: 1.1.0
description: End-to-end academic figure workflow router — from repo or paper to figure prompt via the minimum sibling skills. Use when the user wants a full pipeline, is unsure which academic-figure skill to start with, or says 完整论文配图工作流 / from paper to figure prompt.
stages: [research, writing, review]
tools: [bash]
---

# Academic Figure Workflow Orchestrator

Pack entrypoint. Detect stage, load **only** needed sibling skills, carry compact handoffs.

Shared refs:

- palettes → `../docs/palettes.md`
- missing info → `../docs/missing-info-policy.md`

## Sibling routing

Read a sibling file only when that stage runs:

| skill | when |
|-------|------|
| `../academic-repo-analyzer/SKILL.md` | repository / codebase understanding |
| `../academic-figure-paper-analyzer/SKILL.md` | paper/section → figure plan |
| `../academic-figure-architecture-extractor/SKILL.md` | PDF/images → architecture analysis |
| `../academic-figure-color-expert/SKILL.md` | palette decision |
| `../academic-figure-prompt/SKILL.md` | classic JSON figure spec |
| `../academic-figure-prompt-pastel/SKILL.md` | pastel / ICLR airy style |

## Stage detection

1. **Repo-first** — codebase before figures  
2. **Paper-first** — paper/PDF/outline → plan  
3. **Architecture-extraction-first** — extract/analyze existing diagrams  
4. **Prompt-first** — figure already known  
5. **Color-first** — palette only  

Infer from artifacts; ask only for blockers.

## Default paths (lightest valid)

- Repo-first → repo-analyzer → (paper-analyzer if planning) → (color if needed) → prompt  
- Paper-first → paper-analyzer → (color if needed) → prompt  
- Architecture-first → architecture-extractor → (paper-analyzer if planning) → (color if needed) → prompt  
- Prompt-first → style choice → min missing details → prompt  
- Color-first → color-expert → optional prompt  

Never force the full chain for a single-stage ask.

## Defaults

- **Style family** then palette: follow `docs/palettes.md` (classic JSON vs pastel airy; ≥4 modules → Nature Blue; else Okabe-Ito). Always state the branch.  
- ICLR / NeurIPS / ICML airy / pastel / “现代一点” language → `prompt-pastel` + P1–P3  
- Otherwise → `prompt` JSON + classic 12 presets  
- Repo + paper both present → plan from paper; repo fills technical gaps  
- When user only asks “用什么配色/风格”, load color-expert and the **Scene → palette** section of `docs/palettes.md`


## Handoffs (carry forward, don't re-narrate)

- **Quick Understanding Doc** — task, stack, modules, flows, figure-worthy innovations  
- **Figure Plan** — count, types, section map, priorities, visual musts  
- **Palette Decision** — name, hex, reason, accessibility  
- **Prompt Package / Figure Spec** — final deliverable + assumptions  

## Output shape

1. Current stage  
2. Next action  
3. Result or required clarification  
4. Handoff artifact or final prompt  

## Stop

- requested stage deliverable is done  
- next step blocked on missing source material  
- user wants evaluation, not generation  

Do not auto-advance downstream unless the user asked end-to-end or clearly implied it.
