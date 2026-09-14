# Luna 长语音输入模式与情感引擎预留 v1.1

## 1. 长语音入口 ≠ 任务入口

长语音处理模块必须同时服务任务链与**后续情感引擎**。非任务类叙述、情绪、背景**不得**被当作无效输入丢弃，否则情感引擎接入时入口已被堵死。

## 2. 三大类输入

| 类型 | 含义 | 当前阶段 |
|------|------|----------|
| **任务型** | 有明确动作目标，可映射系统任务，可生成 `task_plan_v1` | **主处理** |
| **混合型** | 同时含任务片段与非任务片段（情绪/背景） | 任务部分走拆解链；非任务进 `non_task_payload` |
| **非任务型** | 倾诉、叙述、无明确任务 | **不生成任务计划**、不 reject；占位域 + 预留出口 |

## 3. 总分流链（v1.1）

```
长文本
  → analyze_long_voice_input_mode（规则）
  → task_only | mixed_task_and_non_task | non_task_only
  → 非任务且无语义任务段：non_task_dialogue_future + non_task_payload
  → 否则：对「任务子串」跑 classify → map → task_plan_v1（与 v1 一致）
```

实现：`capabilities/voice/bridge/voice_long_input_mode_judgement.py`、`run_long_input_task_planning_v1`。

## 4. 解析结果新增字段

`VoiceLongInputParseResult` 含：

- **`input_mode_judgement`**：`mode`、`has_task_content`、`has_non_task_content`、`should_generate_task_plan`、`should_preserve_non_task_payload`
- **`non_task_payload`**：`exists`、`segments[]`（`emotional_context` / `narrative` / `other`）、`handoff_candidate`（默认 `emotion_engine_future`）
- **`mixed_input_flag`**：与 `mode == mixed_task_and_non_task` 一致，便于白盒/日志

## 5. 占位域 `non_task_dialogue_future`

见 `shared/schemas/task_domain_v1.py` 中 `NON_TASK_DIALOGUE_FUTURE`。元数据含 `should_execute_task_plan: false`、`handoff_candidate: emotion_engine_future`、`no_task_plan_generated: true`。

## 6. 模型 / 执行边界（与情感引擎对齐）

**当前规则层只做**：输入模式判断、任务域分类、参数与约束抽取、指令候选、`task_plan_v1`、非任务切分与保留。

**不做**：情感安抚、陪聊、情绪价值输出、最终执行裁决、V2/Final 优化。

## 7. 临时问询 vs 插入任务（概念）

- **一次性临时问询**（不改任务链）：仍由短链 / `no_task_observation` 等既有路径处理；**不**在本模块混写为 `task.insert_temporary`。
- **临时插入任务**（需恢复点）：由任务链协议处理；本文件仅保留类型边界说明，实现不在本轮。
