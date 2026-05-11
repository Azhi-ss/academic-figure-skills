---
id: academic-figure-prompt
name: Academic Figure Prompt
version: 1.2.0
description: Use this skill whenever the user wants detailed English prompts for AI image tools to produce top-conference-quality academic figures, needs prompts for framework diagrams, architecture diagrams, pipeline flowcharts, module detail diagrams, comparison figures, or data-pattern grids. Now also supports JSON structured figure specs for precise layout/text control. Trigger: "论文配图提示词", "生成论文配图", "学术论文生图", "架构图提示词", "框架图提示词", "顶会风格配图", "CVPR 风格图", "NeurIPS 风格图", "paper figure prompt", "academic diagram prompt", "fig JSON spec".
stages: [writing, research, review]
tools: [bash]
---

# Academic Figure Prompt — 学术论文配图提示词生成器

为学术论文生成**极其详细的英文提示词**，供 AI 图片生成工具（NanoBanana / Gemini / Midjourney / DALL-E）生成顶会级别的专业学术配图。

## 核心理念

生成的提示词必须做到三点：**文字克制**、**视觉风格精确**、**关键信息不遗漏**。

**图上只放短标签和结构，公式、参数、长描述放到 Figure Caption。** 实践反复验证：图上文字越多越杂乱，越少越专业。宁可提示词把布局和视觉写得极其精确，也绝不能让图上塞满段落文字。

### 文字预算原则 (Text Budget)

| 元素 | 字数上限 | 示例 |
|------|---------|------|
| 模块标题 | ≤ 5 词 | `HCEA: Hierarchical Co-Evolutionary Architecture` |
| 子组件标签 | ≤ 3 词 | `P_A Explorers` / `EGD Crossover` |
| Pipeline 步骤 | ≤ 2 词 primary + ≤ 2 词 secondary | `Diffuse` + `(forward noise)` |
| 公式标注 | 只保留核心公式，≤ 1 行 | `D = 0.6·Jaccard + 0.4·USR` |
| 箭头标签 | ≤ 3 词 | `Migration / 10 gen` |

### 标签层级 (Label Hierarchy)

图上文字分两级：
- **Primary（大号/显眼）**：模块名、步骤名、关键操作。用户扫一眼必须看懂的。
- **Secondary（小号/可选/可省略）**：方法名、参数范围、补充说明。空间不够时优先砍掉。
- **Caption（不放图上）**：完整公式推导、超参数列表、边界条件说明。这些属于论文图注。

## Input Contract

- **优先输入**：图类型、论文/章节内容、方法或模块描述、必要标签、公式、维度、配色方案、参考图
- **最低可用输入**：至少提供图类型 + 主题/方法概述；其余缺失时允许以占位约束继续
- **缺失处理**：核心内容不足时生成骨架级 prompt，并明确哪些细节是占位项、哪些是推断

## Output Contract

始终输出一个 `Prompt Package`，至少包含：

- 中文图名
- 适用图类型
- 最终英文 image prompt
- 使用的配色方案或默认决定
- 简短中文说明
- 明确列出的假设或待确认项

## 工作流程

### Step 1: 理解论文内容

在生成提示词之前，**必须**先充分理解论文内容：

1. 阅读用户提供的论文/章节源文件（LaTeX、Word、PDF 等）
2. 提取每个章节的核心概念、方法、模型架构、数据流
3. 识别所有需要配图的位置及其内容需求
4. 理解论文中的数学符号、变量含义、维度信息

### Step 2: 分析参考图（如有）

如果用户提供了参考图，**必须**详细分析：

| 分析维度 | 提取内容 |
|---------|---------|
| **配色方案** | 主色、辅色、强调色的精确色值（如 #3A8F85） |
| **布局结构** | 流向（左→右 / 上→下）、分区方式、层次关系 |
| **模块样式** | 框的形状、边框粗细、填充色、圆角大小 |
| **标注方式** | 标题栏样式、公式标注、维度标注、箭头类型 |
| **信息密度** | 每个模块内的子细节数量、嵌入缩略图的使用方式 |
| **特殊元素** | 反馈环路、虚线框、跳接箭头、图例位置 |

