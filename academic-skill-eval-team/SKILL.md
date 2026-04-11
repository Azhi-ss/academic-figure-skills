---
id: academic-skill-eval-team
name: Academic Skill Eval Team
version: 1.0.0
description: Use this skill whenever the user wants to evaluate a skill or skill pack with an agent team, audit trigger phrases, inspect workflow completeness, stress-test prompt robustness, score output quality, or when the user says "测评这个skill", "创建一个agent team测评", "评估这个 skill pack", "skill evaluation", "evaluate this skill", "agent team review", or "benchmark my skill".
stages: [review, research]
tools: [bash]
---

# Academic Skill Eval Team — Skill 多代理测评团队

为单个 `skill` 或整个 `skill pack` 组织一个“多代理评测团队”，从触发词、指令质量、工作流完整性、输出规范、鲁棒性和打包一致性六个维度给出结构化测评结论。

## 核心理念

测评不是简单“夸好不好”，而是回答 4 个问题：

1. 这个 skill 会不会被正确触发？
2. 被触发后，执行流程是否完整、清晰、可落地？
3. 输出是否具体、稳定、可复用？
4. 作为一个可发布 skill，它的包装与协作链路是否一致？

必须基于仓库证据进行判断，禁止空泛评价。

## Agent Team 组成

| 角色 | 关注点 | 必做事项 |
|------|--------|---------|
| **Agent 1: Trigger Auditor** | 触发词与调用时机 | 检查 `manifest.json` 与 `SKILL.md` 的触发场景是否一致，是否覆盖中英双语，是否容易误触发/漏触发 |
| **Agent 2: Workflow Auditor** | 指令结构与执行流程 | 检查 skill 是否包含清晰步骤、边界条件、输入要求、与其他 skill 的衔接 |
| **Agent 3: Output Judge** | 输出模板与可交付性 | 检查输出格式是否稳定、信息是否足够、是否能直接被下游使用 |
| **Agent 4: Red-Team Tester** | 鲁棒性与失败模式 | 设计边界输入、模糊请求、缺信息请求，判断 skill 是否会跑偏、过度脑补或漏掉关键约束 |
| **Agent 5: Pack Integrator** | 整包一致性 | 检查 `manifest.json`、`README.md`、`CHANGELOG.md`、各 skill 描述是否一致，评估工作流配合是否顺畅 |

如果用户只评测单个 skill，仍然保留 5 个角色，但把重点集中到目标 skill；如果用户评测整个 pack，则逐个 skill 给出结论，并补充系统级评价。

## 工作流程

### Step 1: 明确评测对象

先识别用户要测评的是：

- 单个 `SKILL.md`
- 某个技能目录
- 整个 skill pack
- 一个新草案/尚未注册的 skill

若用户没有明确对象，默认评测“当前仓库中最相关的 skill 或整个 pack”。

### Step 2: 收集评测证据

至少检查以下材料：

- `manifest.json`
- 目标 skill 的 `SKILL.md`
- `README.md`
- `CHANGELOG.md`（如存在）
- `examples/`、`docs/` 中与目标 skill 强相关的示例（如存在）

必须区分以下三类问题：

1. **Skill 提示词设计问题**：流程缺失、模板不清、边界不明
2. **包装/注册问题**：manifest、版本、触发词、路径不一致
3. **工作流协同问题**：上下游 skill 之间输入输出难以衔接

### Step 3: 进行 5 代理分工审查

#### Agent 1: Trigger Auditor

重点检查：

- `manifest.json` 的 `trigger_phrases` 是否覆盖自然表达
- `SKILL.md` description 是否准确描述触发条件
- 是否存在过宽触发词导致误激活
- 是否存在过窄触发词导致难以发现
- 中英双语触发是否平衡

#### Agent 2: Workflow Auditor

重点检查：

- 是否有明确的 step-by-step 流程
- 是否定义了输入前提、缺失信息时如何处理
- 是否说明默认策略、可选分支、停止条件
- 是否告诉模型先分析再输出，而不是直接生成结论
- 是否能与其他 skill 串联

#### Agent 3: Output Judge

重点检查：

- 是否有标准输出结构
- 输出字段是否足够让用户直接使用
- 是否有清晰的表格、模板或清单
- 输出是否可被下游 skill 消费
- 是否避免只给空泛建议

#### Agent 4: Red-Team Tester

