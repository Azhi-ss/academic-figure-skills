---
id: academic-figure-prompt-pastel
name: Academic Figure Prompt — Modern ML Airy Style
version: 4.0.0
description: Generate prompts for AI image tools to produce modern ML/RL paper-style figures matching the aesthetic of recent ICLR/NeurIPS/ICML 2024-2025 publications. Key traits — pure white canvas, white panels with soft drop shadow, rounded friendly font (Nunito/Poppins), densely packed but uncluttered floating elements, small pastel token squares, rich inline illustrations, colored keyword text, pill-shaped concept labels. Trigger phrases — "pastel风格论文配图", "现代ML论文配图", "modern ML figure prompt".
stages: [writing, research, review]
tools: [bash]
---

# Academic Figure Prompt — Modern ML Airy Style v4

为学术论文生成**极其详细的英文提示词**，产出的图片风格对标近年 ICLR / NeurIPS / ICML 顶会中常见的**现代柔彩风格**。

---

## ⚠️ 核心风格规则（经 7 轮迭代验证）

### 规则 1：纯白画布 + 白色面板 + 微弱阴影

```
画布（canvas）= 纯白 #FFFFFF，无渐变、无灰度、无暖色调
面板（panel）= 白色 #FFFFFF 圆角矩形 + 极微弱的 soft drop-shadow
          (3px blur, 1px y-offset, rgba(0,0,0,0.06))
区分方式 = 仅靠阴影浮起，不靠灰色填充或边框
```

> ❌ 不要用灰色 `#F5F5F5` 填充面板  
> ❌ 不要用渐变画布背景  
> ✅ 面板是白色，浮在白色画布上，靠阴影区分

### 规则 2：圆角友好字体

```
字体 = 圆角几何无衬线体（Nunito / Poppins / Quicksand / Comfortaa）
特征 = 字母末端圆润，手感友好温暖，不是锐利的 Helvetica/Arial
标题 = semi-bold ~ bold (600-700)，~16-18pt
正文 = regular (400)，~10-11pt
公式 = italic serif (Computer Modern / STIX)
```

> 字体是区分这种风格与传统论文图的核心特征之一

### 规则 3：排满但不拥挤

```
每个面板 = 充满内容（token、曲线、公式、图标、箭头）
元素间距 = 8-12px 微间距，不留大面积空白
整体感 = "信息丰富、排列有序" 而非 "空旷稀疏"
但也不 = 重叠、堆砌、文字墙
```

> ❌ 每个面板只放 1-3 个元素（太空）  
> ❌ 密密麻麻文字标注堆砌（太挤）  
> ✅ 丰富的视觉元素 + 一致的微间距 = 充实而有序

### 规则 4：浮动元素，不嵌套框

```
元素直接浮在白色面板上，不套独立的背景框
不要 box-in-box 嵌套结构
概念名用白色/极淡色 pill 药丸标签
曲线、公式、图标直接画在面板表面
```

### 规则 5：色彩通过 token + 文字 + 曲线传达

```
Token 小方块 = 10-14px 圆角方块，pastel 填充 + 1px 略深边框
彩色文字 = 关键概念名用语义色（coral/teal/purple/green）
曲线线条 = 用 pastel 色画线
面板/画布 = 始终白色，不参与色彩
```

---

## 五种色彩载体

| 载体 | 说明 | 示例 |
|------|------|------|
| **Token 方块** | 小圆角方块，pastel 填充 + 暗 1px 边框 | `soft blue #BBDEFB square with 1px #90CAF9 border, "s₁" label` |
| **彩色文字** | 关键词直接用彩色字体 | `bold coral #E05555 text "Exciter"` |
| **Pill 标签** | 极淡底色圆角药丸 | `faint green-tinted pill badge "Random Forest"` |
| **曲线线条** | 内嵌缩略图的线条颜色 | `sigmoid curve in warm amber #DAA520 line` |
| **叶节点/圆点** | 小彩色圆点标记类别 | `5 tiny circles in blue, pink, amber, purple, green` |

---

## 工作流程

### Step 1: 理解论文内容

1. 阅读论文源文件，提取核心概念、方法、数据流
2. 识别需要配图的位置
3. 理解数学符号和维度

### Step 2: 配色方案选择

**展示选项，等待用户确认后再生成：**