### Step 2.5: 配色方案选择（快速默认模式可用）

**如果用户没有明确指定配色，不要静默锁定为单一方案。先按以下顺序决策：**

1. 若能从用户上下文识别 `venue` / 学科 / 图类型，优先给出“场景推荐方案 + 1 个备选方案”
2. 若上下文不足以判断，再明确告知“当前先使用默认 Okabe-Ito 继续生成”
3. 始终说明：后续可随时切换到其他预设或自定义色值

---

**快速继续（显式默认）：**

> ✅ 如果你暂时不想选配色，我会先用默认 **Okabe-Ito** 继续生成；如果你想要更现代 / 更柔和 / 更期刊风 / 更像 ML 顶会，也可以随时切换。

**场景推荐示例：**
- `NeurIPS / ICML / ICLR` → `ML TopConf Colorblind` / `ML TopConf Tab10`
- `Nature / Science / CVPR` → `Okabe-Ito`
- `材料科学 / 化学 / 多模块框架图` → `Nature Blue`（单色相，最不易杂乱）
- `HCI / CHI` → `Teal-Coral`
- `生物 / 医学` → `Warm Earth` / `Okabe-Ito`

**或者查看全部 10 套预设配色方案：**

| # | 方案名 | 风格定位 | 主色 | 辅色 | 点缀色 |
|---|--------|----------|------|------|--------|
| A | Okabe-Ito 学术标准⭐ | Nature / Science / CVPR 推荐，色盲友好 | Steel Blue `#0072B2` | Warm Orange `#E69F00` | Bluish Green `#009E73` |
| B | Blue 单色系 | 克制、模块详解图适用 | Navy `#1565C0` | Medium Blue `#42A5F5` | Light Blue `#90CAF9` |
| C | Warm Earth | 生物学、医学影像 | Brick Red `#C0392B` | Burnt Orange `#E67E22` | Amber `#F39C12` |
| D | Purple-Green | 数据可视化、IEEE 期刊 | Deep Purple `#6A1B9A` | Forest Green `#2E7D32` | Medium Purple `#AB47BC` |
| E | Grayscale | 仅黑白打印 | Near-black `#212121` | Medium Gray `#616161` | Light Gray `#9E9E9E` |
| F | Teal-Coral | HCI / CHI 现代感 | Dark Teal `#00695C` | Coral `#E64A19` | Medium Teal `#26A69A` |
| G | ML TopConf Tab10 | Matplotlib 默认，熟悉感强 | tab:blue `#1F77B4` | tab:orange `#FF7F0E` | tab:green `#2CA02C` |
| H | ML TopConf Colorblind | Seaborn 色盲友好 | `#0173B2` | `#DE8F05` | `#029E73` |
| I | ML TopConf Deep | Seaborn Deep，柔和稳定，适合多面板密集布局 | `#4C72B0` | `#DD8452` | `#55A868` |
| J | **Nature Blue** ⭐ 新增 | 单色相渐变，4+ 模块框架图首选，视觉最统一 | Navy `#1B3A5C` | Medium Blue `#2E6B9E` | Light Blue `#5BA0D0` |

**额外入口：自定义配色**

如需自定义配色，可直接提供主色/辅色/点缀色 hex 值，或从下方工具选取。

**如需自定义配色，推荐以下工具：**

- **Coolors** — 随机生成 + 锁定调整，导出色板：https://coolors.co
- **ColorHunt** — 精选高质量色板，支持标签筛选：https://colorhunt.co
- **Adobe Color** — 色轮 + 互补/类比/三分配色生成：https://color.adobe.com/create
- **ColorBrewer** — 专为学术数据可视化设计，支持色盲安全验证：https://colorbrewer2.org
- **Viz Palette** — 专为数据可视化配色，实时模拟色盲效果：https://projects.susielu.com/viz-palette
- **Paletton** — 色相环驱动配色方案设计器：https://paletton.com

