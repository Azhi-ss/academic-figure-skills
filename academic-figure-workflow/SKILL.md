---
name: academic-figure-workflow
description: Plan, generate, inspect, and refine academic figures from repositories, papers, draft notes, paper URLs, PDFs, or reference images. Design evidence-grounded academic figures and construct, diagnose, or revise scientific image prompts, including semantic palettes, reference-led styles, prompt engineering, information-density feedback, and FigureSpec v1 compilation. Supports fast-track draft-to-figure generation, user passthrough mode, and replacing AI-rendered text with editable PowerPoint text boxes.
metadata:
  version: "2.2.0"
  stages: [writing, research, review]
---

# Academic Figure Workflow

Produce a grounded academic figure and a stable local artifact. Preserve the user's chosen backend, reference assets, style direction, review preference, and output scope.

If the user asks only to construct, diagnose, or revise a figure prompt, use
this skill's matching output mode and stop before rendering. A prompt-only
request does not require invented render paths or an extra approval gate.

将科学内容编译成可验收的图示。这里是唯一的设计与 prompt 编译入口；不把提示词修辞当作第二次科学设计。

## 按请求选择输出

| 用户意图 | 行动与停止点 |
|---|---|
| 构造画图提示词 / 只写 prompt | construct：设计简报与完整 prompt；不生图 |
| 检查或诊断已有 prompt | diagnose：定位问题、影响与最小修正；不擅改文件或生图 |
| 按反馈修改 prompt | revise：改动、保留项及完整新 prompt；不自动生图 |
| 制作图 / 修改图片 | construct 或 revise 后，本 skill 继续渲染、目检 |
| 只咨询配色或风格 | Palette Decision；不要求完整拓扑，不生图 |
| 把 AI 图里的文字做成可编辑 PPT | 按 `references/editable-pptx.md` 写清单并组装 PPTX；不改源 PNG，不另开 skill |

只问方案时不启动绘图。直接画图时不强加 prompt 确认；按用户的 review 偏好执行。直接画图不代替风格选择。

## 按需读取

Load only what the current stage needs:

- 构造、诊断或修订决策 → `references/prompt-design-logic.md`
- 编译 renderer prompt → `references/json-to-prompt.md`
- 可直接填充的构造/修订样板 → `references/prompt-templates.md`
- 密度、布局、文字或风格细节 → `references/image-prompt-guide.md`
- 案例与迁移检验 → `references/prompt-design-cases.md`
- 实际渲染的结构契约 → `json-schema.md` 和 `figure-spec.schema.json`
- 视觉锚点 → `references/architecture-icons.md`，仅使用符合证据的元素
- 第一次出图前的风格菜单 → `references/style-catalog.md` 与 `references/previews/`
- 色彩与可选风格库 → `references/palettes.md`、`references/styles/`
- Codex native image execution → `references/codex-image-workflow.md`
- 图片验收 → `references/render-audit.md` (required before accepting an image)
- 可编辑 PPT 文字 → `references/editable-pptx.md`。交付栅格图时只告知可以做；用户接受这张图并要求可编辑文字后才读、才组装

超出证据的内容标推断或待确认；用占位符代替编造的模块、损失、维度或结果；没有任何可用来源时停下，并列出最少需要补充的材料。

## Route inputs by inspected content

A URL is not automatically a repository. Inspect it first.

| Input | Route | Execution Behavior |
|---|---|---|
| **Direct User Architecture (Passthrough)** | This skill's design flow | **Skip the analyzer**. User gave explicit nodes/flow; compile FigureSpec v1 and render directly. |
| **Draft Notes / Outline / Partial Draft** | `../academic-figure-analyzer/SKILL.md` | **Draft-to-Figure Fast-Track**. For rough notes, outlines, or sections without full results: focus on Figure 1 framework. |
| **Complete Manuscript (Markdown / LaTeX / PDF / URL)** | `../academic-figure-analyzer/SKILL.md` | **Full Planning**. For complete papers with experiments/results: multi-figure strategy, claim verification, and constraints. |
| **Repository path or repository URL** | `../academic-figure-analyzer/SKILL.md` | Extract semantic architecture graph; omit engineering plumbing (data loaders, trainers). |
| **Paper plus repository** | `../academic-figure-analyzer/SKILL.md` | Paper/user defines narrative & topology; repository supplies parameter & dimension verification. |
| **External style reference** | `../academic-figure-analyzer/SKILL.md` | Extract transferable style from external references. |
| **Existing render to edit** | This skill's revise mode | Preserve its scientific content, topology and visible text, then apply only the requested delta. |

