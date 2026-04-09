---
id: academic-figure-color-expert
name: Academic Figure Color Expert
version: 1.0.0
description: Use this skill whenever the user needs help with academic figure color palettes, wants to choose a color scheme for their paper, needs colorblind-safe design advice, or when the user says "学术配图配色", "论文配色方案", "色盲友好配色", "academic color palette", "colorblind safe figure", "paper color scheme".
stages: [writing, research]
tools: [bash]
---

# Academic Figure Color Expert — 学术配图配色专家

为学术配图提供专业的配色方案建议，包含 9 套预设方案，以及色盲友好设计原则。

## 核心理念

学术配色的三大原则：
1. **功能优先**：颜色服务于信息传达，而非装饰
2. **克制简约**：最多 3 种彩色 + 灰色系
3. **可访问性**：确保色盲读者也能清晰理解

---

## 9 套预设配色方案

### 方案 1: Okabe-Ito（色盲友好 · 顶会推荐）⭐ 默认

**适用场景：** CVPR / NeurIPS / Nature / Science 投稿，色盲安全要求高

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#0072B2` | 主色 — 核心模块边框、节标签 |
| secondary | `#E69F00` | 辅色 — 次要模块边框、替代高亮 |
| tertiary | `#009E73` | 点缀色 — 输出/结果模块（极少量） |
| text | `#333333` | 正文字色 |
| fill | `#FFFFFF` | 画布背景（纯白） |
| section_bg | `#F7F7F7` | 区域背景（极浅灰） |
| border | `#CCCCCC` | 标准边框 |
| arrow | `#4D4D4D` | 箭头/线条 |

**特点：**
- Nature Methods 推荐的色盲友好调色板
- 对红色盲（deuteranopia）最友好（影响 ~6% 男性）
- 黑白打印仍清晰可读
- 顶会论文最常用方案

---

### 方案 2: Blue Monochrome（蓝色单色系 · 灰度兼容）

**适用场景：** 单色系期刊、模块详解图、需灰度打印

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#1565C0` | 主色 — 核心模块边框 |
| secondary | `#42A5F5` | 辅色 — 次要模块边框 |
| tertiary | `#90CAF9` | 点缀色 — 辅助元素 |
| text | `#212121` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F5F8FC` | 区域背景（极浅蓝） |
| border | `#B0BEC5` | 标准边框 |
| arrow | `#37474F` | 箭头/线条 |

**特点：**
- 极度克制、专业感强
- 黑白打印效果极佳
- 适合需要大量细节的模块详解图

---

### 方案 3: Warm Earth（暖土色系 · 生物/医学）

**适用场景：** 生物学、生态学、医学影像论文

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#C0392B` | 主色 — 核心模块边框 |
| secondary | `#E67E22` | 辅色 — 次要模块边框 |
| tertiary | `#F39C12` | 点缀色 — 输出/结果 |
| text | `#2C2C2C` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#FDF6EC` | 区域背景（暖奶油色） |
| border | `#D5C5A1` | 标准边框 |
| arrow | `#5D4037` | 箭头/线条 |

**特点：**
- 温暖、有机的视觉感受
- 适合生物过程、医学影像可视化
- ⚠️ 非色盲最优，建议配合形状编码

---

### 方案 4: Purple-Green（紫绿互补 · 高对比度）

**适用场景：** 数据可视化、对比图、IEEE 期刊

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#6A1B9A` | 主色 — 核心模块边框 |
| secondary | `#2E7D32` | 辅色 — 次要模块边框 |
| tertiary | `#AB47BC` | 点缀色 — 第三类元素 |
| text | `#1A1A1A` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F8F5FC` | 区域背景（浅薰衣草色） |
| border | `#CE93D8` | 标准边框 |
| arrow | `#4A148C` | 箭头/线条 |

**特点：**
- 紫绿互补，视觉对比度高
- 适合对比实验、消融研究
- 数据可视化效果突出

---

### 方案 5: Grayscale（纯灰度 · 打印优先）

**适用场景：** 仅黑白打印的期刊、技术报告

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#212121` | 主色 — 核心模块边框 |
| secondary | `#616161` | 辅色 — 次要模块边框 |
| tertiary | `#9E9E9E` | 点缀色 — 辅助元素 |
| text | `#111111` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F5F5F5` | 区域背景（浅灰） |
| border | `#BDBDBD` | 标准边框 |
| arrow | `#424242` | 箭头/线条 |

**特点：**
- 100% 打印兼容
- 极度专业、极简风格
- 必须通过形状/线条粗细区分类别

---

### 方案 6: Teal-Coral（青蓝珊瑚 · HCI 现代感）

