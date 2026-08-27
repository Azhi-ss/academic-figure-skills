# 学术配图设计与生成实践

本文提供可操作的设计检查项，而不是把某个会议、年份或单张参考图的风格当作普遍规则。优先级始终是：用户明确要求 → 参考图视觉语法 → 内容语义与可读性 → 投稿方明确的生产规范。venue/domain 名称本身不决定风格或颜色。

---

## 目录

1. [先确定读者要理解什么](#先确定读者要理解什么)
2. [参考图驱动的视觉语法](#参考图驱动的视觉语法)
3. [三类常用风格 profile](#三类常用风格-profile)
4. [信息密度与文字预算](#信息密度与文字预算)
5. [语义色区与可访问性](#语义色区与可访问性)
6. [布局、嵌套与连线](#布局嵌套与连线)
7. [字体、图标与插画](#字体图标与插画)
8. [给生图模型的提示词结构](#给生图模型的提示词结构)
9. [生成后的校验与修订](#生成后的校验与修订)

---

## 先确定读者要理解什么

在画框之前，先用一句话回答：读者看完图后应该能复述什么？

常见目标包括：

- 系统从输入到输出如何工作
- 核心机制如何循环、决策或更新
- 哪些边界是确定性的，哪些部分是建议性或可选的
- 多个模块如何共享状态、证据或记忆
- 与基线相比，真正新增了什么

把内容分为三层：

1. **主叙事**：缩略图尺寸下仍能读懂的结构与方向。
2. **辅助解释**：放大后帮助理解的短标签、图标和局部关系。
3. **Caption reserve**：公式展开、参数、条件、实现细节和长句。

如果一项内容不影响图的主叙事，也不需要视觉定位，就放入 caption，而不是继续缩小字体。

---

## 参考图驱动的视觉语法

用户提供参考图时，先分析下列可观察属性，再选 profile 和颜色：

| 维度 | 需要记录的问题 |
|---|---|
| 构图 | 线性、径向、非对称拼图、hero-plus-support，还是其他结构？ |
| 表面 | 白卡片、柔彩色区、无框分组，还是混合？ |
| 边框 | 细线、强描边、虚线、同色系深描边，还是中性灰？ |
| 阴影 | 无阴影、极弱分层阴影，还是明显卡片阴影？ |
| 层级 | 最大视觉区在哪里？辅助区如何围绕它组织？ |
| 嵌套 | 是否存在子卡片？最多几层？ |
| 字体 | 技术无衬线、圆润几何、手绘标题，还是混合层级？ |
| 图标 | 单色线稿、彩色线稿、微型图表、插画角色，还是几何符号？ |
| 连线 | 主流、反馈、可选、异常和引用边分别怎样编码？ |
| 色彩 | 每个色区的浅填充、深描边、标题和图标是否成对？ |

匹配的是这些视觉原则，不复制参考图的标签、品牌资产、专有插画或方法内容。若参考同时含有经典平面线条、柔彩填充和手绘插图，应如实描述这种组合，不要强行二分为 classic 或 pastel。

---

## 三类常用风格 profile

### 1. Classic technical

适合紧凑网络结构、模块细节、严格打印或用户明确要求的技术框图。

- 白色或近白模块可用，但不是所有学术图的默认要求
- 边框较细，几何对齐明确
- 字体以可读性和紧凑性优先
- 颜色主要用于类别、状态或重点，不按模块顺序轮换

### 2. Pastel airy UI

适合 token flow、界面式概念关系和用户明确要求的空气感卡片图。

- 白色卡片、轻边框或克制阴影
- 较多留白，floating token、pill、dot 和轻量曲线
- 通常少嵌套；空白不需要靠公式和图标填满
- 重点是轻盈界面感，不等同于所有“现代 ML 图”

### 3. Illustrated modular

适合叙事型总体框架、多智能体系统、科学工作流和带手绘信息图语法的参考图。

- 白画布上使用低饱和语义色区
- 色区采用 1.5–2.5px 的同色系深描边，通常不加阴影
- 一个 hero 区承担核心机制，约占画面 35–55%；辅助区按重要性分配面积
- 允许一层子卡片表达真实父子结构，避免多层 box-in-box
- 标题可有受控的手绘感，正文保持高可读无衬线
- 线稿插图可以使用色区 accent，不必全部灰色
- 避免等宽泳道和一排完全相同的企业卡片

profile 是起点，不是禁令。参考图或用户要求可以组合其中的表面、线条、字体和图标属性，只要组合有明确来源且视觉一致。

---

## 信息密度与文字预算

密度由内容和最终版面决定，不用固定的 8–12px 间距或“每个框必须有子内容”衡量。

### 建议预算

| 元素 | 建议 |
|---|---|
| 主色区标题 | 2–5 个词 |
| 子卡片标题 | 1–4 个词 |
| 箭头标签 | 1–3 个词，仅在语义不明显时添加 |
| 正文行 | 一个短语；说明性长句移入 caption |
| 公式 | 仅当公式本身是视觉主题或不可替代的一行不变量 |
| 维度 | 仅标在读者需要比较 tensor/shape 变化的边上 |
| 图标 | 有助于快速识别时使用，不设覆盖率指标 |

### 删除顺序

空间不足时，按以下顺序减负：

1. 重复图标与装饰性缩略图
2. 次要说明和可从箭头方向推断的标签
3. 参数、形状细节和公式展开
4. 非关键 legend 项

保留主标题、核心机制、关键分支和权限/状态边界。不要通过把正文压到不可读的小字号来维持内容数量。

---

## 语义色区与可访问性

颜色应绑定稳定角色，而不是“第一个模块蓝、第二个模块橙、第三个模块绿”。同一论文中重复角色保持同色。

### 成对 token

柔彩色区不要只给一个 fill 值。每个区域至少定义：

```yaml
semantic_zone:
  soft_fill: "#......"
  dark_outline: "#......"
  title_text: "#......"
  icon_accent: "#......"
```

`docs/palettes.md` 的 I1 token 给出了可直接使用的蓝、绿、桃、紫、青、金和珊瑚配对。Agentic-science 图中可按实际内容映射 reasoning/planning、evidence/context、deterministic execution、advisory/uncertainty、memory/provenance/recovery、output/report 和 exception/stop；没有出现的角色不必占色。

### 颜色数量

不设置基于 module count 的单色开关，也不设置普遍适用的三色上限：

- 一个连续层级可以用单色明度梯度
- 多个需要快速扫描的子系统可以使用多组低饱和成对 token
- 重复角色应复用已有 token，而不是为每个框创建新颜色
- 特别重要的异常色应稀疏使用

### 可访问性检查

- 普通小字与实际背景以 4.5:1 对比度为目标
- 淡色只作为 fill，不直接作为小字颜色
- 颜色之外再使用标签、形状、线型、图标或位置编码
- 检查灰度预览；关键分支不能只靠红/绿差异
- 若用户或 venue 有更严格规范，以该规范为准

---

## 布局、嵌套与连线

### 先分配视觉权重

在列举所有模块之前，先确定：

- hero 机制或核心循环
- 输入、约束和证据从哪里进入
- 输出、报告或持久化状态在哪里结束
- 哪些组件是辅助、可选或异常路径
- 哪些边必须避开正文和其他连线

### 可选构图

| 叙事 | 可考虑的构图 |
|---|---|
| 顺序处理 | 左到右或上到下 pipeline |
| 迭代优化 | 中央 loop、径向步骤或回环主轴 |
| 多子系统协作 | 非对称 hero-plus-support 拼图 |
| 前后对比 | 两列或镜像布局 |
| 层级内部结构 | 主容器加一层 subcard |
| 多个可比实验 | 对齐网格与共享 legend |

不要把所有 Overall Framework 都自动画成四个等宽白框。

### 嵌套

一层嵌套可以表达真实的 ownership、作用域或内部阶段。第二层以上通常会压缩文字和增加边框噪声；若确实必要，考虑拆成 detail figure。

### 连线语法

先定义边的含义再决定样式，例如：

- 主前向流：实线箭头
- 反馈/更新：弧形或回环箭头
- 可选/建议：虚线
- 异常/停止：不同形状、线型和稀疏 accent
- 持久化写入：指向明确的数据载体或边界

legend 只解释无法从标签和形状直接理解的编码。避免箭头穿过文字、在框边中途失去端点或形成无意义交叉。

---

## 字体、图标与插画

### 字体层级

| Profile | 标题 | 正文 |
|---|---|---|
| Classic technical | Helvetica/Arial/Inter 或 venue 字体 | 同一无衬线家族 |
| Pastel airy UI | Nunito/Poppins/Quicksand 等圆润几何字体 | 清晰无衬线 |
| Illustrated modular | 受控的圆润手绘式 display heading | Inter/Arial/Nunito 等高可读正文 |

在目标单栏或双栏宽度检查最终字号。字体规范应按导出尺寸统一，不要在同一 prompt 中混用互相矛盾的 pt/px 层级。

### 图标与插画

- 技术组件可使用单色微型图或几何符号
- 叙事型框架可以使用受控彩色线稿、人物/机器人式角色、书本、数据库、代码、仪器或对话气泡
- 避免直接使用平台 emoji glyph；它们的字形和渲染不稳定
- 插画应帮助识别角色或动作，而不是为了达到“每个框一个图标”的配额
- 同一图内保持线宽、圆角和细节级别一致

---

## 给生图模型的提示词结构

### 1. 全局与参考语法

先声明图片类型、论文主题、profile 和参考图语法：

```text
Academic framework illustration for [subject]. Preserve the supplied reference's
asymmetric hero-plus-support composition, tinted semantic zones, strong same-hue
outlines, hand-drawn line icons, and no-shadow surface treatment. Reuse visual
grammar only; do not copy labels or branded assets.
```

### 2. 布局与视觉优先级

明确 hero 区的位置和占比、辅助区的关系、输入输出位置、需要留出的箭头通道。空间关系比机械罗列 Box A/Box B 更重要。

### 3. 分区内容

```text
=== ZONE: [name] ===
Position and relative size: [...]
Paired colors: fill [...], outline [...], title [...], icon [...]
Exact short labels: [...]
Internal structure: [none | one level of subcards]
Connections: [...]
```

### 4. 风格规格

说明画布、描边、阴影、字体层级、paired tokens、图标风格、目标版面宽度和宽高比。对 illustrated modular 明确 `strong outline, no drop shadow`；对 airy UI 才使用克制卡片阴影。

### 5. 有针对性的负面约束

优先使用正向描述。负面约束只覆盖高概率错误，例如：

- no extra or duplicated labels
- no equal-card corporate dashboard layout
- no photorealism or glossy 3D chrome
- no unintended gradients
- no emoji glyphs
- no deeper than one-level nested subcards

### 参考图输入

生图后端支持 reference image / image-to-image 时，应直接传入参考图，而不只把它压缩成文字描述。引用视觉语法不意味着复制其方法内容。

### 文字可靠性

生成模型不等于排版引擎。文字较多或必须逐字正确时，优先考虑：

1. 先生成少文字的构图与插画
2. 在 SVG、Typst、Figma、Inkscape 或其他可编辑工具中叠加文本和连线
3. 或在每轮生成后做 OCR 对照并局部修订

---

## 生成后的校验与修订

### 内容正确性

- [ ] 每个可见标签与 approved label list 一致
- [ ] 没有多余、重复、乱码或拼错的词
- [ ] 模块、分支和箭头方向与真实系统一致
- [ ] 可选、反馈、异常和持久化边没有被画成同一种关系

### 视觉语法

- [ ] profile 与参考图分析一致
- [ ] hero 区确实承担核心机制，而不是仅仅更大
- [ ] airy UI 与 illustrated modular 没有被误混为同一种白卡片风格
- [ ] illustrated modular 使用柔彩色区、强同色描边、无阴影和最多一层 subcard
- [ ] 色区使用成对 fill/outline/title/icon token

### 可读性与可访问性

- [ ] 缩放到目标单栏/双栏宽度后正文仍可读
- [ ] 小字与实际背景对比度合格
- [ ] 灰度预览仍能区分关键类别和边
- [ ] 箭头没有穿过文字、丢失端点或形成无法解释的交叉
- [ ] 背景、透明通道和裁切符合投稿要求

### 定向修订

每轮只修最影响阅读的一组问题，并锁定已经正确的部分。例如：

```text
Keep the current composition and all approved labels unchanged. Replace the three
equal white cards with softly tinted semantic zones using the supplied paired
tokens; strengthen same-hue outlines; remove drop shadows; preserve arrow routes.
```

重复检查，直到内容、构图、文字和可访问性同时通过。生成成功只是开始，不是 publication-ready 的判定条件。