> 提示：选好颜色后，直接把主色/辅色/点缀色的 hex 值告诉我即可（如 `主色 #2E7D32，辅色 #C49A00`）。

---

**若用户明确表示想先比较或确认配色，则展示方案并等待确认；否则不因配色缺失而中断，按“用户指定 → 场景推荐 → 默认安全方案”的顺序继续进入 Step 3。**

如果用户已在初始请求中明确指定了配色（如"用蓝绿配色"、"参考我的参考图"），则直接进入 Step 3。

### Step 2.75: 缺信息处理分支

**总原则：** 信息不足时，优先输出“保守但有用”的阶段性结果，而不是停止任务或假装已经掌握全部细节；任何超出已知证据的内容，都必须明确标注为“推断”或“待确认”，必要时改写为占位约束。

#### 情况 1：只有图类型，没有论文内容
- 先生成通用骨架级提示词，覆盖布局、模块关系、标注方式、风格规格
- 将具体模块名、公式、维度、输入输出内容写为可替换占位项
- 明确标注：`当前提示词为通用结构草案，具体内容需结合论文细节补全`

#### 情况 2：只有标题、摘要或局部章节
- 仅基于已有材料提取高置信信息生成提示词
- 对模块细节、公式、维度、实验面板数量采用保守表述
- 不要臆造未出现的子模块、损失函数或实验结果

#### 情况 3：用户没有指定配色
- 先尝试从 `venue`、学科、图类型、参考图中推断最合适的方案
- 若能判断场景，则给出 `场景推荐方案 + 1 个备选方案`
- 若仍无法判断，则明确标注：`当前先使用默认 Okabe-Ito，可后续切换为其他方案`
- 不因缺少配色而停止生成

#### 情况 4：用户没有给参考图，但要求“参考某风格”
- 可以依据用户提到的 venue / 风格关键词生成近似风格约束
- 如果缺少明确视觉参考，则以本 skill 的标准学术风格模板为主
- 不要虚构参考图中的具体元素

#### 情况 5：用户需求很模糊
- 先收缩为最可能的图类型（如 Overall Framework / Module Detail）
- 输出内容应分为：已确认元素、待确认元素、建议补充信息
- 如果连图类型都无法判断，则先给 1 个最稳妥的框架图提示词草案，而不是展开多张假设性图片

### Step 3: 生成提示词

按照下方的「提示词结构模板」为每张图生成提示词。

---

## 提示词结构模板

每个提示词必须包含以下 **四个层次**，缺一不可：

### 层次 1: 全局描述（Global Description）

开头一段话，概括整张图的类型、主题和整体布局。

```
A highly detailed, information-dense academic paper [类型] diagram in the style of
top-tier [目标会议] publications. The diagram illustrates [主题概述], arranged as
[布局描述: e.g., "a rich multi-stage left-to-right pipeline with multiple parallel
pathways, embedded thumbnail visualizations, and dense annotations"].
```

**类型词汇表：**
- architecture / framework / pipeline / flowchart / comparison / ablation
- network architecture / module detail / data flow / system overview

### 层次 2: 分区详细描述（Section-by-Section Description）

用 `=== SECTION NAME ===` 格式分隔每个区域。每个区域内部必须包含：

| 元素 | 要求 | 示例 |
|------|------|------|
| **背景面板** | 极浅色填充 + 色值 | `very faint grey #F7F7F7 background panel` |
| **节标签** | small-caps 文字 + 细灰分割线 | `small-caps Steel Blue label "ENCODER"` |
| **模块框** | 白色填充 + 彩色/灰色边框 | `white rounded-rectangle box with Steel Blue border` |
| **子结构** | 每个模块内部的组件 | `containing three parallel branches...` |
| **嵌入缩略图** | 模块内的小型单色可视化 | `a small monochrome FFT spectrum bar chart thumbnail` |
| **公式标注** | LaTeX 风格公式 | `with formula "HT = 1/(1 + d/d₀)"` |
| **维度标注** | 张量/向量维度 | `labeled "X ∈ R^(120×6)"` |
| **连接箭头** | 箭头类型和标签 | `thin arrow labeled "30-step predicted trajectory"` |