**适用场景：** HCI / CHI 论文、现代感强的 ML 论文

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#00695C` | 主色 — 核心模块边框 |
| secondary | `#E64A19` | 辅色 — 次要模块边框 |
| tertiary | `#26A69A` | 点缀色 — 输出/结果 |
| text | `#212121` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F0F9F8` | 区域背景（浅青色调） |
| border | `#80CBC4` | 标准边框 |
| arrow | `#004D40` | 箭头/线条 |

**特点：**
- 现代、活力的视觉风格
- 冷（青）暖（珊瑚）对比鲜明
- ⚠️ 对红色盲不够友好，建议配合形状编码

---

### 方案 7: ML TopConf Tab10（Matplotlib 默认 · 熟悉感）

**适用场景：** NeurIPS / ICML / ICLR 论文，使用 Matplotlib 默认色

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#1F77B4` | 主色 — 核心模块边框 |
| secondary | `#FF7F0E` | 辅色 — 次要模块边框 |
| tertiary | `#2CA02C` | 点缀色 — 输出/结果 |
| text | `#1F2937` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F8FAFC` | 区域背景 |
| border | `#CBD5E1` | 标准边框 |
| arrow | `#334155` | 箭头/线条 |

**特点：**
- Matplotlib Tab10 默认色，读者极其熟悉
- ML 顶会论文最常见配色
- 与实验图表配色天然一致

---

### 方案 8: ML TopConf Colorblind（Seaborn 色盲友好）

**适用场景：** NeurIPS / ICML / ICLR 论文，需色盲安全

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#0173B2` | 主色 — 核心模块边框 |
| secondary | `#DE8F05` | 辅色 — 次要模块边框 |
| tertiary | `#029E73` | 点缀色 — 输出/结果 |
| text | `#1F2937` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F8FAFC` | 区域背景 |
| border | `#CBD5E1` | 标准边框 |
| arrow | `#334155` | 箭头/线条 |

**特点：**
- Seaborn colorblind 调色板
- 保持 ML 顶会熟悉感的同时优化色盲可访问性
- 推荐作为 Tab10 的安全替代

---

### 方案 9: ML TopConf Deep（Seaborn Deep · 柔和）

**适用场景：** 多面板消融图、性能对比图

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#4C72B0` | 主色 — 核心模块边框 |
| secondary | `#DD8452` | 辅色 — 次要模块边框 |
| tertiary | `#55A868` | 点缀色 — 输出/结果 |
| text | `#1F2937` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#F8FAFC` | 区域背景 |
| border | `#CBD5E1` | 标准边框 |
| arrow | `#334155` | 箭头/线条 |

**特点：**
- Seaborn deep 调色板
- 更柔和、不刺眼的色调
- 适合多面板密集布局

---

## 配色禁忌清单

### ❌ 绝对禁止

| 禁止做法 | 危害 | 替代方案 |
|---------|------|---------|
| 彩色背景面板 | 浪费墨、AI 生图感、不专业 | 白色 + 极浅灰分组 |
| 高饱和度 Header Banner | 廉价感、分散注意力 | 小号 small-caps 文字 + 灰色分割线 |
| 每个模块不同颜色填充 | 混乱、可读性差 | 纯白填充 + 仅边框用色 |
| 彩色缩略图 | 信息过载 | 单色灰度或仅 2 色 |
| 5+ 种颜色同时出现 | 视觉污染 | 最多 3 种色彩 + 灰色系 |
| 彩虹/渐变效果 | 不专业、打印效果差 | 纯色、扁平、无渐变 |
| 深色背景 | 与论文版式冲突、浪费墨 | 白色背景（≥70% 面积） |

### ⚠️ 谨慎使用

| 做法 | 注意事项 |
|-----|---------|
| 仅用颜色编码类别 | 必须同时使用形状/标签编码 |
| 红色/绿色组合 | 对红色盲不友好，改用蓝/橙 |
| 低饱和度色彩 | 确保对比度 ≥4.5:1 |
| 多面板用不同背景 | 统一使用白色/极浅灰 |

---

## 色盲友好设计原则

### 常见色盲类型

| 类型 | 影响人群 | 难以区分 |
|-----|---------|---------|
| **Deuteranopia（红色盲）** | ~6% 男性，~0.4% 女性 | 红 ↔ 绿 |
| **Protanopia（绿色盲）** | ~1% 男性 | 红 ↔ 绿 |
| **Tritanopia（蓝色盲）** | <0.01% | 蓝 ↔ 黄 |

### 色盲友好检查清单

