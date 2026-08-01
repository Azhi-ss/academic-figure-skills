# Architecture Icons and Visual Vocabulary

Every major module in an architecture diagram should have a visual anchor — not just a text label. Use these phrases in image prompts to tell the model what icon/thumbnail to draw.

## Neural network components

| component | prompt phrase |
|-----------|--------------|
| Transformer block | `small icon of stacked horizontal layers with a curved residual arrow on the right, monochrome line art` |
| Attention / MHA | `small attention heatmap grid thumbnail (3x3 cells with varying grey fill) inside or beside the block` |
| Self-attention | `small icon: two rows of dots with arrows connecting each dot to every other, monochrome` |
| Cross-attention | `small icon: two rows of dots (Q on top, KV below) with arrows crossing between rows` |
| MLP / FFN | `small icon: two connected nodes expanding then contracting (fan-out fan-in), monochrome line art` |
| Embedding layer | `small icon: a grid of colored squares (token embedding matrix), monochrome` |
| Positional encoding | `small sinusoidal waveform icon next to the block, thin line` |
| LayerNorm | `small icon: a horizontal bar with a bell curve overlay, monochrome` |
| LM head / classifier | `small icon: a single output node connecting to multiple class labels, monochrome` |
| Residual connection | `curved solid arrow bypassing sub-layers on the right side, dark grey` |
| Skip connection | `dashed curved arrow bypassing layers, labeled with layer number` |

## Data flow components

| component | prompt phrase |
|-----------|--------------|
| Token sequence | `row of small rounded squares (tokens), first one black "CLS", grey ones "SEP", others light grey` |
| Token embedding lookup | `small matrix grid icon with an arrow pointing to one highlighted row` |
| Data pipeline | `small horizontal bar chart thumbnail or data flow icon` |
| Checkpoint | `small floppy-disc or save icon, monochrome thin line art` |
| Sampling / decoding | `small branching tree icon (beam search), monochrome` |
| KV cache | `small stacked memory layers icon, monochrome` |

## Input / output modalities

| component | prompt phrase |
|-----------|--------------|
| Audio waveform | `small audio waveform thumbnail (oscillating line), monochrome` |
| Mel spectrogram | `small mel spectrogram thumbnail (horizontal bands with varying brightness), monochrome` |
| Image input | `small image frame icon with diagonal cross, monochrome line art` |
| 3D / point cloud | `small 3D scatter of dots forming a cube or sphere, monochrome` |
| Ray / camera | `small camera frustum icon with rays, monochrome line art` |
| Volume rendering | `small icon: dots along a ray with varying opacity (circles sized by weight)` |
| MLP (NeRF) | `small icon: 4-5 vertical nodes connected by lines (fully connected), monochrome` |
| Text output | `small document or text lines icon, monochrome` |
| Molecular structure | `small molecule/atom graph icon (nodes connected by bonds), monochrome line art` |
| Protein / MSA | `small grid icon with rows of letters (sequence alignment), monochrome` |

## GAN / generative components

| component | prompt phrase |
|-----------|--------------|
| Generator | `small icon: an up-arrow through stacked layers (upsampling), monochrome` |
| Discriminator | `small icon: a magnifying glass over a real/fake label, monochrome` |
| GAN loss | `small icon: two competing arrows (G vs D), monochrome` |
| Diffusion / denoising | `small icon: noise dots progressively forming a clean image (3 stages)` |
| VAE / autoencoder | `small icon: funnel narrowing then widening, monochrome` |

## GNN / scientific components

| component | prompt phrase |
|-----------|--------------|
| Graph convolution | `small node-edge graph icon with highlighted neighbors, monochrome` |
| Message passing | `small icon: nodes with directional arrows along edges, monochrome` |
| Encoder-processor-decoder | `three connected blocks with a graph icon in the center, monochrome` |
| Weather grid | `small globe/grid icon with latitude-longitude lines, monochrome` |
| RBF / kernel | `small Gaussian bell curve icon, monochrome thin line` |
| Coordinate system | `small 3D axes icon (x,y,z), monochrome line art` |

## Detection / CV components

| component | prompt phrase |
|-----------|--------------|
| CNN backbone | `small icon: stacked feature maps (3 decreasing rectangles), monochrome` |
| Object queries | `small row of learned query dots (100 dots), with one highlighted` |
| Bipartite matching | `small icon: two rows of dots with crossing lines (Hungarian matching)` |
| Bounding box | `small rectangle with corner markers, monochrome line art` |
| Positional encoding (spatial) | `small grid with sinusoidal overlay, monochrome` |

## Status / weight indicators

| status | prompt phrase |
|--------|--------------|
| Frozen / fixed | `dashed border, small "[Fixed]" pill tag in grey` |
| Trainable | `solid border, small "[Tune]" pill tag in accent color` |
| Optional / gated | `dotted border with small gate icon` |

## Usage rules

1. **One icon per major block** — place it inside or immediately beside the block title
2. **Monochrome line art only** — use the block's border color or dark grey, never filled color icons
3. **Small (16-24px equivalent)** — icons are visual anchors, not illustrations
4. **Consistent style** — all icons in one figure must use the same line weight and level of detail
5. **If no suitable icon exists**, use a simple geometric shape (circle, square, triangle) as the visual anchor rather than leaving the block as pure text