**关键原则：每个模块框内部都必须有子内容。不允许出现空白占位框。**

### 层次 3: 全局标注（Global Annotations）

- 维度标注沿主要箭头：`"R^(120×6)", "R^(30×6)", "R^14", "R^5"`
- 反馈环路（如有）：`dashed feedback arrow from output back to input`
- 图例（如有）：`legend box in bottom-right corner`
- 跨区域连接：`skip connection dashed arrow from Stage 1 to Stage 3`

### 层次 4: 风格规格（Style Specifications）

每个提示词末尾必须附加完整的风格描述，将选定方案的色值填入。

---

## 配色方案色值表

用户在 Step 2.5 中选定方案后，从下方取对应色值填入提示词末尾的 STYLE SPECIFICATIONS。

### 方案 A: Okabe-Ito 学术标准（默认）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Steel Blue `#0072B2` | 核心模块边框、节标签、主箭头 |
| secondary | Warm Orange `#E69F00` | 次要模块边框、替代高亮 |
| tertiary | Bluish Green `#009E73` | 输出/结果模块（极少量） |
| text | Charcoal `#333333` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Faint Grey `#F7F7F7` | 大区域分组 |
| border | Light Grey `#CCCCCC` | 普通框体（1px） |
| arrow | Dark Grey `#4D4D4D` | 连接线 |

### 方案 B: Blue Monochrome（蓝色单色系）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Deep Blue `#1565C0` | 核心模块边框 |
| secondary | Light Blue `#42A5F5` | 次要模块边框 |
| tertiary | Pale Blue `#90CAF9` | 辅助元素 |
| text | Near-black `#212121` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Very Pale Blue `#F5F8FC` | 大区域分组 |
| border | Blue-gray `#B0BEC5` | 普通框体 |
| arrow | Dark Blue-gray `#37474F` | 连接线 |

### 方案 C: Warm Earth（暖土色系）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Brick Red `#C0392B` | 核心模块边框 |
| secondary | Burnt Orange `#E67E22` | 次要模块边框 |
| tertiary | Amber `#F39C12` | 输出/结果 |
| text | Charcoal `#2C2C2C` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Warm Cream `#FDF6EC` | 大区域分组 |
| border | Sand `#D5C5A1` | 普通框体 |
| arrow | Brown `#5D4037` | 连接线 |

### 方案 D: Purple-Green（紫绿互补）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Deep Purple `#6A1B9A` | 核心模块边框 |
| secondary | Forest Green `#2E7D32` | 次要模块边框 |
| tertiary | Medium Purple `#AB47BC` | 第三类元素 |
| text | Near-black `#1A1A1A` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Lavender tint `#F8F5FC` | 大区域分组 |
| border | Light Purple `#CE93D8` | 普通框体 |
| arrow | Dark Purple `#4A148C` | 连接线 |

### 方案 E: Grayscale（纯灰度）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Near-black `#212121` | 核心模块边框 |
| secondary | Medium Gray `#616161` | 次要模块边框 |
| tertiary | Light Gray `#9E9E9E` | 辅助元素 |
| text | Black `#111111` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Off-white `#F5F5F5` | 大区域分组 |
| border | Silver `#BDBDBD` | 普通框体 |
| arrow | Dark Gray `#424242` | 连接线 |

### 方案 F: Teal-Coral（青蓝珊瑚）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | Dark Teal `#00695C` | 核心模块边框 |
| secondary | Coral `#E64A19` | 次要模块边框 |
| tertiary | Medium Teal `#26A69A` | 输出/结果 |
| text | Near-black `#212121` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | Pale Teal tint `#F0F9F8` | 大区域分组 |
| border | Light Teal `#80CBC4` | 普通框体 |
| arrow | Very Dark Teal `#004D40` | 连接线 |

