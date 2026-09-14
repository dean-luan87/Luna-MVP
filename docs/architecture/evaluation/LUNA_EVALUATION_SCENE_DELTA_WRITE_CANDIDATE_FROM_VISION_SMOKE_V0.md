# Luna 评测 — Scene Delta Write Candidate from Vision Smoke v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001`  
**Runner**：`tools/evaluation/midplatform/run_scene_delta_write_candidate_from_vision_ingest_stub_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_write_candidate_from_vision_ingest_stub_v0.py`

## 输入（Vision bus replay 根目录）

须为 **绝对路径**，且包含：

- `vision_recognition_ingest_readonly_event_payload.json`（含 **`ingest_matrix_ref`**）  
- `vision_recognition_ingest_readonly_replay_consumer_view.json`  
- `vision_recognition_ingest_readonly_replay_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_from_vision_ingest_stub_v0.py \
  --bus-replay-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_ingest_readonly_bus_replay_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_from_vision_ingest_stub_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/midplatform/verify_scene_delta_write_candidate_from_vision_ingest_stub_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_from_vision_ingest_stub_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `scene_delta_write_candidate_from_vision_summary.json` | 摘要与构建错误 |
| `scene_delta_write_candidate_from_vision.json` | `scene_delta_write_candidate_from_vision_v0` |
| `scene_delta_write_candidate_vision_evidence_matrix.json` | 证据矩阵导出 |
| `scene_delta_write_candidate_vision_gate_stub.json` | gate 占位 |
| `scene_delta_write_candidate_vision_audit_report.json` | audit |
| `scene_delta_write_candidate_from_vision_notes.md` | 短说明 |
| `scene_delta_write_candidate_from_vision_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_SMOKE_GO_NO_GO_PACK_V0.md`。
