# LUNA Voice — ASR Boundary Contract v0（Phase-VoiceInteraction-Readiness-002）

## 目的

冻结 **ASR 子系统与 voice input session 之间** 的职责边界，使 `request_id` / `trace_id` / `session_id` / `utterance_id` / `final_text` 有统一入口合同，**不接**真实 ASR runtime。

## ASR **只负责**

- **Audio in → transcript candidate**：字节流/帧 → 文本候选（含 partial）。
- **Partial transcript**：流式中间结果（不触发下游 Qianwen / TTS）。
- **Final transcript**：终结帧或会话段结束时的定稿文本（见 `ASRFinalTextEventV0`）。
- **Confidence / latency / provider status**：可观测性与选型依据。
- **终结性状态信号**：`no_speech` / `timeout` / `cancelled` / `provider_error` / `low_confidence`（与状态机一致）。

## ASR **不负责**

- **语义解释**、**意图判断**、**任务决策**（归属 semantic / intent / task 层）。
- **直接调用 Qianwen**、**直接调用 TTS**、**直接播放**。
- **修改 session 之外的主链状态**（除向 session 层上报 ASR 事件与 trace 字段外，不写入业务世界状态）。

## 与 session 的边界

- ASR **产出** `ASRFinalTextEventV0`（或等价序列化）；**不**决定「是否进入 Qianwen」。
- **Voice input session** 持有 `session_id`、utterance 生命周期；ASR **必须**携带 `session_id` + `utterance_id` 以便 trace 拼接。
- **仅**当状态机进入 **`final_text_ready`** 且 `asr_status == final`（或合同允许的等价组合）时，session 才允许将文本交给语义层（见 `LUNA_VOICE_ASR_STATE_MACHINE_V0.md`）。

## 硬约束（本阶段）

- **不**接真实 ASR provider；**不**调用 Whisper；**不**改 `capabilities/voice/runtime/*` 行为（本 phase 仅文档 + 合同类型）。
