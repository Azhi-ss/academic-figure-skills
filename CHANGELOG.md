# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.0] - 2026-10-01

### Changed

- 第一次出图前必须确认风格。用户未点名风格、也没有要跟随的参考图时，workflow 展示 `references/previews/` 中的 6 张预览并停下；「直接画图」只把 `prompt_review` 设为 `waived`，不代替选风格。
- FigureSpec 增加 `style_selection`（`pending` / `confirmed` / `waived`）。`--render-ready` 拒绝缺字段或 `pending`；`confirmed` 需要非空 `style_preset`，或 `reference-led` 且已有参考图。
- 版本：包 4.1.0，workflow 2.1.0。
- 运行时支持子 agent 时，独立的来源分析、独立的图、以及已完成图的只读复核都要开 worker。每个 worker 的任务包就是它的 spec：已定的科学内容和风格，加上必须按顺序执行的设计检查。风格菜单、单图顺序步骤和最终交付仍留在主 agent。
- 箭头画错时不得改用等大图标条来换端点。这条对所有风格生效，不限于手绘模块风。语义修改必须保住已确认的构图、主区、嵌套层和机制标签；保不住就停下来报告。图计划的「最短」只禁止臆造模块，执行路径上的次要站仍要留下。字数建议不能拿来删掉风格要求的机制行。
- 手绘模块风的区内默认是开放线稿和有来源的机制行，只给真实的一层分组加子卡。编译不得把每个站点收成等大图标；审核把这种图判为风格不符。

## [4.0.0] - 2026-10-01

### Changed

- 5 个 skill 合并为 2 个：
  - `academic-repo-analyzer`、`academic-figure-draft-analyzer`、`academic-figure-architecture-extractor` → `academic-figure-analyzer`（`references/repo.md`、`paper.md`、`reference-figure.md`）
  - `academic-figure-designer` → `academic-figure-workflow`
- 交接格式（SemanticArchitecture@1、FigurePlan@1、ReferenceAnalysis@1、FigureSpec@1、RenderAudit@2）与校验行为不变。
- benchmark 脚本移到仓库根 `scripts/`（`fetch_benchmark_repos.py`、`run_repo_benchmarks.py`、`create_sparse_fixture.py`）。
- 版本：包 4.0.0，workflow 2.0.0，analyzer 1.0.0。
- 从 3.x 升级：

```bash
npx skills remove --global academic-figure-designer academic-repo-analyzer academic-figure-draft-analyzer academic-figure-architecture-extractor
npx skills add Azhi-ss/academic-figure-skills -g --all
```

### Removed

- 删除 `scripts/sync_shared_refs.py` 与跨 skill 的重复副本（风格、色板、审计、缺信息政策改为各自 skill 目录内的唯一副本）。

## [3.3.0] - 2026-10-01

### Added

- workflow 自带由 designer 同步的 `figure-spec.schema.json`、`scripts/validate_figure_spec.py` 与 `scripts/clean_image_metadata.py`，单独安装时 SKILL.md 中的校验与清理命令可直接运行。
- `test_clean_image_metadata.py` 改为 unittest，纳入 `unittest discover`；新增 PNG 文本元数据剥离断言。

### Changed

- FigureSpec 校验器直接读取 `figure-spec.schema.json`（标准库 schema 子集解释器），删除与 schema 重复的手写字段检查；字段形状诊断统一为 `schema.<keyword>`，跨字段、引用与 render-ready 检查不变。
- 移除 legacy 兼容模式与 style profile 别名：未版本化 spec 与 `modern-technical-vector` 等别名直接报错；`--strict-v1` 保留为无操作参数以兼容旧调用。
- `strip_image_metadata()` 返回 `(original_bytes, cleaned_bytes)`，删除恒为 `True` 的 success 位；删除无效的 `--recursive` 参数（目录始终递归）。
- `sync_shared_refs.py` 改为数据驱动的同步计划，删除符号链接防护、原子写入与 Unicode 文件名碰撞检查；`palettes.md` 只同步到 designer 与 workflow。
- `validate_skill_pack.py` 复用 FigureSpec 报告类型与 manifest 解析，改为校验 `docs/prompts/*.spec.json`；legacy benchmark `prompt-spec.json` 不再参与校验。
- 技能版本：designer 2.3.0、workflow 1.8.0、repo-analyzer 1.5.1、draft-analyzer 1.4.1、architecture-extractor 1.3.1；FigureSpec@1 格式不变。

### Fixed

- 示例 `pastel_airy_ui_agentic_bo.spec.json` 的非法 `layout.composition` 与 `authority_boundaries` 形状（示例 spec 此前从未被校验）。
- `modern-technical-vector` 同时是 schema 枚举值和别名的矛盾；README profile 表改用 canonical id `classic-technical`。
- 可信工作区根无法解析时，render-ready 校验不再抛出 `UnboundLocalError`。

