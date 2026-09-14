# Luna Evaluation — Mock Handshake Generic Trace GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_executor_mock_handshake_generic_v0.py`  
**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001`

## GO

- **mock request / ACK** 存在；schema 为 `*_generic_v0`。  
- **`source_type`** 为 **`ocr_evidence`** 或 **`vision_recognition_evidence`**。  
- **`request_scope=no_write_handshake`**；**`ack_status=accepted_for_shape_only`**。  
- **`reason_codes`** 含 `mock_handshake_only`、`no_write_allowed`、`generic_trace_stub_accepted`。  
- **`executor_invoked` / `real_executor_invoked` / `write_attempted` / `write_committed`** 均为 **false**。  
- **JSONL** 含 5 个必需事件（含 **`generic_trace_shape_validated`**）；每行含 **`source_type`**。  
- **`compatibility_report.overall_ok=true`**；**audit** 与 verifier 清单一致。

## CONDITIONAL_GO

- 仅单一 **source_type** smoke 通过、另一未跑（无写路径时由流程标注，非 verifier 自动降级）。

## NO_GO

- 调用真实 executor；写 Scene Delta / DB；**`write_attempted` / `write_committed=true`**；写 rehearsal log / WAL。  
- 调用 AI / 导航 / 真实 provider；**audit** 缺失或与 no-write 矛盾。

## 一句话

本 smoke **只**对 **generic trace stub** 做内存 mock 握手与 synthetic ACK；**不**调用真实执行器、**不**落库。
