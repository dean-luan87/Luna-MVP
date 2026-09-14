# Luna — MidPlatform Vision Recognition Ingest ReadOnly Event Payload v0

**Phase**：`Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001`（载荷与回放层）  
**前置（须均为 GO）**：

- `MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`  
- `Vision-Recognition-Evidence-ReadOnly-Consumer-001`  
- `Vision-Recognition-Evidence-Pack-Stub-001`  

## 目标

将 **`midplatform_vision_recognition_ingest_candidate_v0`** 封装为 **只读事件载荷**（`vision_recognition_ingest_readonly_event_payload_v0`），并在 **模拟** Product Bus 上完成 **JSONL 回放日志** + **只读 replay consumer** 校验与视图生成：

- **`event_type`**：`midplatform.vision_recognition.readonly_ingest_candidate`  
- **`payload_scope`**：`read_only_replay`  
- 保留 `evidence_count`、`provider` / `provider_level`、`fact_status_summary`、`synthetic_summary`、`evidence_by_frame`、`evidence_by_roi_type`、`geometry_summary`、`source_chain_summary`；附带 **`ingest_matrix_ref`** 供 consumer 校验矩阵行数。  
- **`allowed_consumers`**：`readonly_replay_consumer`、`manual_review_later`  
- **`forbidden_actions`**：与 ingest candidate 同构的六类禁止项。

## 严禁

无真实消息队列（Kafka / Redis / NATS 等）、无 gRPC/HTTP 外连 Bus、无数据库写入、无 MidPlatform fact / Scene Delta / WorldModel、无 AI interpretation / 导航 / 真实视觉 / YOLO / Supervision 主线 / VLM / OCR。

## 回放日志阶段（JSONL）

1. `event_payload_created`  
2. `event_replayed`  
3. `readonly_consumer_received`  
4. `readonly_consumer_view_generated`  
5. `no_write_action_confirmed`  

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_RECOGNITION_INGEST_READONLY_BUS_REPLAY_SMOKE_V0.md`。

## 与 OCR 线的关系

与 **OCR Ingest → Product Bus ReadOnly Replay** 同构；真实 Bus 接入须 **另开 phase**。

## 与 ingest candidate 的关系

建议上一 phase：**MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001**（见 [LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md](./LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md)）。

## 建议下一跳

**Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001**：由本 phase 的 **只读 event payload** + **`ingest_matrix_ref`** 生成 **Scene Delta write candidate**（仍为候选、不写 Scene Delta），见 [LUNA_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_V0.md) 与 `../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_SMOKE_V0.md`。
