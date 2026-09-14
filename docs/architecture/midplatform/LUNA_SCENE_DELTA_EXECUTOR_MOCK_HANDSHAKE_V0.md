# Luna MidPlatform — Scene Delta Executor Mock Handshake v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-001`

## 目的

在 **内存 mock executor** 中消费 **`scene_delta_executor_trace_stub_v0`** 形状上下文，生成 **`scene_delta_mock_executor_request_v0`** 与 **`scene_delta_mock_executor_ack_v0`（synthetic ACK）**，并落盘 **握手 trace（JSONL）**、**兼容报告** 与 **no-write audit**，用于与未来 **真实 Scene Delta executor** 的 **握手 / 入参 / ACK** 对齐。

## 边界

- **不**调用真实 executor；**不**写 Scene Delta；**不**落库；**不**写 MidPlatform 事实 / WorldModel；**不**调用 AI / OCR provider；**不**改 OCR routing。
- **不**写 rehearsal log；**不**对任何 WAL 做 append（`rehearsal_log_written=false`，`wal_append_invoked=false`）。
- **ACK**：`ack_status=accepted_for_shape_only`；`executor_invoked=false`；`real_executor_invoked=false`；`write_attempted=false`；`write_committed=false`。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_V0.md)。
