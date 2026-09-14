# Render Audit Protocol

Use this protocol after every generated academic figure and after each targeted
edit. A successful image-generation API response is not evidence that the figure
is correct. Inspect the image at original resolution and compare it with the
confirmed FigureSpec, source evidence, and any reference image.

## Inputs and output

Required inputs:

- the validated `academic-figure/FigureSpec@1` object;
- the rendered image at an absolute local path;
- source figure plan and evidence locations;
- reference images when `style_profile` is `reference-led`.

Emit a JSON-compatible audit:

```text
schema: academic-figure/RenderAudit@2
figure_id, render_revision, image_path (absolute)
image_sha256, spec_sha256 (lowercase SHA-256 of exact file bytes)
spec_validation: {status: pass|fail|unverified}
image_inspection: {status: pass|fail|unverified, evidence}
nodes[]: {id, status: pass|fail|unverified, evidence}
edges[]: {id, from, to, kind, direction, line, label,
          status: pass|fail|unverified, evidence}
checks:
  semantic_topology, visible_text, background, layout,
  style_fidelity, accessibility
  (each check is {status: pass|fail|unverified, evidence})
pass: true|false
defects[]: {check, severity, observed, expected, evidence, edit_instruction}
targeted_edit: string|null
semantic_edits_used: 0|1|2
semantic_edits_remaining: 2|1|0
residual_risks[]
```

## Revision binding and complete ledgers

New audits use RenderAudit@2. Keep legacy @1 records for history, but do not
upgrade their booleans mechanically into observed @2 results. Bind each audit to
one actual image and one actual FigureSpec by path, revision, and raw-file
SHA-256. Finish any export/metadata transformation before binding the delivered
file, then inspect that exact final file. A new file or changed spec needs a new
audit; do not copy forward a previous image's pass.

FigureSpec validation and actual image inspection are independent. Record their
statuses separately. If the image cannot be opened, or an arrowhead is too
ambiguous to identify, use `unverified`, not a guessed `pass`. Evidence describes
what was inspected, including region or endpoints; “spec valid” is not visual
evidence. Image inspection status says whether inspection was performed; defects
found during inspection belong in the individual check statuses.

Derive the complete node and edge ledger from the spec, not from what is easiest
to see. Cover every component and every connection exactly once. Use declared
edge IDs; for a legacy connection without an ID, use its stable one-based position
as `edge_001`, `edge_002`, etc. Copy from/to/kind/direction/line/label exactly;
for omitted direction/line use `unspecified`, and omitted label is an empty
string. Semantic kind remains required. This does not authorize rendering a scientifically ambiguous spec.

Check the image against the ledger, then scan the image for extra edges and
forbidden shortcuts; a required-edge ledger alone cannot detect invented arrows.
Record that second scan and authority-boundary checks under semantic_topology.
Record the actual text-inventory and final-size inspection under the relevant
checks. Reset all statuses to unverified for every new image, including style-only
and single-arrow edits, and recheck all required edges outside the edited region.

For the bundled record validator (it does NOT inspect pixels), run:

```bash
python3 <workflow>/scripts/validate_render_audit.py \
  --spec <spec.json> --image <image.png> <audit.json>
```

Exit 0 means the bound record is complete and all asserted statuses pass; exit 1
means a valid record is failed/unverified; exit 2 means malformed, incomplete or
mismatched evidence, including a stale digest or misleading aggregate pass.
When workflow's script is not installed, perform the same ledger checks manually
and state that record validation was manual. Never call this script's exit 0
proof of scientific accuracy or image quality: it cannot verify the truthfulness
of a human/model's visual assertions.

A legal top-level `pass: true` requires all node/edge/check statuses, spec
validation and image inspection to pass, with no critical or major defect.
Any fail or unverified status blocks acceptance. A complete record of a failed
image is useful and must remain failed.

`severity` is `critical`, `major`, or `minor`. A critical or major defect makes
the audit fail. Minor defects may pass only when they do not change scientific
meaning, legibility, accessibility, or the requested visual identity.

## 1. Semantic topology

Treat the FigureSpec component and connection lists as a directed graph.

- Every required component appears exactly once unless duplication is explicitly
  specified as a repeated stage.
- Every rendered arrow has the correct source, target, direction, kind, and label.
- Required branches, loops, authority boundaries, budget effects, and persistence
  paths are present.
- Forbidden components, connections, causal implications, performance claims, and
  copied scientific content are absent.
- Advisory, executed, feedback, persistence, and exception paths remain visually
  distinguishable according to the spec.

Any missing, invented, reversed, or merged scientific edge is a **critical**
defect. Do not approve a visually attractive but semantically incorrect render.

## 2. Visible text

Compare the image against the complete `visible_text` inventory, using visual
inspection and OCR when available.

- Every required string is present, spelled correctly, and assigned to the right
  component or connection.
