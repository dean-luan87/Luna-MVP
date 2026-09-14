# Luna — Vision Frame ROI Proposal and Segmentation Stub v0

**Phase**：`Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001`  
**前置（须均为 GO）**：

- `Vision-VideoFrame-Minimal-Ingest-001`  
- `Vision-FrameTrace-StreamRegistry-001`  
- `Vision-Frame-Input-Governance-001`  
- `Vision-External-Supervision-Adapter-Experiment-001`（可为 GO；本 phase **不依赖** Supervision，Supervision 仍为 **外部实验线**）

## 目标

在 **已治理且 accepted** 的帧上，用 **规则 / stub** 生成 ROI proposal，并产出 **`vision_provider_input_pack_v0`**：

- 每个 accepted 帧至少五类 ROI：`center_roi`、`ground_roi`、`upper_sign_roi`、`left_roi`、`right_roi`。  
- 每个 ROI 含 `bbox_in_frame`、`polygon_in_frame`（由 bbox 派生的轴对齐 stub）、`source_frame_id`、`source_image_ref`、`coordinate_space`、`task_hint`、`segmentation_stub`（`mask_available=false`）。  
- 为每个 ROI **写入磁盘 crop**，并在 pack 的 `input_units` 中引用 **crop 的 `image_ref`**，附带完整 **`coordinate_transform`**（`frame_roi_crop` 模式）。  
- 聚合 `vision_roi_proposal_candidate.json`、`vision_roi_proposal_matrix.json`、`vision_provider_input_unit_matrix.json`、`vision_roi_source_chain_summary.json` 与 audit。

## 核心原则

- **模型不能直接消费整帧**；后续任意视觉识别 provider **只能**消费本 phase 产出的 **`vision_provider_input_pack_v0`**（或其 bundle 中的单帧 pack）。  
- **Segmentation** 本 phase 仅 **metadata stub**；不跑真实 mask / 分割网络。

## 严禁

无 YOLO、真实 detector、Supervision **主线**、VLM、OCR、AI interpretation、MidPlatform fact、Scene Delta、WorldModel、导航决策、真实摄像头、实时硬件采集。

## 产物 bundle：`vision_provider_input_pack.json`

评测根目录写入 **`vision_provider_input_pack_bundle_v0`**：顶层字段 `bundle_schema`、`packs`（每个元素即一帧的 `vision_provider_input_pack_v0` 对象，含 `input_units` 与 `source_chain`）。

## Vision 阶段表（评测对齐，v0）

| Phase | Verdict（当前叙述） |
|-------|---------------------|
| Vision-VideoFrame-Minimal-Ingest-001 | GO |
| Vision-FrameTrace-StreamRegistry-001 | GO |
| Vision-External-Supervision-Adapter-Experiment-001 | GO（外部实验；不接主线） |
| Vision-Frame-Input-Governance-001 | GO |
| Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 | **GO**（以 `verify_vision_roi_proposal_stub_smoke_v0` 为准） |
| Vision-Lightweight-Recognition-Adapter-Selection-001 | **GO**（以 `verify_vision_lightweight_recognition_adapter_selection_smoke_v0` 为准；见 [LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md](./LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md)） |

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_FRAME_ROI_PROPOSAL_STUB_SMOKE_V0.md`。

## 与主线顺序的关系

对应 [Vision 主线 phase 顺序与输入门控 v0](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md) 中的 **第 4 步**；建议下一工程 phase：**Vision-Lightweight-Recognition-Adapter-Selection-001**（见 [LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md](./LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md)）。

## 后续参考阶段（PLANNED / NOT_STARTED）

**Phase-Vision-Supervision-Structure-Reference-Analysis-001** = **PLANNED / NOT_STARTED**：拆解 Roboflow Supervision 的 Detections / mask / tracker / zone 等抽象，映射到 Luna 自有类型（如 `VisionDetectionEvidence` / `VisionROIProposalCandidate` / `VisionTrackingEvidence`）。**仅作结构参考**，**不**替代本主线顺序；**不**在本 ROI stub phase 调用 Supervision 主线。
