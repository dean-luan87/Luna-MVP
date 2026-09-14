# Luna Decision Validation Layer — Concept Planning v1

**Phase:** Phase-P1-Midplatform-Luna-Decision-Validation-Layer-Planning-v1-001  
**Layer:** L2.5 Decision Validation（Agent Planning 与 Tool OS 之间）  
**Status:** Planning only — no teacher models, no network, no tool execution

## 1. 为什么需要 L2.5

L2 Agent Planning 输出 `agent_plan_candidate`：目标、步骤、工具计划、handoff 候选。  
在进入 L3 Tool OS 之前，Luna 需要**独立验证**该计划是否合理——这不是重新决策，而是执行前自检。

```
L0 Constitution
        ↓
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
L2.5 Decision Validation Layer   ← 本阶段
        ↓
L3 Tool Operating System
        ↓
L4 Tools / Models
```

## 2. 核心原则

Decision Validation Layer **不是决策者**：

- 不生成最终计划
- 不替代 Agent Planning
- 不直接修改 `selected_plan_candidate`

它只回答：

1. 当前 plan 是否合理？
2. 是否存在冲突？
3. 是否需要额外信息？
4. 是否允许进入 Tool OS？
5. 是否需要人工确认？

## 3. 与相邻层边界

| 上游 L2 | L2.5 Validation | 下游 L3 |
|---------|-----------------|---------|
| 输出 agent_plan_candidate | 消费 plan + situation | 接收 readiness handoff |
| 拥有 selected plan | 不拥有 plan | 执行 admission / runner |
| 生成 tool plan | 验证 tool plan 合理性 | 实际执行工具 |

## 4. 验证源演进路线（本阶段 vs 未来）

**本阶段（单验证源）：**

```
Policy Validator + Case Library Validator + Rule Validator
        ↓
validation_candidate
```

**未来扩展（不重构架构）：**

```
Validation Source:
    policy
    case_library
    human_feedback
    single_teacher_model      ← 第二阶段
    multiple_teacher_models   ← 第三阶段
```

多 Teacher 交叉验证时，**验证层主人仍是 Luna 规则与经验体系**，不会出现「几个模型吵架谁说了算」——Teacher 只提供 validation evidence candidate。

## 5. 输入 / 输出

### 输入：`decision_validation_input_candidate`

- `agent_plan_candidate`
- `situation_understanding_candidate`
- `policy_context`
- `case_library_candidates`（本阶段可为空）
- `user_goal_candidate_optional`

### 输出：`decision_validation_candidate`

- `validation_status_candidate`: `validated_candidate` | `needs_review` | `blocked_candidate` | `insufficient_information`
- `validation_result`: alignment score, risk, conflicts, contradictions
- `validation_reason_candidates`
- `tool_execution_readiness_candidate`（非执行许可，是 handoff 就绪候选）
- `alternative_plan_candidates`（建议备选，不改变 Agent Planning 所有权）
- `trace_refs`

## 6. 验证维度

| 维度 | 说明 |
|------|------|
| Situation alignment | Plan 是否符合 L1 处境 |
| Constitution / Policy | 违反则 blocked |
| Missing information | Plan 是否 addressing 当前缺口 |
| Noop discipline | noop 是否合理 |
| Risk sensitivity | 高风险场景提高验证要求 |
| User goal conflict | 用户目标与视觉默认冲突 → needs_review |

## 7. 本阶段禁止

- 真实 Gemini / Qwen / GPT / VLM 验证
- 联网、执行工具、触发 runner、写 fact
- 覆盖 Agent Planning selected plan
- 多模型仲裁（留给未来阶段）

## 8. 下一阶段建议

**优先：** Phase-P1-Midplatform-Luna-Decision-Validation-Layer-DryRun-v1-001  
接入 L1 → L2 → L2.5 链，验证 Luna 在执行前主动检查自己的计划。