### Removed

- `docs/prompts/*.txt`（与 `.spec.json` 的 `prompt` 字段重复）、根目录 `scripts/clean_image_metadata.py`、`docs/codex-image-workflow.md`（workflow 内副本为唯一来源）、`examples/classic-repos/`（并入 `examples/benchmarks/README.md`），以及三个未使用的 `references/palettes.md` 副本。

## [3.2.0] - 2026-09-10

### Added

- 在现有 designer 中加入 construct / diagnose / revise 三个 prompt 模式及明确停止点；prompt-only 不调用 renderer，也不虚构运行路径。
- 提示词设计参考、完整构造/修订模板和本地反馈衍生案例；区分真实用户需求、合成回归场景与尚未验证的历史图片。
- RenderAudit@2：image/spec 原始字节 SHA-256 绑定、独立 spec-validation/image-inspection 状态、完整节点与逐边证据。
- stdlib 审核记录校验器与回归测试：缺边、过期摘要、伪造整体 PASS、未验证项和语义字段不匹配无法通过。程序验证记录而非图像像素。

### Changed

- 移除强制每节点“图标 + 小图 + 公式卡”和固定容器比例；依据科学角色选择必要视觉锚点。
- 将颜色丰富度、内容密度、排版层级分别处理；多 agent 讨论须有真实消息交互证据。
- 明确在科学骨架确认后、布局定稿前融入风格；同步 designer、编译器、模板与 figure worker，复用已选风格并保留仅换风格时的科学约束，不新增确认关卡。
- 局部图像编辑显式保留关键边，并对整张新图重新审核；不沿用上一版的 PASS。
- 统一编译器、模板、workflow 和共享执行/审核文档；FigureSpec@1 保持兼容。designer 2.2.0、workflow 1.7.0。
- 采用 Nuwa 主题提炼方法辅助整理开发经验；交付技能无 Nuwa 运行时依赖。

## [3.1.0] - 2026-08-27

### Added

- Direct Codex `image_gen.imagegen` generation and reference-image editing before compatible skill/MCP fallbacks; internal prompts are not returned when review is waived.
- Reference-aware article, DOI, arXiv, PDF, and figure routing; architecture extraction now records transferable style grammar separately from source-paper content.
- Versioned `FigurePlan@1`, `FigureSpec@1`, `ReferenceAnalysis@1`, and `RenderAudit@1` handoffs.
- Post-generation original-detail inspection with the best current render as the first edit reference, at most two defect-driven targeted edits, preserved revisions, and stable absolute workspace output paths.
- Three canonical surface profiles (`classic-technical`, `pastel-airy-ui`, `illustrated-modular`) plus a separate `reference-led` override mode.
- A formal FigureSpec schema and standard-library validator covering evidence sources, semantic safeguards, connection direction, canonical style profiles, local or recent-conversation references, prompt-review state/hash, trusted-workspace render readiness, symlink-safe references, and workspace-contained outputs.
- Shared-reference synchronization and pack-level validation for frontmatter, manifest versions, style-library copies, and legacy-spec migration warnings.

### Changed

- Replaced mandatory plan/style/prompt gates with conditional review. Explicit direct-generation requests waive prompt review while retaining semantic and render audits.
- Removed module-count-driven palette selection from the workflow; reference grammar, production constraints, and semantic roles now drive visual decisions.
- Prompt transport must use structured tool arguments, standard input, or prompt files rather than shell interpolation.
- Reclassified the legacy real-repository benchmark as a structural/keyword smoke test; it is not evidence of semantic accuracy, render quality, or reference fidelity.
- Reclassified named style files into surface, composition, color/material, accessibility, and print layers; removed venue/domain-to-palette shortcuts and content-inventing decoration defaults.
- Consolidated `academic-figure-prompt-pastel` into the unified `academic-figure-prompt` (v2.0.0) covering all canonical styles (`classic-technical`, `pastel-airy-ui`, `illustrated-modular`, and `reference-led`).
- Standardized all image prompt outputs into **Strict Prose Normalization (Zero Markdown Syntax)** to completely eliminate markdown symbols and floating title banners leaking into diffusion image renders.
- Synchronized published skill metadata: workflow 1.5.0, repo analyzer 1.4.0, paper analyzer 1.3.0, architecture extractor 1.3.0, color expert 1.4.0, unified prompt engine 2.0.0.


## 3.0.0

- Workflow redesigned as conversational figure assistant: two mandatory confirmation gates (Figure Plan → prompt) before image generation.
- Phase 3 image generation: calls `gpt-image-generation` skill (cpa-gpt-image-2) or sensenova MCP when available; falls back to delivering the structured prompt when no image model is reachable.
- Workflow version 1.3.0 → 1.4.0; pack version 2.9.0 → 3.0.0.