### 方案 G: ML TopConf Tab10（Matplotlib 默认）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | tab:blue `#1F77B4` | 核心模块边框 |
| secondary | tab:orange `#FF7F0E` | 次要模块边框 |
| tertiary | tab:green `#2CA02C` | 输出/结果 |
| text | slate-800 `#1F2937` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | slate-50 `#F8FAFC` | 大区域分组 |
| border | slate-300 `#CBD5E1` | 普通框体 |
| arrow | slate-700 `#334155` | 连接线 |

### 方案 H: ML TopConf Colorblind（Seaborn 色盲友好）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | `#0173B2` | 核心模块边框 |
| secondary | `#DE8F05` | 次要模块边框 |
| tertiary | `#029E73` | 输出/结果 |
| text | `#1F2937` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | `#F8FAFC` | 大区域分组 |
| border | `#CBD5E1` | 普通框体 |
| arrow | `#334155` | 连接线 |

### 方案 I: ML TopConf Deep（Seaborn Deep · 柔和）

| 元素 | 色值 | 用途 |
|------|------|------|
| primary | `#4C72B0` | 核心模块边框 |
| secondary | `#DD8452` | 次要模块边框 |
| tertiary | `#55A868` | 输出/结果 |
| text | `#1F2937` | 所有标签 |
| fill | Pure White `#FFFFFF` | 所有内容框 |
| section_bg | `#F8FAFC` | 大区域分组 |
| border | `#CBD5E1` | 普通框体 |
| arrow | `#334155` | 连接线 |

### 额外入口：用户自定义

从参考图中提取，或使用调色工具选定色值后，按如下格式告知：

```
主色：#XXXXXX（核心模块边框/节标签）
辅色：#XXXXXX（次要模块/强调）
点缀色：#XXXXXX（输出结果，可选）
背景：#XXXXXX（区域分组背景，建议极浅）
文字：#XXXXXX（建议深色）
```

---

## 配色禁忌（避免 AI 生图感）

| 禁止做法 | 替代做法 |
|---------|---------|
| 4-5 种彩色背景面板 | 白色为主 + 极浅灰分组 |
| 高饱和度 Header Banner Bar | 小号 small-caps 文字标签 + 灰色分割线 |
| 每个模块不同颜色填充 | 纯白填充 + 仅边框用色 |
| 彩色缩略图 | 单色灰度或仅用 2 色 |
| 5+ 种颜色同时出现 | 最多 3 种色彩 + 灰色系 |
| 彩虹/渐变效果 | 纯色、扁平、无渐变 |

---

## 图片类型专用模板

### 类型 1: 总体框架图（Overall Framework）

```
结构: [输入] → [阶段1] → [阶段2] → ... → [输出]
要求:
- 各阶段用 small-caps 文字标签 + 细灰色分割线（不用彩色背景面板）
- 核心模块用主色边框，次要模块用辅色边框，普通模块用 Grey 边框
- 所有模块白色填充，无彩色填充
- 阶段间箭头标注数据维度和含义
- 每个阶段内展示 2-4 个子模块，子模块内嵌入单色缩略图
- 底部或顶部添加反馈/跳接连接（灰色虚线）
```

### 类型 2: 网络架构图（Network Architecture）

```
结构: [输入层] → [编码器堆叠] → [核心模块（并行分支）] → [输出头]
要求:
- 并行分支用不同边框色区分，内部均为白色填充
- 每个分支内标注操作名称 + 单色缩略图
- 残差连接用灰色虚线弧形箭头
- 维度标注在每层转换处（灰色小字）
- 重复层用 "×N" 灰色虚线框标识
```

### 类型 3: 模块详解图（Module Detail）

```
结构: [输入] → [操作1] → [中间表示] → [操作2] → [输出]
要求:
- 每步操作用白色独立框，关键操作用主色边框，次要用 Grey 边框
- 中间表示用单色灰度缩略图可视化（频谱图、热力图等）
- 跳接/残差连接用灰色虚线
- 公式标注在对应操作框旁（灰色小字）
```

