---
name: academic-repo-analyzer
description: Analyze ML, AI4Science, Systems, and research repositories into an evidence-backed semantic architecture graph for paper figure planning. Code serves as supporting evidence; paper narrative and user intent remain the primary source of truth.
metadata:
  version: "1.5.0"
  stages: [research, review]
---

# Academic Repo Analyzer

Produce a concise repository understanding document plus a machine-readable **Semantic Architecture Handoff v1**. The handoff describes scientific roles and executable relationships, not the repository's folder layout or engineering boilerplate.

Read `keywords.md` only when task or framework classification is uncertain. Read `references/missing-info-policy.md` when evidence is sparse.

## Core Principle: Narrative Priority & Non-Intrusive Extraction

1. **Paper & User Narrative > Code Implementation**:
   - A paper figure depicts the **scientific contribution and conceptual data flow**, not the full software engineering artifact.
   - Omit engineering plumbing (such as `DataLoader`, `Trainer`, `Logger`, `ConfigParser`, `DeviceManager`, or `Optimizer` setup) unless the paper specifically contributes a training algorithm or infrastructure system.
2. **Fact-Checking & Parameter Grounding**:
   - When a paper draft or user architecture is already present, the repo analyzer acts as a **supporting fact-checker** (verifying tensor dimensions, loss formulas, exact module names, and execution directions) rather than re-inventing the architecture.

## Input contract

- Prefer: repository path, README, dependencies, entry points, core model/algorithm files, configs, and tests that establish behavior.
- Accept: partial repository, isolated model files, core algorithm script.
- Minimum: one README, entry point, or core implementation file.
- Record the source revision when Git metadata is available.
- Treat names and README claims as leads; verify figure-critical claims in code or tests.

## Output contract

Keep the human summary to roughly 30–70 lines, then emit the handoff block below.

1. Repository overview and scientific task.
2. Evidence/completeness statement listing what was inspected.
3. Semantic components and their responsibilities.
4. Executed/advisory/feedback/persistence connections.
5. Authority or trust boundaries when agents, tools, evaluators, or external systems are involved.
6. Figure suggestions (Overall Framework, Network Architecture, Module Detail, Concept/Motivation, Protocol/Sequence).
7. `Semantic Architecture Handoff v1`.

## Workflow

### 1. Locate evidence

Find the README, dependency files, entry scripts (`train`, `main`, `eval`, `inference`, `predict`, `run`, `simulate`, `benchmark`), configs, and core algorithm files. Top-level directories are discovery cues only; they are never counted as architecture modules.

For a large repository, inspect the top level and a justified sample of core files. State the sampling boundary. Do not claim full coverage from keyword hits.

### 2. Classify task and implementation stack

Identify the scientific objective, primary framework, data/experiment interface, and main execution path with file or symbol evidence. Mark unsupported inferences explicitly.

### 3. Build the semantic graph

Create one component only when it has a distinct scientific or execution responsibility that belongs in a paper figure. A component may span several files, and one file may implement several components.

For every component record:

- stable `id` and short display `label`;
- `role`:
  - **General ML / Deep Learning**: `input_data`, `encoder_backbone`, `fusion_interaction`, `loss_objective`, `task_head`, `model`, `output`;
  - **Agentic / Interactive**: `reasoning`, `decision`, `deterministic_execution`, `observation`, `memory`, `persistence`, `advisory`, `exception`;
  - **Systems / Modular**: `source`, `scheduler`, `processor`, `storage`, `sink`, `other`;
- `figure_importance`: `primary` or `secondary`;
- evidence pointers such as `path:line`, class, function, test, or config key;
- one-sentence responsibility and explicit non-authority when scientifically important.

Record connections separately. Use `executed`, `advisory`, `feedback`, `persistence`, or `exception` as the connection kind. Do not infer an edge solely because two files import each other.

### 4. Derive visual groups

Group related components by responsibility or narrative stage. Report:

- `semantic_component_count`: number of evidence-backed components;
- `visual_group_count`: number of meaningful regions in the proposed figure;
- `peer_module_count`: largest set of genuinely equivalent sibling components.

These counts help layout planning. None of them selects a palette by itself.

### 5. Emit the handoff

```json
{
  "schema": "academic-figure/SemanticArchitecture@1",
  "source_revision": "<commit-or-unknown>",
  "domain": "<controlled-domain>",
  "evidence_level": "high|partial|sparse",
  "components": [
    {
      "id": "backbone",
      "label": "Encoder Backbone",
      "role": "encoder_backbone",
      "figure_importance": "primary",
      "responsibility": "Extracts multi-scale feature representations.",
      "evidence": ["models/backbone.py:ResNet"]
    }
  ],
  "connections": [
    {
      "from": "input_data",
      "to": "backbone",
      "kind": "executed",
      "label": "raw inputs",
      "evidence": ["models/pipeline.py:forward"]
    }
  ],
  "authority_boundaries": [],
  "semantic_component_count": 1,
  "visual_group_count": 1,
  "peer_module_count": 0,
  "figure_types": ["Overall Framework"],
  "forbidden_claims": ["<claims the figure must not imply>"]
}
```

Controlled domain: `CV`, `NLP`, `Speech/Audio`, `RL`, `Robotics`, `Multimodal`, `TimeSeries`, `Generative`, `Protein/AI4Science`, `GNN/ScientificComputing`, `Systems/Infrastructure`, `ScientificComputing(non-ML)`, or `Other`.

## Sparse evidence

- No README: infer cautiously from code and label the inference.
- No entry point: limit the result to component-level structure.
- No core implementation: report task/stack only and omit unsupported edges.
- Almost empty repository: provide the minimum missing materials instead of inventing an architecture.

## Stop

Stop when the human summary and valid handoff are delivered. Suggest figure planning only when the user wants the next stage.
