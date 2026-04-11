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

### Step 3.5: 缺信息处理分支

**总原则：** 信息不足时，优先输出“保守但有用”的阶段性结果，而不是停止任务；任何超出已知证据的判断，都必须明确标注为“推断”或“待确认”。

#### 情况 1：只有标题和摘要
- 先识别研究主题、任务领域、可能的核心贡献类型
- 输出高层级配图建议，如是否需要 Overall Framework、是否大概率需要 Module Detail、是否建议准备 Comparison / Ablation
- 不要假装已经知道具体子模块、公式细节或实验设计

#### 情况 2：只有 Introduction / Method，缺少 Experiments
- 优先规划引言图、总体框架图、方法架构图、核心模块细节图
- 对实验对比图、消融图、可视化分析图只给“预留建议”，不要写得过于具体
- 在输出中明确标注：`实验章节缺失，因此结果类图表仅作占位建议`

#### 情况 3：只有部分章节或节选段落
- 只对已提供章节做局部规划
- 输出中明确区分 `已覆盖章节`、`未覆盖章节`、`待补充后再判断的图`
- 不要把局部分析写成整篇论文的最终规划

#### 情况 4：没有论文正文，只有代码仓库理解文档
- 可以基于 `repo-analyzer` 产出的“快速理解文档”给出初步配图规划
- 但必须标注：`当前规划偏向系统/方法视角，论文叙事结构仍需结合正文复核`

#### 情况 5：用户需求很模糊
- 若材料足够，直接分析
- 若材料不足，先输出：
  1. 当前可判断的图类型
  2. 还不能判断的部分
  3. 最需要补充的章节（优先 `Method` / `Experiments` / `Analysis`）

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

### 信息完整度说明
- **已分析材料**：[摘要 / 引言 / 方法 / 实验 / 附录 / 仓库文档]
- **当前输出类型**：完整规划 / 阶段性规划 / 局部规划
- **高置信信息**：[一定值得做的图及其依据]
- **待确认信息**：[需要更多上下文后再确认的图、章节或细节]
- **建议补充材料**：[最值得补充的章节或文件]

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

在开始生成具体提示词前，不要在本 skill 内维护独立的配色清单；默认将配色选择交给「Academic Figure Color Expert」，并按以下顺序决策：

1. `用户指定`：如果用户已明确指定配色或参考图，则沿用用户要求
2. `场景推荐`：如果能识别投稿 venue、学科或图类型，则优先推荐对应方案
3. `默认安全方案`：如果信息不足，则明确说明先采用 `Okabe-Ito`

**场景级建议示例：**
- `CVPR / NeurIPS / Nature` → `Okabe-Ito` / `ML TopConf Colorblind`
- `HCI / CHI` → `Teal-Coral`
- `生物 / 医学` → `Warm Earth` / `Okabe-Ito`
- `多面板密集消融图` → `ML TopConf Deep`

> 提示：将“投稿 venue / 学科 / 图类型 / 是否需要色盲友好”传给「Academic Figure Color Expert」，再把配色结果传给「Academic Figure Prompt」技能生成具体提示词。

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

## 信息完整度说明
[已分析材料、当前输出类型、高置信信息、待确认信息、建议补充材料]

## 📋 章节配图规划
[逐章节列出推荐配图类型、理由、建议内容]

## 🎯 优先级建议
[按优先级列出必须有/强烈推荐/推荐的配图]

## 🎨 配色方案建议
[说明配色决策顺序、给出场景级建议，或建议将配色选择交给 Academic Figure Color Expert]
```

---

## 注意事项

1. **领域自适应**：根据论文具体领域（CV/NLP/Robotics/Medical）调整配图建议
2. **贡献导向**：确保每个核心创新点都有对应的配图
3. **视觉叙事**：配图顺序应符合读者理解论文的逻辑路径
4. **灵活调整**：根据论文实际篇幅和投稿要求调整配图数量
5. **后续衔接**：规划完成后，建议使用「Academic Figure Prompt」技能生成具体提示词