## 2.9.0

- Real-repo benchmarks: six public repository clones plus the sparse fixture.
- Vendored `references/` in all skills, fixing broken `../docs/` links after install.
- Generalized repo-analyzer coverage for AI4Science and research code.
- Wired `module_count` and `aspect_ratio` end to end.
- Fixed example and schema drift.

## [2.8.0] - 2026-07-25

### Added
- 🛠 **architecture-extractor**: real `scripts/extract_pdf_figures.py` (pdfimages / PyMuPDF / optional pdftoppm) + size filter report
- 📘 **examples/**: aligned with Palette Decision handoff + JSON figure spec default
- 🗺 **docs/palettes.md**: scene→style family→palette decision guide (figure type / venue / domain / vibe recipes + checklist)


### Changed
- 🧹 **Skill rewrite (writing-great-skills pass)**: slim all 7 `SKILL.md` files; steps + checkable completion criteria; progressive disclosure of reference
- 🎨 **Palette SSOT**: single source of truth in `docs/palettes.md` (12 presets); removed duplicated hex tables from prompt / paper-analyzer / architecture-extractor / color-expert body
- 📐 **academic-figure-prompt**: schema/examples moved to `json-schema.md`; Text Budget + JSON-default kept in skill body
- 🔍 **academic-repo-analyzer**: keyword tables moved to `keywords.md`
- 🧭 **Defaults aligned**: ≥ 4 modules → Nature Blue; else Okabe-Ito (workflow, color-expert, prompt agree)
- 🧾 **architecture-extractor**: removed unverifiable performance claims (≥92%, ≤10s/PDF); scoped as agent-driven analysis with honest tool gaps
- 📝 **Descriptions**: shorter model-facing descriptions; leading words front-loaded
- 📚 **Shared policy**: `docs/missing-info-policy.md` for sparse-input handling
- 🔢 **Pack**: 2.7.0 → 2.8.0; skill versions bumped

### Fixed
- 🐛 Palette count inconsistency across README / color-expert / prompt (9 vs 10 vs 12 vs 13)
- 🐛 README badge version lag (2.5.0 vs manifest)

## [2.7.0] - 2026-05-11

### Changed
- 🔄 **academic-figure-prompt v1.3.0**: JSON spec is now the **default output format** — all framework/architecture/flowchart/module/comparison figures output JSON by default
- 🔄 **academic-figure-prompt**: Old text prompt template demoted to "备选" (fallback, simple scenes only)
- 🔄 **academic-figure-prompt**: Title changed from "学术论文配图提示词生成器" to "学术论文配图 JSON 规范生成器"
- 🔄 **academic-figure-workflow**: Routing updated to reflect JSON-first output
- 🔢 **Pack**: 2.6.0 → 2.7.0

## [2.6.0] - 2026-05-11

### Added
- 📐 **academic-figure-prompt**: JSON Structured Figure Spec output format — `exact_text_to_render`, `relative_position`, `layout_and_content_blocks`, label hierarchy, and `RENDERING_RULES` patterns for precise layout/text control
- 📝 **academic-figure-prompt**: Text Budget principle — per-element word limits (≤5 for titles, ≤3 for labels, ≤2 for pipeline steps) preventing cluttered figures
- 🏷️ **academic-figure-prompt**: Label Hierarchy (Primary/Secondary/Caption) — formulas and parameters go to figure captions, not on-figure
- 🎨 **academic-figure-color-expert**: Nature Blue / Deep Blue Monochrome scheme (#1B3A5C → #2E6B9E → #5BA0D0 → #8EAEC4) — field-validated for 4+ module framework diagrams
- 🎨 **academic-figure-color-expert**: Monochrome vs Polychrome philosophy section — when to use single-hue vs multi-hue

### Changed
- 🔄 **academic-figure-prompt**: Quality checklist rebalanced — "text restraint" replaces "max information density"; "caption separation" replaces "no simplification"
- 🔄 **academic-figure-prompt**: Core philosophy changed from "max information density at all costs" to "labels on figure, details in caption"
- 🔢 **academic-figure-prompt**: v1.1.0 → v1.2.0
- 🔢 **academic-figure-color-expert**: v1.1.0 → v1.2.0

### Fixed
- 🐛 Real-world validation: verbose descriptions in figure specs produce unreadable cluttered output — now prevented by Text Budget + exact_text_to_render pattern

## [2.5.0] - 2026-04-15

### Added
- ✨ **New Skill**: `academic-figure-architecture-extractor` - Extract and analyze architecture diagrams from PDFs, filter invalid images, analyze diagram structure, auto-match color schemes
- 🎨 **Color Schemes**: Added 3 new palettes (12 total):
  - Grayscale Print Friendly - IEEE-recommended, 100% black-and-white compatible
  - Nature/Science Standard - Official top-journal style
  - Biomaterials Cross-Disciplinary - For materials science + AI intersection
- 📚 **Documentation**: Added architecture extraction workflow to README
- 🔧 **Gitignore**: Added `.codex` to ignore list

### Changed
- 🔄 **Workflow**: Updated `academic-figure-workflow` to support architecture extraction stage
- 📝 **README**: Removed eval-team section, added architecture extractor usage examples
- 🔢 **Versioning**: Bumped pack version to `2.5.0`

### Removed
- ❌ **Deprecated**: `academic-skill-eval-team` (per user request)

## [2.4.0] - 2026-04-11

### Added
- **New Skill**: `academic-skill-eval-team` - Multi-agent evaluation team for reviewing a single skill or the whole skill pack before release
- **README**: Added usage entry for skill evaluation workflow

### Changed
- **Versioning**: Bumped pack version in `manifest.json` and `README.md` to `2.4.0`

## [2.3.1] - 2026-04-09

### Added
- 📚 **Documentation**: Added `CONTRIBUTING.md` - Complete contributing guide
- 📚 **Documentation**: Added `docs/academic-references.md` - Academic references and citations
- 📚 **Documentation**: Added `docs/best-practices.md` - 2024-2025 top conference best practices
- 📚 **Examples**: Added `examples/` directory with 4 complete end-to-end workflow examples
  - `01-repo-analyzer-example.md` - Repo analyzer output example
  - `02-paper-analyzer-example.md` - Paper analyzer output example
  - `03-figure-prompt-example.md` - Figure prompt output example
  - `04-end-to-end-workflow.md` - Complete conversation workflow

### Fixed
- 🔧 **Consistency**: Unified copyright holder in LICENSE (Azhi-ss)
- 🔧 **Consistency**: Fixed academic-figure-prompt version in manifest.json (1.0.0 → 1.1.0)
- 🔧 **Documentation**: Updated manifest.json description to reflect 9 palettes

## [2.3.0] - 2026-04-09

### Added
- ✨ **New Skill**: `academic-repo-analyzer` - Analyze ML/DL code repositories to understand what they do, identify model architecture, core algorithms, tech stack, and key innovations. Generates a "quick understanding document" that can be passed to paper-analyzer.
- 📚 **Documentation**: Added example architecture diagram in README
- 🔗 **Workflow**: Complete end-to-end workflow from repo analysis → figure planning → color selection → prompt generation

### Enhanced
- 🎨 **Color Expert**: Extended domain coverage (physics, chemistry, economics, life sciences)
- 📝 **Figure Prompt**: Added quick-start mode with default Okabe-Ito palette
- 🔄 **Paper Analyzer**: Updated to support 9 color schemes and extended domains

### Fixed
- 🔧 **Consistency**: Unified version numbers across all files
- 🔧 **Color Schemes**: Standardized to 9 palettes across all skills
- 🔧 **Manifest**: Fixed repository URL and author information

## [2.2.0] - 2026-04-09

### Added
- 🎨 **New Skill**: `academic-figure-color-expert` - Academic color palette expert with 9 preset schemes plus colorblind-safe design principles
- 📝 **New Skill**: `academic-figure-paper-analyzer` - Analyze academic papers to plan which figures to generate
- 🌈 **Color Schemes**: 9 preset palettes (Okabe-Ito, Blue Monochrome, Warm Earth, Purple-Green, Grayscale, Teal-Coral, ML TopConf Tab10, ML TopConf Colorblind, ML TopConf Deep)

### Enhanced
- 🎯 **Figure Prompt**: Expanded from 8 to 9 color schemes
- 📚 **README**: Complete rewrite with quick-start guide and usage examples

## [2.1.0] - 2026-04-09

### Added
- ✨ **New Skill**: `academic-figure-prompt-pastel` - Modern ML/RL paper-style figures matching ICLR/NeurIPS/ICML 2024-2025 aesthetics
- 🎨 **Pastel Style**: Pure white canvas, white panels with soft shadow, rounded fonts, pastel token squares, pill-shaped labels

### Enhanced
- 📝 **Figure Prompt**: Added cross-reference to pastel style
- 🔗 **Workflow**: Added pastel style as alternative to classic style

## [2.0.0] - 2026-04-09

### Added
- 🚀 **Initial Release**: Complete skill pack for academic figure generation
- ✨ **Core Skill**: `academic-figure-prompt` - Classic style (Okabe-Ito / Nature / CVPR) prompt generation
- 📚 **Documentation**: Full README with installation and usage instructions
- 🔧 **Manifest**: Complete skill registration with trigger phrases

## [1.0.0] - 2026-04-08

### Added
- 🌱 **Prototype**: Initial concept and single skill implementation
