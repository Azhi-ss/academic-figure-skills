# FigureSpec to Image Prompt Compilation

Compile settled design decisions into rendering instructions without changing scientific content. This is the single compiler. Use `prompt-design-logic.md` first for construction, diagnosis, or revision; do not infer new science during compilation.

## Invariants

1. Preserve every declared component and every edge's endpoints, direction, kind, line semantics and label.
2. Add no unsourced dimensions, formulas, claims, legends, icons or capabilities. A reference supplies style, not evidence for the target method.
3. Only approved `visible_text` and explicitly reconciled component/edge labels are visible. If local label fields and the global inventory disagree, repair the design before compiling.
4. Evidence pointers, caption notes, JSON keys and production metadata are not visible. Hex colors are style instructions, not labels.
5. Reference images remain structured image inputs when supported; prose does not replace reference conditioning.
6. Use compact natural-language paragraphs, without Markdown headings, emphasis, bullet markers or tables around instructions. Do not remove approved scientific symbols merely because they resemble markup.
7. Prompt-only output does not claim rendering or visual validation occurred. A draft brief may precede render-ready FigureSpec; never fabricate output paths to satisfy a prompt-writing request.

## One compilation order

This is the prose order, not the design-decision order. Settle the style grammar before finalizing layout; composition and component descriptions must already embody it even though detailed style tokens appear in section 5. If only a content brief exists, return to design before compiling, rather than appending a style slogan to an otherwise frozen prompt.

### 1. Purpose

Name the figure type and one communication goal. State the dominant scientific mechanism and any high-risk meaning to avoid. Default to no overall canvas title; when requested, lock exactly one short non-banner title.

### 2. Composition and components

Describe the reading order, dominant region, supporting groups and connector channels. Use approximate proportions only when they help, not for every container. Nest cards only when they express real hierarchy; a comparison grid need not have a hero region.

For illustrated-modular, state the unequal region proportions, which clusters stay open, and the few modules that receive a local outline. Put each sourced mechanism line in that cluster's prose. Do not compile one equal framed icon per component. A secondary station on an executed path stays in its region at a smaller scale.

Describe optional visual anchors already selected in the spec. A label-only node is valid. A useful hero schematic may replace several repetitive icons. No mandatory icon + mini-plot + math-card bundle.

Select visuals by the role they explain, not by the field's stereotypes:

| Meaning to communicate | Possible visual, if declared |
|---|---|
| Propose or reason about an action | small line-art agent with one short decision question |
| Independent assessment | reviewer role and bounded advisory output; no invented consensus |
| Uncertainty or acquisition | sourced schematic curve or actual deterministic plot |
| Representation or transformation | token stream, tensor slices or connection matrix |
| Experiment or observation | actual supported apparatus or measured-data symbol |
| Memory and provenance | record stack or event graph, distinct from validation |

Do not insert a GP surface, threshold test, coupling formula or wet-lab robot merely because the paper concerns optimization. Any illustrative curve without measured data must be identified as schematic in approved labels or caption notes. Quantitative plots use actual data and deterministic plotting.

### 3. Closed topology

Translate each declared edge exactly once, identifying source and target by visible label and region when necessary. Include direction, semantic kind, line style and exact label when present. Internal IDs identify checks and are not visible labels unless separately approved.

For example: “Draw a solid forward executed arrow from Selection to Experiment, labelled Submit. Draw a dashed advisory arrow from Review to Fusion.” Use this only when those nodes and edges are actually declared.

State prohibited shortcuts explicitly where they would change meaning, then “Draw no other inter-module connections.” Spatial proximity never implies an edge. Preserve distinct bidirectional or backward edges without silently converting them to a forward pipeline.

### 4. Visible text

Provide a closed list of exact visible strings, grouped by region. Distinguish plot labels and necessary legends from caption-only parameters, evidence and caveats. Never ask for rendered placeholder text or production instructions. A closed inventory is an intent constraint, not an OCR guarantee.

### 5. Visual grammar and semantic color

Describe marks, stroke character, fills, typography, spacing, illustration level and shadow policy, then map actual roles to paired soft fill / dark outline-title / optional accent tokens. Add non-color encodings for scientifically important distinctions.

Style exclusions must agree with the selected grammar. A declared scientific 3D surface is not “3D chrome”; do not request it and simultaneously forbid all 3D. White is the common default, not an override of a user-approved domain-specific background.

### 6. Defect constraints and geometry

End with specific failure prevention: no extra edges, role confusion, duplicate labels, unreadable text, overlap or clipping; add only applicable style exclusions. State aspect ratio and final-scale legibility intent. Physical width and exact point sizes are export/audit metadata, not a guarantee from a raster model.

## Revisions

Update the design first. For prompt revision, output a coherent complete new prompt plus a short change/preservation summary; do not accumulate contradictory append-only patches.

For an actual image edit, use a bounded edit prompt with the inspected baseline image: observed defect, exact correction, and explicit critical edges/labels/authority boundaries to preserve. “Everything else unchanged” may supplement, but cannot replace, that list. After editing, audit the entire required graph, including edges outside the edited region.

## Length and backend suitability

Use the shortest lossless brief. About 180–450 English words often works, but never drop essential edges or the selected profile's composition to meet a word target. Hero proportion, nesting, mark language, and sourced mechanism lines stay for every profile. Do not meet that word range by replacing open region interiors with an equal icon strip. An arrow repair copies that composition unchanged. Dense labels, precise equations or fragile topology may warrant deterministic SVG/drawio/Typst or hybrid vector text. Preserve the user's chosen backend and current tool policies; if a switch changes the requested deliverable materially, explain and obtain direction. Never claim that prose guarantees exact geometry or typography.

## Preflight

Check component/edge coverage, source support, closed visible text, compatible style constraints, reference-input selection and an objective image checklist. Specification validation proves the input contract, not the generated pixels.
