# LUNA MidPlatform Model Switching Applicability Matrix v0

## Phase

- Phase-MidPlatform-ModelSwitch-001

## Purpose

矩阵化说明：中台统一切换规则适用于哪些模块、典型 provider/fallback 链如何写、哪些 invocation_mode 推荐哪个 latency_profile。

## Matrix（示例）

| Capability | invocation_mode | latency_profile | preferred providers | fallback_chain (example) |
|---|---|---|---|---|
| TTS | realtime_critical | realtime_critical | qwen_online | qwen → piper → macOS_say |
| TTS | realtime_normal | realtime_normal | qwen_online | qwen → piper → macOS_say |
| ASR | realtime_normal | realtime_normal | cloud_asr | cloud_asr → whisper_local → keyword_mode → not_available |
| OCR | realtime_normal | realtime_normal | paddleocr_vl | paddleocr_vl → paddleocr → system_ocr → not_available |
| Vision | realtime_normal | realtime_normal | vlm_semantic | vlm → yolo → lightweight_detector → not_available |
| Semantic | interactive_quality | interactive_quality | cloud_llm | cloud_llm → local_llm → rule_baseline |
| Decision | realtime_critical | realtime_critical | model_assisted | model_assisted → rule_engine → MONC → safe_freeze |
| Offline eval | offline_evaluation | offline_batch | pinned_local | pinned_local → fallback_baseline |

## Notes

- preferred providers 代表“质量优先候选”，但必须受 hard_timeout + fallback + circuit breaker 约束。
- offline_evaluation 必须 pinned provider（可复现优先），在线 provider 禁止进入离线基线。

