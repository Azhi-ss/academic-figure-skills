# 学术配图风格库 (Academic Figure Style Library)

风格库提供可组合的视觉 profile，不替代用户明确要求，也不把 venue 名称当作固定审美。选择顺序是：

1. 用户明确指定的风格、颜色、打印和可访问性要求
2. 参考图的可观察视觉语法
3. 内容的叙事结构与语义区域
4. 投稿规范、纸张/屏幕载体、全篇既有视觉系统等可验证生产约束
5. 无更强证据时的安全默认

参考图语法包括构图、面板表面、描边、阴影、字体气质、图标、嵌套层级、密度、连线和成对色彩。复用这些原则，不复制参考图的文字、logo、品牌插画、系统拓扑或性能声明。

## 6 个内置核心风格与代表论文索引

| 名称 | 类型 | 代表论文与图号索引 (Representative Paper & Fig) | 核心视觉特征 |
|---|---|---|---|
| **现代前沿技术框线风** | `surface_profile` | **DeepSeek-V3** (arXiv:2412.19437) Fig 2<br>**DiT** (ICCV 2023) Fig 2<br>**Mamba** (ICML 2024) Fig 1 | 现代大模型张量架构：彩色张量维度条 ($h_t, c_t^{KV}$)、注意力多层热力图、Top-K 门控概率柱状图、正交微米走线 |
| **编辑手绘模块风** | `surface_profile` | **MLEvolve** (arXiv:2606.06473) Fig 1–2（风格语法）<br>**Agentic-MatriBO** Fig 1 | illustrated modular：非对称 hero 或 left-hero/right-stack、最多一层 subcard、强描边、无阴影、手绘式短标题和受控线稿插画 |
| **有色语义分区图示风** | `color_material_layer` | **DASH** (arXiv:2608.00641) Fig 1<br>**Agentic-MatriBO** Fig 1 | paired semantic tokens；柔彩 fill、深同色 outline、可读 title、受控 icon accent |
| **现代柔彩空气风** | `surface_profile` | **Brunzema et al.** (arXiv:2608.00316) Fig 1 & 3<br>**SWE-agent** (ICML 2024) Fig 2<br>**Voyager** (NeurIPS 2023) Fig 1 | airy UI：纯白浮动卡片、柔杏数学代理与柔雾冰蓝 Agent、深灰高对比评估锚点、虚线作用域容器、叠层演进上下文与大比率呼吸感留白 |
| **对比消融实验风** | `composition_variant` | **KAN** (arXiv:2404.19756) Fig 1<br>**SimPO** (arXiv:2405.14734) Fig 1 | 左右高对比分栏、Baseline 固定权重 vs Ours 边上可学习 B-样条非线性曲线 $\phi(x)$ 与节点纯求和 $\sum$ |
| **双保真度引导闭环风** | `surface_profile` / `composition_variant` | **LABO** (arXiv:2605.22054) Fig 1 | 上下双宏观容器、双保真度配对色彩（珊瑚红真机实验/残差 vs 板岩蓝大模型代理）、门禁判定菱形 $p_\Delta(x^*) < \tau?$、3D 高斯过程响应曲面与极值搜索闭环 |

`surface_profile` 决定画布、面板、描边、字体和插画语言；
`composition_variant` 只改变叙事布局；`color_material_layer` 叠加在前两者之上，不得覆盖参考图的 surface grammar。

## 两个柔彩模块文件的职责边界

- [有色语义分区图示风.md](styles/有色语义分区图示风.md) 是**颜色/材质层**：定义 semantic zone 如何配对 fill、outline、title 和 icon accent，可与多种布局组合。
- [编辑手绘模块风.md](styles/编辑手绘模块风.md) 是**完整构图 profile**：定义 hero-plus-support、手绘标题、插画和拓扑校验；其默认色彩直接引用前者与 `docs/palettes.md` 的 I1 tokens。

两者保留是为了兼容已有风格名。只要需要柔彩分区而不需要手绘叙事时，单独使用“有色语义分区”；需要完整 illustrated modular 效果时，使用“编辑手绘模块风”并组合 semantic tokens。

## 风格定义文件

- [现代前沿技术框线风.md](styles/现代前沿技术框线风.md)
- [编辑手绘模块风.md](styles/编辑手绘模块风.md)
- [有色语义分区图示风.md](styles/有色语义分区图示风.md)
- [现代柔彩空气风.md](styles/现代柔彩空气风.md)
- [对比消融实验风.md](styles/对比消融实验风.md)
- [双保真度引导闭环风.md](styles/双保真度引导闭环风.md)

## Codex 定向编辑提示

当用户要求保留现有风格时，向 Codex 提供参考图并锁定已经正确的构图、文字和色彩 token；编辑指令只描述需要改变的区域。不要在修一条箭头或一个标签时重新解释整套风格，也不要把正确的 illustrated modular 色区重置为等宽白卡片。

## 用户自定义风格库

自定义风格可存放在 `~/.academic-figure-skills/styles/*.md`。工作流具备本地文件访问能力时，可将其与内置风格一起发现；同名风格按用户明确选择优先。自定义文件同样应说明适用范围、参考语法来源、颜色载体、可访问性检查和禁止复制的内容。
