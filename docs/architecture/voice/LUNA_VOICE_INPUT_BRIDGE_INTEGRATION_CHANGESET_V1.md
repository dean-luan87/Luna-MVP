# Luna 语音输入接线 v1 — 变更清单

## 1. 新增或强化的对象

| 路径 | 说明 |
|------|------|
| `capabilities/voice/bridge/voice_input_bridge_adapter.py` | `adapt_voice_input_for_bridge`：反查白名单条目 + reason_code |
| `capabilities/voice/bridge/voice_input_to_bridge.py` | `voice_input_to_bridge_decision`：VoiceInputEvent → BridgeDecision + proposal/query/response |
| `capabilities/voice/bridge/voice_input_core_placeholder.py` | `dispatch_voice_bridge_to_core_placeholder`：主链边界占位，无真实执行 |
| `capabilities/voice/schemas/voice_input_rejection_result.py` | 可追踪 reject 轻量对象 |
| `capabilities/voice/bridge/route_types.py` | 新增 `SESSION_WAKE`、`INPUT_REJECTED` |
| `capabilities/voice/bridge/voice_input_router.py` | 唤醒句对 strip 后正文再匹配白名单 |
| `capabilities/voice/runtime/voice_shortcut_registry.py` | `cf_yes`/`cf_no`；`get_by_id`；单字短语整句匹配防误伤 |
| `tests/test_voice_input_bridge_integration_v1.py` | 接线场景 1–6 + 仅唤醒 |

**小补丁（任务态「暂停/继续」）**：`task_pause`/`task_resume` 增加短语 **「暂停」「继续」**；`dev_pause`/`dev_resume` 改为 **「暂停播报」「继续播报」**（设备显式），使 **`is_task_mode=True`** 时短词优先走 **TaskActionProposal**，与设备播报分流。详见 [LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md](./LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md) §3.1。

## 2. 已接通的 route（摘要）

- **DEVICE_CONTROL** ← 设备类 `shortcut_type=device_control`
- **TASK_LIFECYCLE** ← `task_control`（`task_start_nav` 为 `direct`，其余默认确认降级）
- **TASK_CONTEXT_ENHANCEMENT** ← `task_query` → `TaskContextQuery`
- **CONFIRMATION** ← `confirmation_feedback` + `pending_confirmation_id`（证据语义）
- **FEEDBACK_RESPONSE** ← `session_control`（会话结束）
- **SESSION_WAKE** ← 仅「艾达」、无正文、无 shortcut
- **INPUT_REJECTED** ← 路由 reject
- **RESERVED_OPEN_DIALOGUE** + **reject_or_degrade** ← 窗口内未命中白名单的自由文本（v1 不扩展开放意图）

## 3. 与 Core 的接口位

- **当前**：`dispatch_voice_bridge_to_core_placeholder` 仅返回 `received` + `trace` 字典，证明 **可进入主链边界**。
- **未做**：真实 TaskChain 调度、设备执行、记忆写入。

## 4. 仍未做

- 真实 Core/TaskChain handler 替换 placeholder  
- 完整待确认队列与 `pending_confirmation_id` 生命周期  
- 输出面（TTS/Piper）任何改动  

## 5. 为什么这轮仍不是完整对话系统

仅完成 **受控输入 → Bridge 标准对象 → 占位 Core**，无开放域理解、无多轮对话状态机、无情感与长语音 LLM；Voice 宪法中的 **proposal/query/response** 仍由 Core 裁决。

---

说明文档：[LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md](./LUNA_VOICE_INPUT_BRIDGE_INTEGRATION_V1.md)
