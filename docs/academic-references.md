# 学术引用与最佳实践

本文档收录了学术配图和可视化的权威参考资料。

---

## 配色方案参考文献

### Okabe-Ito 调色板

**文献来源：**
> Okabe, M., & Ito, K. (2008). *Color Universal Design (CUD): How to make figures and presentations that are friendly to colorblind people*. Nature Methods, 5(8), 681-683.

**摘要：**
本文提出了一套对色盲友好的配色方案，已成为学术可视化的事实标准。该方案考虑了三种主要色盲类型：
- Deuteranopia（红色盲，~6% 男性）
- Protanopia（绿色盲，~1% 男性）
- Tritanopia（蓝色盲，<0.01%）

**推荐应用场景：**
- CVPR、ICCV、ECCV 等计算机视觉会议
- Nature、Science、Cell 等综合期刊
- 需要广泛传播的学术成果

### Matplotlib 调色板

**文献来源：**
> Hunter, J. D. (2007). *Matplotlib: A 2D graphics environment*. Computing in Science & Engineering, 9(3), 90-95.

**摘要：**
Matplotlib 的默认调色板（Tab10、Tab20 等）已成为机器学习社区最熟悉的配色方案。Seaborn 进一步扩展了这些调色板，提供了 colorblind、deep、muted 等变体。

**推荐应用场景：**
- NeurIPS、ICML、ICLR 等机器学习会议
- 多组对比实验可视化
- 消融实验多面板图

### Viridis 连续色图

**文献来源：**
> van der Walt, S., & Smith, N. (2015). *A better default colormap for matplotlib*. BIDS Blog.

**摘要：**
Viridis 是一个感知均匀（perceptually uniform）的连续色图，确保数值差异在视觉上是等比例的。它同时具有：
- 优秀的色盲友好性
- 灰度打印可读性
- 低视觉疲劳

**推荐应用场景：**
- 注意力热力图
- 损失曲面可视化
- 梯度流分析
- t-SNE/UMAP 降维可视化

---

## 学术可视化原则

### Tufte 的可视化原则

**文献来源：**
> Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.

**核心原则：**
1. **最大化数据墨水比（Data-Ink Ratio）** - 删除不传达信息的装饰
2. **避免图表垃圾（Chart Junk）** - 移除过度的阴影、渐变、3D效果
3. **保持图表完整性** - 包含上下文、标注、误差线
4. **启用微阅读（Microreading）** - 高密度、高分辨率展示

### IEEE 可视化指南

**文献来源：**
> IEEE Transactions on Visualization and Computer Graphics (TVCG) - Author Guidelines

**关键要求：**
- 矢量格式优先（PDF、EPS、SVG）
- 字体大小 ≥ 8pt（缩放后仍可读）
- 线条宽度 ≥ 0.5pt
- 对比度 ≥ 4.5:1（文字与背景）

---

## 色盲友好设计检查清单

基于以下权威资源：
- Color Universal Design (Okabe & Ito, 2008)
- Web Content Accessibility Guidelines (WCAG 2.1)
- Viz Palette (https://projects.susielu.com/viz-palette)

### 设计前检查
- [ ] 避免使用红/绿组合作为唯一区分方式
- [ ] 选择有明确文献支持的调色板
- [ ] 计划双重编码：颜色 + 形状/标签/线条样式

### 设计中检查
- [ ] 使用 Viz Palette 实时模拟色盲效果
- [ ] 验证灰度打印时仍可区分所有元素
- [ ] 关键信息不依赖颜色传达

### 设计后检查
- [ ] 文字对比度 ≥ 4.5:1（使用 WebAIM Contrast Checker）
- [ ] 在真实投影仪上测试（亮度通常更低）
- [ ] 请色盲同事/同学提供反馈

---

## 推荐工具

### 配色工具
| 工具 | 用途 | 链接 |
|------|------|------|
| **ColorBrewer 2.0** | 学术数据可视化配色 | https://colorbrewer2.org |
| **Viz Palette** | 实时色盲模拟 | https://projects.susielu.com/viz-palette |
| **WebAIM Contrast** | 对比度检查 | https://webaim.org/resources/contrastchecker |
| **Coolors** | 随机生成+锁定调整 | https://coolors.co |
| **Adobe Color** | 色轮+互补/类比配色 | https://color.adobe.com/create |

### 可视化工具
| 工具 | 用途 | 链接 |
|------|------|------|
| **Matplotlib** | Python 学术绘图 | https://matplotlib.org |
| **Seaborn** | 统计数据可视化 | https://seaborn.pydata.org |
| **Manim** | 数学动画（3Blue1Brown） | https://www.manim.community |
| **TikZ/PGFPlots** | LaTeX 原生绘图 | https://pgfplots.net |
| **Inkscape** | 矢量图编辑 | https://inkscape.org |

---

## 顶会论文配图分析

### CVPR 风格
- **特点**：工程感强、信息密度高
- **配色**：Okabe-Ito 或类似方案
- **常见图表类型**：
  - 网络架构图（方框+箭头）
  - 定性结果对比（图像网格）
  - 定量指标对比（柱状图/折线图）

### NeurIPS 风格
- **特点**：理论与实证结合
- **配色**：Matplotlib Tab10/colorblind
- **常见图表类型**：
  - 算法框图
  - 训练曲线（带误差线）
  - t-SNE/UMAP 降维可视化
  - 消融实验多面板图

### Nature/Science 风格
- **特点**：极简主义、强调概念清晰
- **配色**：非常克制，通常 2-3 种颜色
- **常见图表类型**：
  - 概念示意图
  - 主要结果概览图
  - 补充材料包含大量技术细节

---

## 引用格式

如果在您的工作中使用了本技能包，可以这样引用（可选）：

```bibtex
@software{academic-figure-skills,
  author = {Azhi-ss},
  title = {Academic Figure Skills: AI-powered academic figure generation skill pack},
  year = {2026},
  url = {https://github.com/Azhi-ss/academic-figure-skills},
  version = {2.3.0}
}
```

同时请确保引用您实际使用的配色方案的原始文献！