### 类型 4: 对比/消融图（Comparison / Ablation）

```
结构: N 列并排，每列一个变体
要求:
- 共享的基础结构用相同灰色边框
- 差异部分用主色或辅色边框高亮 + 灰色虚线框标出
- 每列顶部标注变体名称（small-caps）
- 底部可添加性能指标对比条（仅用主色 + 辅色 + Grey）
```

### 类型 5: 数据/行为模板图（Data / Behavior Patterns）

```
结构: 1×N 网格，每格一个类别
要求:
- 每格为白色框 + 细灰色边框，顶部标签用主色小字
- 格内嵌入该类别的单色/双色典型可视化（轨迹、波形等）
- 用主色 / 辅色区分正面/负面类别（如有对比语义）
- 关键特征用文字标签
- 底部共享坐标轴（如有）
```

---

## 缩略图词汇表（Thumbnail Vocabulary）

| 数据类型 | 缩略图描述 |
|---------|-----------|
| 时间序列 | `a small time-series waveform thumbnail` |
| 频率谱 | `a small frequency spectrum bar chart thumbnail` |
| 注意力图 | `a small monochrome attention heatmap grid thumbnail` |
| 轨迹 | `a small 3D orbital trajectory curve thumbnail` |
| 概率分布 | `a small probability distribution bar chart thumbnail` |
| 决策树 | `a small decision tree branching diagram thumbnail` |
| 混淆矩阵 | `a small confusion matrix heatmap thumbnail` |
| 网络节点 | `a small neural network layer diagram thumbnail` |
| 特征向量 | `a small horizontal feature vector bar visualization` |
| 散点图 | `a small scatter plot with cluster coloring thumbnail` |
| 感受野 | `a progressively larger receptive field grid icon` |
| 卷积核 | `a small convolution filter kernel grid thumbnail` |
| 梯度流 | `a small gradient flow direction arrow diagram` |
| 损失曲线 | `a small training loss convergence curve thumbnail` |
| ROC 曲线 | `a small ROC curve with AUC shading thumbnail` |
| 图像样本 | `a small example image/photo thumbnail` |
| 点云 | `a small 3D point cloud visualization thumbnail` |
| 热力图 | `a small spatial heatmap overlay thumbnail` |

---

## 质量检查清单

生成每个提示词后，对照以下清单自检：

- [ ] **文字克制**：每个标签 ≤ 5 词，公式 ≤ 1 行。没有段落文字出现在图上。
- [ ] **标签层级**：Primary 标签突出，Secondary 标签收窄/可省略。Details 留给 caption。
- [ ] **色彩克制**：仅使用 2-3 种色彩，无多余颜色
- [ ] **白色主导**：≥70% 面积为白色/近白色，无彩色背景面板
- [ ] **边框而非填充**：模块用白色填充 + 彩色/灰色细边框，而非彩色填充
- [ ] **分区方式**：用 small-caps 文字标签 + 灰色分割线，不用彩色 banner bar
- [ ] **维度标注**：主要数据流箭头上标注了维度（如 R^(N×D)），但不过度
- [ ] **公式精简**：仅核心公式留在图上（≤ 1 行），完整推导在图注中
- [ ] **缩略图嵌入**：关键模块内嵌入了单色/双色缩略可视化
- [ ] **完整性**：论文中所有核心组件都在图中体现，无遗漏
- [ ] **连接清晰**：并行路径、残差连接、反馈环路都有明确描述
- [ ] **风格规格**：末尾包含完整的 STYLE SPECIFICATIONS 段落（含色值约束和禁止项）
- [ ] **Caption 分离**：详细公式、参数列表、边界条件留给 Figure Caption，不堆在图上
- [ ] **灰度测试**：描述确保图片在黑白打印时仍可完整阅读

---

## JSON 结构化配图规范 (推荐替代纯文本 Prompt)

