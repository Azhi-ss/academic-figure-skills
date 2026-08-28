# Architecture Icons and Visual Vocabulary

Use visual anchors when they clarify a scientific role or establish the figure's visual story. A figure does **not** need one icon per box. Prefer one coherent hero illustration plus a few supporting anchors over a row of generic enterprise icons.

Match the selected style grammar:

- technical vector: restrained monochrome line art;
- illustrated modular: rounded hand-drawn line art with at most one semantic accent color per anchor;
- print-safe: silhouette, hatch, or geometric markers that survive grayscale.

Icons are communication devices, not decorations or evidence. Never add a laboratory robot, wet-lab action, external database, or autonomous capability unless the source material supports it.

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
| Skip connection | `dashed curved arrow bypassing layers; add a layer label only when FigureSpec supplies the exact text` |

## Data flow components

| component | prompt phrase |
|-----------|--------------|
| Token sequence | `row of small rounded token squares; render token names only when FigureSpec supplies the exact strings` |
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
| MLP (NeRF) | `small fully connected node-layer icon, monochrome; show an exact depth only when sourced` |
| Text output | `small document or text lines icon, monochrome` |
| Molecular structure | `small molecule/atom graph icon (nodes connected by bonds), monochrome line art` |
| Protein / MSA | `small sequence-alignment grid using abstract bars or sourced residue letters only, monochrome` |

## GAN / generative components

| component | prompt phrase |
|-----------|--------------|
| Generator | `small icon: an up-arrow through stacked layers (upsampling), monochrome` |
| Discriminator | `small icon: a magnifying glass over a two-way classification marker, monochrome; use class words only when sourced` |
| GAN loss | `small icon: two competing arrows (G vs D), monochrome` |
| Diffusion / denoising | `small progression from noisy dots to a clean image; use an exact stage count only when sourced` |
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

## Agentic scientific workflows and Bayesian optimization

These are optional visual metaphors, not default content. Use an entry only when
the corresponding component exists in FigureSpec. Any label, variable,
candidate count, memory category, laboratory apparatus, or agent embodiment must
come from the evidence-backed visible-text/component fields.

| concept | prompt phrase |
|---|---|
| Task / research state | `document with a compact question line and only the sourced state markers, rounded scientific line art` |
| Evidence scope | `magnifying glass over a bounded node-edge evidence graph, with a subtle scope ring` |
| Provenance manifest | `several cited document slips connected to one manifest sheet; no invented identifiers or body text` |
| Typed policy | `decision diamond feeding the sourced number of abstract action tabs, clean line illustration` |
| Planner / agent reasoning | `compact decision or reasoning glyph in the selected illustration language; use a robot motif only when the user or reference requests one` |
| Cognitive reasoning / LLM query | `electronic brain chip glyph surrounded by concise quoted natural-language dialogue bubbles with prior prompts` |
| Uncertainty gauge meter | `half-circle colored gauge meter with a pointer needle indicating calibrated variance / confidence` |
| Gating criterion / decision | `decision diamond with threshold condition (e.g. p_Delta(x*) < tau?), branching downward to a green checkmark badge (Yes) and red cross badge (No)` |
| 3D GP Response Surface (hero) | `3D Gaussian Process response surface with blue-to-red elevation mesh, highlighted elliptical discrepancy region X_R*, and a mathematical coupling formula card` |
| 1D Acquisition Function | `1D multi-peak acquisition function curve with coordinate axes, observation dots, and a prominent red peak point x* marked with a magnifying glass pointer` |
| Physical / Wet-Lab Experiment | `chemistry laboratory glassware (beakers, flask, microscope) and a computer monitor showing real measurement curves` |
| Council / critique | `the sourced number of reviewer markers converging on one annotated decision card` |
| Deterministic harness | `gear aligned with a tabular execution grid, crisp mechanical line art` |
| Gaussian Process fit (surrogate) | `mini 2D coordinate plot with arrow axes, a solid fitted mean curve, a same-hue uncertainty ribbon with dashed bounds, and contrasting observation points; bind hues to FigureSpec semantic tokens` |
| Initial observations / Warm starts | `small 2D Cartesian coordinate plot with circular observations along a nonlinear trajectory; use only the sourced observation count` |
| Candidate pool | `compact structured candidate grid with an abstract header band and highlighted rows; place no generated field names, ranks, variables, or values` |
| Working memory | `temporary state card with a short-lived marker; only FigureSpec-provided labels may appear` |
| Episodic memory | `ordered event cards along a timeline arrow; only FigureSpec-provided labels may appear` |
| Semantic memory | `versioned knowledge or rule cards; only FigureSpec-provided labels may appear` |
| Candidate shortlist | `small candidate grid with the sourced number of inputs merging into one selected row` |
| Oracle / lookup | `bounded lookup table returning one observation cell; do not imply a database or live service unless sourced` |
| Observation commit | `one result card crossing a durable checkpoint line` |
| Budget | `small counter or gauge with one increment tick, not a currency symbol` |
| Reflection / memory update | `dashed feedback loop from outcome to the declared memory/state component; no agent icon unless sourced` |
| Event graph | `short causal chain of typed nodes with directional edges` |
| Playbook / rules | `versioned notebook pages with one promoted rule tab` |
| Recovery checkpoint | `stacked state cards beside a save milestone, no lock icon` |
| Direct exception / stop | `coral report sheet on a short bypass path, used only for exception semantics` |

## Detection / CV components

| component | prompt phrase |
|-----------|--------------|
| CNN backbone | `small icon: stacked feature maps (3 decreasing rectangles), monochrome` |
| Object queries | `small row of learned query dots with one highlighted; do not imply a query count unless sourced` |
| Bipartite matching | `small icon: two rows of dots with crossing lines (Hungarian matching)` |
| Bounding box | `small rectangle with corner markers, monochrome line art` |
| Positional encoding (spatial) | `small grid with sinusoidal overlay, monochrome` |

## Status / weight indicators

| status | prompt phrase |
|--------|--------------|
| Frozen / fixed | `dashed border with a neutral status marker; render a word only when FigureSpec provides it` |
| Trainable | `solid border with an accent status marker; render a word only when FigureSpec provides it` |
| Optional / gated | `dotted border with small gate icon` |

## Usage rules

1. **Anchor the narrative, not every container.** Use anchors for the hero element and major semantic regions; text-only utility subcards are acceptable.
2. **Keep one illustration language.** Do not mix emoji glyphs, stock UI icons, photorealistic assets, and technical line art.
3. **Scale by importance.** A hero mechanism may be a real mini-illustration; secondary anchors remain small.
4. **Bind color semantically.** In illustrated profiles, an anchor may use its region's dark outline plus one accent fill. In classic profiles, keep it monochrome.
5. **Prefer a meaningful shape to a forced icon.** Loops, decision diamonds, graphs, mini-plots, and state cards can carry more information than a generic gear.
6. **Audit capability implications.** An icon must not suggest automation, validation, wet-lab execution, security, or external access that the implementation does not have.
