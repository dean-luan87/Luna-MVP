# Luna — CrossModal Fusion Review Queue v0

**Phase**：`Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001`

## 目的

将 Vision–OCR **fusion candidate dry-run** 产物接入 **review queue**（`pending_review`），作为中台写入 / AI 解释 / Scene Delta 候选之前的缓冲层。

## 原则

- Review queue **不是**事实库、Scene Delta 或 WorldModel。
- 所有候选默认 `pending_review`；`auto_approve_allowed=false`；禁止自动转 confirmed。
- 不重新调用 OCR / Vision provider；不写任何事实层。

## 输入

`cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0` 目录下的 fusion candidates、matrix、risk、source chain、dry-run audit。

## 评测

[LUNA_EVALUATION_CROSS_MODAL_FUSION_REVIEW_QUEUE_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_FUSION_REVIEW_QUEUE_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001**（见 [LUNA_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_V0.md](./LUNA_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_V0.md)）。
