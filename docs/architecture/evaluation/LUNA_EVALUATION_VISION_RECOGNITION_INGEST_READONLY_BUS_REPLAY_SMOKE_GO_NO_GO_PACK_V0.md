# Luna 评测 — Vision Recognition Ingest ReadOnly Bus Replay GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/midplatform/verify_vision_recognition_ingest_readonly_bus_replay_smoke_v0.py`  
**Phase**：`Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001`

## GO

- **event_payload**、**replay_log**、**replay_consumer_view**、**replay_audit** 齐全。  
- `schema_version=vision_recognition_ingest_readonly_event_payload_v0`；`event_type=midplatform.vision_recognition.readonly_ingest_candidate`。  
- `payload_scope=read_only_replay`；`candidate_id`、`source_candidate_ref` 非空；`evidence_count > 0`。  
- `provider=vision_stub`，`provider_level=stub`；`fact_status_summary` / `synthetic_summary` 与 `evidence_count` 一致。  
- `evidence_by_frame`、`evidence_by_roi_type`、`geometry_summary` 非空；`forbidden_actions` 六键齐全且为 **true**。  
- replay log 含全部五阶段；`replay_consumer_view.validation_errors` 为 **[]**。  
- audit：`event_payload_created`、`replay_executed`、`readonly_consumer_received` 为 **true**；禁止类字段均为 **false**（含 `database_write_invoked`、`external_bus_invoked`）。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 `source_chain_summary` 较弱等）。

## NO_GO

- 写入事实 / Scene Delta / WorldModel；调用 AI / 导航 / 真实视觉 / YOLO / Supervision / VLM / OCR；**真实**外部 Bus 或 DB 写入（audit 非 false）。  
- `payload_scope` 非 `read_only_replay`；`validation_errors` 非空；关键产物或 audit 缺失。

## 一句话

本 smoke **只**验证 Vision ingest candidate → **只读事件载荷** → **模拟回放** → **只读 consumer**；**不**接真实 MQ、**不**写库。
