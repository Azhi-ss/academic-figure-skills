---
name: academic-figure-paper-analyzer
description: Plan evidence-backed figures for a paper, manuscript, outline, PDF, or paper webpage. Use to map scientific claims to figure roles, visual narratives, required topology, and publication constraints before rendering.
metadata:
  version: "1.3.0"
  stages: [research, review]
---

# Academic Paper Analyzer and Figure Planner

Produce a human-readable figure strategy and a machine-readable **Figure Plan v1**. Plan figures around the paper's claims and reader questions, not around a fixed count or a generic pipeline template.

Read `references/missing-info-policy.md` when the paper is incomplete. If a repository handoff or extracted reference-style profile exists, carry it forward without renaming fields.

## Input contract

- Prefer: manuscript text or source, abstract, method, experiments, target venue/page limit, semantic architecture handoff, and any reference figures.
- Accept: local PDF, paper URL/HTML, Word/LaTeX/Markdown, section draft, outline, or title plus abstract.
- A URL is a paper source only after its content is inspected; do not classify every URL as a code repository.
- If a PDF or webpage cannot be read in the current environment, report that limitation rather than inventing paper structure.

## Output contract

Include:

1. Paper overview: question, contribution, evidence, and intended venue constraints.
2. Completeness statement: sections and artifacts actually inspected.
3. Per-figure recommendation with a controlled type and `must`, `strong`, or `nice` priority.
4. A one-sentence communication goal: what the reader should understand after viewing the figure.
5. Required nodes, edges, authority boundaries, and forbidden implications.
6. Aspect ratio and final publication width hint.
7. `Figure Plan v1` JSON.

Controlled figure types: `Overall Framework`, `Network Architecture`, `Module Detail`, `Comparison/Ablation`, `Data Behavior`.

## Workflow

### 1. Parse the paper's argument

Map Introduction, Method, Experiments, Analysis, and Limitations. For each claimed contribution, record the source span and the evidence that could support a visual statement. Separate proposed mechanisms from measured results.

### 2. Assign visual jobs

Recommend a figure only when a visual materially improves understanding.

| Reader question | Common type | Typical priority |
|---|---|---|
| What is the end-to-end idea and authority/data flow? | Overall Framework | must |
| What is the internal executable structure? | Network Architecture | must or strong |
| How does the central mechanism work? | Module Detail | must or strong |
| Which choices matter empirically? | Comparison/Ablation | strong |
| How does behavior change over data, time, or conditions? | Data Behavior | strong or nice |

Do not use venue stereotypes or fixed counts as requirements. Page budget, number of distinct contributions, and available evidence determine the count. Combine figures when they answer the same reader question; omit decorative figures.

### 3. Design the narrative topology

For each figure specify:

- `communication_goal` and `claim_scope`;
- `hero_element`: the dominant visual story, not merely the largest box;
- `required_nodes` and `required_connections` from source evidence;
- `secondary_context` that may be dropped under space pressure;
- `forbidden_claims` and `forbidden_connections`;
- `authority_boundaries` for agent/tool/oracle systems;
- `text_budget`: short labels, with detail reserved for the caption;
- `reference_style_profile` if the user supplied a reference image.

An Overall Framework need not be a left-to-right chain. Choose among a loop, storyboard, asymmetric modular collage, layered authority diagram, central mechanism with satellites, or pipeline according to the scientific story.

### 4. Set publication geometry

- Overall Framework: usually 16:9 or 3:2 at double-column width.
- Network Architecture: 16:9, 3:2, or a tall layout when the real topology requires it.
- Module Detail: commonly 4:3 or 1:1.
- Comparison/Ablation: match the number and reading order of panels.
- Data Behavior: let axes and panel count determine the geometry.

Specify the intended final width (`89 mm` single-column or `183 mm` double-column) as export metadata. Do not pretend a raster image model can enforce physical point sizes exactly; use the render audit at final scaled size.

### 5. Emit Figure Plan v1

```json
{
  "schema": "academic-figure/FigurePlan@1",
  "source_revision": "<paper-or-repo-revision>",
  "venue": null,
  "sources": [],
  "figures": [
    {
      "figure_id": "fig1",
      "figure_type": "Overall Framework",
      "priority": "must",
      "communication_goal": "<one sentence>",
      "claim_scope": ["<evidence-backed claim>"],
      "hero_element": "<loop|mechanism|modular collage|pipeline|other>",
      "required_nodes": ["<component-id>"],
      "required_connections": ["<from-id> -> <to-id>: <kind>"],
      "authority_boundaries": [],
      "secondary_context": [],
      "forbidden_claims": [],
      "forbidden_connections": [],
      "aspect_ratio": "16:9",
      "final_width_mm": 183,
      "style_profile_hint": null,
      "reference_assets": [],
      "open_questions": [],
      "confidence": "high|partial|sparse",
      "review_status": "pending|confirmed|waived"
    }
  ]
}
```

The example defines fields only. Replace every placeholder with sourced content or an explicit null/empty value.

## Sparse input

- Title and abstract only: plan high-level visual jobs; do not name hidden submodules.
- Method without experiments: plan method figures and mark result figures as blocked.
- Repository handoff only: produce a system-centric plan and flag narrative review.
- Reference image only: analyze visual grammar, but request or locate the target system content before planning its topology.

## Stop

Stop after delivering the strategy and Figure Plan v1. Do not generate prompts or images unless the user requested the downstream workflow.