| # | 方案名 | Token 色 | 文字强调色 |
|---|--------|----------|-----------|
| P1 | **Warm ML** | 粉 `#FFD0D0` · 蓝 `#BBDEFB` · 黄 `#FFF3C4` · 紫 `#E1BEE7` · 绿 `#C8E6C9` | coral `#E05555` · teal `#1A9988` · purple `#6A5ACD` · green `#3A8F3A` |
| P2 | **Cool Research** | 蓝 `#B3E5FC` · 靛 `#C5CAE9` · 灰蓝 `#CFD8DC` · 青 `#B2DFDB` · 薰衣草 `#D1C4E9` | navy `#1565C0` · indigo `#3949AB` · teal `#00897B` |
| P3 | **Earthy Warm** | 米 `#FFE0B2` · 驼 `#D7CCC8` · 灰绿 `#C8E6C9` · 灰 `#E0E0E0` · 浅棕 `#EFEBE9` | brown `#6D4C41` · olive `#827717` · forest `#2E7D32` |
| P4 | **自定义** | 用户指定 | 用户指定 |

### Step 3: 生成提示词

按下方模板逐层生成。

---

## 布局灵活性原则

面板数量和大小**根据内容决定**，不强制对称：

```
布局 A（参考图常见）：不等大 2×2 或 1+2
┌────────────────┐  ┌──────────┐
│  大面板 (主流程)  │  │  面板 2    │
│                │  │          │
└────────────────┘  └──────────┘
       ┌─────────────────────┐
       │  面板 3 (宽条形)       │
       └─────────────────────┘

布局 B：3-panel 不对称
┌──────────┐  ┌────────────────┐
│  面板 1    │  │  面板 2 (大)     │
└──────────┘  │                │
┌──────────┐  │                │
│  面板 3    │  │                │
└──────────┘  └────────────────┘

布局 C：横向流水线
┌──────┐  ┌──────┐  ┌──────┐
│ 面板1 │  │ 面板2 │  │ 面板3 │
└──────┘  └──────┘  └──────┘

布局 D：等分 2×2（仅在内容量对称时使用）
```

**原则**：
- 面板数量 2-5 个，大小按内容量分配
- 主流程面板可以更大，细节面板可以更小
- 不要为了对称而硬凑成 2×2
- 面板间 ~20px 间距

---

## 提示词结构模板

### 层次 1: 全局描述

```
A richly detailed academic paper [类型] diagram in the modern style of top-tier
ICLR/NeurIPS 2024-2025 publications. The diagram illustrates [主题概述].

CANVAS: Pure flat white (#FFFFFF). No gradient, no tint, no grey.

PANELS: [N] large rounded-rectangle panels (radius ~20px) with white (#FFFFFF)
fill and very subtle soft drop-shadow (3px blur, 1px y-offset, rgba(0,0,0,0.06)).
Panels sit on the white canvas, distinguished only by their barely-perceptible
shadow.

FONT: Friendly rounded geometric sans-serif (Nunito / Poppins / Quicksand).
Titles semi-bold to bold (600-700), ~16-18pt. Body regular (400), ~10-11pt.
Math in italic serif (Computer Modern). The rounded font gives a warm, approachable,
modern feel.

CONTENT DENSITY: Panels are FILLED with content — tokens, curves, formulas, icons,
arrows — with consistent 8-12px micro-spacing. "Thoughtfully packed" not "sparse".

NO NESTED BOXES: Elements float directly on white panel surfaces. Only pill-shaped
labels for concept names.

Arranged as [布局描述].
```

### 层次 2: 面板描述

使用 `=== PANEL: [名称] ===` 分隔每个面板。

```
=== PANEL: [名称] ===

White panel, subtle shadow, rounded corners ~20px.

Title: Bold [颜色] rounded font "[标题]" (~18pt).

Content (packed, floating elements):
  [元素描述...]
```

每个面板内元素类型：

| 元素 | 描述格式 | 注意 |
|------|---------|------|
| **Token 序列** | `3 soft blue #BBDEFB squares with 1px #90CAF9 border, labeled "x  y  z"` | 要写明 border |
| **Pill 标签** | `a faint green pill badge "Random Forest" in green text` | 有极淡底色 |
| **彩色标题** | `bold coral #E05555 text "Exciter"` | 直接浮在面板上 |
| **曲线缩略图** | `a small sigmoid in warm amber #DAA520 line (~30×20px), tiny grey axes` | 直接画在面板上 |
| **公式** | `italic serif formula: "X_k → f_θ(X_k)"` | 浮在面板上 |
| **小图标/插画** | `a small satellite schematic in thin grey lines with blue dot trail` | 有细节的插画 |
| **决策树** | `a binary tree in thin grey lines, leaf nodes as tiny colored circles` | 有多层分支 |
| **箭头** | `thin 1.5px dark grey #555 arrow with small arrowhead` | 简洁 |

