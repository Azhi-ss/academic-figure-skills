# FigureSpec to Image Prompt Compilation

Compile FigureSpec v1 into natural-language rendering instructions without changing its scientific content. The prompt is a backend adapter, not a second design stage.

## Invariants

1. Preserve every component ID and every connection endpoint.
2. Do not add dimensions, formulas, model variants, legends, icons, or side notes absent from FigureSpec.
3. Do not convert style tokens into visible words such as `WHITE FILL`, `300 DPI`, hex codes, or stroke widths.
4. Only values in `visible_text` and explicit block label fields may be rendered as text.
5. `caption_note`, evidence pointers, JSON keys, and production metadata are never visible.
6. Reference images remain structured image inputs when the backend supports them; prose is not a replacement for reference conditioning.
7. **Strict Prose Normalization (Zero Markdown Syntax)**: Prompts must be clean structured natural language prose. Never use Markdown formatting symbols (such as `#`, `**`, `*`, `- `, backticks, or `|---|` tables) inside the prompt sent to the image model. Models frequently paint Markdown syntax tokens as visual text artifacts on the canvas.

## Compilation order

### 1. Lead with figure purpose and style grammar

Name the figure type, communication goal, aspect ratio, canvas, and selected style profile. Describe observable grammar—composition, marks, fills, stroke character, typography, spacing, and illustration level—rather than relying on venue names or vague words such as “professional.” Default to no canvas title because the figure title normally belongs in the external caption. If the user, FigureSpec, or supplied reference explicitly includes a title, compile that exact string once as a short non-banner heading with reserved whitespace.

### 2. Describe composition by visual hierarchy

Start with the hero element and major semantic regions. For each region state its approximate position/proportion, fill/outline token, and permitted nesting depth. Then describe primary components in reading order and secondary context last.

Do not mechanically list JSON order. Preserve explicit gaps and unconnected regions.

### 2.1 Scientific Visual Metaphor Compilation (Preventing Text Dumps)

When components represent structured computation, representations, or experiments, prefer a sourced visual schematic over a text dump. Select archetypes compatible with the paper's actual modality:

- **Neural & Representation Components**:
  - *Feature / Tensor Blocks*: 3D orthogonal colored tensor blocks or stacked 2D feature slices with dimension annotations (e.g. `$B \times C \times H \times W$`).
  - *Attention / Cross-Modal Matrix*: multi-layer square heatmap grid with diverging color intensity or bipartite connecting lines.
  - *Loss / Objective Constraint*: mathematical minimization formula block with dashed purple bounding box.
- **Pipeline & Stage Flows**:
  - *Sequential Stages*: discrete rounded container cards with stage header pills and bold primary process icons.
  - *Data Stream / Token Sequence*: horizontal array of rounded pills with clear left-to-right flow arrows.
- **Systems, Data & Memory**:
  - *Storage / Memory Buffer*: clean cylinder database glyph or node-edge episodic graph.
  - *Queue / Buffer / Scheduler*: partitioned horizontal stack with incoming/outgoing directional arrows.
- **Optimization & Decision Components**:
  - *Surrogate / Function Fitting*: mini 2D coordinate plot with black x/y axes, solid blue fitted mean curve, dashed confidence bounds, shaded light-blue uncertainty ribbon, and orange scatter points.
  - *Candidate Pool / Shortlist*: compact structured table with header band and sourced rows.
  - *Decision / Policy Module*: compact decision/reasoning glyph or structured badge; avoid robot characters unless explicitly requested.
  - *Experimental Evaluation*: bounded evaluation table, simulator block, or benchmark metric bar chart based on sourced modality.

### 3. State topology as a closed list

Translate each connection exactly once:

```text
[from label] → [to label], [executed/advisory/feedback/persistence/exception],
[solid/dashed/dotted], optional visible label "..."
```

Add: “Draw no other inter-module connections.” This reduces invented shortcuts. Do not infer an edge from spatial proximity.

### 4. Lock visible text

Provide a compact closed list of exact visible strings, grouped by region. Say that no other words, JSON keys, production terms, or placeholder text may appear. This is an intent constraint, not a guarantee; RenderAudit must still inspect the resulting image.

### 5. Describe semantic color tokens

For each semantic zone provide paired tokens:

```text
zone: soft fill #..., dark outline/title #..., optional icon accent #...
```

State non-color encodings for advisory, exception, fixed/trainable, or other distinctions. Do not substitute a single palette name for role mapping.

### 6. End with negative constraints and geometry

Use a short defect-oriented list: no unintended or duplicated title banner, no extra modules or edges, no garbled text, no transparent/dark background, no clipping or overlap, no gradients/3D/branding, and any style-specific exclusions. State the aspect ratio last.

## Prompt length

Use the shortest prompt that preserves the spec. Roughly 180–450 English words is usually sufficient, but topology correctness has priority over a fixed word count. Long visible-text inventories belong in a deterministic SVG/drawio/Typst workflow rather than an ever-longer image prompt.

## Backend suitability

- **Image generation/editing:** conceptual, illustrated, or low-text frameworks where visual language matters.
- **Deterministic vector renderer:** text-heavy architectures, exact mathematical notation, dense legends, or strict topology.
- **Hybrid:** image-generated illustration or background plus deterministic text/vector overlay.

When the selected backend cannot plausibly satisfy the text/topology contract, return the spec or switch to a compatible deterministic renderer instead of claiming exact control.

## Preflight

- Every prompt component maps to one FigureSpec component.
- Every prompt connection maps to one FigureSpec connection.
- No content was inferred during compilation.
- Exact visible strings are separated from production instructions.
- Style reference paths remain available to the renderer.
- RenderAudit has an objective checklist for the output.
