# Academic Figure Skills

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

AI 驱动的学术论文配图技能包，适用于 Claude Code / Gemini CLI / Cursor 等 AI 编程助手。从代码仓库分析到论文配图规划，再到高质量提示词生成。

## 技能列表

| 技能 | 功能 | 触发词 |
|-----|------|--------|
| **academic-repo-analyzer** | 分析 ML/DL 代码仓库，识别任务类型、模型架构、技术栈 | "分析代码仓库"、"repo analyzer" |
| **academic-figure-paper-analyzer** | 分析论文内容，规划需要的配图类型和数量 | "分析论文配图需求"、"论文需要哪些图" |
| **academic-figure-color-expert** | 9 套预设配色方案，含色盲友好设计原则 | "学术配图配色"、"论文配色方案" |
| **academic-figure-prompt** | 经典风格（Okabe-Ito / Nature / CVPR）提示词生成 | "论文配图提示词"、"生成论文配图" |
| **academic-figure-prompt-pastel** | 现代 ML 风格（ICLR / NeurIPS 2024-2025）提示词 | "pastel风格论文配图"、"现代ML论文配图" |

## 完整工作流

```
代码仓库 → repo-analyzer → 快速理解文档 
                              ↓
                         paper-analyzer → 配图规划
                              ↓
                         color-expert → 配色选择
                              ↓
                         figure-prompt → 生成提示词
                              ↓
                         NanoBanana/Gemini → 配图
```

## 安装

### 方式 1：npx skills（推荐）

```bash
npx skills add Azhi-ss/academic-figure-skills
```

### 方式 2：手动安装

```bash
git clone https://github.com/Azhi-ss/academic-figure-skills.git

# Claude Code
cp -r academic-figure-skills/* ~/.claude/skills/

# Gemini CLI
cp -r academic-figure-skills/* ~/.gemini/skills/
```

## 使用示例

```
# Step 1: 分析代码仓库
You: 帮我分析这个 ML 代码仓库
AI:  [扫描文件 → 识别任务类型 → 提取技术栈 → 生成快速理解文档]

# Step 2: 规划论文配图
You: 基于这份文档，帮我规划论文配图
AI:  [分析内容 → 识别关键章节 → 输出配图规划报告]

# Step 3: 选择配色方案
You: 我要投 NeurIPS，推荐什么配色？
AI:  [推荐 ML TopConf 方案 → 展示色值 → 说明适用场景]

# Step 4: 生成配图提示词
You: 用 Okabe-Ito 配色，帮我画一个总体框架图
AI:  [生成极其详细的英文提示词，包含布局、色值、标注、风格规格]
```

## 配色方案（9 套）

| 方案 | 适用场景 |
|-----|---------|
| Okabe-Ito | CVPR / NeurIPS / Nature，色盲友好 ⭐ |
| Blue Monochrome | 单色系期刊，灰度打印兼容 |
| Warm Earth | 生物学、医学影像 |
| Purple-Green | 数据可视化、IEEE 期刊 |
| Grayscale | 仅黑白打印 |
| Teal-Coral | HCI / CHI 现代感 |
| ML TopConf Tab10 | Matplotlib 默认，熟悉感强 |
| ML TopConf Colorblind | Seaborn 色盲友好 |
| ML TopConf Deep | 多面板消融图 |

## 许可证

MIT License
