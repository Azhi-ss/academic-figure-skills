# 四层

自下而上：干净背景、透明框架、透明图标、真文本框。

最终画面等于这四层。文本框是唯一的文字。不要用色块去盖源图上的旧字，也不要改源 PNG。

示意图里的卡片、箭头和示意曲线可以重画。重画会改变笔触和曲线形状，这是这条路径的结果，不是失败。

## 抠图底色

```bash
python3 scripts/probe_palette.py SOURCE.png
```

用它打印的 `recommended_key`。`size` 是源图像素，不要用括号里的采样尺寸。

背景、框架、图标里的填充、描边、图标和曲线都不能使用这个颜色。模型若把卡片内部涂成抠图底色，去底时填充会消失，这一层要重出。

## 出图

先看源图，再出图。源图是这一次的编辑目标。

背景提示词：

```text
以刚刚显示的这张图片作为唯一编辑目标，在它的基础上擦除。只保留画布本身的底色。不要文字、图标、卡片、箭头、图表，也不要把分区的颜色洗进背景。
```

框架提示词：

```text
以刚刚显示的这张图片作为唯一编辑目标，在它的基础上提取框架。纯色背景，背景色值为 KEY。框架包括容器及其原来的填充和标题条、连线、箭头、示意图表。形状、大小、位置与源图一致。不要普通文字，不要将准备单独摆放的图标画进去。填充保持原色，任何填充、描边、图表都不要使用 KEY。
```

把 `KEY` 换成探到的色值。

框架出来后，列出源图里的图标，减去框架里已经有的。只把缺少的那些画进图标表：方形画布，纯 `KEY` 背景，等分格子，每格一个，居中留白，不画分割线，不要文字，颜色不要用到 `KEY`。已经在框架里的图标不要再写入 `icons`。

渐变字、徽章字、普通字体写不出的字，归图标，不进文本框。

## 文字

从源图逐段读取已有的字。不改写，不合并，不新增。

`size_px` 是字的像素高度，不是文本框高度。文本框可以更高，用来垂直居中。先定粗细、字号和换行，再挪框。只有标题加粗。

整页用同一个 `font`，按源图里字的样子选，不用另一类字体顶上：

| 源图里的字 | `--style` |
|---|---|
| 漫画、圆头、气泡字 | `comic`（Comic Neue；没有就装 `fonts-comic-neue`） |
| 马克笔、手写，但不是圆头漫画 | `hand` |
| 框线、柔彩界面、普通无衬线 | `technical` |
| 衬线 | `serif` |

风格名只是提示。语义分区图如果字是普通无衬线，用 `technical`，不要因为剖面叫手绘就改成漫画字。

```bash
python3 scripts/pick_font.py --style comic
```

它打印要写入每段 `font` 的家族。漫画字只用 Comic Neue。没装时脚本会执行 `sudo apt-get install -y fonts-comic-neue` 再选一次，不改用无衬线。其它风格缺字体时列出 `fc-list` 并退出。中文只有列表里带 CJK 的家族能写，没有就停。

框架里如果还留着个别字，不要再为这些字建文本框，否则同一句话会出现两次。能重出框架就重出一次；仍然留着，就在交付说明里写出来。

## layout.json

放在运行目录里，图片路径相对这个文件。省略 `slide_width_in` 和 `slide_height_in` 时，页尺寸是源图像素除以 96。

```json
{
  "units": "fraction",
  "ref_width": 1376,
  "ref_height": 768,
  "background": "background.png",
  "frame": "frame.png",
  "icons": [
    {"file": "icons/ic_r1c1.png", "x": 0.07, "y": 0.30, "w": 0.04, "h": 0.08,
     "source_bbox": [96, 230, 55, 60]}
  ],
  "texts": [
    {"text": "Zone title", "x": 0.06, "y": 0.14, "w": 0.22, "h": 0.04,
     "source_bbox": [84, 108, 300, 32], "size_px": 18, "color": "#682008",
     "bold": true, "align": "center", "valign": "middle", "font": "<pick_font.py 打印的家族>"}
  ]
}
```

`x = x_px / ref_width`，`y` 和 `h` 除以 `ref_height`，`w` 除以 `ref_width`。`source_bbox` 是源图像素 `[x, y, w, h]`。

## 命令

在本 skill 目录执行。`RUN` 是这次的运行目录。

```bash
python3 scripts/chroma_key.py --input "$RUN/frame_raw.png" --out "$RUN/frame.png" --preset frame-safe --scale 2 --force
python3 scripts/chroma_key.py --input "$RUN/icons_raw.png" --out "$RUN/icons_t.png" --preset icon-safe --scale 2 --force
python3 scripts/slice_grid.py "$RUN/icons_t.png" "$RUN/icons" --auto --pad 24 --contact-sheet --prefix ic
python3 scripts/layout_guard.py "$RUN/source.png" "$RUN/layout.json" --strict
python3 scripts/compose_pptx.py "$RUN/layout.json" "$RUN/figure.pptx" --preview-dir "$RUN/preview"
```

切片后看 `icons/icons_contact_sheet.png`。有图标被切断或贴边，就加大留白重出图标表，不要从源图补裁。

合成预览和源图并排看一次。字压住图标，或同一句话出现两次，改 `layout.json` 再合成一次，然后停。