- No JSON keys, prompt instructions, hex codes, production notes (`WHITE FILL`,
  `300 DPI`, stroke widths), watermarks, or unexplained text are visible.
- No duplicated, truncated, fused, hallucinated, or illegible labels remain.
- Mathematical symbols, identifiers, capitalization, and branch labels preserve
  their specified meaning.
- Text remains readable at the intended 89 mm or 183 mm publication width, not
  merely when zoomed to the generation resolution.

Scientific text errors are critical. Optional secondary-label loss is major when
it damages interpretation and minor only when the FigureSpec marks it optional.

## 3. Background and artifact integrity

- Canvas dimensions match the requested aspect ratio within raster rounding.
- The background is the specified solid color; when white is required, corner and
  inter-panel pixels are opaque `#FFFFFF`, not transparent, gray, or black.
- No accidental alpha channel, crop, border, compression damage, checkerboard,
  watermark, or model signature is present.
- Metadata and provenance cleanliness: sanitize and strip all C2PA manifests, JUMBF markers, EXIF, and AI generation metadata using `clean_image_metadata.py` before final delivery.
- The file extension matches the encoded media type and the image opens normally.

A background or opacity that differs from the FigureSpec, a wrong crop, or a
wrong aspect ratio is a major defect. A file that cannot be decoded is critical.

## 4. Layout and publication-scale legibility

- Components follow the planned reading order, grouping, hierarchy, focal point,
  and relative emphasis.
- Boxes, illustrations, labels, legends, and arrowheads do not overlap or collide.
- Connections do not ambiguously cross nodes or terminate in empty space.
- Margins and whitespace are intentional; the figure is neither an empty template
  nor a uniformly dense wall of boxes.
- Primary information survives a thumbnail/publication-width check; secondary
  detail may recede but must not become visual noise.
- Repeated elements align consistently while semantic exceptions remain salient.

Overlap that hides meaning or an ambiguous connector is major. Minor alignment
variation is minor only when the intended reading order stays unambiguous.

## 5. Style fidelity

For a built-in profile, check the profile's composition, marks, strokes, fills,
typography, spacing, motifs, and emphasis—not just its named colors. For a supplied
reference, compare transferable visual grammar while keeping the new method's
content and topology independent.

- Composition and visual hierarchy match the selected profile or reference.
- Palette colors have the specified semantic roles and relative area; do not wash
  every region with equally saturated color.
- Stroke language, arrow curvature, illustration level, panel treatment, corner
  geometry, typography character, and whitespace match the intended family.
- Absent traits from the reference stay absent: do not add enterprise swimlanes,
  heavy dark borders, gradients, shadows, 3-D chrome, clip art, or generic robot
  motifs unless the profile calls for them.
- A reference's labels, metrics, branding, scientific objects, and topology are not
  copied merely to imitate its appearance.

A palette match with the wrong composition or mark language does **not** pass style
fidelity. Clearly landing in the wrong style family is major.

## 6. Accessibility and print behavior

- Normal-size text has at least 4.5:1 contrast against its actual background;
  large text has at least 3:1.
- Essential outlines, arrows, markers, and focus boundaries have at least 3:1
  graphical contrast against adjacent colors; pale decorative dividers do not
  carry semantic meaning.
- Critical distinctions use color plus a second cue such as label, shape, marker,
  hatching, or line style.
- Simulated protanopia, deuteranopia, and tritanopia views preserve required
  distinctions when a simulation tool is available.
- A grayscale preview preserves topology, grouping, and exception branches.
- Thin strokes, pale tokens, and small type remain discernible at publication size.

Record the measured foreground/background pairs when contrast tooling is
available. Never infer accessibility from a palette name alone.

## Targeted-edit policy

The initial render may receive **at most two targeted semantic visual edits**.
A single retry for a transient API/transport failure does not consume this
budget because it did not attempt to change the image semantics.

1. Audit the initial render and rank defects by semantic risk.
2. If it fails, write one bounded edit instruction containing only the observed
   defects, their exact expected replacements, and an explicit list of critical nodes, edge endpoints/directions/types,
   visible labels and authority boundaries to preserve. “Keep everything else”
   alone is not a preservation contract.
3. Inspect the edited image and emit a newly bound audit. Recheck the full
   required edge ledger, not just the repaired connector; do not assume an edit
   preserved topology or text.
4. If needed, perform one final targeted edit, then audit again.
5. After two targeted edits, stop. Deliver the best valid artifact only if all
   critical and major checks pass; otherwise mark the render incomplete and report
   residual defects instead of silently accepting it or starting an unbounded loop.

Do not use a whole-image style rewrite to repair one spelling error or connector.
Conversely, do not patch isolated colors when the audit shows the entire style
family or composition is wrong; use the first targeted edit to correct that bounded
systemic defect and preserve grounded content.
