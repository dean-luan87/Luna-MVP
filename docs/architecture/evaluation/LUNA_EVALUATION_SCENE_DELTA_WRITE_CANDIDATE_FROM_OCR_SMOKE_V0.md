# Luna Evaluation — Scene Delta Write Candidate from OCR Ingest Stub Smoke v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001`

## 目的

验证可由 **`ocr_ingest_readonly_event_payload.json`**（默认来自 **OCR bus replay smoke** 目录）及 **`geometry_matrix_ref`** 指向的几何矩阵，生成 **`scene_delta_write_candidate_from_ocr_v0`**、**gate stub** 与 **audit**；全程 **无 Scene Delta 写入、无事实写入、无 AI、无 OCR provider、无外部总线、无 DB**。

## 前置

- `Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001` = GO  
- `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001` = GO  
- `Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001` = GO  

**默认输入 bus replay 根目录**：`_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_from_ocr_ingest_stub_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_write_candidate_from_ocr_ingest_stub_v0.py \
  --smoke-root /ABS/PATH/_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0
```

可选：自定义 bus replay 根或事件载荷路径：

```bash
python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_from_ocr_ingest_stub_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0 \
  --bus-replay-root /ABS/PATH/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0

python3 tools/evaluation/midplatform/run_scene_delta_write_candidate_from_ocr_ingest_stub_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0 \
  --event-payload /ABS/PATH/ocr_ingest_readonly_event_payload.json
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_write_candidate_from_ocr_summary.json` | 输入路径、`source_event_id`、候选 `candidate_id`、构建错误。 |
| `scene_delta_write_candidate_from_ocr.json` | Scene Delta write candidate 主体。 |
| `scene_delta_write_candidate_evidence_matrix.json` | `evidence_items` 矩阵导出。 |
| `scene_delta_write_candidate_gate_stub.json` | 闸门占位。 |
| `scene_delta_write_candidate_audit_report.json` | Stub audit。 |
| `scene_delta_write_candidate_notes.md` | 短说明。 |
| `scene_delta_write_candidate_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
