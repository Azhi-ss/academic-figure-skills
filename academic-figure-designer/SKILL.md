---
name: academic-figure-designer
description: Design evidence-grounded academic figures and construct, diagnose, or revise scientific image prompts. Use for figure layout, semantic palettes, reference-led styles, prompt engineering, information-density feedback, and FigureSpec v1 compilation.
metadata:
  version: "2.2.0"
  stages: [writing, research, review]
---

# Academic Figure Designer and Prompt Engine

将科学内容编译成可验收的图示。这里是唯一的设计与 prompt 编译入口；不把提示词修辞当作第二次科学设计。

## 按请求选择输出

| 用户意图 | 行动与停止点 |
|---|---|
| 构造画图提示词 / 只写 prompt | construct：设计简报与完整 prompt；不生图 |
| 检查或诊断已有 prompt | diagnose：定位问题、影响与最小修正；不擅改文件或生图 |
| 按反馈修改 prompt | revise：改动、保留项及完整新 prompt；不自动生图 |
| 制作图 / 修改图片 | construct 或 revise 后交给 workflow 渲染、目检 |
| 只咨询配色或风格 | Palette Decision；不要求完整拓扑，不生图 |

只问方案时不启动绘图。直接画图时不强加 prompt 确认；按用户的 review 偏好执行。

## 按需读取

- 构造、诊断或修订决策 → `references/prompt-design-logic.md`
- 编译 renderer prompt → `references/json-to-prompt.md`
- 可直接填充的构造/修订样板 → `references/prompt-templates.md`
- 密度、布局、文字或风格细节 → `references/image-prompt-guide.md`
- 案例与迁移检验 → `references/prompt-design-cases.md`
- 实际渲染的结构契约 → `json-schema.md` 和 `figure-spec.schema.json`
- 视觉锚点 → `references/architecture-icons.md`，仅使用符合证据的元素
- 色彩与可选风格库 → `references/palettes.md`、`references/styles/`
- 证据不足 → `references/missing-info-policy.md`
- 图片验收 → `references/render-audit.md`

## 设计流程

1. 写出读者问题及图的核心答案，区分主内容、支撑内容、caption-only。
2. 从上游分析或用户输入提取稳定 component IDs、typed connections、权限边界、禁止关系及证据。不从参考图借算法，不把缺失证据填成确定事实。
3. 在科学骨架明确后、布局定稿前确定风格。复用用户已选风格；有参考图时先查看并提取视觉语法，无参考时选择适合内容的 profile。风格参与后续构图，不作为写完 prompt 后追加的装饰句；详见 `references/prompt-design-logic.md`。
4. 联合科学含义与所选风格设计阅读顺序、主区、语义分组、连线通道及必要视觉锚点。只有真实层级需要时才嵌套；比例是构图辅助。图标、小图、公式卡、机器人或气泡均可选，纯标签节点合法。
5. 锁定可见文字、语义颜色与非颜色编码，检查所选风格下的文字容量与可读性；编译前闭合全部边。修订先写 Delta 与 Invariants，颜色修改不改变科学拓扑。
6. 将内容、布局与风格统一编译为完整的紧凑自然语言，而非给旧 prompt 叠加风格补丁。prompt-only 在此交付；渲染任务再补齐、校验 FigureSpec 并移交执行。

用户直接描述架构时跳过不必要的仓库扫描。将其记为 `sources` 中的 `user_instruction`，证据为原请求；component IDs 使用稳定 snake_case。执行、建议、反馈、存储和异常连接分开，不靠位置推断连线。

## 风格与语义配色

保留四个 canonical `style_profile`：

- `classic-technical`：技术线图、精确拓扑、克制色彩、清晰无衬线文字。
- `pastel-airy-ui`：轻边界与白色卡片，颜色主要落在 token、曲线和重点，不堆叠卡片。
- `illustrated-modular`：有色语义分区、成对浅底/深轮廓、可选择手绘线稿和角色插图；不默认每区同等密度。
- `reference-led`：依据已查看的参考图提取布局、线条、填色、字体、插图和留白语法；不等同于手绘风。

色相随职责绑定，不按代码目录数配色。Agentic 图可参考 reasoning 蓝、context 绿、execution 桃、advisory 紫、memory 青、output 金、stop 珊瑚红；这些是领域预设而非通用事实。支持丰富配色、灰度印刷或数据需要的深色背景。遵循参考/用户确定的 surface 和 shadow 规则，避免一处要求 3D 而另一处全局禁止 3D。

正文与底色保持足够对比度；关键差别用颜色加线型、标签或形状双编码。Palette Decision 输出 profile、选择理由、语义绑定、底色/正文/轮廓、一个备选与可复制 tokens。

## 文字与编译

区域标题通常不超过 5 词、标签/边标签通常不超过 3 词；这是缩写建议，不得破坏科学含义。只放必要且有来源的公式。先移走次要文本，再考虑分图或确定性排版，不通过无限缩小字体增加密度。

模型输入用 compact prose，不用 Markdown 标题、加粗、列表或表格包围指令；保留批准的数学符号及精确标签。默认图题放外部 caption，只有用户或设计明确要求时才显示一个短图题。顺序为目的、构图与组件、闭合边清单、精确可见文字、风格配色、缺陷约束及比例，详见编译器。

## 渲染交接与验证

实际渲染使用 `academic-figure/FigureSpec@1`，保持现有 schema 兼容。所有边有正确端点，`visible_text` 闭合；参考、输出路径与 workspace_root 均来自真实运行环境。prompt-only 不需要编造渲染环境。

渲染前立即执行（脚本路径按实际安装位置解析）：

```bash
python3 <designer>/scripts/validate_figure_spec.py --strict-v1 --render-ready \
  --workspace-root <trusted-actual-root> <spec.json>
```

`prompt_review: requested` 展示并停下；`confirmed` 必须匹配已审核 prompt 的 SHA-256，改变后重新请求审核；`waived` 内部传参且不在回答中贴出。校验失败不调用 renderer。

交给 `academic-figure-workflow` 使用当前可用的原生图片工具；每次图片编辑前先看基线图，之后保存新版本并重新逐节点、逐边目检。FigureSpec PASS 不代表图片 PASS。只有 prompt 的产物不宣称已经通过图片验收。
