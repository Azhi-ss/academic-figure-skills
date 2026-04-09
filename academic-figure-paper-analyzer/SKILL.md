---
id: academic-figure-paper-analyzer
name: Academic Paper Analyzer & Figure Planner
version: 1.0.0
description: Use this skill whenever the user wants to analyze an academic paper to plan which figures to generate, identify figure-worthy content, suggest figure types and count per section, or when the user says "分析论文配图需求", "论文需要哪些图", "论文配图规划", "paper figure planning", "analyze paper for figures", "which figures does my paper need".
stages: [research, review]
tools: [bash]
---

# Academic Paper Analyzer & Figure Planner — 学术论文配图规划师

分析学术论文内容，规划需要生成的配图，识别值得配图的内容，建议每个章节的图表类型和数量。

## 核心理念

好的配图规划是成功论文的一半。通过系统性地分析论文结构，识别关键可视化点，确保：
- 每个核心贡献都有对应的配图
- 图表类型与内容匹配
- 视觉叙事逻辑连贯
- 读者理解路径清晰

## 工作流程

### Step 1: 论文结构解析

首先，提取论文的完整章节结构：

```markdown
论文结构清单：
├── Abstract（摘要，通常不配图）
├── Introduction（引言）
├── Related Work（相关工作，通常不配图）
├── Method / Proposed Approach（方法）
│   ├── Sub-section 3.1（子章节）
│   ├── Sub-section 3.2（子章节）
│   └── Sub-section 3.3（子章节）
├── Experiments（实验）
├── Analysis / Visualization（分析/可视化）
└── Conclusion（结论，通常不配图）
```

**必须识别的章节：**
- 引言/动机章节
- 方法/架构章节
- 关键模块/创新点章节
- 实验/结果章节
- 分析/可视化章节

### Step 2: 配图需求识别

逐章节扫描，标记值得配图的内容：

| 内容类型 | 推荐配图类型 | 优先级 |
|---------|-------------|--------|
| **端到端 pipeline 描述** | Overall Framework（总体框架图） | ⭐⭐⭐ 最高 |
| **网络架构/层结构描述** | Network Architecture（网络架构图） | ⭐⭐⭐ 最高 |
| **新颖模块/机制详细描述** | Module Detail（模块细节图） | ⭐⭐⭐ 最高 |
| **多个方法/变体对比** | Comparison / Ablation（对比消融图） | ⭐⭐ 高 |
| **数据/表征行为分析** | Data Behavior（数据行为图） | ⭐⭐ 高 |
| **数学公式密集的章节** | Module Detail（模块细节图） | ⭐⭐ 高 |
| **算法伪代码描述** | Network Architecture / Module Detail | ⭐⭐ 高 |
| **损失函数定义** | Module Detail（模块细节图） | ⭐⭐ 高 |
| **注意力机制描述** | Module Detail + Data Behavior | ⭐⭐ 高 |
| **训练/验证曲线展示** | Data Behavior（数据行为图） | ⭐ 中 |
| **t-SNE/UMAP 可视化** | Data Behavior（数据行为图） | ⭐ 中 |
| **注意力热力图展示** | Data Behavior（数据行为图） | ⭐ 中 |
| **特征图可视化** | Data Behavior（数据行为图） | ⭐ 中 |

### Step 3: 配图数量建议

根据论文类型和篇幅，建议配图数量：

| 论文类型 | 推荐配图数量 | 典型配置 |
|---------|-------------|---------|
| **顶会长文（CVPR/NeurIPS）** | 6-8 张 | 1×框架 + 1×架构 + 2×模块 + 1×对比 + 1×分析 |
| **顶会短文（ICLR Workshop）** | 4-5 张 | 1×框架 + 1×架构 + 1×模块 + 1×对比 |
| **期刊论文（IEEE/Nature）** | 8-12 张 | 1×框架 + 2×架构 + 3×模块 + 2×对比 + 2×分析 |
| **arXiv 技术报告** | 5-7 张 | 灵活配置，突出核心贡献 |

### Step 4: 生成配图规划报告

按照以下格式输出配图规划：

