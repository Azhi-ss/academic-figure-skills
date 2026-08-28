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

### 2. Describe composition by visual hierarchy and spatial proportions

Start with macro-containers, layout proportions, and spatial division across the canvas:

- **Macro-to-Micro Container Allocation**: Express spatial division explicitly by height/width percentage (e.g. `Top container: 30-35% height`, `Bottom container: 65-70% height`). This prevents the image model from clustering components into a corner or leaving massive empty dead space.
- **Nested Card Architecture**: Use outer macro-containers with subtle dashed or light borders, and nest structured solid white sub-cards inside. This creates depth and multi-level organization without relying on drop shadows.
- **Hero Focal Region**: Allocate 35–50% of visual attention to the central contribution (e.g., 3D response surface, complex policy loop, or multi-branch neural mechanism) and surround it with supporting context modules.

Do not mechanically list JSON order. Preserve explicit spatial gaps and reading directions.

### 2.1 Scientific Visual Metaphor Compilation (SVMC: Preventing Text Dumps & Empty Boxes)

When components represent structured computation, representations, or experiments, never output generic empty text boxes. Inject the **Micro-Visual Trinity** for each key node:
1. **Header Tag / Icon Badge**: Leading domain glyph (e.g. 💡 idea bulb, 🔬 microscope, 🔍 search loop).
2. **Concrete Scientific Schematic**: Actual plot or geometric visualization (e.g. 3D GP mesh, 1D multi-peak curve, tensor block, heatmap, state graph).
3. **Micro Mathematical/Data Card**: Core equation, uncertainty gauge, dialogue bubble, or bounded data table.

Select archetypes compatible with the paper's actual modality:

- **Optimization & Active Learning Components**:
  - *3D Gaussian Process / Response Surface*: 3D elevation mesh with diverging color gradients, highlighted elliptical focused regions ($\mathcal{X}_R^*$), and a mathematical coupling formula card ($f_R(x) = \rho f_L(x) + \delta(x)$).
  - *1D Acquisition Function*: 1D curve with coordinate axes, observation dots, and a prominent red peak marker ($x^* = \arg\max \alpha_t(x)$) with a magnifying glass pointer.
  - *Gating & Decision*: Decision diamond asking a threshold condition ($p_\Delta(x^*) < \tau?$) with branching checkmark (Yes) and cross (No) badges.
  - *Cognitive Reasoning & Uncertainty*: Brain/chip glyph with quoted natural-language dialogue bubbles, paired with a half-circle uncertainty gauge meter and mini prediction table.
  - *Physical / Wet-Lab Experiments*: Laboratory apparatus (glassware, beakers, microscope) paired with a computer monitor showing measurement curves.
- **Neural & Representation Components**:
  - *Feature / Tensor Blocks*: 3D orthogonal colored tensor blocks or stacked 2D feature slices with dimension annotations (e.g. `$B \times C \times H \times W$`).
  - *Attention / Cross-Modal Matrix*: multi-layer square heatmap grid with diverging color intensity or bipartite connecting lines.
  - *Loss / Objective Constraint*: mathematical minimization formula block with dashed purple bounding box.
- **Pipeline & Stage Flows**:
  - *Sequential Stages*: discrete rounded container cards with stage header pills and bold primary process icons.
  - *Data Stream / Token Sequence*: horizontal array of rounded pills with clear left-to-right flow arrows.
- **Systems, Data & Memory**:
  - *Storage / Memory Buffer*: clean cylinder database glyph or node-edge episodic graph (EventGraph).
  - *Queue / Buffer / Scheduler*: partitioned horizontal stack with incoming/outgoing directional arrows.

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
