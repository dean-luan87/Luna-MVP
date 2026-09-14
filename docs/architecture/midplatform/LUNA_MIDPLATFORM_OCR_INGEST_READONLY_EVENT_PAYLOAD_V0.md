# Luna MidPlatform — OCR Ingest Read-Only Event Payload v0

**Phase**: `Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001`（事件载荷契约）

## 目的

定义 **`ocr_ingest_readonly_event_payload_v0`**：将 **`midplatform_ocr_evidence_ingest_candidate_v0`** 压缩为可在 **模拟 Product Bus** 上回放的 **只读事件载荷**，携带 `candidate_id`、`text_joined`、`evidence_by_roi`、`geometry_matrix_ref`（指向几何矩阵 JSON 文件）、`provider_summary`、`source_chain_summary`，并显式列出 **allowed_consumers** 与 **forbidden_actions**。

## 边界

- **模拟 bus**：不连接 Kafka / Redis / NATS / gRPC / HTTP 等真实外部总线（`external_bus_invoked=false`）。
- **不写**：MidPlatform 事实、Scene Delta、WorldModel；**不**调用 AI 解释、**不**调用 OCR provider、**不**改 OCR routing；**不**做数据库写入。

## 回放日志（Replay Log）

JSONL，每行一条 JSON，**阶段**（`stage`）须依次覆盖：

1. `event_payload_created`  
2. `event_replayed`  
3. `readonly_consumer_received`  
4. `readonly_consumer_view_generated`  
5. `no_write_action_confirmed`  

## 评测入口

见 [LUNA_EVALUATION_OCR_INGEST_READONLY_BUS_REPLAY_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_OCR_INGEST_READONLY_BUS_REPLAY_SMOKE_V0.md)。
