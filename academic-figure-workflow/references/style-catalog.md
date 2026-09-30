# 风格确认目录

第一次出图前，若用户没有点名风格、也没有给出要跟随的参考图，按本表展示全部预览并停下。预览图与本文件同在 skill 目录内，单独安装后仍然可用。展示时读取图片本身，让用户看到图，不要只给文件名。

修图、只改颜色、用户已点名风格、或参考图走 `reference-led` 时，不再展示这张菜单。

| 名称 | style_profile | 预览 | 一行特征 |
|---|---|---|---|
| 现代前沿技术框线风 | `classic-technical` | `previews/modern_technical_vector_deepseek_mla.jpg` | 彩色张量条、注意力热力图、正交细线 |
| 编辑手绘模块风 | `illustrated-modular` | `previews/illustrated_modular_agentic_matribo.jpg` | 手绘描边、非对称分区、线稿插画 |
| 有色语义分区图示风 | `illustrated-modular` | `previews/paired_semantic_zones_dash.jpg` | 柔彩填色、同色深描边、语义色区 |
| 现代柔彩空气风 | `pastel-airy-ui` | `previews/pastel_airy_ui_agentic_bo.jpg` | 白底大留白、轻卡片、柔彩 token |
| 对比消融实验风 | `classic-technical` | `previews/contrast_ablation_kan.jpg` | 左右对比分栏，突出差异曲线 |
| 双保真度引导闭环风 | `classic-technical` | `previews/dual_fidelity_loop_labo.jpg` | 上下双容器、冷暖配对、判定闭环 |

路径相对于 `references/`。用户选定后把名称写入 `style_preset`，把表中的 profile 写入 `style_profile`，并把 `style_selection` 记为 `confirmed`。
