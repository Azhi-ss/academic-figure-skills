# Academic Figure Skills

![Version](https://img.shields.io/badge/version-2.8.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

AI 驱动的学术论文配图技能包，适用于 Claude Code / Gemini CLI / Cursor 等 AI 编程助手。从代码仓库分析到论文配图规划，再到高质量提示词生成。

## 快速开始（30 秒上手）

1. **安装**：`npx skills add Azhi-ss/academic-figure-skills`
2. **分析仓库**："帮我分析这个 ML 代码仓库"
3. **生成配图**："用 Okabe-Ito 配色，生成总体框架图提示词"

## 示例配图

以下为使用本技能包生成提示词后创建的学术配图示例：

<table>
<tr>
<td align="center" width="33%">
<img src="docs/images/example-architecture.png" alt="Claude Opus 4.6 提示词 + Gemini NanoBanana2Flash 生成" />
<br/><sub><b>Claude Opus 4.6 提示词 + Gemini NanoBanana2Flash</b></sub>
</td>
<td align="center" width="33%">
<img src="docs/images/example-gemini-doubao.png" alt="豆包 2.0 Pro 提示词 + Gemini NanoBanana2Flash 生成" />
<br/><sub><b>豆包 2.0 Pro 提示词 + Gemini NanoBanana2Flash</b></sub>
</td>
<td align="center" width="33%">
<img src="docs/images/example-glm5.png" alt="GLM-5 提示词 + Gemini NanoBanana2Flash 生成" />
<br/><sub><b>GLM-5 提示词 + Gemini NanoBanana2Flash</b></sub>
</td>
</tr>
</table>

## 技能列表

| 技能 | 功能 | 触发词 |
|-----|------|--------|
| **academic-figure-workflow** | 总入口路由：判断 repo / paper / prompt / color / 架构分析 入口，只加载必要 sibling | "帮我从仓库到配图走一遍"、"完整论文配图工作流"、"which skill should I use first" |
| **academic-repo-analyzer** | ML/DL 仓库快速理解文档（任务、栈、架构、配图线索） | "分析代码仓库"、"仓库分析"、"repo analyzer" |
| **academic-figure-paper-analyzer** | 论文配图规划（类型、数量、优先级） | "分析论文配图需求"、"论文需要哪些图"、"paper figure planning" |
| **academic-figure-architecture-extractor** | 架构图/PDF 图结构分析与重绘参数 | "提取论文架构图"、"架构图分析"、"architecture diagram extraction" |
| **academic-figure-color-expert** | Palette Decision（12 套预设，色盲友好） | "学术配图配色"、"论文配色方案"、"academic color palette" |
| **academic-figure-prompt** | 经典学术 JSON 配图规范（默认） | "论文配图"、"学术配图JSON"、"paper figure prompt" |
| **academic-figure-prompt-pastel** | 现代 ML 柔彩 / ICLR–NeurIPS airy 风格英文 prompt | "pastel风格论文配图"、"现代ML论文配图" |

## 完整工作流

```
用户请求 → academic-figure-workflow（判断入口）
                                   ↓
             repo-analyzer / paper-analyzer / architecture-extractor / color-expert / figure-prompt
                                   ↓
                        结构化 handoff artifact
                                   ↓
                    JSON figure spec 或英文 prompt
                                   ↓
                         NanoBanana/Gemini → 配图
```

架构图路径：

```
PDF/图 → architecture-extractor → (paper-analyzer) → color-expert → prompt → 重绘
```

不知道从哪开始时直接说：

- `帮我从仓库到配图走一遍`
- `完整论文配图工作流`
- `which skill should I use first`

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
# 场景 1: 从代码仓库到配图
You: 帮我分析这个 ML 代码仓库
AI:  [扫描文件 → 识别任务类型 → 提取技术栈 → 生成快速理解文档]

You: 基于这份文档，帮我规划论文配图
AI:  [分析内容 → 识别关键章节 → 输出配图规划报告]

You: 我要投 NeurIPS，推荐什么配色？
AI:  [先定 classic/pastel → 再按 scene 推荐 ML TopConf / Okabe-Ito 等]

You: 用 Okabe-Ito 配色，帮我画一个总体框架图
AI:  [生成 JSON 配图规范 / 英文提示词]
```

```
# 场景 2: 从 PDF 分析架构图并重绘
You: 从这篇 PDF 中提取架构图
AI:  [extract_pdf_figures.py → 结构分析 → 重绘参数]

You: 用 Nature/Science 顶刊配色重新绘制第一张架构图
AI:  [Palette Decision → JSON figure spec]
```

## 配色方案（12 套）+ 风格选择

单一事实源：[`docs/palettes.md`](docs/palettes.md)

**先选风格族，再选色系：**

| 风格族 | 何时用 | 技能 | 色系来源 |
|--------|--------|------|----------|
| Classic academic | CVPR/Nature/IEEE、框线架构图、JSON spec | `academic-figure-prompt` | 下表 12 套 |
| Pastel airy | ICLR/NeurIPS 现代柔彩、token/面板风 | `academic-figure-prompt-pastel` | P1 / P2 / P3 |

场景配方（图类型 / venue / 领域 / “太花了” / 黑白印刷等）见 `docs/palettes.md` 的 **Scene → palette decision** 与 **Worked decision recipes**。

| 方案 | 适用场景 |
|-----|---------|
| Okabe-Ito | 默认多色；CVPR / NeurIPS / Nature，色盲友好 |
| Nature Blue | 默认单色；≥ 4 模块框架图 |
| Blue Monochrome | 模块详解、灰度友好 |
| Warm Earth | 生物 / 医学 |
| Purple-Green | 对比消融、IEEE |
| Grayscale | 纯灰度 |
| Teal-Coral | HCI / CHI |
| ML TopConf Tab10 | Matplotlib 熟悉感 |
| ML TopConf Colorblind | ML 顶会 + 色盲安全 |
| ML TopConf Deep | 多面板消融 |
| Print-Safe Gray | 严格黑白印刷 |
| Journal Standard | Nature/Science 多类别图 |

默认规则：`用户指定 → 场景推荐 → 安全默认`（≥ 4 模块用 Nature Blue，否则 Okabe-Ito）。


## 文档与资源

| 文档 | 说明 |
|-----|------|
| **[docs/palettes.md](docs/palettes.md)** | 12 套配色 SSOT + classic/pastel 场景决策指南 |

| **[docs/missing-info-policy.md](docs/missing-info-policy.md)** | 缺信息时的统一策略 |
| **[CHANGELOG.md](CHANGELOG.md)** | 版本历史 |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 贡献指南 |
| **[docs/academic-references.md](docs/academic-references.md)** | 学术引用 |
| **[docs/best-practices.md](docs/best-practices.md)** | 顶会配图实践 |
| **[examples/](examples/)** | 端到端示例 |

## 常见问题 FAQ

### Q: 生成的提示词是英文还是中文？
A: 给图片模型的 prompt / JSON 内容用英文；对用户的说明可用中文。

### Q: 支持哪些 AI 图片生成工具？
A: NanoBanana、Gemini、DALL-E、Midjourney 等主流工具。

### Q: 不确定配色怎么办？
A: 按“用户指定 → 场景推荐 → 默认安全方案”。信息不足时会明确使用 Okabe-Ito 或 Nature Blue（≥ 4 模块），并可随时切换。详见 `docs/palettes.md`。

### Q: 可以只使用其中一个技能吗？
A: 可以。每个技能独立；workflow 只在需要路由时使用。

### Q: 必须按顺序使用吗？
A: 不需要。可单独用 prompt / color-expert / repo-analyzer，或走完整流水线。

## 许可证

MIT License

## 致谢

本项目受到 [LINUX DO](https://linux.do/) 社区的启发和支持。