当用户需要精确控制画面布局、文字位置和渲染规则时，输出以下 JSON 格式。**实践表明：JSON 结构化 spec 比纯英文 prompt 生成的图更可控、更干净。**

### JSON 顶层结构

```json
{
  "diagram_type": "图表类型标签",
  "diagram_title_rendering": "None",
  "style_and_colors": { ... },
  "layout_and_content_blocks": [ ... ],
  "RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": [ ... ]
}
```

### `layout_and_content_blocks` 核心模式

每个 block 描述图上一个区域，关键字段：

| 字段 | 用途 | 示例 |
|------|------|------|
| `relative_position` | 画面中的相对位置 | `"Top Left"`, `"Mid-Right"` |
| `shape` | 框的形状、颜色、边框样式、填充 | `"Dark Navy Blue (#1B3A5C) 2px dashed border, white fill"` |
| `exact_title_to_render_inside` | 模块标题 — 图上就渲染这几个词 | `"HCEA: Hierarchical Co-Evolutionary Architecture"` |
| `exact_label` | 组件标签 — 精确到词 | `"Input"` |
| `exact_text` | 任何显示文字 | `"MMPolymer Transformer\nPredicts Tg & Dk"` |
| `exact_floating_text` | 浮在箭头旁、图标旁的小字 | `"Valid linear polymer"` |
| `secondary_note` | 二级小字，空间不够时可省略 | `"(ETKDGv3)"` |
| `icon` | 图标描述（始终单色灰阶线稿） | `"Compass icon, thin Dark Navy Blue line art"` |
| `flow` | 该 block 后的箭头方向、颜色、样式 | `"Horizontal arrow pointing RIGHT to CFM container"` |
| `failure_branch` / `success_branch` | 条件分支 | fail: red arrow to trash; pass: green arrow to next |
| `branch_yes` / `branch_no` | Diamond 决策节点分支 | yes: → output; no: dashed loop back |
| `internal_content.layout` | 内部布局描述 | `"Three equal-width vertical columns"` |

### 文字精确控制原则（最重要）

- 所有显示在画面上的文字，必须通过 `exact_*` 字段锁定，**不允许生成工具自行编造文字**
- 主标签 `exact_label` 用 ≤ 2 词，`secondary_note` 用 ≤ 2 词（字号减半）
- 完整公式、参数列表通过 `caption_note` 标记为"放图注"，**不在图上渲染**
- 所有 `exact_text` 中可以用 `\n` 断行，但每行 ≤ 5 词

### Pipeline 标签层级示例

```json
{
  "step_1": {
    "icon": "SMILES text string icon",
    "exact_label": "Input",
    "secondary_note": "SMILES"
  },
  "step_2": {
    "icon": "2D → 3D molecular transform icon",
    "exact_label": "Embed",
    "secondary_note": "ETKDGv3"
  }
}
```

> 生成工具看到 `exact_label: "Input"` 就在图标下渲染 "Input"，看到 `secondary_note: "SMILES"` 就在下面用小字渲染 "SMILES"。没有 `description` 字段给生成工具自由发挥。

### RENDERING_RULES 范式

```json
"RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": [
  "NEVER render JSON keys, field names, or underscores as visible text.",
  "Render text ONLY within designated exact_* fields.",
  "All container boxes use WHITE (#FFFFFF) fill with COLORED BORDERS ONLY.",
  "Icons are monochrome thin grey line art. No colored icons.",
  "Feedback loop arrows are DASHED. Main forward flow arrows are SOLID.",
  "No gradients, no 3D effects, no shadows. Flat vector style throughout.",
  "Canvas is pure white (#FFFFFF). No background tint, no watermark."
]
```

### 完整 JSON 示例（精简版总体框架图）

