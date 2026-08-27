---
name: academic-repo-analyzer
description: Analyze ML, AI4Science, and research repositories into an evidence-backed semantic architecture graph for paper figure planning. Use for repository understanding or repo-to-figure tasks; do not use directory counts as visual modules or palette signals.
metadata:
  version: "1.4.0"
  stages: [research, review]
---

# Academic Repo Analyzer

Produce a concise repository understanding document plus a machine-readable **Semantic Architecture Handoff v1**. The handoff describes scientific roles and executable relationships, not the repository's folder layout.

Read `keywords.md` only when task or framework classification is uncertain. Read `references/missing-info-policy.md` when evidence is sparse.

## Input contract

- Prefer: repository path, README, dependencies, entry points, core model/algorithm files, configs, and tests that establish behavior.
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
6. Two to four figure suggestions using the controlled types.
7. `Semantic Architecture Handoff v1`.

Controlled figure types: `Overall Framework`, `Network Architecture`, `Module Detail`, `Comparison/Ablation`, `Data Behavior`.

## Workflow

### 1. Locate evidence

Find the README, dependency files, entry scripts (`train`, `main`, `eval`, `inference`, `predict`, `run`, `simulate`, `benchmark`, `demo`, `app`, `serve`), configs, core packages, and relevant tests. Top-level directories are discovery cues only; they are never counted as architecture modules.

For a large repository, inspect the top level and a justified sample of core files. State the sampling boundary. Do not claim full coverage from keyword hits.

### 2. Classify task and implementation stack

Identify the scientific objective, primary framework, data/experiment interface, and main execution path with file or symbol evidence. Mark unsupported inferences explicitly.

### 3. Build the semantic graph

Create one component only when it has a distinct scientific or execution responsibility that belongs in a paper figure. A component may span several files, and one file may implement several components.

For every component record:

- stable `id` and short display `label`;
- `role`: `input`, `reasoning`, `decision`, `model`, `deterministic_execution`, `observation`, `memory`, `persistence`, `output`, `exception`, or `other`;
- `figure_importance`: `primary` or `secondary`;
- evidence pointers such as `path:line`, class, function, test, or config key;
- one-sentence responsibility and explicit non-authority when scientifically important.

Record connections separately. Use `executed`, `advisory`, `feedback`, `persistence`, or `exception` as the connection kind. Do not infer an edge solely because two files import each other.

For agentic systems, identify who may propose, compute, commit observations, update state, stop, or call an external system. These authority boundaries are often more figure-worthy than package boundaries.

### 4. Derive visual groups

Group related components by responsibility or narrative stage. Report:

- `semantic_component_count`: number of evidence-backed components;
- `visual_group_count`: number of meaningful regions in the proposed figure;
- `peer_module_count`: largest set of genuinely equivalent sibling components.

These counts help layout planning. **None of them selects a palette by itself.** A four-stage timeline, four peer encoders, and four authority domains require different visual treatment.

### 5. Emit the handoff

Use JSON so downstream skills do not reinterpret free-form Markdown:

```json
{
  "schema": "academic-figure/SemanticArchitecture@1",
  "source_revision": "<commit-or-unknown>",
  "domain": "<controlled-domain>",
  "evidence_level": "high|partial|sparse",
  "components": [
    {
      "id": "policy",
      "label": "Typed Policy",
      "role": "decision",
      "figure_importance": "primary",
      "responsibility": "Proposes the next typed action.",
      "evidence": ["path/to/file.py:ClassName"]
    }
  ],
  "connections": [
    {
      "from": "policy",
      "to": "harness",
      "kind": "advisory",
      "label": "typed proposal",
      "evidence": ["path/to/controller.py:function"]
    }
  ],
  "authority_boundaries": ["<short evidence-backed statement>"],
  "semantic_component_count": 0,
  "visual_group_count": 0,
  "peer_module_count": 0,
  "figure_types": ["Overall Framework"],
  "forbidden_claims": ["<claims the figure must not imply>"]
}
```

Controlled domain: `CV`, `NLP`, `Speech/Audio`, `RL`, `Robotics`, `Multimodal`, `TimeSeries`, `Generative`, `Protein/AI4Science`, `GNN/ScientificComputing`, `ScientificComputing(non-ML)`, or `Other`.

The example is structural, not content to copy. Populate only evidence-backed values; do not leave fabricated sample components in the final handoff.

## Sparse evidence

- No README: infer cautiously from code and label the inference.
- No entry point: limit the result to component-level structure.
- No core implementation: report task/stack only and omit unsupported edges.
- Almost empty repository: provide the minimum missing materials instead of inventing an architecture.

## Stop

Stop when the human summary and valid handoff are delivered. Suggest figure planning only when the user wants the next stage.
