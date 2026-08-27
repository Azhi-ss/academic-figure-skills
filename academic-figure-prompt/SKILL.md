---
name: academic-figure-prompt
description: Build evidence-grounded FigureSpec v1 artifacts and normalized structured rendering briefs for all academic figure styles (classic-technical, pastel-airy-ui, illustrated-modular, and reference-led).
metadata:
  version: "2.0.0"
  stages: [writing, research, review]
---

# Academic Figure Spec and Prompt (Unified Engine)

Create a structured `academic-figure/FigureSpec@1` first, then compile a normalized structured rendering brief in natural language. This skill serves as the single authoritative prompt compiler for all figure styles.

Load only as needed:

- spec contract → `json-schema.md` and `figure-spec.schema.json`
- prompt compilation → `references/json-to-prompt.md`
- visual brief guidance → `references/image-prompt-guide.md`
- composition scaffolds → `references/prompt-templates.md`
- visual anchors & SVMC → `references/architecture-icons.md`
- palette/style fallback → `references/palettes.md` and optional `references/styles/`
- missing evidence → `references/missing-info-policy.md`

## Supported Style Profiles

Select one canonical `style_profile` (or compose with layer overlays from `docs/styles/`):

1. **`classic-technical` (经典学术框线风)**:
   - Clean white background, thin 1.5pt crisp outlines, restrained subtle tints.
   - High contrast, orthogonal alignment, strict box/arrow engineering topology.
   - High-density tabular parameters and formal sans-serif typography (Helvetica/Inter).
2. **`pastel-airy-ui` (现代柔彩空气风)**:
   - White canvas with floating white cards and faint borders.
   - Generous negative space, floating pills/tokens, and lightweight curves.
   - Interface-like feel without multi-level nested boxes.
3. **`illustrated-modular` (编辑手绘模块风 / 有色语义分区图示风)**:
   - White canvas with content-driven soft-tinted semantic zones.
   - Strong same-hue 1.5–2.5px dark outlines and **no drop shadows**.
   - Asymmetric hero region (~35–55% visual focus) with supporting modules arranged by real semantics.
   - Content-grounded editorial line art tied to declared semantics, such as documents, graphs, gears, databases, decision badges, or other sourced visual anchors.
4. **`reference-led` (参考图驱动自由风格)**:
   - Extracts observable visual grammar (composition, marks, stroke, typography, illustration level) directly from a user-supplied reference image without copying proprietary content or topology.

## Strict Prompt Formatting Standard (Prose Normalization)

All generated image prompts **MUST be compiled as normalized structured natural language (Compact Prose)**:

> [!IMPORTANT]
> **Zero Markdown Syntax in Image Prompts**:
> Never use Markdown formatting symbols (such as `#` headers, `**bold**`, `*italic*`, markdown bullet lists `- item`, backticks, or ASCII markdown tables `| --- |`) inside the prompt string sent to diffusion/image models. Image models frequently hallucinate and render Markdown syntax tokens as literal text on the canvas.
> Use clean, comma-and-sentence structured prose grouped by numbered container blocks or semantic zones.

### Canonical Prompt Structure

1. **Lead & Purpose**: High-level figure goal, aspect ratio, canvas background (pure white `#FFFFFF`), and style profile. Default to an external paper caption with no canvas title. If the user, FigureSpec, or supplied reference explicitly requires a title, lock exactly one short non-banner title and reserve whitespace for it.
2. **Layout & Hero Focus**: Numbered container panels and proportions (e.g. 3-column sandwich layout, central hero region).
3. **Semantic Container Blocks**: For each container, describe inner title pill, sub-cards, data flow, and scientific visual metaphors (SVMC: GP curves, candidate tables, apparatus, memory graphs).
4. **Topology & Connections**: Explicit source -> destination connections, line styles (solid for forward, dashed for feedback/advisory), and edge labels.
5. **Visual Constraints**: Negative defect constraints (*No unintended or duplicated title banner, no floating text, no gradients, no 3D chrome, no photorealism, no shadows*).

## Text Budget

Visible text must remain structural and publication-legible:

| Element | Guideline |
|---|---|
| Region or module title | usually no more than 5 words |
| Short label | usually no more than 3 words |
| Arrow label | usually no more than 3 words |
| Core formula | at most one short sourced line |
| Parameters, evidence, caveats | caption only |

Drop secondary labels before reducing them below readable final-paper size.

## Workflow

### 1. Close the Semantic Graph
Copy component IDs, labels, groups, and typed connections from upstream analysis. Every component and edge needs evidence or an explicit user instruction. Carry `must_not_claim`, `forbidden_connections`, and authority boundaries into the spec.

### 2. Choose Composition & Visual Metaphor (SVMC)
Select composition from scientific narrative (pipeline, loop, asymmetric collage, sandwich, comparison grid). Apply **Scientific Visual Metaphor Compilation (SVMC)**:
- Surrogate/GP: embedded 2D coordinate plot with blue mean curve, dashed confidence bounds, light-blue shaded ribbon, orange scatter points.
- Candidate Pool: compact structured grid/table with header band and sourced rows.
- Experiment: laboratory test-tube rack or simulation block based on sourced evidence.
- Decision Agents: friendly line-art robot glyph or decision badge.
- Memory: node-edge network graph or episodic timeline.

### 3. Bind Style & Color Tokens Semantically
Bind paired tokens to semantic regions: background, soft fill, dark outline/title, optional icon accent, and exception color from `docs/palettes.md`.

### 4. Emit FigureSpec v1
Conform to `figure-spec.schema.json`. Required features include:
- `style_profile`: `classic-technical`, `pastel-airy-ui`, `illustrated-modular`, or `reference-led`.
- unique component IDs, closed visible-text list, sources, typed connections with valid endpoints.
- `prompt_review: requested|confirmed|waived` and conditional `prompt_reviewed_sha256`.
- declared absolute `workspace_root` and `output_path`.

### 5. Validate FigureSpec v1
Immediately before every render or edit, run:

```bash
python3 academic-figure-prompt/scripts/validate_figure_spec.py \
  --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

### 6. Hand off for Rendering & Repair
When called from `academic-figure-workflow`, pass the validated rendering package forward. Use the current session's native `image_gen.imagegen` interface. If prompt review is `waived`, keep prompt internal as a tool parameter and deliver the rendered image directly.