### 层次 3: 风格规格

```
=== STYLE SPECIFICATIONS ===

Canvas: Pure white #FFFFFF. No gradient.
Panels: White #FFFFFF, radius ~20px, soft shadow (3px blur, rgba(0,0,0,0.06)).
Font: Rounded sans-serif (Nunito/Poppins/Quicksand). Titles bold ~16-18pt,
body regular ~10pt, math italic serif. Warm and friendly, NOT angular Helvetica.
Density: Panels FILLED with content. 8-12px micro-spacing. No dead space.
Structure: Floating elements on white panels. No nested boxes.

Token colors (with 1px darker border):
  - [语义]: [fill] / [border] / [text emphasis]
  ...

Arrows: 1-1.5px dark grey #555, neat arrowheads. Some curved.
Pill labels: Faint pastel tint + thin matching border, rounded ~8px.
Colored text: Concept names in semantic colors (coral, teal, purple, green).

No 3D, no gradients on elements, no heavy shadows. Flat vector.
Resolution: [宽] × [高] px minimum.
```

---

## 内部元素词汇表

### Token 方块

| 用途 | 描述 |
|------|------|
| 状态/输入 | `soft blue #BBDEFB square, 1px #90CAF9 border, "s₁" label` |
| 动作/预测 | `soft pink #FFD0D0 square, 1px #EF9A9A border, "a₁" label` |
| 特征/统计 | `soft purple #E1BEE7 square, 1px #CE93D8 border` |
| 奖励/输出 | `soft green #C8E6C9 square, 1px #A5D6A7 border` |
| 指标/数学 | `soft amber #FFF3C4 square, 1px #FFE082 border` |

### 曲线与图表

| 类型 | 描述 |
|------|------|
| 损失曲线 | `descending curve in coral #E05555 line, tiny grey axes` |
| sigmoid | `sigmoid curve in warm amber #DAA520 line` |
| 频谱 | `bar spectrum with 6 bars in soft pink, varying heights` |
| 概率分布 | `5 colored bar segments of varying widths` |
| 振荡波 | `oscillating wave in amber line` |

### 插画与图标

| 类型 | 描述 |
|------|------|
| 循环流 | `4-node cycle: "A"→"B"→"C"→"D" in tiny colored text with curved arrows` |
| 网络结构 | `input bars → hidden layers with dot connections → output, thin grey lines` |
| 决策树 | `binary branching tree, grey lines, colored circle leaf nodes` |
| 轨迹扇形 | `multiple curves fanning out from a point, solid mean + dashed bounds` |
| 金字塔 | `3 levels of increasing width, converging to ⊕ fusion` |
| 压缩漏斗 | `wide dot cluster → converging lines → narrow column of tokens` |

---

## 质量检查清单

- [ ] **纯白画布**：canvas = `#FFFFFF`，无渐变、无灰底
- [ ] **白色面板**：panel fill = `#FFFFFF`，靠 soft shadow 浮起
- [ ] **圆角字体**：指定 Nunito/Poppins/Quicksand，不是 Helvetica
- [ ] **排满内容**：每个面板充满元素（token+曲线+公式+图标），无大片空白
- [ ] **微间距**：元素间 8-12px，不重叠不拥挤
- [ ] **无嵌套框**：元素浮在面板上，无 box-in-box
- [ ] **Pill 标签**：概念名用极淡色药丸标签
- [ ] **彩色文字**：关键词用语义色（coral/teal/purple/green）
- [ ] **Token 有边框**：小方块 pastel 填充 + 1px 暗边框
- [ ] **丰富插画**：有曲线、网络图、决策树、轨迹图等，不光是方块
- [ ] **公式渲染**：italic serif，浮在面板上
- [ ] **友好现代**：整体像 2024 ICLR oral 的图，温暖可亲

---

## 输出格式

```markdown
### 图 X.Y — [中文图名]

适用类型：[框架图/架构图/模块图/对比图]
配色方案：[已选方案名]
推荐分辨率：[宽高比]

​```
[完整英文提示词]
​```
```

---

## 注意事项

1. **提示词语言**：英文（AI 图片工具英文效果最佳），说明用中文
2. **长度不限**：宁长勿短，细节越多效果越好
3. **参考图优先**：用户提供参考图时以参考图为准
4. **字体是灵魂**：务必强调 Nunito/Poppins，这是风格关键
5. **白底是底线**：画布和面板都是白色，任何灰色填充都是错误
