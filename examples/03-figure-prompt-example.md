# Example: Figure Prompt Output

This example shows the output from the `academic-figure-prompt` skill.

---

# 学术配图提示词（Okabe-Ito 配色）

## 🎨 配色方案确认

| 颜色 | Hex | 用途 |
|------|-----|------|
| Steel Blue | `#0072B2` | 主流程、主要模块边框 |
| Warm Orange | `#E69F00` | 辅流程、次要模块边框 |
| Bluish Green | `#009E73` | 创新点高亮 |
| Vermillion | `#D55E00` | 损失/优化模块 |
| Sky Blue | `#56B4E9` | 连接箭头 |
| Yellow | `#F0E442` | 标注背景 |
| Black | `#000000` | 文字、细边框 |
| Dark Gray | `#666666` | 辅助线、次要文字 |
| Light Gray | `#CCCCCC` | 背景分隔线 |

---

## 📝 总体框架图提示词

```
A highly detailed, information-dense academic paper overall framework diagram in the style of top-tier CVPR/Nature publications. The diagram illustrates a diffusion model for image generation, arranged as a horizontal pipeline from left (input) to right (output).

=== LEFT SECTION: INPUT ===
White background panel with light gray `#CCCCCC` border, small-caps label "INPUT" at top-left in dark gray `#666666`. Inside:
- Gaussian noise distribution visualization (monochrome, bell curve)
- Text embedding representation (sequence of small squares)
- Label: "x_T ~ N(0, I)" and "c" in small black text

=== CENTER SECTION: DENOISING ===
White background panel with light gray `#CCCCCC` border, small-caps label "DENOISING PROCESS" at top-left in dark gray `#666666`. Inside:
- U-Net architecture overview with steel blue `#0072B2` border
- Time embedding module with warm orange `#E69F00` border
- Cross-attention module highlighted with bluish green `#009E73` border
- All modules have WHITE FILL, no colored fill
- Arrows show data flow, labeled with dimensions
- Repeat indicator "×50" in light gray dashed box

=== RIGHT SECTION: OUTPUT ===
White background panel with light gray `#CCCCCC` border, small-caps label "OUTPUT" at top-left in dark gray `#666666`. Inside:
- Generated image preview (monochrome sketch placeholder)
- VAE decoder icon with steel blue `#0072B2` border
- Label: "x_0" in small black text

=== GLOBAL ELEMENTS ===
- Horizontal arrows connecting sections, sky blue `#56B4E9`
- Formula: "ε_θ(x_t, t, c)" centered above U-Net
- Legend at bottom-right showing color meanings
- No gradient, no 3D effects, no photorealistic elements

=== STYLE SPECIFICATIONS ===
- Background: Pure white `#FFFFFF`
- Font: Clean sans-serif (Computer Modern / Latin Modern style)
- Line weight: 1.5pt for main borders, 0.75pt for secondary
- Resolution: 300 DPI, 16:9 aspect ratio
- NO GRADIENT, NO SHADING, NO PHOTOREALISTIC ELEMENTS
- Vector illustration, technical diagram style

Make sure every module box contains sub-content, dimensions are labeled on all main arrows, and at least 50% of modules have embedded monochrome thumbnail visualizations. The diagram should be readable in grayscale.
```

---

*This is an example output for demonstration purposes.*