---

## 论文配图规划报告

### 📊 论文概览

| 项目 | 内容 |
|-----|------|
| **论文主题** | [简要描述论文核心主题] |
| **主要贡献** | [1-3 句话总结核心创新点] |
| **推荐配图总数** | [X] 张 |

### 📋 章节配图规划

#### 1. Introduction / 引言

**推荐配图：** Overall Framework（总体框架图）× 1

**理由：**
- 读者第一眼需要看到完整图景
- 建立论文的视觉叙事起点
- 帮助读者快速定位后续细节的位置

**建议内容：**
- 从原始输入到最终输出的完整流程
- 标注关键阶段（Encoder / Decoder / Loss 等）
- 突出本文的创新模块位置

---

#### 2. Method / Proposed Approach / 方法

**推荐配图：** Network Architecture（网络架构图）× 1

**理由：**
- 展示系统的精确层级结构
- 明确各层的操作类型和维度变化
- 为后续模块详解提供上下文

**建议内容：**
- 逐层展示网络结构（Conv / BN / Attention / MLP 等）
- 标注张量维度变化（B×C×H×W 格式）
- 标记残差/跳接连接
- 可选：宏观+微观双面板布局

---

#### 3. [关键模块子章节]

**推荐配图：** Module Detail（模块细节图）× [1-2]

**理由：**
- 深入展示论文的核心创新点
- 揭示内部数据流动和操作机制
- 突出数学公式与可视化的对应

**建议内容：**
- 中央展示核心机制（占用 60-70% 画布）
- 操作节点明确标注（⊗ matmul / ⊕ add / [;] concat / σ softmax）
- 关键公式叠加显示
- 角落添加上下文缩略图
- 底部标注时间/空间复杂度

---

#### 4. Experiments / 实验

**推荐配图：** Comparison / Ablation（对比消融图）× 1

**理由：**
- 可视化展示本文方法与基线的对比
- 突出消融实验的效果
- 让性能差异一目了然

**建议内容：**
- N×M 网格布局（行=输入变体，列=方法）
- 本文方法列用主色高亮
- 底部叠加关键指标
- 可选：差异区域放大插图

---

#### 5. Analysis / Visualization / 分析

**推荐配图：** Data Behavior（数据行为图）× [1-2]

**理由：**
- 展示数据/表征的行为模式
- 提供消融之外的深层洞察
- 增强论文的可信度和完整性

**建议内容：**
- 多面板组合（2×2 或 1×3）
- 注意力热力图 + t-SNE/UMAP + 训练曲线
- 每面板类型遵循严格约定
- 清晰的图例和标注

---

### 🎯 优先级建议

| 优先级 | 配图类型 | 说明 |
|-------|---------|------|
| **必须有** | Overall Framework | 论文的门面，读者第一眼 |
| **必须有** | Network Architecture | 展示系统的精确结构 |
| **必须有** | [关键模块] Module Detail | 突出核心创新点 |
| **强烈推荐** | Comparison / Ablation | 可视化验证效果 |
| **推荐** | Data Behavior | 增强分析深度 |

### 🎨 配色方案建议

在开始生成具体提示词前，请先选择配色方案：

| # | 方案名 | 适用场景 |
|---|--------|---------|
| A | Okabe-Ito（默认） | CVPR / NeurIPS / Nature，色盲友好 |
| B | Blue Monochrome | 单色系期刊，灰度打印兼容 |
| C | Teal-Coral | HCI / CHI 现代感 |
| D | ML TopConf Tab10 | Matplotlib 默认，熟悉感强 |

> 提示：选好配色方案后，可以使用「Academic Figure Prompt」技能生成具体的图片提示词。

---

## 配图类型详解

### 类型 1: Overall Framework（总体框架图）

**适用场景：**
- 论文 Introduction 章节
- 作为 Figure 1 展示完整图景
- 需要让读者快速理解系统全貌

**关键元素：**
- 输入模态区块（左）
- 处理阶段区块（中）
- 输出结果区块（右）
- 阶段间箭头标注数据类型/维度
- 分组虚线框标注阶段角色（Encoder / Decoder）

