# Luna 语音长输入拆解接入 v1

> **状态**：长输入在系统内的 **第一层结构化任务计划**（`task_plan_v1`）骨架；**不接模型**、**不生成 V2/Final**。  
> **任务规格基线**：[LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md](../task/LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md)、[LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md](../task/LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md)、[LUNA_TASK_PLAN_V1_V2_FINAL_V1.md](../task/LUNA_TASK_PLAN_V1_V2_FINAL_V1.md)、[LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md](../task/LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md)。  
> **语音输入与接线**：[LUNA_VOICE_INPUT_MAINLINE_V1.md](./LUNA_VOICE_INPUT_MAINLINE_V1.md)、[LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md](./LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md)。

## 1. 为什么在输入接线后先接长输入拆解骨架

输入主线与 Bridge 已能产出 `VoiceInputEvent` 与 `BridgeDecision`，但 **长句** 尚未落 **`task_plan_v1`**。本阶段把「切段后的长文本」接入 **域分类 → 指令映射 → 原始任务计划**，使后续模型只需 **填充/对齐** 既有 schema，而非定义系统语言。

## 2. 当前只做：分类 → 映射 → task_plan_v1

固定顺序（**不可颠倒**）：

1. `DomainClassificationResult`（规则版分类器）  
2. `VoiceLongInputInstructionCandidate[]`（白名单指令候选）  
3. `TaskPlan`（`plan_version="v1"`）

入口：`capabilities/voice/bridge/voice_long_input_task_planner.py` → `run_long_input_task_planning_v1`。

## 3. 当前不做

- 真实模型接入  
- `task_plan_v2` / `task_plan_final`  
- 图书馆/知识协同 **真实调用**（仅预留位）  
- 自动确认/执行  
- 情感对话、自由闲聊  

## 4. 颗粒度与关系限制（v1）

- 主任务 1 个 + 次任务 0～2 个；**超过 3 个分段** → `clarification_needed`，不生成完整计划。  
- 关系：`sequential` / `conditional` / `accompanying`（由候选 `relation_hint` 表达）；**不做**复杂 DAG。

## 5. 预留的协同增强接口位

`TaskPlan`（v1）上：

- `knowledge_collaboration_pending = true`  
- `task_optimization_pending = true`  
- `next_stage = "knowledge_collaboration_and_optimization"`  

表明下一阶段从 **V1 结果** 继续，而非推翻本链。

## 6. 模块索引

| 模块 | 职责 |
|------|------|
| `voice_long_input_task_planner.py` | 协调器入口 |
| `voice_long_input_domain_classifier.py` | 规则域分类 |
| `voice_long_input_instruction_mapper.py` | 指令候选映射 |
| `voice_long_input_task_plan_builder.py` | 组装 `task_plan_v1` |
| `voice_long_input_parse_result.py` | 总结果包装 |
| `voice_long_input_instruction_candidate.py` | 单条指令候选 |

---

变更清单：[LUNA_VOICE_LONG_INPUT_TASK_PLANNING_CHANGESET_V1.md](./LUNA_VOICE_LONG_INPUT_TASK_PLANNING_CHANGESET_V1.md)
