---
id: academic-figure-paper-analyzer
name: Academic Paper Analyzer & Figure Planner
version: 1.1.0
description: Figure plan for academic papers — section-to-figure mapping, types, counts, and priority. Use when the user wants paper figure planning, 论文配图规划, or which figures a paper needs.
stages: [research, review]
tools: [bash]
---

# Academic Paper Analyzer & Figure Planner

Produce an executable **Figure Plan**. No palette tables here — hand venue/domain/figure types to color-expert later.

Missing info: → `references/missing-info-policy.md`

## Input Contract

- Prefer: paper PDF/LaTeX/Word, section drafts, abstract, method/experiments, repo quick-understanding doc, extracted architecture notes
- Minimum: title+abstract, or one method/experiment section, or a repo understanding doc
- Missing: partial plan with 推断 / 待确认

## Output Contract — Figure Plan

- paper overview (topic, contributions)
- completeness block
- per-section figure recommendations
- priority ranking (must / strong / nice)
- palette: style family hint (classic vs pastel) + venue: <venue or None> + domain: <domain> — not hex tables; see `references/palettes.md`
- module_count_framework: <int> (carried from repo Handoff when present)

## Steps

### Step 1: Parse structure

Map sections: Intro, Method (+ sub), Experiments, Analysis. Note missing sections.

Done when: section list exists and each is marked present / absent / partial.

### Step 2: Mark figure-worthy content

| content | figure type | priority |
|---------|-------------|----------|
| end-to-end pipeline | Overall Framework | must |
| network / layer structure | Network Architecture | must |
| novel module / mechanism | Module Detail | must |
| method variants / baselines | Comparison / Ablation | strong |
| representation / attention behavior | Data Behavior | strong / medium |
| dense math or loss | Module Detail | strong |
| curves / t-SNE / heatmaps | Data Behavior | medium |

Done when: every must-level contribution has at least one figure entry or an explicit “insufficient evidence” note.

### Step 3: Count and prioritize

| paper class | typical count |
|-------------|---------------|
| top-conference long | 6–8 |
| short / workshop | 4–5 |
| journal | 8–12 |
| arXiv tech report | 5–7 flexible |

Done when: total count + must/strong/nice table is filled.

### Step 4: Emit Figure Plan report

Include per-section: type × count, why, must-appear visual elements, aspect ratio hint.

| type | aspect | core elements |
|------|--------|---------------|
| Overall Framework | 16:9 | input → stages → output; innovation callouts |
| Network Architecture | 16:9 / 3:2 | layers, dims, residuals |
| Module Detail | 4:3 | central mechanism, ops (⊗ ⊕ σ), sparse formula |
| Comparison / Ablation | 16:9 | N×M grid, ours highlighted |
| Data Behavior | 4:3 / 1:1 | multi-panel heatmaps / curves / embeddings |

Emit aspect_ratio per figure in the Figure Plan so prompt skills can copy it into the spec.

Done when: report matches Output Contract and completeness block is honest.

## Domain packs (optional cues)

- **CV:** framework + arch + module + visual comparison + attention maps  
- **NLP:** framework + transformer arch + attention module + metrics + embeddings  
- **RL/Robotics:** state→policy→action loop + networks + trajectories  
- **Medical:** imaging pipeline + U-Net/ViT + qualitative grid + ROC/features  
- **Protein / AI4Science:** folding pipeline + Evoformer/module detail + MSA or structure behavior  
- **GNN / Scientific computing:** message-passing module + encoder-processor-decoder framework + rollout trajectories  

## Sparse-input cases

| materials | plan style |
|-----------|------------|
| title + abstract only | high-level types only; no fake submodules |
| method without experiments | plan method figures; results as placeholders |
| partial sections | local plan; separate covered vs uncovered |
| only repo understanding doc | system-centric draft; flag narrative review needed |

## Stop

Stop when the Figure Plan for available materials is delivered. Do not generate prompts unless the user asks.