**推荐宽高比：** 16:9

---

### 类型 2: Network Architecture（网络架构图）

**适用场景：**
- Method 章节详细架构描述
- 需要展示精确层级结构
- 包含层类型、维度、参数计数

**关键元素：**
- 各层几何形状区分（Conv / BN / Attention / MLP）
- 张量维度标注（B×C×H×W）
- 残差/跳接连接弧形箭头
- 重复块×N 标注
- 可选：宏观+微观双面板

**推荐宽高比：** 16:9 或 3:2

---

### 类型 3: Module Detail（模块细节图）

**适用场景：**
- 关键创新模块详解
- 注意力机制、损失函数、融合策略
- 需要展示内部数据流动

**关键元素：**
- 中央核心机制（60-70% 画布）
- 操作节点（⊗ / ⊕ / [;] / σ）
- 数据流按角色颜色编码
- 关键公式叠加显示
- 上下文缩略图
- 复杂度标注

**推荐宽高比：** 4:3

---

### 类型 4: Comparison / Ablation（对比消融图）

**适用场景：**
- 实验结果可视化
- 与基线方法对比
- 消融研究展示

**关键元素：**
- N×M 网格布局
- 列标题标注方法名
- 本文方法列高亮
- 底部指标数值
- 可选：差异区域放大插图

**推荐宽高比：** 16:9

---

### 类型 5: Data Behavior（数据行为图）

**适用场景：**
- 注意力可视化
- 特征分布分析
- 训练曲线展示
- t-SNE/UMAP 可视化

**关键元素：**
- 多面板组合（2×2 或 1×3）
- 注意力热力图（白→主色顺序色阶）
- t-SNE/UMAP 散点图（每类一色）
- 训练曲线（实线=本文，虚线=基线）
- 特征图网格

**推荐宽高比：** 4:3 或 1:1

---

## 常见论文领域适配

### 计算机视觉（CV）

**典型配图组合：**
1. Overall Framework（输入图像→输出结果）
2. Network Architecture（CNN/Transformer 层级）
3. Module Detail（注意力模块/新颖块）
4. Comparison（视觉效果对比）
5. Data Behavior（注意力热力图/特征图）

### 自然语言处理（NLP）

**典型配图组合：**
1. Overall Framework（文本→编码器→解码器→输出）
2. Network Architecture（Transformer 层级）
3. Module Detail（自注意力机制）
4. Comparison（性能对比条形图）
5. Data Behavior（注意力热力图/t-SNE）

### 机器人/强化学习（Robotics/RL）

**典型配图组合：**
1. Overall Framework（状态→策略→动作→奖励）
2. Network Architecture（策略网络/Q 网络）
3. Module Detail（状态表示/奖励函数）
4. Comparison（学习曲线对比）
5. Data Behavior（轨迹可视化/t-SNE）

### 医学影像（Medical Imaging）

**典型配图组合：**
1. Overall Framework（医学影像→分割/检测→输出）
2. Network Architecture（U-Net/ViT 变体）
3. Module Detail（创新模块）
4. Comparison（定性结果对比）
5. Data Behavior（特征可视化/ROC 曲线）

---

## 输出格式

每次分析完成后，按照以下格式输出：

```markdown
# 论文配图规划报告

## 📊 论文概览
[论文主题、主要贡献、推荐配图总数]

## 📋 章节配图规划
[逐章节列出推荐配图类型、理由、建议内容]

## 🎯 优先级建议
[按优先级列出必须有/强烈推荐/推荐的配图]

## 🎨 配色方案建议
[列出适用的配色方案供选择]
```

---

## 注意事项

1. **领域自适应**：根据论文具体领域（CV/NLP/Robotics/Medical）调整配图建议
2. **贡献导向**：确保每个核心创新点都有对应的配图
3. **视觉叙事**：配图顺序应符合读者理解论文的逻辑路径
4. **灵活调整**：根据论文实际篇幅和投稿要求调整配图数量
5. **后续衔接**：规划完成后，建议使用「Academic Figure Prompt」技能生成具体提示词
