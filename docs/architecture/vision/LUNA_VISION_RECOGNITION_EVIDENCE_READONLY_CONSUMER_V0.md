# Luna — Vision Recognition Evidence ReadOnly Consumer v0

**Phase**：`Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001`  
**前置（须均为 GO）**：

- `Vision-Recognition-Evidence-Pack-Stub-001`  
- `Vision-Lightweight-Recognition-Adapter-Selection-001`  
- `Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  

## 目标

证明 **`vision_recognition_evidence_pack_v0`** 可被 **只读消费者** 安全读取、遍历与聚合，产出 **`vision_recognition_evidence_readonly_consumer_view_v0`**：

- 保留 **synthetic / stub / not_fact** 语义；**不**把 stub label 当作事实。  
- 聚合：`evidence_by_frame`、`evidence_by_roi_type`、`label_summary`、`geometry_summary`、`source_chain_summary`。  
- 派生矩阵：`vision_recognition_evidence_by_frame_matrix`、`vision_recognition_evidence_by_roi_matrix`、`vision_recognition_evidence_geometry_summary`。

## 严禁

无 MidPlatform fact、Scene Delta、WorldModel、AI interpretation、导航、YOLO、Supervision **主线**、VLM、OCR；**不得**生成 `confirmed_object`、`confirmed_fact`、`navigation_action`、`scene_delta_candidate`、`world_model_candidate`、`ai_interpretation` 等语义载荷（实现层对输出键做静态自检）。

## Vision 阶段表（评测对齐，v0）

| Phase | Verdict（当前叙述） |
|-------|---------------------|
| Vision-VideoFrame-Minimal-Ingest-001 | GO |
| Vision-FrameTrace-StreamRegistry-001 | GO |
| Vision-Frame-Input-Governance-001 | GO |
| Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 | GO |
| Vision-Lightweight-Recognition-Adapter-Selection-001 | GO |
| Vision-Recognition-Evidence-Pack-Stub-001 | GO |
| Vision-Recognition-Evidence-ReadOnly-Consumer-001 | **GO**（以 `verify_vision_recognition_evidence_readonly_consumer_v0` 为准） |
| MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001 | **GO**（以 `verify_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0` 为准；见 [../midplatform/LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md](../midplatform/LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md)） |
| Vision-External-Supervision-Adapter-Experiment-001-Rerun-After-Install | GO / **EXTERNAL_EXPERIMENT** |
| Vision-Supervision-Structure-Reference-Analysis-001 | **PLANNED / NOT_STARTED** |

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md`。

## 与下一工程 phase 的关系

建议下一跳：**MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001**（见 [../midplatform/LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md](../midplatform/LUNA_MIDPLATFORM_VISION_RECOGNITION_EVIDENCE_READONLY_INGEST_CANDIDATE_V0.md)）：中台只读 ingest 候选，与 OCR 线同构。

## 与 OCR 线的对齐

与 OCR **evidence readonly consumer** 同构：先证明 **证据包可被安全消费**，再进入 **MidPlatform read-only ingest candidate**（上表已链至该 phase）。
