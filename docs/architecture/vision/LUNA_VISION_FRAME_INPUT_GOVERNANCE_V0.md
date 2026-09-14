# Luna — Vision Frame Input Governance v0

**Phase**：`Phase-Vision-Frame-Input-Governance-001`  
**前置**：`Vision-VideoFrame-Minimal-Ingest-001` = GO；`Vision-FrameTrace-StreamRegistry-001` = GO；`Vision-External-Supervision-Adapter-Experiment-001` = CONDITIONAL_GO 或 GO（本 phase **不依赖** Supervision）。

## 目标

在 **任何** YOLO / VLM / OCR / 视角识别 provider 之前，对 **已采样、已入 trace** 的帧做 **输入治理**：

- 是否接受进入下游、是否需 resize / crop、是否可作为关键帧候选；  
- 产出 **`vision_frame_input_governance_matrix`**（逐帧）与 **`vision_frame_input_governance_summary`**；  
- 产出 **`vision_frame_input_candidate_v0`**（写入 `vision_provider_input_candidate.json`）：仅声明 `input_governance_only`，并 **禁止** 下一阶段直接进入 recognition / 导航 / 中台写入。

## 硬性规则

- 矩阵与候选中 **`eligible_for_recognition` 恒为 false**；summary 中 **`eligible_for_recognition_count` 恒为 0**。  
- 允许的下一跳：**`roi_proposal_stub`**；**不得**在本 phase 调用识别 provider、不得将 Supervision 接入主线。

## STCM / Performance

本 phase **不** 实现真实 Performance Controller；每帧与 summary 预留 **`stcm_deadline_hint`**、**`frame_validity_hint`**、**`performance_budget_hint`**、**`degradation_reason_codes`**（占位字符串 / 空列表）。

## 严禁

无 YOLO、OCR、VLM、AI interpretation、MidPlatform fact、Scene Delta、WorldModel、导航决策、真实摄像头、Supervision 主线、OCR routing 变更。

## Vision 阶段表（评测对齐，v0）

| Phase | Verdict（当前叙述） |
|-------|---------------------|
| Vision-VideoFrame-Minimal-Ingest-001 | GO |
| Vision-FrameTrace-StreamRegistry-001 | GO |
| Vision-External-Supervision-Adapter-Experiment-001 | CONDITIONAL_GO（未安装 supervision 时） |
| Vision-Frame-Input-Governance-001 | **GO**（以 `verify_vision_frame_input_governance_v0` 为准；默认 trace smoke 下 10/10 接受） |
| Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 | **GO**（以 `verify_vision_roi_proposal_stub_smoke_v0` 为准；规则 ROI + pack + crop） |

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_FRAME_INPUT_GOVERNANCE_V0.md`。

## 与主线顺序的关系

本 phase 对应 [Vision 主线 phase 顺序与输入门控 v0](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md) 中的 **第 3 步**；下一工程 phase 建议：**Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001**（见 [LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md](./LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md)），再之后为轻量识别适配（主线文档第 5 步）。