```json
{
  "diagram_type": "Scientific Closed-Loop System Architecture",
  "diagram_title_rendering": "None",
  "style_and_colors": {
    "background": "White (#FFFFFF)",
    "main_block_color_palette": {
      "Module_A": "Dark Navy Blue (#1B3A5C) dashed border, white fill",
      "Module_B": "Medium Blue (#2E6B9E) dashed border, white fill",
      "Aux_block": "Steel Gray (#8EAEC4) thin solid border, white fill"
    },
    "flow_arrow_colors": {
      "main_forward_flow": "Dark Grey (#4D4D4D) straight arrows",
      "feedback_loop": "Dark Grey (#4D4D4D) dashed curved arrow"
    }
  },
  "layout_and_content_blocks": [
    {
      "relative_position": "Top Left",
      "shape": "Rounded rectangular box, Light Blue thin border, white fill",
      "exact_text_to_render": "BRICS Fragment Library\n→ Initial Population",
      "flow": "Horizontal arrow pointing RIGHT to Main Module"
    },
    {
      "relative_position": "Top Center",
      "shape": "Large rectangular container, Dark Navy Blue 2px dashed border, white fill",
      "exact_title_to_render_inside": "Module A: Name",
      "internal_content": {
        "layout": "Three equal-width vertical columns",
        "column_1": { "exact_header": "Sub-A", "icon": "compass icon", "exact_text_below_icon": "Operation" }
      },
      "flow": "Horizontal arrow pointing RIGHT to Module B"
    }
  ],
  "RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": [
    "NEVER render JSON keys as visible text.",
    "All boxes use WHITE fill with COLORED BORDERS only."
  ]
}
```

### 何时用 JSON 格式 vs 纯文本 Prompt

| 场景 | 推荐格式 |
|------|---------|
| 框架图、架构图（模块多、流程复杂） | JSON spec |
| 需要精确控制每个位置的文字 | JSON spec |
| 需要反复迭代调优 | JSON spec |
| 简单示意图（≤ 3 个模块） | 纯文本 prompt |
| 数据图、热力图、曲线图 | 纯文本 prompt |
| 用户明确要求 "给我一段 prompt" | 纯文本 prompt |

---

## 输出格式

每个提示词用 markdown 代码块包裹：

### 适用 JSON Spec 时

```markdown
### 图 X.Y — [中文图名]

适用类型：[框架图/架构图/模块图/对比图]
配色方案：[已选方案名]
推荐分辨率：[宽高比]

#### 信息完整度说明
- **已分析材料**：[论文、摘要、章节、参考图]
- **当前输出类型**：JSON 结构化配图规范
- **配色来源**：用户指定 / 场景推荐 / 默认方案
- **Caption 预留**：[应该放到图注中的公式、参数、边界条件]
- **待确认信息**：[需要用户核实的模块名、公式、布局]

​```json
[JSON 结构化配图规范]
​```
```

### 适用纯文本 Prompt 时

```markdown
### 图 X.Y — [中文图名]

适用类型：[框架图/架构图/模块图/对比图]
配色方案：[已选方案名]
推荐分辨率：[建议的宽高比，如 16:9, 3:2]

#### 信息完整度说明
- **已分析材料**：[论文、摘要、章节、参考图、用户明确要求]
- **当前输出类型**：完整提示词 / 阶段性提示词 / 通用骨架提示词
- **配色来源**：用户指定 / 场景推荐 / 默认安全方案
- **高置信信息**：[已明确出现的模块、流程、术语、配色或风格要求]
- **待确认信息**：[公式、维度、具体模块命名、实验面板数量等]
- **Caption 预留**：[应该移到图注的内容]

​```
[完整英文提示词]
​```
```

---

## 注意事项

1. **提示词语言**：提示词本身必须为英文，说明文字用中文
2. **长度不限**：宁长勿短，信息密度是第一优先级
3. **领域自适应**：根据论文领域（CV、NLP、Robotics、医学等）调整缩略图和图标选择
4. **参考图优先**：如果用户提供了参考图，配色和布局以参考图为准，覆盖预设方案
5. **批量生成**：当用户要求为整篇论文生成配图时，按章节组织，并给出优先级建议
