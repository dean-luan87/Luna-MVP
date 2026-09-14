# LUNA MidPlatform Model Fallback & Circuit Breaker Policy v0

## Phase

- Phase-MidPlatform-ModelSwitch-001

## Fallback chain（统一规则）

### Mandatory requirements

- **fallback_chain 不得为空**
- provider 失败不得伪造成功（必须结构化失败）
- fallback 后能力边界必须收缩（不得提升权限/不得放开 side effects）
- fallback 结果必须记录：
  - provider_selected
  - fallback_used / fallback_provider / fallback_reason
  - contract gates（schema_valid / forbidden_output_detected / output_contract_valid）

### Examples（示例链）

- **TTS**
  - qwen_online → piper_local → macOS_say_legacy
- **OCR**
  - paddleocr_vl → paddleocr_lightweight → system_ocr → not_available
- **ASR**
  - cloud_asr → whisper_local → local_keyword_mode → not_available
- **Vision**
  - vlm_semantic → yolo_local → lightweight_detector → not_available
- **Decision**
  - model_assisted → rule_engine → MONC_minimum_navigation → safe_freeze

## Circuit breaker（统一熔断）

### Common fields

- failure_count_threshold
- failure_window_ms
- open_duration_ms
- half_open_probe_count
- circuit_state: closed | open | half_open
- circuit_reason

### Recommended defaults

- failure_count_threshold = 3
- failure_window_ms = 300000（5 min）
- open_duration_ms = 300000（5 min）
- half_open_probe_count = 1

### Failure types included（统一失败分类）

- timeout
- provider_exception
- missing_api_key
- network_unavailable
- invalid_result_schema
- forbidden_output_detected
- health_check_failed
- dependency_unavailable
- safety_gate_failed

### State transitions

- 连续失败达到阈值 → open
- open 期间跳过该 provider → 直接走 fallback_chain
- open 结束 → half_open
- half_open probe 成功 → closed
- half_open probe 失败 → open（重新计时）