- [ ] **主色选择**：优先使用 Okabe-Ito 或 ML TopConf Colorblind
- [ ] **双重编码**：颜色 + 形状/标签/线条样式同时使用
- [ ] **对比度验证**：文字与背景对比度 ≥4.5:1
- [ ] **避免组合**：避免红/绿、蓝/黄作为唯一区分方式
- [ ] **灰度测试**：图片在黑白打印时仍可完整阅读
- [ ] **关键信息**：不依赖颜色传达关键信息

### 推荐工具

| 工具 | 用途 | 链接 |
|-----|------|------|
| ColorBrewer | 学术数据可视化配色 | https://colorbrewer2.org |
| Viz Palette | 实时模拟色盲效果 | https://projects.susielu.com/viz-palette |
| WebAIM Contrast | 对比度检查 | https://webaim.org/resources/contrastchecker |
| Coolors | 随机生成+锁定调整 | https://coolors.co |
| ColorHunt | 精选高质量色板 | https://colorhunt.co |
| Adobe Color | 色轮+互补/类比/三分配色 | https://color.adobe.com/create |

---

## 按投稿 venue 推荐

### 计算机视觉顶会

| Venue | 推荐方案 | 理由 |
|------|---------|------|
| **CVPR / ICCV / ECCV** | Okabe-Ito / ML TopConf Colorblind | 色盲安全、领域标准 |
| **NeurIPS / ICML / ICLR** | ML TopConf Tab10 / Colorblind / Deep | 读者熟悉、与实验图一致 |
| **Nature / Science** | Okabe-Ito | 期刊官方推荐 |
| **IEEE Transactions** | Purple-Green / Blue Monochrome | 高对比度、专业感 |

### 其他领域

| 领域 | 推荐方案 |
|-----|---------|
| **HCI / CHI** | Teal-Coral / Okabe-Ito |
| **生物学 / 医学** | Warm Earth / Okabe-Ito |
| **机器人学** | Blue Monochrome / Okabe-Ito |
| **理论计算机科学** | Grayscale / Blue Monochrome |

---

## 自定义配色指南

如果需要自定义配色，请按以下步骤：

### Step 1: 确定主色

选择 1 种主色用于核心模块边框：
- 推荐从预设方案中选择，或使用 Coolors/ColorHunt 探索

### Step 2: 选择辅色

选择 1-2 种辅色用于次要元素：
- 与主色形成对比但和谐
- 避免使用过多色彩

### Step 3: 填充灰色系

按以下格式提供完整配色：

```
主色：#XXXXXX（核心模块边框/节标签）
辅色：#XXXXXX（次要模块/强调）
点缀色：#XXXXXX（输出结果，可选）
背景：#FFFFFF（必须纯白或近白）
文字：#333333（建议深色）
```

### Step 4: 验证可访问性

- [ ] 检查文字对比度 ≥4.5:1
- [ ] 模拟色盲效果确认可区分
- [ ] 验证黑白打印可读性

---

## 输出格式

当用户询问配色建议时，按照以下格式输出：

```markdown
# 学术配图配色建议

## 🎨 推荐方案

### 方案 [编号]: [方案名]

| 角色 | 色值 | 用途 |
|-----|------|------|
| primary | `#XXXXXX` | 核心模块边框、节标签 |
| secondary | `#XXXXXX` | 次要模块边框、替代高亮 |
| tertiary | `#XXXXXX` | 输出/结果模块（极少量） |
| text | `#XXXXXX` | 正文字色 |
| fill | `#FFFFFF` | 画布背景 |
| section_bg | `#XXXXXX` | 区域背景 |
| border | `#XXXXXX` | 标准边框 |
| arrow | `#XXXXXX` | 箭头/线条 |

**适用场景：** [适用的 venue/领域]
**特点：** [3-5 个关键点]

---

## ✅ 配色检查清单

- [ ] 白色主导（≥70% 面积）
- [ ] 仅边框用色，模块纯白填充
- [ ] 最多 3 种彩色 + 灰色系
- [ ] 无渐变、无阴影、无 3D 效果
- [ ] 色盲友好（如需要）
- [ ] 黑白打印仍可读

## 🛠️ 推荐工具

- ColorBrewer — 学术数据可视化配色
- Viz Palette — 色盲效果模拟
- WebAIM Contrast — 对比度检查
```

---

## 注意事项

1. **预设优先**：优先推荐 9 套预设方案，而非让用户从零开始
2. **安全第一**：涉及色盲安全要求时，默认推荐 Okabe-Ito
3. **领域适配**：根据论文领域和投稿 venue 调整建议
4. **克制原则**：始终强调"少即是多"的配色理念
5. **后续衔接**：配色确定后，建议使用「Academic Figure Prompt」技能生成具体提示词
