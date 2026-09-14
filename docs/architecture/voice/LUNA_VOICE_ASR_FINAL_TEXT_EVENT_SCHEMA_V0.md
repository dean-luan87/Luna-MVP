# LUNA Voice — ASR Final Text Event Schema v0

## 规范来源

- 代码真源：`capabilities/voice/input/asr_final_text_event_contract_v0.py`（`ASRFinalTextEventV0` / `ASRFinalTextHardAuditV0`）。
- 本文件为架构侧 **人类可读** 摘要。

## JSON 形状（逻辑）

| 字段 | 类型 | 说明 |
|------|------|------|
| `event_id` | string | ASR 事件唯一 id |
| `event_type` | const | 固定 `voice.asr.final_text` |
| `request_id` | string | 请求级关联（对齐 RequestTrace） |
| `trace_id` | string | 分布式追踪关联 |
| `session_id` | string | 语音输入会话 |
| `utterance_id` | string | 单次用户发声单元 |
| `source_audio_ref` | string | 音频引用（URI/句柄；不含裸文件系统绝对路径要求） |
| `provider_id` | string | ASR provider 逻辑 id |
| `language` | enum | `zh` \| `en` \| `mixed` \| `unknown` |
| `text` | string | **ASR 原文，必须保留** |
| `normalized_text` | string \| null | 可为 null；**本阶段不做语义改写** |
| `confidence` | number | 0.0–1.0 约定，具体校准后续 phase |
| `is_final` | boolean | 协议层是否终结帧 |
| `asr_status` | enum | `final` \| `no_speech` \| `timeout` \| `cancelled` \| `provider_error` \| `low_confidence` |
| `latency_ms` | integer | ASR 侧耗时 |
| `hard_audit` | object | 见下 |

### `hard_audit`

| 字段 | 类型 | 说明 |
|------|------|------|
| `qianwen_invoked` | bool | ASR 路径必须为 **false** |
| `tts_invoked` | bool | 必须为 **false** |
| `playback_invoked` | bool | 必须为 **false** |
| `navigation_action` | string \| null | 必须为 **null**（ASR 不触发导航） |
| `midplatform_invoked` | bool | 必须为 **false** |
| `world_write_invoked` | bool | 必须为 **false** |

## 与下游的关系

- **不得**在 `asr_status ∈ {no_speech, timeout, cancelled, provider_error}` 时将 `text` 送入 Qianwen（见状态机与 fallback 文档）。
- **`low_confidence`**：仅允许 **confirm / repeat / suppress** 路径，**本阶段不定义播报**。