For an article URL, use an available web/browser/document reader to obtain the paper text, captions, and linked figures. For a PDF, use a PDF-capable reader for paper content. If academic-figure-analyzer is not installed, perform the minimum equivalent analysis and mark the degraded path.

## Keep versioned internal artifacts

Store these as JSON-compatible objects. Do not make the user read them unless requested.

### FigurePlan v1

```text
schema: academic-figure/FigurePlan@1
source_revision, venue
sources[]: {kind, uri_or_absolute_path, revision_or_page, evidence}
figures[]: {
  figure_id, figure_type, priority, communication_goal, claim_scope[], hero_element,
  required_nodes[], required_connections[], authority_boundaries[], secondary_context[],
  forbidden_claims[], forbidden_connections[], aspect_ratio, final_width_mm,
  style_profile_hint, reference_assets[],
  open_questions[], confidence, review_status: pending|confirmed|waived
}
```

Components and connections are semantic and evidence-backed. A code directory count is not a figure hierarchy or palette decision.

### FigureSpec v1

```text
schema: academic-figure/FigureSpec@1
figure_id, plan_revision, sources[], prompt (internal), aspect_ratio, final_width_mm
topology: {components[], connections[], groups[], authority_boundaries[]}
visible_text[], caption_notes[], layout
style_profile: classic-technical|pastel-airy-ui|illustrated-modular|reference-led
style_preset, style_source, style_grammar, semantic_color_roles
style_selection: pending|confirmed|waived (render-ready rejects pending or missing)
reference_images[]: checked absolute local paths or recent-conversation descriptors
conversation-reference transient status stays in the execution packet
must_not_claim[], forbidden_connections[], negative_constraints[]
prompt_review: requested|confirmed|waived
prompt_reviewed_sha256: required only when prompt_review is confirmed
workspace_root: absolute declaration that must match the runtime-trusted root
output_path: absolute path inside that root
```

The internal `prompt` is renderer input, not a required user-facing deliverable.
When `prompt_review` is `waived`, persist it only with the working artifacts and
never paste it into the chat response.

### RenderAudit v2

```text
schema: academic-figure/RenderAudit@2
figure_id, render_revision, image_path, image_sha256, spec_sha256
spec_validation: {status}
image_inspection: {status, evidence}
nodes[]: {id, status, evidence}
edges[]: {id, from, to, kind, direction, line, label, status, evidence}
checks: {semantic_topology, visible_text, background, layout,
         style_fidelity, accessibility} (each: {status, evidence})
pass, defects[], targeted_edit, semantic_edits_used, semantic_edits_remaining
```

Statuses are `pass|fail|unverified`. See the shared audit protocol for exact
revision binding, complete graph coverage, and aggregate-pass requirements.
Keep historical v1 audits as history; new renders require v2 inspection records.

## Build the plan

Create the shortest FigurePlan that closes scientific ambiguity. Shortest means no speculative modules. A station on an executed path stays in the figure even if its importance is secondary; `secondary_context` is only for context that does not change the path. When a reference exists, its transferable **style grammar** takes priority over venue stereotypes and preset defaults. Match composition, mark language, illustration level, region treatment, typography, spacing, arrow grammar, emphasis, and semantic color roles. Do not copy the reference's claims, labels, branding, or topology unless it is the user's redraw or edit baseline.

Use plan review only when unresolved choices would materially change the result, the user asks to review it, or required content is still a placeholder. Otherwise record `review_status: waived` and continue. An unrelated reply is never confirmation.

## 设计流程

