# LUNA Voice — ASR Trace / Replay / Audit Contract v0

## 范围

定义 **未来 ASR runtime** 在 trace / replay / 导出时必须携带的字段集合。**本阶段不**写真实 runtime trace，不接线。

## 必备字段（导出行 / replay bundle）

| 字段 | 说明 |
|------|------|
| `request_id` | 与 RequestTrace 对齐 |
| `trace_id` | 跨模块拼接 |
| `session_id` | voice input session |
| `utterance_id` | 单次发声 |
| `source_audio_ref` | 音频溯源 |
| `provider_id` | ASR provider |
| `asr_status` | 终结状态（含错误类） |
| `partial_count` | partial 更新次数（无流式则为 0） |
| `final_text` | 定稿文本；无文本时为空串并与状态一致 |
| `confidence` | 最终或聚合置信度 |
| `latency_ms` | ASR 总耗时 |
| `fallback_reason` | 如切换 provider / suppress 的原因码；无则 null |
| `hard_audit` | 与 `ASRFinalTextHardAuditV0` 同形 |

## Replay 最小可复现包（建议）

- `ASRFinalTextEventV0` 完整 JSON  
- 同 utterance 的 **partial 序列摘要**（可选文件：`partial_count` + 最后一条 partial 文本哈希，防泄密后续定义）

## 与 Voice Output Governance TRW 的关系

- ASR trace **上游**于输出治理；字段名允许在 TRW adapter 中映射，但 **不得丢失** `utterance_id` / `asr_status` / `fallback_reason`。