至少构造 3 类挑战输入：

1. **模糊请求**：用户目标不完整，仅给一句话
2. **缺信息请求**：缺少论文、图片、仓库、配色等关键输入
3. **混合请求**：多个目标混在一起，容易偏题

对每类输入都要判断：

- skill 会如何响应
- 是否会出现幻觉式补全
- 是否会跳过必要澄清
- 是否会输出不可执行结果

#### Agent 5: Pack Integrator

重点检查：

- `manifest.json`、`README.md`、`SKILL.md` 的版本和描述是否一致
- 新 skill 是否融入现有工作流
- 是否需要在 README 中暴露该 skill 的用途
- 是否存在路径、命名、术语不一致
- 整个 pack 是否形成清晰的“输入 → 分析 → 输出”闭环

### Step 4: 评分

每个维度按 `1-5` 分打分，并说明理由：

| 维度 | 说明 |
|------|------|
| **Discoverability** | 触发词与 skill 定位是否清晰、易发现 |
| **Instruction Quality** | 指令是否具体、结构化、少歧义 |
| **Workflow Completeness** | 输入、步骤、分支、边界条件是否完整 |
| **Output Usefulness** | 输出是否稳定、具体、能直接交付 |
| **Robustness** | 对模糊/缺失/混合输入是否稳健 |
| **Pack Consistency** | 与 manifest、README、上下游技能是否一致 |

评分建议：

- `5` = 可直接发布，只有轻微优化项
- `4` = 总体可靠，存在少量中等优先级改进项
- `3` = 可用但不稳，发布前建议修正关键问题
- `2` = 问题较多，容易误触发或输出不稳定
- `1` = 结构性缺陷明显，不建议发布

### Step 5: 形成结论

最终必须给出：

1. 总评等级：`可直接发布 / 小修后发布 / 需要重构后再评测`
2. 总分与分项得分
3. 每个代理的主要发现
4. `Top 3` 高优先级修改建议
5. 可直接复测的 challenge prompts

## 输出格式

严格按以下模板输出：

---

## Skill Eval Report

### 1. Scope
- **评测对象**：
- **评测范围**：单 skill / 整包
- **证据来源**：

### 2. Overall Verdict
- **结论**：可直接发布 / 小修后发布 / 需要重构后再评测
- **总分**：X/30
- **一句话总结**：

### 3. Scorecard

| 维度 | 分数 | 结论 | 证据 |
|------|------|------|------|
| Discoverability | X/5 |  |  |
| Instruction Quality | X/5 |  |  |
| Workflow Completeness | X/5 |  |  |
| Output Usefulness | X/5 |  |  |
| Robustness | X/5 |  |  |
| Pack Consistency | X/5 |  |  |

### 4. Agent Findings

#### Agent 1: Trigger Auditor
- 优点：
- 问题：
- 建议：

#### Agent 2: Workflow Auditor
- 优点：
- 问题：
- 建议：

#### Agent 3: Output Judge
- 优点：
- 问题：
- 建议：

#### Agent 4: Red-Team Tester
- 挑战输入 1：
- 挑战输入 2：
- 挑战输入 3：
- 主要风险：

#### Agent 5: Pack Integrator
- 一致性问题：
- 工作流问题：
- 建议：

### 5. Priority Fixes
1. 
2. 
3. 

### 6. Retest Prompts
- 
- 
- 

---

## 质量标准

一个高质量的测评报告必须满足：

- 所有结论都有仓库证据支撑
- 能区分“skill 本身的问题”和“打包文档的问题”
- 不只指出问题，还给出可执行修复建议
- 能指出最可能失败的用户输入场景
- 对单 skill 和整包都适用

## 注意事项

- 不要只因为内容长就给高分，重点看是否可执行
- 不要把 README 写得好等同于 skill 设计得好
- 不要因为示例漂亮就忽略边界条件
- 如果发现版本不一致、触发词不一致、工作流断裂，必须明确指出
- 如果证据不足，要明确写出“证据不足”，不要臆测

## 与其他技能的关系

此 skill 不负责生成论文配图内容，而是负责评估其他 skill 的质量。它适合在以下场景使用：

- 新 skill 发布前做一次结构化评审
- 对已有 skill 做回归检查
- 检查整个 pack 的协作闭环是否完整
- 在开源发布前发现触发词、README、版本、输出模板等问题
