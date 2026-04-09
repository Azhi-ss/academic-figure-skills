<p align="center">
  <img src="https://raw.githubusercontent.com/LigphiDonk/academic-figure-generator/main/logo.png" alt="Academic Figure Generator Logo" width="220" />
</p>

# Academic Figure Skills

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

AI-powered academic figure generation skill pack for AI coding assistants (Claude Code / Gemini CLI / Cursor). Analyze repos/papers, plan figures, generate publication-quality prompts with colorblind-safe palettes.

> 从代码仓库到论文配图的完整 AI 工作流。

## 示例配图

以下为使用本技能包生成的学术配图示例：

<table>
<tr>
<td align="center" width="100%">
<img src="docs/images/example-architecture.png" alt="网络架构图示例" />
<br/><sub><b>网络架构图示例（由 skills 生成的提示词创建）</b></sub>
</td>
</tr>
</table>

## 技能清单

| 技能 | 说明 | 触发词 |
|-----|------|--------|
| **academic-repo-analyzer** | 代码仓库分析器（识别任务/模型/技术栈） | "分析代码仓库"、"repo analyzer" |
| **academic-figure-paper-analyzer** | 论文配图规划分析器 | "分析论文配图需求"、"论文需要哪些图" |
| **academic-figure-color-expert** | 学术配色专家（9套预设 + 色盲友好设计） | "学术配图配色"、"论文配色方案" |
| **academic-figure-prompt** | 经典学术配图提示词生成（Okabe-Ito / Nature / CVPR 风格） | "论文配图提示词"、"生成论文配图" |
| **academic-figure-prompt-pastel** | 现代 ML Pastel 风格提示词（ICLR / NeurIPS 2024-2025） | "pastel风格论文配图"、"现代ML论文配图" |

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

## 安装方式

### 方式 1：使用 npx skills 一键安装（推荐）

```bash
npx skills add LigphiDonk/academic-figure-skills
```

### 方式 2：手动安装

```bash
git clone https://github.com/LigphiDonk/academic-figure-skills.git

# Claude Code
cp -r academic-figure-skills/* ~/.claude/skills/
# Gemini CLI
cp -r academic-figure-skills/* ~/.gemini/skills/
```

## 使用示例

```
# 从代码仓库开始
You: 帮我分析这个 ML 代码仓库
AI:  [扫描文件 → 识别任务类型 → 提取技术栈 → 生成快速理解文档]

# 论文配图规划
You: 基于这份文档，帮我规划论文配图
AI:  [分析内容 → 识别关键章节 → 输出配图规划报告]

# 配色选择
You: 我要投 NeurIPS，推荐什么配色？
AI:  [推荐 ML TopConf 方案 → 展示色值 → 说明适用场景]

# 生成提示词
You: 用 Okabe-Ito 配色，帮我画一个总体框架图
AI:  [生成极其详细的英文提示词，包含布局、色值、标注、风格规格]
```

## 技能详情

### 🔍 academic-repo-analyzer（代码仓库分析）

- 扫描 ML/DL 代码仓库结构
- 自动识别任务类型（CV/NLP/RL/Robotics/多模态）
- 提取技术栈（PyTorch/TensorFlow/JAX + 辅助库）
- 识别模型架构（Transformer/CNN/GAN/Diffusion 等）
- 生成"快速理解文档"，可直接传给 paper-analyzer

### 📊 academic-figure-paper-analyzer（论文配图规划）

- 分析论文结构，识别值得配图的章节
- 建议配图数量和类型（框架图/架构图/模块图/对比图/数据图）
- 按优先级推荐配图方案
- 支持 CV/NLP/Robotics/Medical 等领域适配

### 🎨 academic-figure-color-expert（配色专家）

- 9 套预设配色方案（Okabe-Ito、ML TopConf、色盲友好等）
- 按投稿 venue 推荐（CVPR/NeurIPS/Nature/IEEE）
- 色盲友好设计原则和验证工具
- 自定义配色指南

### 🖼️ academic-figure-prompt（经典风格提示词）

- 8 种预设学术配色方案
- 5 种图表类型：框架图、网络架构图、模块详解图、对比/消融图、数据模板图
- 生成极其详细的英文提示词
- 支持从参考图提取配色和布局

### ✨ academic-figure-prompt-pastel（现代 ML 风格）

- ICLR / NeurIPS 2024-2025 现代美学
- 纯白画布、柔和阴影、圆角字体
- Pastel 色块、胶囊形状标签

## 配色方案（9套）

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

## 相关项目

- [Academic Figure Generator](https://github.com/LigphiDonk/academic-figure-generator) - 完整的 Web 应用版本

## 许可证

本项目基于 [MIT License](./LICENSE) 开源。
