# Luna — MidPlatform Vision Recognition Evidence ReadOnly Ingest Candidate v0

**Phase**：`Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`  
**前置（须均为 GO）**：

- `Vision-Recognition-Evidence-ReadOnly-Consumer-001`  
- `Vision-Recognition-Evidence-Pack-Stub-001`  
- `Vision-Lightweight-Recognition-Adapter-Selection-001`  

## 目标

让中台以 **只读 ingest 候选**（`ingest_scope=read_only_candidate`）接收 **Vision recognition evidence** 的消费视图与聚合结果：

- 产物 **`midplatform_vision_recognition_ingest_candidate_v0`**：保留 `evidence_count`、`provider` / `provider_level`、`fact_status_summary`、`synthetic_summary`、`evidence_by_frame`、`evidence_by_roi_type`、`geometry_summary`、`source_chain_summary`。  
- **`midplatform_vision_recognition_ingest_matrix_v0`**：逐条证据的 frame / ROI / label / geometry / synthetic / `not_fact`。  
- **`forbidden_actions`**：显式声明禁止写事实、Scene Delta、WorldModel、AI 解释、导航、真实视觉 provider。  
- **`allowed_next_actions`**：`manual_review`、`vision_scene_delta_candidate_later`、`real_provider_retest_later`（均为 **后续** phase，不在本 phase 执行）。

## 输入与依赖

除用户列出的 consumer 产物外，需 **`vision_recognition_evidence_readonly_consumer_summary.json`** 中的 **`vision_recognition_evidence_pack_root`**，用于回读 **`vision_recognition_evidence_matrix.json`**（生成逐条 ingest 矩阵；与 OCR 线「consumer + 上游矩阵」同构）。

## 核心原则

- **Stub / synthetic / not_fact** 语义必须 **原样进入** candidate，**不得**标为 confirmed fact。  
- **无任何写路径**：不写 MidPlatform fact、不写 Scene Delta、不写 WorldModel。

## 严禁

无 AI interpretation、导航决策、真实视觉 provider、YOLO、Supervision **主线**、VLM、OCR 调用、routing 变更。

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md`。

## 与 OCR 中台 ingest 候选的关系

与 **MidPlatform OCR Evidence ReadOnly Ingest Candidate** 同构：先 **只读候选**，再谈 Bus 回放 / Scene Delta candidate 等下游。

## 与下一工程 phase 的关系

建议下一跳：**Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001**（见 [LUNA_MIDPLATFORM_VISION_RECOGNITION_INGEST_READONLY_EVENT_PAYLOAD_V0.md](./LUNA_MIDPLATFORM_VISION_RECOGNITION_INGEST_READONLY_EVENT_PAYLOAD_V0.md)）：只读 **event payload** + **模拟 Product Bus 回放** + **replay consumer**，与 OCR bus replay 同构。
