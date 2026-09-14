# Luna Evaluation — Scene Delta Executor Mock Handshake Smoke v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-001`

## 目的

验证 **内存 mock executor** 可基于 **executor trace stub** 目录产物生成 **mock request**、**synthetic ACK**、**handshake trace JSONL**、**compatibility report** 与 **audit**；全程 **无真实 executor、无写入、无 rehearsal log / WAL**。

## 前置

- `Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001` = GO  
- `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001` = GO  

**默认输入 trace stub 根目录**：`_eval_out/scene_delta_executor_trace_stub_from_dryrun_smoke_v0/`

## 输入

除 `scene_delta_executor_trace_stub.json` 等四文件外，Runner 需同目录 **`scene_delta_executor_trace_stub_summary.json`**，并读取其中 **`input_paths.write_candidate`** 作为 mock request 的 **`candidate_payload_ref`**。

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_mock_handshake_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_executor_mock_handshake_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_mock_handshake_v0.py \
  --smoke-root /ABS/PATH/_eval_out/scene_delta_executor_mock_handshake_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_mock_handshake_summary.json` | 摘要、`request_id` / `ack_id`、输入根路径。 |
| `scene_delta_mock_executor_request.json` | Mock 请求载荷。 |
| `scene_delta_mock_executor_ack.json` | Synthetic ACK。 |
| `scene_delta_mock_handshake_trace.jsonl` | 握手事件 JSONL。 |
| `scene_delta_mock_handshake_compatibility_report.json` | 形状与策略兼容检查。 |
| `scene_delta_mock_handshake_audit_report.json` | No-write audit。 |
| `scene_delta_mock_handshake_notes.md` | 短说明。 |
| `scene_delta_mock_handshake_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
