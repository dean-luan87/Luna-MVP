# Luna Evaluation — Scene Delta Executor Mock Handshake from Generic Trace v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_executor_mock_handshake_generic_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_executor_mock_handshake_generic_v0.py`

## 输入（generic trace stub 根目录）

须包含：

- `scene_delta_executor_trace_stub_generic_summary.json`（含 `input_paths.write_candidate`）  
- `scene_delta_executor_trace_stub_generic.json`  
- `scene_delta_executor_planned_step_matrix_generic.json`  
- `scene_delta_executor_input_compatibility_report_generic.json`  
- `scene_delta_executor_trace_stub_generic_audit_report.json`  

## 命令

**Vision generic trace**：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_mock_handshake_generic_v0.py \
  --generic-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_vision_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_vision_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_mock_handshake_generic_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_vision_smoke_v0
```

**OCR generic trace 回归**：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_mock_handshake_generic_v0.py \
  --generic-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_ocr_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_ocr_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_mock_handshake_generic_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_ocr_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_mock_handshake_generic_summary.json` | 摘要、`source_type`、request/ack id |
| `scene_delta_mock_executor_request_generic.json` | generic mock request |
| `scene_delta_mock_executor_ack_generic.json` | synthetic ACK |
| `scene_delta_mock_handshake_trace_generic.jsonl` | 5 行握手事件（含 `source_type`） |
| `scene_delta_mock_handshake_compatibility_report_generic.json` | `overall_ok` |
| `scene_delta_mock_handshake_audit_report_generic.json` | no-write audit |
| `scene_delta_mock_handshake_generic_notes.md` | 短说明 |
| `scene_delta_mock_handshake_generic_verifier_report.json` | meta-verifier |

GO / NO_GO：见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_GO_NO_GO_PACK_V0.md)。
