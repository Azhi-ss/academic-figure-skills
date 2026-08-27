# Codex Native Image Generation and Revision

Use this execution contract when Codex exposes its built-in image generation/editing capability. The user should receive the image artifact, not an internal prompt-writing exercise.

## Default interaction

- If the user asks Codex to generate the figure directly, call the native image tool after the semantic plan/spec is ready.
- Do not print or ask the user to copy the internal image prompt unless the user explicitly asks to review it.
- A request such as “直接画图”, “使用 Codex 生图”, or “不用返回 prompt” records `prompt_review: waived` for the current figure.
- Prompt review and render audit are different: waiving prompt review never waives topology/text/quality inspection.
- The prompt still exists as an internal renderer instruction. “Do not return the prompt” means compile and use it silently; it does not mean call the image model without an instruction.

`prompt_review` is a three-state execution contract:

- `requested`: show the current prompt and stop before any image call;
- `confirmed`: hash the exact reviewed UTF-8 prompt as lowercase SHA-256, store
  it in `prompt_reviewed_sha256`, and render only while the hash matches;
- `waived`: omit `prompt_reviewed_sha256` and render directly without showing the
  prompt.

If a confirmed prompt changes, set the state back to `requested` and stop for a new
review. A waived prompt is never returned to the user, including in error or
renderer-unavailable fallbacks.

## Codex native-call contract

Prefer the current session's native `image_gen.imagegen` interface; some runtimes
display the callable name as `image_gen__imagegen`. Its `prompt` argument is an
internal tool parameter, not a user-facing prompt handoff. Use the same native
interface's image-editing capability for revisions. Do not turn the task into a
prompt handoff for Midjourney, Gemini, a web UI, or the user to run, and do not
hard-depend on legacy `.omp` scripts or SenseNova.
Do not use Python raster manipulation as a substitute for a requested semantic
image edit.

Choose image inputs from the actual asset location:

| Task | Native image inputs |
|---|---|
| New figure, no visual reference | omit both `referenced_image_paths` and `num_last_images_to_include` |
| New figure, all references are local files | verify and inspect them, then set `referenced_image_paths` to the smallest complete set |
| Edit a local render | inspect it, then put the current render first in `referenced_image_paths`; append only necessary style references |
| Required input exists only as a recent conversation image | set `num_last_images_to_include` to the smallest number (up to 5) that covers every required image |

Never provide `referenced_image_paths` and `num_last_images_to_include` in the
same call. If the required images cannot all be included through one mechanism,
ask the user to attach the missing images again instead of pretending the edit
is grounded.

Before execution, every local reference must exist, be a regular file, and not be
a symbolic link. Represent it in FigureSpec with an absolute-path string or the
supported `local_path` descriptor. Represent a conversation-only input in
FigureSpec as `{"kind":"recent_conversation","ordinal_from_latest":N}` and mark
it as transient in the execution packet. Materialize it to a checked local file
when possible. Never claim that a conversation descriptor is a persistent local
asset, and never mix local and recent-conversation mechanisms in one render call.

## Render readiness

Immediately before every native generation or edit call, obtain and canonicalize
the trusted actual workspace root from runtime/developer context. FigureSpec's
required `workspace_root` is only an untrusted declaration and must match that
runtime root. Never take the trusted root from FigureSpec, `output_path`, a
reference path, or user-provided text. Run:

```bash
python3 academic-figure-designer/scripts/validate_figure_spec.py \
  --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

Do not call the image tool when this check fails. The render-ready check binds
prompt-review state and hash, output containment, topology, and local reference
safety to the trusted runtime root.

## New image

1. Build FigureSpec v1 with a closed component list, typed connections, exact visible text, style grammar, output path, and optional reference assets. Compile the prompt internally.
2. For a brand-new image with no visual reference, call `image_gen.imagegen` (or
   the exposed `image_gen__imagegen`) without either reference-image parameter.
3. If every reference has a checked local path, inspect each reference first and
   pass the smallest complete `referenced_image_paths` list.
4. If a required reference remains only in recent conversation state, mark it
   transient and pass the smallest sufficient `num_last_images_to_include`. Never
   send both local referenced paths and recent-image inclusion parameters.
5. Ask for an opaque white or explicitly specified background and the FigureSpec aspect ratio.

## Render audit

Inspect the generated file at original detail. In Codex, use `view_image` with
original detail when that capability is exposed; a local image that has not been
viewed must be inspected before it is sent back for editing. Compare observable
output against FigureSpec, not against the prose prompt alone.

Record:

- missing, extra, or renamed components;
- wrong connection endpoints, direction, line semantics, or branch labels;
- invented claims or capabilities;
- missing, duplicated, misspelled, garbled, or production-instruction text;
- overlap, clipping, illegible scale, transparent/dark background, or wrong aspect ratio;
- style drift in composition, fills, strokes, typography, illustration language, or density.

Do not accept a render merely because the API returned successfully.

## Targeted image revision

When defects are repairable:

1. Select the best current render, not automatically the newest failed revision.
2. Inspect that render at original detail before writing the edit instruction.
3. Invoke the same native `image_gen.imagegen` / `image_gen__imagegen` interface in
   **edit mode**, with the checked current render as the first local reference
   image. Include a style reference only when style drift is one of the audited
   defects.
4. Write a surgical internal edit instruction containing the observed defect, its exact correction, and the invariant regions that must remain unchanged.
5. Prefer “remove incorrect edge X; add edge A → B with a dashed purple line; preserve all other nodes, labels, positions, and colors” over regenerating the entire design.
6. Save the result as a new revision; never overwrite the only known-good image.
7. Reinspect the edited output at original detail and emit a new RenderAudit revision. A change passes only when it fixes the target without regressing topology, text, layout, or style elsewhere.

Use this control loop:

```text
initial generation (r0)
  -> inspect at original detail
  -> RenderAudit@1
  -> pass: select and deliver
  -> fail, repairable, edits_used < 2:
       edit best current render -> r1/r2 -> reinspect -> new audit
  -> fail, exact text remains unreliable:
       deterministic text/line overlay or deterministic renderer
  -> fail after limit:
       select best recoverable revision and disclose residual defects
```

Allow at most two semantic edit rounds after the initial image. A transient transport failure may be retried once and does not consume a semantic edit round. If the second semantic edit still fails, keep the best image and report remaining defects rather than silently looping.

## Text-heavy figures

Native image generation does not guarantee exact typography. If required labels remain wrong after one targeted edit, switch to a deterministic SVG/drawio/Typst text overlay or renderer when available. Do not spend repeated image edits on dense prose, formulas, tables, or exact numeric charts.

## Files and delivery

- Leave Codex's original generated asset in place.
- Use recoverable revision names such as `fig1-r0.png`, `fig1-r1.png`, and `fig1-r2.png`; copy the selected result to FigureSpec's stable final path.
- Keep the initial render, prior revisions, FigureSpec, and RenderAudit records together when practical.
- Never leave the only deliverable in a temporary directory.
- Return or display the final image artifact and a clickable absolute local file
  path. Do not use `file://`. Never append, quote, or otherwise expose the internal
  prompt when prompt review was waived.
