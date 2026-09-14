# Luna — Vision Recognition Evidence Pack v0

**Phase**：`Phase-Vision-Recognition-Evidence-Pack-Stub-001`  
**前置（须均为 GO）**：

- `Vision-Lightweight-Recognition-Adapter-Selection-001`  
- `Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  
- `Vision-Frame-Input-Governance-001`  

## 目标

将 **vision_stub** 的 `vision_provider_stub_result` / `vision_recognition_candidate_matrix` 等产物，整理为 Luna 自有的 **`VisionRecognitionEvidencePack v0`**：

- **`evidence_scope=synthetic_stub_candidate`**，**`fact_status=not_fact`**（包级与 item 级一致）。  
- **`provider_trace`** 保留 provider / level / `real_provider_invoked`。  
- **items** 保留 `source_frame_id`、`unit_id`、`roi_id`、`bbox_in_frame` / `bbox_in_unit`、`crop_image_ref`（来自矩阵）、`coordinate_transform`（回读 `vision_provider_input_pack`）。  
- **`source_chain`** 指向 input pack、selection report、stub result 路径及 `vision_recognition_evidence_pack_built`。

## 核心原则

- **Provider 输出不是事实**；**stub label 不是现实对象**；证据包仅为 **候选视觉证据**。  
- **下游不得**将 stub 证据写入事实层（本 phase 亦不写 MidPlatform / Scene Delta / WorldModel）。

## 严禁

无 YOLO、Supervision **主线**、VLM、OCR、AI interpretation、MidPlatform fact、Scene Delta、WorldModel、导航决策；**不得**将 stub label 标为 fact。

## Vision 阶段表（评测对齐，v0）

| Phase | Verdict（当前叙述） |
|-------|---------------------|
| Vision-VideoFrame-Minimal-Ingest-001 | GO |
| Vision-FrameTrace-StreamRegistry-001 | GO |
| Vision-Frame-Input-Governance-001 | GO |
| Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 | GO |
| Vision-Lightweight-Recognition-Adapter-Selection-001 | GO |
| Vision-Recognition-Evidence-Pack-Stub-001 | **GO**（以 `verify_vision_recognition_evidence_pack_stub_v0` 为准） |
| Vision-Recognition-Evidence-ReadOnly-Consumer-001 | **GO**（以 `verify_vision_recognition_evidence_readonly_consumer_v0` 为准；见 [LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md)） |
| Vision-External-Supervision-Adapter-Experiment-001-Rerun-After-Install | GO / **EXTERNAL_EXPERIMENT** |
| Vision-Supervision-Structure-Reference-Analysis-001 | **PLANNED / NOT_STARTED** |

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_RECOGNITION_EVIDENCE_PACK_STUB_V0.md`。

## 与下一工程 phase 的关系

建议下一跳：**Vision-Recognition-Evidence-ReadOnly-Consumer-001**（见 [LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md)）：只读遍历与聚合，证明 evidence pack 可被安全消费。

## 与后续真实 provider 的关系

先固定 **Luna 证据包形状** 与 **只读消费** 契约；后续接入 YOLO / Supervision / VLM 时 **替换 provider**，**不改变**下游对 `vision_recognition_evidence_pack_v0` 的消费结构（须仍通过 governance → pack → selection → evidence 链）。