1. 写出读者问题及图的核心答案，区分主内容、支撑内容、caption-only。
2. 从上游分析或用户输入提取稳定 component IDs、typed connections、权限边界、禁止关系及证据。不从参考图借算法，不把缺失证据填成确定事实。
3. 在科学骨架明确后、布局定稿前确认风格。按下一节的风格确认规范执行；未确认前不做布局定稿，也不生图。风格参与后续构图，不作为写完 prompt 后追加的装饰句；详见 `references/prompt-design-logic.md`。
4. 联合科学含义与所选风格设计阅读顺序、主区、语义分组、连线通道及必要视觉锚点。只有真实层级需要时才嵌套；比例是构图辅助。图标、小图、公式卡、机器人或气泡均可选。纯标签节点只在所选风格允许时使用。任何风格的主区比例、嵌套层和标记语言都不要收成等大图标条。
5. 锁定可见文字、语义颜色与非颜色编码，检查所选风格下的文字容量与可读性；编译前闭合全部边。修订先写 Delta 与 Invariants，颜色修改不改变科学拓扑。
6. 将内容、布局与风格统一编译为完整的紧凑自然语言，而非给旧 prompt 叠加风格补丁。prompt-only 在此交付；渲染任务再补齐、校验 FigureSpec 并移交执行。

用户直接描述架构时跳过不必要的仓库扫描。将其记为 `sources` 中的 `user_instruction`，证据为原请求；component IDs 使用稳定 snake_case。执行、建议、反馈、存储和异常连接分开，不靠位置推断连线。

## Confirm style before the first render

Do this after the scientific skeleton is clear and before layout or the renderer prompt. Follow `references/prompt-design-logic.md` for reference handling and bounded style-only revisions. This gate applies only to the first render. Revisions, color-only edits, a style the user already named, and a reference image the user asked to follow do not open the menu again.

- No named style and no style reference: read `references/style-catalog.md`, show all six previews by displaying the image files themselves, add one line of traits each, then stop. Do not call the image tool in that turn.
- “直接画图”, “使用 Codex 生图”, or “不用返回 prompt” sets `prompt_review: waived` only. It does not choose a style.
- The user named a style or profile: record that `style_preset` and its catalog `style_profile`, set `style_selection: confirmed`, and continue without asking again.
- The user supplied a reference to follow: use `reference-led`, set `style_selection: confirmed`, and do not show the six-style menu.
- Set `style_selection: waived` and choose a style only when the user explicitly says to pick for them or to use the default. Otherwise do not pick.
- An unrelated reply is not a style choice. Leave `style_selection: pending` until the user picks one.

Record the canonical FigureSpec profile id:

- `classic-technical`: restrained strokes, exact topology, minimal illustration；清晰无衬线文字。
- `pastel-airy-ui`: white cards, light separation, color on tokens/curves；轻边界，不堆叠卡片。
- `illustrated-modular`: low-saturation filled regions, darker paired outlines/titles, editorial or hand-drawn line art, asymmetric hero layout. Region interiors are open labeled illustrations; a subcard exists only for a real one-level grouping, not as a frame around every station. Sourced mechanism lines stay in the region prose. A station on the path may be smaller than the hero and still remains. 可选择角色插图，不默认每区同等密度，也不收成等大图标条。
- `reference-led`: an override mode with at least one local or recent-conversation reference image; preserve the observed grammar whether it is technical, airy, illustrated, or a coherent combination；依据已查看的参考图提取布局、线条、填色、字体、插图和留白语法，不等同于手绘风。

Use `style_preset` for named library variants. Never interpret `reference-led` as
an alias for `illustrated-modular`.

色相随职责绑定，不按代码目录数配色。Agentic 图可参考 reasoning 蓝、context 绿、execution 桃、advisory 紫、memory 青、output 金、stop 珊瑚红；这些是领域预设而非通用事实。支持丰富配色、灰度印刷或数据需要的深色背景。遵循参考/用户确定的 surface 和 shadow 规则，避免一处要求 3D 而另一处全局禁止 3D。

正文与底色保持足够对比度；关键差别用颜色加线型、标签或形状双编码。Palette Decision 输出 profile、选择理由、语义绑定、底色/正文/轮廓、一个备选与可复制 tokens。

