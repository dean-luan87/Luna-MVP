# Luna 任务协议与模型接入门 v1

> **结论（顺序）**：**先定协议和系统语言 → 再接模型 → 最后再调效果。**  
> 当前阶段做的是 **系统**，不是 demo；**系统语言的主导权必须在实现侧**，不能让模型先定义 schema。

> **系统规格基线（定稿，接模型前必读）**  
> - [LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md](./LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md)（任务域分类表 v1）  
> - [LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md](./LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md)（内部任务指令映射表 v1）  
> - [LUNA_TASK_PLAN_V1_V2_FINAL_V1.md](./LUNA_TASK_PLAN_V1_V2_FINAL_V1.md)（task_plan_v1 / v2 / final）

---

## 1. 为什么不能先接模型

缺的不是「一个会理解长语音的模型」，而是：**模型产出之后，要吐什么、系统怎么接、哪些字段能进主链。**

若先接模型，典型会出现：

| # | 问题 | 后果 |
|---|------|------|
| 1 | **模型输出无锚点** | 自然语言很多，但未定义必填/候选/可映射系统指令/仅说明性文字 → 接进来后要 **返工 schema** |
| 2 | **系统边界被模型带着跑** | 未先定义 `task_plan_v1/v2/final`、`knowledge_collaboration`、`task_optimization` 时，模型容易越权「直接帮你规划」→ **主链与治理边界混乱** |
| 3 | **白盒与图书馆无法观察** | 对象未定 → 抽链、归档、优化比对、经验提炼 **无法稳定落地** |
| 4 | **误把模型效果当系统能力** | 换模型或换 prompt 后 **整套逻辑散掉**；内核仍空 |

---

## 2. 正确顺序（三步）

### 第一步：先定系统协议（模型接入前必须完成）

1. [任务域分类表 v1](./LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md)  
2. [内部任务指令映射表 v1](./LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md)  
3. [task_plan_v1 / v2 / final](./LUNA_TASK_PLAN_V1_V2_FINAL_V1.md) + `TaskPlan` / `TaskPlanItem` / `PlanDelta`  
4. **知识协同（knowledge_collaboration）**：输入/输出形状见下文与 `shared/schemas/knowledge_collaboration.py`  
5. **任务优化（task_optimization）**：V1→V2 增强与可追踪优化，见下文与 `shared/schemas/task_optimization.py`  
6. **执行 / 拒绝 / 确认** 的判定边界：见 [§4](#4-执行--拒绝--确认-判定边界-v1)

### 第二步：再接模型

模型职责 **仅限于**：把长语音 / 长文本 **翻译成协议要求的结构化候选**（parser / 候选生成器），**不是裁判**。

### 第三步：效果调优

参数量、多模型、字段错误率、补确认策略等，均在 **schema 与边界已定** 之后进行。

---

## 3. knowledge_collaboration（协议含义）

**含义**：在 **不改变用户明确字面意图为唯一事实源** 的前提下，将 **记忆、环境、经验** 作为 **增强信号** 注入，用于生成 **task_plan_v2** 的输入侧协作结果。

**约束**：

- 只 **增强**，不 **偷偷覆盖** 用户明确输入（与 task_plan 文档硬规则一致）。  
- 产出应可写入 `TaskPlan` 的 `metadata` / `optimization_reason` / `plan_delta`，供白盒与图书馆消费。

**工程占位**：`KnowledgeCollaborationContext` / `KnowledgeCollaborationResult`（`shared/schemas/knowledge_collaboration.py`）。

---

## 4. task_optimization（协议含义）

**含义**：在 **task_plan_v1** 基础上，生成 **task_plan_v2** 时所记录的 **可追踪优化决策**（重排、补字段、建议确认等），与 **`PlanDelta`** 对齐。

**约束**：

- **不直接执行**；高风险或重排需 **`confirmation_needed` / `requires_confirmation`**。  
- 与 **内部指令映射表** 中的 `task_chain_impact_level`、`requires_confirmation_default` 一致审查。

**工程占位**：`TaskOptimizationRecord`（`shared/schemas/task_optimization.py`）。

---

## 5. 执行 / 拒绝 / 确认 判定边界 v1

| 判定 | 谁负责 | 输入依据 | 输出形态 |
|------|--------|----------|----------|
| **可执行** | **Core / TaskChain**（非 Voice，非模型） | `task_plan_final` + 治理与设备策略 | 进入执行管线 |
| **拒绝** | Core / 治理 | `unsupported_or_reject`、越权、未接入能力、`InstructionMappingRecord` 不允许的模式 | `should_reject`、可追溯 reason；**不静默** |
| **确认** | Core / 确认链 | `requires_confirmation_default`、高风险设备/任务、V2 与 V1 不一致且 `confirmation_needed` | 待确认队列 + `ConfirmationResponse` 证据链 |

**原则**：Voice 与模型只提交 **候选**；**裁决权** 在 Core/TaskChain（与 Voice 宪法一致）。

---

## 6. 与现有文档索引

| 文档 / 代码 | 作用 |
|-------------|------|
| `LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md` | 8 域 + 分类规则 |
| `LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md` | 系统指令 + 治理字段 |
| `LUNA_TASK_PLAN_V1_V2_FINAL_V1.md` | 三层计划 + plan_delta + 硬规则 |
| `TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md` | 任务链 × 主链 |
| `shared/schemas/task_plan.py` | `TaskPlan`、`PlanDelta` |
| `shared/schemas/instruction_mapping.py` | `InstructionMappingRecord` |
| `shared/schemas/knowledge_collaboration.py` | 知识协同占位 |
| `shared/schemas/task_optimization.py` | 任务优化占位 |

---

## 7. 一句话判断

**先做结构，再接模型。**  
模型接入时只需 **对着 schema 吐结构**；系统边界、可观察性与可替换性才有保障。
