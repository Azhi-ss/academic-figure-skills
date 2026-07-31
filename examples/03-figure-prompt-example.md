# Example: Figure Prompt Output

Default deliverable from `academic-figure-prompt`: **JSON figure spec** + Palette Decision hex from `docs/palettes.md`.

---

### 图 1 — 扩散模型总体框架图

适用类型：Overall Framework  
配色方案：Okabe-Ito（用户指定 / scene: CVPR）  
推荐分辨率：16:9

#### Palette Decision（handoff）

```
palette: Okabe-Ito
primary / secondary / tertiary: #0072B2 / #E69F00 / #009E73
text / fill / section_bg / border / arrow: #333333 / #FFFFFF / #F7F7F7 / #CCCCCC / #4D4D4D
reason: user-specified; colorblind-safe CVPR default
accessibility: colorblind-safe
```

#### 信息完整度说明

- **已分析材料**：方法概述 + 用户指定 Okabe-Ito
- **当前输出类型**：JSON 结构化配图规范
- **Caption 预留**：完整 ε 预测目标公式、采样步数超参
- **待确认信息**：U-Net 内部通道数是否上图

```json
{
  "diagram_type": "Diffusion Overall Framework",
  "diagram_title_rendering": "None",
  "aspect_ratio": "16:9",
  "style_and_colors": {
    "background": "White (#FFFFFF)",
    "main_block_color_palette": {
      "Input": "Steel Blue (#0072B2) 1.5px solid border, white fill",
      "Denoise": "Steel Blue (#0072B2) 1.5px solid border, white fill",
      "Attention": "Bluish Green (#009E73) 1.5px solid border, white fill",
      "TimeEmbed": "Warm Orange (#E69F00) 1.5px solid border, white fill",
      "Output": "Steel Blue (#0072B2) 1.5px solid border, white fill"
    },
    "flow_arrow_colors": {
      "main_forward_flow": "Dark Grey (#4D4D4D) solid arrows"
    }
  },
  "layout_and_content_blocks": [
    {
      "relative_position": "Left",
      "shape": "Rounded rect, #CCCCCC thin border, white fill",
      "exact_title_to_render_inside": "INPUT",
      "internal_content": {
        "layout": "vertical stack",
        "item_1": {
          "icon": "monochrome bell-curve thumbnail",
          "exact_label": "Noise",
          "secondary_note": "x_T"
        },
        "item_2": {
          "icon": "token squares row",
          "exact_label": "Condition",
          "secondary_note": "c"
        }
      },
      "flow": "Horizontal arrow RIGHT to Denoising"
    },
    {
      "relative_position": "Center",
      "shape": "Large rounded rect, Steel Blue (#0072B2) border, white fill",
      "exact_title_to_render_inside": "DENOISING",
      "internal_content": {
        "layout": "three columns",
        "column_1": {
          "exact_label": "U-Net",
          "secondary_note": "backbone"
        },
        "column_2": {
          "exact_text": "Time Emb\nWarm Orange border"
        },
        "column_3": {
          "exact_text": "Cross-Attn\nBluish Green border"
        },
        "repeat_count": {
          "exact_text": "×50"
        }
      },
      "caption_note": "ε_θ(x_t, t, c) full objective in figure caption",
      "flow": "Horizontal arrow RIGHT to Output"
    },
    {
      "relative_position": "Right",
      "shape": "Rounded rect, #CCCCCC thin border, white fill",
      "exact_title_to_render_inside": "OUTPUT",
      "internal_content": {
        "item_1": {
          "icon": "monochrome image sketch",
          "exact_label": "x_0"
        },
        "item_2": {
          "exact_label": "VAE Dec"
        }
      }
    }
  ],
  "RENDERING_RULES_AND_NEGATIVE_PROMPT_INSTRUCTIONS": [
    "Render text ONLY within designated exact_* fields.",
    "All container boxes use WHITE (#FFFFFF) fill with COLORED BORDERS ONLY.",
    "Icons are monochrome thin grey line art.",
    "Weight status MUST use dashed/solid borders or subtle pill tags ([Fixed] vs [Tune]).",
    "NO emojis, NO lock/fire/lightning decorative symbols, NO 3D rendering.",
    "Flat vector: no gradients, no 3D.",
    "Canvas is pure white (#FFFFFF)."
  ]
}
```

> 简单数据图或用户明确要求 prose 时，才退回纯文本 prompt（见 skill `json-schema.md`）。

---

*Demonstration output only.*
