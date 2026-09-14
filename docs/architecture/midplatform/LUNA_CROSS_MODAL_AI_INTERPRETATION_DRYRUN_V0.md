# Luna — CrossModal AI Interpretation DryRun v0

**Phase**：`Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001`

## 目的

对 `pending_review` 的 review queue item 生成 **AI interpretation dry-run**（`template_stub`），不调用外部 LLM，不改变批准状态。

## 原则

- 解释候选 **不是**事实；不得改变 `approval_status` / `review_status`。
- 不写 MidPlatform / Scene Delta / WorldModel；不做导航；不自动批准。

## 输入

| 根目录 | 作用 |
|--------|------|
| `cross_modal_fusion_review_queue_smoke_v0` | review queue items |
| `cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0` | fusion candidate payload |

## 评测

[LUNA_EVALUATION_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001**（见 [LUNA_CROSS_MODAL_SCENE_DELTA_CANDIDATE_DRYRUN_V0.md](./LUNA_CROSS_MODAL_SCENE_DELTA_CANDIDATE_DRYRUN_V0.md)）。
