# Academic Figure Skills

![Version](https://img.shields.io/badge/version-2.8.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Stars](https://img.shields.io/github/stars/Azhi-ss/academic-figure-skills?style=social)

**Academic paper figure skills for Claude Code, Cursor, Codex & Gemini CLI.**  
AI 驱动的学术论文配图技能包：仓库分析 → 配图规划 → 色盲友好配色 → JSON 配图规范 / 现代 pastel 提示词。

**7 skills · palette SSOT · classic / pastel** · Install: `npx skills add Azhi-ss/academic-figure-skills -g --all`


## 快速开始（30 秒）

```bash
# 全局安装全部技能（推荐）
npx skills add Azhi-ss/academic-figure-skills -g --all
```

然后对 agent 说：

1. `"帮我分析这个 ML 代码仓库"`
2. `"用 Okabe-Ito 配色，生成总体框架图"`  
   或 `"ICLR 那种现代柔彩风格画一张 token 流图"`

先看有哪些 skill（不安装）：

```bash
npx skills add Azhi-ss/academic-figure-skills -l
```

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

| 技能 | 功能 | 触发词示例 |
|-----|------|-----------|
| **academic-figure-workflow** | 总入口路由：repo / paper / color / 架构分析 / prompt | 完整论文配图工作流、which skill first |
| **academic-repo-analyzer** | ML/DL 仓库快速理解文档 | 分析代码仓库、repo analyzer |
| **academic-figure-paper-analyzer** | 论文配图规划（类型、数量、优先级） | 论文需要哪些图、paper figure planning |
| **academic-figure-architecture-extractor** | PDF/图结构分析 + 本地提取脚本 | 提取论文架构图、architecture diagram |
| **academic-figure-color-expert** | 风格族 + 12 套配色 Palette Decision | 学术配图配色、Nature Blue |
| **academic-figure-prompt** | **经典** JSON 配图规范（默认） | 论文配图、学术配图JSON |
| **academic-figure-prompt-pastel** | **现代柔彩** ICLR/NeurIPS airy prompt | pastel风格、现代ML论文配图 |

## 完整工作流

```
用户请求 → academic-figure-workflow（判断入口）
                                   ↓
  repo-analyzer / paper-analyzer / architecture-extractor
               / color-expert / figure-prompt(/pastel)
                                   ↓
                        结构化 handoff artifact
                                   ↓
              JSON figure spec 或 pastel 英文 prompt
                                   ↓
                    NanoBanana / Gemini / Midjourney
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

仓库已公开，`npx skills` 从 GitHub 拉取；**push 到 `main` 即更新分发**，无需 npm publish。

```bash
# 全局安装全部 7 个 skill
npx skills add Azhi-ss/academic-figure-skills -g --all

# 仅列出仓库内 skill（不安装）
npx skills add Azhi-ss/academic-figure-skills -l

# 只装其中一个
npx skills add Azhi-ss/academic-figure-skills -g -s academic-figure-prompt -y

# 更新到 main 最新
npx skills update Azhi-ss/academic-figure-skills -g -y

# 查看已安装
npx skills list -g
```

也可用完整 URL：

```bash
npx skills add https://github.com/Azhi-ss/academic-figure-skills -g --all
```

发现页（skills.sh）：搜索 `academic-figure-skills` 或 owner `azhi-ss`。

### 方式 2：手动（开发调试）

```bash
git clone https://github.com/Azhi-ss/academic-figure-skills.git
# 将各个 skill 目录链到 agent skills 路径，例如：
# ln -s "$PWD/academic-figure-prompt" ~/.claude/skills/academic-figure-prompt
```

更推荐始终用 `npx skills add`，避免把整个 monorepo 误拷进 skills 目录。

## 使用示例

```
# 场景 1: 从代码仓库到配图
You: 帮我分析这个 ML 代码仓库
AI:  [扫描 → 任务/栈/架构 → 快速理解文档]

You: 基于这份文档，帮我规划论文配图
AI:  [Figure Plan：类型 / 数量 / 优先级]

You: 我要投 NeurIPS，推荐什么配色？
AI:  [先定 classic vs pastel → scene 推荐色系 + hex]

You: 用 Okabe-Ito，生成总体框架图
AI:  [JSON figure spec]
```

```
# 场景 2: PDF 架构图重绘
You: 从这篇 PDF 提取架构图
AI:  [extract_pdf_figures.py → 结构分析 → 重绘参数]

You: Nature/Science 风格重绘第一张
AI:  [Palette Decision → JSON figure spec]
```

```
# 场景 3: 现代柔彩
You: ICLR 2025 那种空气感，画一张 attention token 流图
AI:  [academic-figure-prompt-pastel · P2 Cool Research]
```

## 配色方案（12 套）+ 风格选择

单一事实源：[`docs/palettes.md`](docs/palettes.md)

**先选风格族，再选色系：**

| 风格族 | 何时用 | 技能 | 色系 |
|--------|--------|------|------|
| Classic academic | CVPR / Nature / IEEE、框线架构图 | `academic-figure-prompt` | 下表 12 套 |
| Pastel airy | ICLR/NeurIPS 现代柔彩、token/面板 | `academic-figure-prompt-pastel` | P1 / P2 / P3 |

场景配方（图类型 / venue / 领域 / 「太花了」/ 黑白印刷）见 `docs/palettes.md` 的 **Scene → palette decision** 与 **Worked decision recipes**。

| 方案 | 适用场景 |
|-----|---------|
| Okabe-Ito | 默认多色；CVPR / Nature，色盲友好 |
| Nature Blue | 默认单色；≥ 4 模块框架图 |
| Blue Monochrome | 模块详解、灰度友好 |
| Warm Earth | 生物 / 医学 |
| Purple-Green | 对比消融、IEEE |
| Grayscale | 纯灰度 |
| Teal-Coral | HCI / CHI |
| ML TopConf Tab10 | 对齐 Matplotlib 实验色 |
| ML TopConf Colorblind | ML 顶会 + 色盲安全 |
| ML TopConf Deep | 多面板消融 |
| Print-Safe Gray | 严格黑白印刷 |
| Journal Standard | Nature/Science 多类别图 |

默认：`用户指定 → 场景推荐 → 安全默认`（≥ 4 模块 → Nature Blue，否则 Okabe-Ito）。

## 文档与资源

| 文档 | 说明 |
|-----|------|
| **[docs/palettes.md](docs/palettes.md)** | 12 套配色 SSOT + classic/pastel 场景决策 |
| **[docs/missing-info-policy.md](docs/missing-info-policy.md)** | 缺信息时的统一策略 |
| **[CHANGELOG.md](CHANGELOG.md)** | 版本历史 |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 贡献指南 |
| **[docs/academic-references.md](docs/academic-references.md)** | 学术引用 |
| **[docs/best-practices.md](docs/best-practices.md)** | 顶会配图实践 |
| **[examples/](examples/)** | 端到端 handoff 示例 |

## 常见问题 FAQ

### Q: 怎么装到 Claude Code / Cursor？
A: `npx skills add Azhi-ss/academic-figure-skills -g --all`。CLI 会检测本机 agent 并写入对应 skills 目录。

### Q: 更新后别人还是旧版？
A: 用户需执行 `npx skills update Azhi-ss/academic-figure-skills -g -y`，或重新 `add`。分发源是 GitHub `main` 最新提交。

### Q: 生成的是英文还是中文？
A: 给图片模型的 JSON / prompt 用英文；对用户的说明可用中文。

### Q: 默认 JSON 还是纯文本 prompt？
A: **经典路径默认 JSON figure spec**（`exact_*` 控字）。简单数据图或用户明确要求时才用纯文本。柔彩路径是英文 prose prompt。

### Q: classic 和 pastel 怎么选？
A: 框线架构 / 顶刊经典 → classic + 12 套色板。空气感面板 / token / 「ICLR 那种」→ pastel P1–P3。不要混在同一张图。详见 `docs/palettes.md`。

### Q: 不确定配色怎么办？
A: `用户指定 → 场景推荐 → 默认安全方案`。不足时会标明使用 Okabe-Ito 或 Nature Blue（≥ 4 模块）。

### Q: 可以只装/只用一个技能吗？
A: 可以。`-s <skill-name>` 单装；使用时每个 skill 独立，workflow 仅在需要路由时用。

### Q: 必须按顺序跑完整流水线吗？
A: 不需要。可直接 prompt / color-expert / repo-analyzer。

## 许可证

MIT License

## 致谢

本项目受到 [LINUX DO](https://linux.do/) 社区的启发和支持。
