# Luna — Supervision Adapter A/B Test v0

**Phase**：`Phase-Vision-Supervision-Adapter-AB-Test-001`  
**性质**：evaluation-only 结构对比 — **不接** Vision runtime 主线。

## 目的

对比 **rule_stub ROI** 与 **supervision_synthetic_adapter** 产物，评估 Supervision 结构是否适合作为 `vision_detection_evidence_v0` 的 adapter 候选（非检测质量评分）。

## 前置

- Vision-Supervision-Structure-Reference-Analysis-001 = GO  
- VisionDetectionEvidence-Schema-Alignment-001 = GO  
- Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 = GO  

## 严禁

主线、YOLO、真实 detector、VLM/OCR、AI interpretation、MidPlatform / Scene Delta / WorldModel 写入、导航决策、将 synthetic 标为 fact。

## 评测

见 [LUNA_EVALUATION_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md](../evaluation/LUNA_EVALUATION_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md)。

## 建议下一跳

**Phase-Vision-Gated-YOLO-Candidate-Adapter-001**：见 [LUNA_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md](./LUNA_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md)。
