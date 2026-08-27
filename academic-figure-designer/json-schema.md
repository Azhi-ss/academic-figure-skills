# FigureSpec v1 Contract

The machine-readable schema is `figure-spec.schema.json`. This document explains the design intent and migration from legacy prompt specs.

## Identity and sources

```json
{
  "schema": "academic-figure/FigureSpec@1",
  "figure_id": "fig1",
  "plan_revision": "plan-1",
  "sources": [
    {
      "kind": "repository|paper|reference_image|user_instruction",
      "uri_or_path": "<source>",
      "revision_or_page": "<commit/page/figure>",
      "evidence": "<short pointer>"
    }
  ]
}
```

Sources support scientific content. A reference image may support visual grammar without supporting the target method's labels or topology.

## Components

Each visible semantic unit has a stable unique ID:

```json
{
  "id": "policy",
  "label": "Typed Policy",
  "role": "decision",
  "group_id": "reasoning",
  "importance": "hero|primary|secondary",
  "visible_text": ["Typed Policy", "KEEP", "CHANGE", "PROBE", "STOP"],
  "visual_anchor": "decision diamond with four action tabs",
  "evidence": ["Policy/controller.py:PolicyDecision"],
  "caption_note": "Long explanation kept off the figure"
}
```

Do not create a component for every code directory or helper class. Components represent figure-worthy responsibilities.

## Connections

Connections are first-class so topology can be validated:

```json
{
  "id": "policy-to-harness",
  "from": "policy",
  "to": "bo-compilation",
  "kind": "executed|advisory|feedback|persistence|exception",
  "direction": "forward|backward|bidirectional",
  "line": "solid|dashed|dotted",
  "label": "KEEP / CHANGE",
  "evidence": ["runtime/controller.py:run_round"]
}
```

Every endpoint must match one component ID. Spatial proximity never implies a connection. Include `forbidden_connections` when a wrong shortcut would change the scientific meaning.

## Layout

```json
{
  "topology": {
    "groups": [
      {
        "id": "reasoning",
        "label": "Research and Agent Layer",
        "component_ids": ["task", "evidence", "policy", "reflection"]
      }
    ]
  },
  "layout": {
    "composition": "pipeline|loop|storyboard|layered_boundary|central_mechanism|modular_collage|comparison_grid|custom",
    "hero": "policy",
    "reading_order": ["task", "evidence", "policy", "bo-compilation"],
    "group_regions": {"reasoning": "left 40%"},
    "nesting_depth": 1,
    "whitespace": "compact|balanced|open",
    "routing_notes": ["STOP bypasses the deterministic harness"]
  }
}
```

Use one nesting level only when it communicates real hierarchy. `hero` may name a component or group ID.

## Style grammar and semantic tokens

```json
{
  "style_profile": "illustrated-modular",
  "style_preset": "editorial-hand-drawn",
  "style_source": "reference",
  "reference_images": ["/absolute/path/to/reference.png"],
  "style_grammar": {
    "marks": "rounded editorial line art",
    "fills": "low-saturation tinted regions",
    "strokes": "dark same-hue 3px-equivalent outlines",
    "typography": "rounded hand-lettered headings, readable dark labels",
    "shadow": "none",
    "density": "balanced"
  },
  "semantic_color_roles": {
    "reasoning": {
      "fill": "#EDF4FA",
      "outline": "#163E64",
      "title": "#163E64",
      "icon_accent": "#5A9BD4"
    },
    "exception": {
      "fill": "#FFF1EE",
      "outline": "#B63A2B",
      "title": "#8E2D22",
      "icon_accent": "#FA7E6E"
    }
  }
}
```

Canonical profile IDs are `classic-technical`, `pastel-airy-ui`,
`illustrated-modular`, and `reference-led`. Specific named style files belong in
`style_preset`, not `style_profile`. `reference-led` is an override mode: it
preserves the supplied reference's observed grammar, whether that grammar is
technical, airy, illustrated, or a coherent combination. It never means
“illustrated modular by default.” The style grammar determines fills, borders,
typography, icon treatment, and shadow policy; no global white-fill or
monochrome rule applies to every profile.

