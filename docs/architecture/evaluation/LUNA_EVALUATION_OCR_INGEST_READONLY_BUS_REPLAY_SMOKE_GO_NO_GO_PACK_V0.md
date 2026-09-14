# LUNA Evaluation — OCR Ingest Read-Only Bus Replay Smoke GO / NO-GO Pack v0

**Phase**: `Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001`

## GO

- `ocr_ingest_readonly_event_payload.json` **存在**，`schema_version` = **`ocr_ingest_readonly_event_payload_v0`**，`event_type` = **`midplatform.ocr_evidence.readonly_ingest_candidate`**，`payload_scope` = **`read_only_replay`**。
- `candidate_id`、`source_candidate_ref`、`geometry_matrix_ref` **非空**；`evidence_count` **≥ 1**；`text_joined` **非空**；`evidence_by_roi` **非空对象**。
- `forbidden_actions` **五键齐全**且值为 **true**（声明禁止）。
- `ocr_ingest_readonly_replay_log.jsonl` **含全部必选 stage**。
- `ocr_ingest_readonly_replay_consumer_view.json` **存在**。
- **Audit**：`event_payload_created` / `replay_executed` / `readonly_consumer_received` = **true**；`midplatform_fact_written`、`scene_delta_written`、`world_model_written`、`ai_interpretation_invoked`、`ocr_provider_invoked`、`ocr_routing_changed`、`database_write_invoked`、`external_bus_invoked` = **false**。

## CONDITIONAL_GO

- Replay consumer view 中 **`validation_errors` 非空**（非关键字段），但 payload 与 audit 硬门禁仍满足。
- 或 **`provider_summary` 在载荷中为空**导致 consumer view 标记缺失，但 **无写路径**。

## NO_GO

- 任一 **写路径** 或 **外部真实总线** 被触发（audit 违背）。
- **调用 AI / OCR provider** 或 **改 OCR routing**（本 phase 实现禁止；audit 须为 false）。
- Payload **缺失**、**schema / event_type / payload_scope 不匹配**、**forbidden_actions 不齐**、**replay log 缺 stage**、**audit 缺失**。

## 一句话

本阶段只验证 **OCR ingest candidate 能作为只读事件载荷在模拟 Product Bus 中回放并被消费**；**不写事实层、不写 Scene Delta、不写 WorldModel、不调用 AI 解释**。
