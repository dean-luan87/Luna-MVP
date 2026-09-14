# Luna Evaluation — Contract Conformance Generic GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_executor_contract_conformance_generic_v0.py`  
**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001`

## GO

- **contract skeleton** 存在；`schema_version=scene_delta_executor_contract_skeleton_generic_v0`；**`contract_reference_mode=local_skeleton`**。  
- **`source_type`** 为 **`ocr_evidence`** 或 **`vision_recognition_evidence`**。  
- request / ACK **conformance matrix** 全部 **`ok=true`**；ACK **`reason_codes`** 含 **`generic_trace_stub_accepted`**。  
- **`no_write_mode_checks_ok=true`**；conformance **audit** 与 verifier 清单一致。

## CONDITIONAL_GO

- 仅单一 **source_type** smoke 通过；或 **local_skeleton** 下存在非关键 optional 字段差异（soft_notes）。

## NO_GO

- 缺 required fields；**unsupported source_type**；**write_attempted / write_committed / real_executor** 为 true；写 DB / WAL / rehearsal / Scene Delta / 事实层；调用 AI / 导航 / provider；**audit** 缺失。

## 一句话

本 smoke **只**对 generic mock request/ACK 做 **local_skeleton** 静态对齐；**不**调用真实执行器、**不**落库。
