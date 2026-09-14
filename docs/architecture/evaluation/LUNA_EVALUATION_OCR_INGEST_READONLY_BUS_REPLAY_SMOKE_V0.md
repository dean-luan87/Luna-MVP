# Luna Evaluation — OCR Ingest Read-Only Product Bus Replay Smoke v0

**Phase**: `Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001`

## 目的

验证 **`midplatform_ocr_evidence_ingest_candidate`** 产物可被封装为 **`ocr_ingest_readonly_event_payload_v0`**，经 **模拟 Product Bus** 回放日志链路后，由 **只读 replay consumer** 消费并生成 **`ocr_ingest_readonly_replay_consumer_view_v0`**。全程 **无真实消息队列**、**无数据库写入**、**无事实层 / Scene Delta / WorldModel 写入**、**无 AI / OCR provider 调用**。

## 前置

- `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001` = GO  
- `Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001` = GO  

**默认输入 ingest 根目录**：`_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_ocr_ingest_readonly_bus_replay_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0

python3 tools/evaluation/midplatform/verify_ocr_ingest_readonly_bus_replay_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0
```

可选：

```bash
python3 tools/evaluation/midplatform/run_ocr_ingest_readonly_bus_replay_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0 \
  --ingest-root /ABS/PATH/_eval_out/midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0
```

## 读取的 Ingest 输入

| 文件 | 作用 |
|------|------|
| `midplatform_ocr_evidence_ingest_candidate.json` | 构建 event payload 的主体字段与 `candidate_id` |
| `midplatform_ocr_evidence_ingest_audit_report.json` | 血缘输入（runner 读取校验存在；不并入 payload） |
| `midplatform_ocr_evidence_ingest_text_matrix.json` | 血缘输入（存在性校验） |
| `midplatform_ocr_evidence_ingest_geometry_matrix.json` | `geometry_matrix_ref` 指向该文件 |
| `midplatform_ocr_evidence_ingest_source_chain_summary.json` | 血缘输入（存在性校验） |

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_ingest_readonly_bus_replay_summary.json` | 输入/输出路径、event 元数据、校验错误摘要。 |
| `ocr_ingest_readonly_event_payload.json` | 只读事件载荷。 |
| `ocr_ingest_readonly_replay_log.jsonl` | 回放阶段日志。 |
| `ocr_ingest_readonly_replay_consumer_view.json` | Replay consumer 视图。 |
| `ocr_ingest_readonly_replay_audit_report.json` | Bus replay audit。 |
| `ocr_ingest_readonly_bus_replay_notes.md` | 短说明。 |
| `ocr_ingest_readonly_bus_replay_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