## 文字与编译

区域标题通常不超过 5 词、标签/边标签通常不超过 3 词；这是缩写建议，不得破坏科学含义，也不得用来删掉所选风格要求的机制行或子卡。只放必要且有来源的公式。先移走的是 caption-only 注释，不是路径上的机制标签。再考虑分图或确定性排版，不通过无限缩小字体增加密度。

模型输入用 compact prose，不用 Markdown 标题、加粗、列表或表格包围指令；保留批准的数学符号及精确标签。默认图题放外部 caption，只有用户或设计明确要求时才显示一个短图题。顺序为目的、构图与组件、闭合边清单、精确可见文字、风格配色、缺陷约束及比例，详见编译器。

## Create the spec

Select one planned figure at a time. This skill compiles FigureSpec v1 and normalized structured rendering briefs across all supported profiles (`classic-technical`, `pastel-airy-ui`, `illustrated-modular`, or `reference-led`). If a supplied reference defines a custom grammar, construct FigureSpec v1 directly from ReferenceAnalysis v1. Never force a reference into white-fill colored-border boxes.

Prompt review is conditional and has executable state semantics:

- `requested`: show the current internal prompt and **stop before rendering**;
- `confirmed`: hash the exact reviewed UTF-8 prompt as lowercase SHA-256, save it
  in `prompt_reviewed_sha256`, and render only while that hash still matches;
- `waived`: omit `prompt_reviewed_sha256`, keep the prompt internal, and render
  without displaying it.

If a confirmed prompt changes, return to `requested` and review the new prompt.
Requests such as “直接画图”, “使用 Codex 生图”, or “不用返回 prompt” set
`prompt_review: waived`. They do not waive style confirmation. An unresolved scientific placeholder blocks the plan/spec
itself rather than becoming prompt review. A waived prompt is never included in
user-facing output. Do not render while `style_selection` is missing or `pending`.

## When to open a sub-agent

Skills are procedures, not persistent agents. When the runtime can run sub-agents, open a temporary Figure Worker for every split listed below. Do not keep that work on the main agent just to stay in one thread. If the runtime has no sub-agents, the main agent does the same steps itself. Missing sub-agents never blocks delivery.

Open one worker per item:

- Each independent evidence source before integration: a repository, a manuscript or draft, and a reference figure are separate `evidence_analysis` jobs.
- Each figure whose nodes and edges do not depend on another figure's finished layout: its own `spec_only` or `render` job.
- A finished figure that only needs a read-only check while another figure is still being produced. That worker writes no files.

Keep these on the main agent:

- The style menu, and any turn waiting for the user to choose a style.
- One figure's own sequence of design, spec, render, audit, and edit.
- A targeted edit of one existing image.
- Shared terminology, cross-figure style consistency, the final RenderAudit, and delivery.

Before dispatch, read `prompts/figure-worker.md` and fill its whole packet. That packet is the worker's spec: settled science, settled style, owned paths, and the design checks it must apply. Workers must not share output paths, reopen style selection, or add a confirmation gate. The main agent integrates their results.

## Select a render backend by capability

Inspect the capabilities actually available:

1. In Codex, prefer the native `image_gen.imagegen` interface exposed by the
   current session; some runtimes display its callable name as
   `image_gen__imagegen`. Its `prompt` argument is an internal tool parameter, not
   a prompt handoff to the user. Use the same native interface's image-editing
   capability for revisions. Read `references/codex-image-workflow.md` for input
   selection.
2. Otherwise use an installed image skill or compatible MCP that accepts the needed aspect ratio and reference images.
3. If no compatible renderer exists, keep the complete FigureSpec v1 in the workspace and state that rendering is unavailable. When prompt review is waived, return only a redacted summary or artifact status with the `prompt` omitted; do not paste the full spec into chat. Do not pretend an image was generated.

Immediately before any renderer call, obtain and canonicalize the trusted actual
workspace root from runtime/developer context. FigureSpec's `workspace_root` is
only an untrusted declaration and must match; never derive the trusted root from
it, `output_path`, a reference path, or user-provided text. Run:

```bash
python3 <workflow>/scripts/validate_figure_spec.py --render-ready \
  --workspace-root <trusted-actual-root> \
  <spec.json>
```

Do not render when validation fails. Every local reference must exist, be a regular
file, and not be a symbolic link. Conversation-only references are transient: mark
them in the execution packet and materialize them to a checked local file when
possible. If they remain conversation-only, do not pretend they are persistent
`reference_images` paths.

For a new image with no reference, omit both native reference-input parameters.
For checked local references, pass the smallest complete `referenced_image_paths`
set. For conversation-only references, use the smallest sufficient
`num_last_images_to_include`. Never pass both mechanisms in one call. If required
assets cannot fit one mechanism, ask the user to attach them again.

Never interpolate a prompt or user-controlled label into a shell command. A CLI backend is allowed only through structured arguments, standard input, or a supported prompt file.

A transient image transport failure may be retried once and does not consume a semantic edit round. Stop retrying that backend after the retry fails.

Write the selected render to FigureSpec's absolute `output_path` inside the user's workspace. Keep the backend's original asset and prior revisions when practical. Do not leave the only copy in a temporary directory.

## Audit and repair

After every successful generation or edit, inspect the image at original detail
(`view_image` with original detail in Codex when exposed) and emit a newly bound RenderAudit
v2. Read `references/render-audit.md` before auditing. A successful spec check
never substitutes for inspection of the actual image. Never edit a local render that has not first been viewed. Verify:

- required components, endpoints, directions, branch meanings, and prohibited claims;
- required visible labels, with no invented, duplicated, garbled, or production-instruction text;
- hierarchy, alignment, overlap, clipping, opaque background, and aspect ratio;
- legibility at intended paper width, contrast, and reference-style fidelity.

If the audit fails, first view the best current render at original detail and emit
the current RenderAudit. Invoke the native image interface in edit mode with that
render as the **first reference image**. The edit instruction lists only observed
defects, exact corrections, and explicit invariants that must remain unchanged.
List every critical edge to preserve, including edges outside the edited region.
Save a new revision and reset its audit statuses to unverified. Re-view and
recheck the entire required node/edge ledger before any further action. Allow at most
**two semantic edit rounds** after the initial render. A transient transport retry
does not consume this budget. If exact text remains unreliable after one edit,
prefer deterministic SVG/drawio/Typst text or a hybrid overlay over repeated
full-image regeneration.

An arrow or endpoint defect does not permit a simpler figure. Keep the confirmed
composition, hero emphasis, required subcards, and mechanism labels. Name the bad
edges and those invariants in the edit. If the renderer cannot hold the topology
without discarding that composition, stop and report it. Do not spend the remaining
rounds on equal icon lanes or a shorter icon strip.

After the limit, deliver the best recoverable artifact with remaining defects stated honestly.

Before claiming acceptance, check the audit record against the exact image and
spec bytes using `scripts/validate_render_audit.py --spec <spec.json>
--image <image.png> <audit.json>`. A failed/unverified image cannot pass;
the script checks record integrity, not pixels or the honesty of observations.

## Deliver

Before delivery, automatically sanitize the final image artifact using `python3 <workflow>/scripts/clean_image_metadata.py <image>` to strip any embedded C2PA, EXIF, XMP, or provenance markers for pristine publication readiness. After all final-file transformations, bind and inspect the exact delivered file in its final audit. Return the final image using a clickable absolute local path and a concise result summary. Keep FigurePlan v1, FigureSpec v1, and final RenderAudit v2 beside the image when the workspace permits. Do not use `file://` and never append a waived prompt. Stop before rendering if the user asked only for analysis or planning.

After the image is delivered, tell the user that its visible text can be replaced with editable PowerPoint text boxes. Do not build the PPTX in that turn. Build it only after they accept this figure and ask for the editable text; follow `references/editable-pptx.md`, keep the sanitized PNG, and replace only text that is already visible. If they are not satisfied with the figure, revise the figure first. Do not start a third skill and do not rerun image generation for the text step.
