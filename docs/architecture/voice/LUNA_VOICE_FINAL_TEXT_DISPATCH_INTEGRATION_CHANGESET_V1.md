# 变更清单：语音主线「切段后最终文本分流」v1

## 新增文件

| 文件 | 说明 |
|------|------|
| `capabilities/voice/runtime/voice_final_text_dispatch_result.py` | `VoiceFinalTextDispatchResult`：统一出口（`request_id`、`session_id`、`dispatch_type`、可选 `bridge_decision` / `long_input_parse_result` / `rejection_result` 等） |
| `capabilities/voice/runtime/voice_final_text_dispatcher.py` | `dispatch_voice_final_text(...)`：分流主入口 |
| `capabilities/voice/runtime/voice_input_length_mode_classifier.py` | 规则版长短模式判定（不接模型） |
| `tests/test_voice_final_text_dispatch_integration_v1.py` | 场景 1–6 + 路由 reject + 待确认分支 + 可观测性 |
| `docs/architecture/voice/LUNA_VOICE_FINAL_TEXT_DISPATCH_INTEGRATION_V1.md` | 集成说明 |
| `docs/architecture/voice/LUNA_VOICE_FINAL_TEXT_DISPATCH_INTEGRATION_CHANGESET_V1.md` | 本文档 |

## 修改文件

| 文件 | 说明 |
|------|------|
| `capabilities/voice/runtime/voice_input_session_manager.py` | 新增 `process_final_text_with_dispatch(...)`，内部调用 `process_final_text` + `dispatch_voice_final_text` |

## 分流规则摘要

1. **白名单短指令优先于长输入拆解**：`shortcut_id` 已命中 → `short_controlled_input`。
2. **长自然语言**（窗口内或任务态下已 accept、且无白名单）：→ `long_task_planning_input`。
3. **有待确认上下文时**，仅 `confirmation_feedback` 命中 → `short_controlled_input`（先于长输入理解）。
4. **长输入拆解只产出 `task_plan_v1`**：不进入 V2 / Final / 执行。
5. **分流可观察**：`dispatch_reason_code`、`notes`、`metadata`。

## 哪些输入进入短链

- 路由 `reject` 以外的 **白名单** 命中（含设备 / 任务 / 问询 / 会话结束 / confirmation 短语）。
- **仅「艾达」唤醒、无正文**（会话激活）。
- **待确认上下文** 下 registry 判定为 `confirmation_feedback` 的输入。

## 哪些输入进入长链

- 已 accept，且 **无** `shortcut_id`，且 **非** 仅唤醒、**非** 噪声占位，且 **未** 被上一条 confirmation 规则截获 → 调用 `run_long_input_task_planning_v1`。

典型：窗口内「先去商场，再找便利店买点吃的」「去医院，路上顺便看看有没有便利店」。

## 哪些会 reject

- 路由层已拒绝（如普通态无唤醒无窗口）。
- 分流层判定的 **纯噪声占位**（极短、无任务语义）。

## 为何本轮仍不是「完整长语音执行系统」

- **不接模型**：长短判定与域分类仍为规则。
- **不接执行**：短链止于 `BridgeDecision` 占位；长链止于 `task_plan_v1`（或结构化 `rejection_needed`）。
- **不跑 V2 / Final / 图书馆**：与 [LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md](./LUNA_VOICE_LONG_INPUT_TASK_PLANNING_V1.md) 边界一致。

本步目标仅是：**在主线内把短链与长链正式分开**，并让长自然语言稳定进入 `task_plan_v1`，为后续接模型与执行层打基础。
