# Luna MidPlatform — Scene Delta Executor Mock Handshake from Generic Trace v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001`

## 目的

在 **内存 mock executor** 中消费 **`scene_delta_executor_trace_stub_generic_v0`**（**OCR** 或 **Vision** `source_type`），生成 **generic mock request / ACK**、**握手 JSONL trace**、**兼容报告** 与 **no-write audit**，与旧 OCR 专用 mock handshake（`scene_delta_executor_trace_stub_v0`）并存。

## 前置（须均为 GO）

- `Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001`  
- Vision / OCR **generic trace stub** smoke 均通过  

## 边界

- **不**调用真实 executor；**不**写 Scene Delta；**不**落库；**不**写 MidPlatform 事实 / WorldModel；**不**调用 AI / 导航 / OCR / Vision provider。  
- **不**写 rehearsal log；**不** WAL append。  
- **ACK**：`ack_status=accepted_for_shape_only`；`reason_codes` 含 **`generic_trace_stub_accepted`**。

## 与旧 OCR mock handshake 的关系

- **保留**：`run_scene_delta_executor_mock_handshake_v0.py` 仍消费 **`scene_delta_executor_trace_stub.json`**（OCR 专用 trace）。  
- **新增**：本 phase 消费 **`scene_delta_executor_trace_stub_generic.json`**；下游应逐步迁移到 generic 路径。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md)。

## 与上一 phase 的关系

输入来自 [LUNA_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md](./LUNA_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md) 产物目录。

## 建议下一跳

**Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001**：对 generic mock request/ACK 做 **local_skeleton** 合同静态对齐，见 [LUNA_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_V0.md](./LUNA_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_V0.md)。
