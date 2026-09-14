# Luna Evaluation — Scene Delta Executor Contract Conformance Generic v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_executor_contract_conformance_generic_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_executor_contract_conformance_generic_v0.py`

## 输入（generic mock handshake 根目录）

- `scene_delta_mock_executor_request_generic.json`  
- `scene_delta_mock_executor_ack_generic.json`  
- `scene_delta_mock_handshake_compatibility_report_generic.json`  
- `scene_delta_mock_handshake_audit_report_generic.json`  

## 命令

**Vision**：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_contract_conformance_generic_v0.py \
  --generic-mock-handshake-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_vision_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_vision_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_contract_conformance_generic_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_vision_smoke_v0
```

**OCR 回归**：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_contract_conformance_generic_v0.py \
  --generic-mock-handshake-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_generic_ocr_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_ocr_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_contract_conformance_generic_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_contract_conformance_generic_ocr_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_contract_skeleton_generic_v0.json` | local_skeleton 合同骨架 |
| `scene_delta_executor_contract_conformance_generic_summary.json` | 摘要、`source_type` |
| `scene_delta_executor_request_conformance_matrix_generic.json` | request 字段矩阵 |
| `scene_delta_executor_ack_conformance_matrix_generic.json` | ACK 字段矩阵 |
| `scene_delta_executor_contract_gap_report_generic.json` | gap / optional / disclaimer |
| `scene_delta_executor_no_write_contract_report_generic.json` | no-write 合同检查 |
| `scene_delta_executor_contract_conformance_audit_report_generic.json` | audit |
| `scene_delta_executor_contract_conformance_generic_verifier_report.json` | meta-verifier |

GO / NO_GO：见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_GO_NO_GO_PACK_V0.md)。