`reference_images` accepts absolute local-path strings (or equivalent
`{"kind":"local_path","path":"..."}` descriptors) and recent-conversation
descriptors such as
`{"kind":"recent_conversation","ordinal_from_latest":1}`. Mark such an input
as transient in the separate execution packet; `transient` is not a FigureSpec
field.
Before execution, each local path must exist, resolve to a regular file, and not
be a symlink. Conversation descriptors are transient; materialize them to a
checked local file when possible and never describe them as persistent assets.
Do not mix local and recent-conversation mechanisms in one spec because the
Codex native call cannot send both at once. Recent-conversation ordinals are
limited to 1–5.

## Internal renderer instruction and review state

```json
{
  "prompt": "Internal lossless renderer instruction compiled from this spec.",
  "prompt_review": "confirmed",
  "prompt_reviewed_sha256": "60f6b3a2f7f8d173c0f84eae35c5da9da7d121f0352d68f8e5256651c9f67a99"
}
```

`prompt_review` is an execution state as well as a visibility state:

- `requested`: show the exact current prompt and stop; rendering is not allowed;
- `confirmed`: store the lowercase SHA-256 digest of the exact reviewed UTF-8
  prompt in `prompt_reviewed_sha256` and render only while it still matches;
- `waived`: omit `prompt_reviewed_sha256`, render with the prompt as an internal
  tool argument, and never expose it to the user, including in a fallback.

Any prompt change after confirmation returns the state to `requested` for a new
review. The preferred Codex renderer is the native `image_gen.imagegen` interface
(sometimes exposed as `image_gen__imagegen`); its prompt parameter is not a
user-facing prompt handoff.

It never disables RenderAudit. When the user asks Codex to draw directly or says
not to return a prompt, record `waived`, use the prompt internally, and deliver
the image rather than a prompt handoff.

## Text, caption, and constraints

```json
{
  "visible_text": ["Task and State", "Typed Policy", "No Oracle Budget"],
  "caption_notes": ["Evidence manifest membership is provenance, not truth verification."],
  "must_not_claim": ["autonomous wet-lab validation"],
  "forbidden_connections": ["policy -> numeric_prediction"],
  "negative_constraints": ["no extra modules", "opaque white canvas", "no production instruction text"]
}
```

`visible_text` is a closed intent list: the image prompt should request no other words. It is not an OCR guarantee. The workflow must inspect the generated image, and text-heavy figures should use a deterministic renderer or overlay.

## Output geometry

```json
{
  "aspect_ratio": "16:9",
  "final_width_mm": 183,
  "workspace_root": "/absolute/workspace",
  "output_path": "/absolute/workspace/path/fig1.png"
}
```

Physical width is export and audit metadata. `workspace_root` and `output_path`
must both be absolute, and the output must remain inside that root. The declared
`workspace_root` does not establish trust: the caller obtains the canonical
trusted actual root from runtime/developer context, passes it separately to the
validator, and requires the declaration to match. Never derive the trusted root
from FigureSpec, `output_path`, references, or user text. Do not tell a raster
image model that a pixel canvas itself has exact 8pt or 10pt typography; test
legibility after scaling to the intended width.

## Validation

Run:

```bash
python3 academic-figure-designer/scripts/validate_figure_spec.py \
  --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

Run this immediately before every generation or edit, and do not call the image
tool when it fails. Render-ready validation checks prompt-review state and hash,
the artifact version, enumerations, IDs, endpoint references, required
layout/style/output fields, trusted-root containment, local-reference safety, and
basic text constraints. It cannot prove factual correctness or visual quality;
those require evidence review and RenderAudit after each result.

For native execution, omit both reference selectors for a new image without a
reference. Use the smallest complete `referenced_image_paths` set for checked
local files, or the smallest sufficient `num_last_images_to_include` for
conversation-only inputs; never pass both. A targeted repair views and audits the
best current render, places it first in `referenced_image_paths`, locks all
correct regions, saves a new revision, and re-audits it. Allow at most two
semantic edit rounds; a transient transport retry does not count.

Legacy `diagram_type` / `layout_and_content_blocks` specs may be read in compatibility mode but should be migrated before new rendering.
