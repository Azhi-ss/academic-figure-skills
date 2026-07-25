# Example: Complete End-to-End Workflow

Handoffs between skills after the v2.8 rewrite. Compact artifacts only — no duplicated palette tables.

---

## 对话示例

### User: 帮我分析这个 ML 代码仓库

**Stage: Repo-first → `academic-repo-analyzer`**

> 产出 **Quick Understanding Doc**（见 `01-repo-analyzer-example.md`）  
> 含：任务/栈/架构/配图线索 + 信息完整度说明  
> 下一跳：需要配图规划时再开 paper-analyzer

---

### User: 基于这份文档，帮我规划论文配图

**Stage → `academic-figure-paper-analyzer`**

> 产出 **Figure Plan**（见 `02-paper-analyzer-example.md`）  
> 配色仅 handoff 提示，不写 hex：
>
> ```
> venue: CVPR
> figure_types: framework, architecture, module, ablation
> module_count_framework: 4+
> hint: Okabe-Ito or Nature Blue per docs/palettes.md
> ```

---

### User: 我要投 CVPR，推荐什么配色？

**Stage → `academic-figure-color-expert`**（读 `docs/palettes.md`）

> **Palette Decision**
>
> ```
> palette: Okabe-Ito
> primary / secondary / tertiary: #0072B2 / #E69F00 / #009E73
> text / fill / section_bg / border / arrow: #333333 / #FFFFFF / #F7F7F7 / #CCCCCC / #4D4D4D
> reason: scene=CVPR; colorblind-safe default (module count for this figure ≤3 polychrome OK)
> accessibility: colorblind-safe
> alternate: Nature Blue — if framework grows to ≥4 modules
> ```

---

### User: 用 Okabe-Ito 配色，帮我画一个总体框架图

**Stage → `academic-figure-prompt`**

> 默认输出 **JSON figure spec**（见 `03-figure-prompt-example.md`）  
> 消费上游 Palette Decision，不再内嵌 12 套色表  
> 可复制到 NanoBanana / Gemini 等工具

---

### User: 想要现代一点的风格，ICLR 2024 那种

**Stage → `academic-figure-prompt-pastel`**

> Prompt Package：白底白面板 + soft shadow + Nunito/Poppins + P2 Cool Research tokens  
> 与 classic JSON skill 分流（leading word: pastel / airy）

---

### User: 从这篇 PDF 提取架构图并分析

**Stage → `academic-figure-architecture-extractor`**

```bash
python3 academic-figure-architecture-extractor/scripts/extract_pdf_figures.py \
  paper.pdf -o /tmp/arch-extract/paper
```

> 读 `extract-report.json` → agent 结构分析 → 重绘参数（palette **names**）  
> 再接 color-expert / prompt

---

## 工作流图

```
代码仓库 / 论文 / PDF
        ↓
academic-figure-workflow（路由，按需加载）
        ↓
repo-analyzer → paper-analyzer → color-expert → prompt(/pastel)
        ↑                              ↑
architecture-extractor ───────────────┘
        ↓
JSON figure spec 或 pastel 英文 prompt
        ↓
NanoBanana / Gemini / Midjourney
```

共享事实源：`docs/palettes.md` · `docs/missing-info-policy.md`

---

*Demonstration workflow only.*
