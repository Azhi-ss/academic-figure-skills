# Example: Complete End-to-End Workflow

This example shows how all skills work together in a complete workflow.

---

## 完整端到端对话示例

### User: 帮我分析这个 ML 代码仓库

**Claude (使用 academic-repo-analyzer):**
> 正在分析您的代码仓库...
>
> [扫描目录结构 → 识别任务类型 → 提取技术栈 → 生成快速理解文档]
>
> # 仓库快速理解文档
>
> ## 📊 仓库概览
> | 项目 | 内容 |
> |-----|------|
> | **仓库名称** | vision-transformer-classification |
> | **任务类型** | 计算机视觉（图像分类） |
> | **核心框架** | PyTorch |
> | **主要架构** | Vision Transformer (ViT) |
>
> ... [完整文档见 01-repo-analyzer-example.md]
>
> 💡 提示：现在可以使用「Academic Paper Analyzer & Figure Planner」技能，基于这份快速理解文档来规划详细的论文配图。

---

### User: 基于这份文档，帮我规划论文配图

**Claude (使用 academic-figure-paper-analyzer):**
> 正在规划论文配图...
>
> # 论文配图规划报告
>
> ## 📄 论文基本信息
> | 项目 | 内容 |
> |-----|------|
> | **论文主题** | Vision Transformer 图像分类 |
> | **目标会议** | CVPR 2024 |
> | **推荐配色** | Okabe-Ito ⭐ |
> | **预估配图数** | 5-7 幅 |
>
> ... [完整文档见 02-paper-analyzer-example.md]
>
> 💡 提示：现在可以使用「Academic Figure Color Expert」选择配色方案，或直接使用「Academic Figure Prompt」生成配图提示词。

---

### User: 我要投 CVPR，推荐什么配色？

**Claude (使用 academic-figure-color-expert):**
> 为您推荐 **Okabe-Ito** 配色方案 ⭐
>
> | 颜色 | Hex | 用途 |
> |------|-----|------|
> | Steel Blue | `#0072B2` | 主色 |
> | Warm Orange | `#E69F00` | 辅色 |
> | Bluish Green | `#009E73` | 点缀 |
>
> **理由：**
> - ✅ Nature Methods 2008 权威推荐
> - ✅ 对红色盲（~6%男性）最友好
> - ✅ CVPR/NeurIPS 顶会广泛使用
> - ✅ 黑白打印可读性极佳
>
> 💡 色盲模拟预览：https://projects.susielu.com/viz-palette

---

### User: 用 Okabe-Ito 配色，帮我画一个总体框架图

**Claude (使用 academic-figure-prompt):**
> 正在生成提示词...
>
> # 学术配图提示词（Okabe-Ito 配色）
>
> ## 🎨 配色方案确认
> | 颜色 | Hex | 用途 |
> |------|-----|------|
> | Steel Blue | `#0072B2` | 主流程、主要模块边框 |
> | Warm Orange | `#E69F00` | 辅流程、次要模块边框 |
> | ... | ... | ... |
>
> ## 📝 总体框架图提示词
> ```
> A highly detailed, information-dense academic paper overall framework diagram...
> ```
>
> ... [完整提示词见 03-figure-prompt-example.md]
>
> 💡 您可以将此提示词复制到 NanoBanana、Gemini、DALL-E 3 或 Midjourney 中生成配图！

---

### User: 想要现代一点的风格，ICLR 2024 那种

**Claude (使用 academic-figure-prompt-pastel):**
> 正在生成现代 ML 风格提示词...
>
> # 现代 ML 风格配图提示词（Pastel）
>
> ## 🎨 风格说明
> - 纯白画布 + 白色面板 + 微弱阴影
> - 圆角友好字体（Nunito/Poppins/Quicksand）
> - Pastel 色系 Token 方块
> - 胶囊形状（pill-shaped）概念标签
>
> ## 📝 提示词
> ```
> A clean, modern academic diagram in the style of ICLR/NeurIPS 2024-2025 papers...
> ```
>
> 💡 这种风格非常适合展示 Transformer、注意力机制、Token 流动等现代 ML 概念！

---

## 工作流总结

```
代码仓库
    ↓
[academic-repo-analyzer] → 仓库快速理解文档
    ↓
[academic-figure-paper-analyzer] → 配图规划报告
    ↓
[academic-figure-color-expert] → 配色方案选择
    ↓
[academic-figure-prompt] 或 [academic-figure-prompt-pastel] → 提示词生成
    ↓
NanoBanana / Gemini / DALL-E / Midjourney → 配图生成
```

---

*This is an example workflow for demonstration purposes.*
