# Luna 语音主线：切段后最终文本分流集成 v1

> **前置阅读**：[LUNA_VOICE_INPUT_MAINLINE_V1.md](./LUNA_VOICE_INPUT_MAINLINE_V1.md)、[LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md](./LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md)、[LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md](./LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md)。

## 1. 为什么要在 `process_final_text` 后加分流层

此前 **短输入主链**（`VoiceInputEvent` → `voice_input_to_bridge_decision` → `BridgeDecision`）与 **长输入拆解 v1**（`run_long_input_task_planning_v1` → `task_plan_v1`）各自可用，但主线出口不统一：窗口内非白名单长句会落入 `RESERVED_OPEN_DIALOGUE`，与「长句应进任务拆解」的目标不一致。

在 **`process_final_text` 已产出标准 `VoiceInputEvent` 之后** 增加 **统一分流**，实现：

- **单出口对象** `VoiceFinalTextDispatchResult`，便于白盒、日志、后续 Bridge / 图书馆只读一处。
- **短链 / 长链 / reject** 三类互斥，上层不必猜测「这次是 Bridge 还是 task_plan」。
- **不改变** `VoiceInputEvent` 与 `task_plan_v1` 的结构；长链仍止于规划，不接执行。

## 2. 短输入链与长输入链如何区分（规则版，不接模型）

分流判定在 `voice_input_length_mode_classifier.classify_voice_input_length_mode`，顺序写死：

| 优先级 | 结果 | 条件 |
|--------|------|------|
| 1 | `rejected_input` | 路由层已 `reject`（如无唤醒且无窗口等） |
| 2 | `short_controlled_input` | 仅唤醒词、无正文（会话激活 / SESSION_WAKE） |
| 3 | `short_controlled_input` | 白名单命中（`shortcut_id` 非空） |
| 4 | `short_controlled_input` | **有待确认上下文** 且 registry 命中 `confirmation_feedback` |
| 5 | `rejected_input` | 纯噪声占位（极短、无语义） |
| 6 | `long_task_planning_input` | 其余已 accept、非受控短句 → `run_long_input_task_planning_v1` |

长句特征（多动作、顺序/条件/伴随词等）由 **长输入拆解器内部规则** 处理；分流层对「非白名单自然语言」默认走长链，避免再冒充短控制命令。

## 3. 为什么白名单与 confirmation 优先

- **白名单短指令**（如「暂停任务」「到哪了」）必须稳定进入 Bridge，**不得**因句长或包含逗号误送入长输入拆解器。
- **待确认上下文** 下，用户先说「是 / 不是 / 不用了」等，语义是 **确认或修正**，必须先走 **confirmation 证据链**，不能先当长任务规划。

实现上：路由已命中白名单则 `shortcut_id` 已设；若上游未写入 shortcut 但声明 `pending_confirmation_context=True`，则用 registry 再匹配一轮 `confirmation_feedback`。

## 4. 长输入当前只到 `task_plan_v1`

- 分流为 `long_task_planning_input` 时，仅调用 `run_long_input_task_planning_v1`。
- 产出 `VoiceLongInputParseResult`（含 `task_plan_v1` 或 `rejection_needed` 等），**不**进入 V2、Final、执行器、图书馆协同。

## 5. 本轮明确不做什么

- 不接 **模型** 做长短判定或意图分类（判定为规则）。
- 不实现 **V2 / Final** 任务计划阶段。
- 不改变 **输出侧** TTS/播报策略。
- 不提供 **长语音采集优化** 建议。

## 6. 主入口与接线

| 组件 | 路径 |
|------|------|
| 统一结果 | `capabilities/voice/runtime/voice_final_text_dispatch_result.py` |
| 分流主入口 | `capabilities/voice/runtime/voice_final_text_dispatcher.py` |
| 长短判定 | `capabilities/voice/runtime/voice_input_length_mode_classifier.py` |
| 会话便捷方法 | `VoiceInputSessionManager.process_final_text_with_dispatch(...)` |

调用顺序：**先** `process_final_text`（或直接用 `process_final_text_with_dispatch`），**再**由 dispatcher 决定短链 `voice_input_to_bridge_decision` 或长链 `run_long_input_task_planning_v1`。

## 7. 可观测性

`VoiceFinalTextDispatchResult` 含 `dispatch_reason_code`、`notes`、`metadata`（含 `length_mode_reason_code` 等），用于说明 **为何短链 / 为何长链 / 为何拒绝**。
