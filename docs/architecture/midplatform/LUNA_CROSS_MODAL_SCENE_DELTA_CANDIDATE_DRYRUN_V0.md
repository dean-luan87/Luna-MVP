# Luna — CrossModal Scene Delta Candidate DryRun v0

**Phase**：`Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001`

## 目的

从 fusion candidate、review queue、AI interpretation dry-run 生成 **Scene Delta candidate dry-run**，不调用 executor、不写 Scene Delta。

## 原则

- `write_allowed=false`，`gate_status=not_evaluated`，`requires_gate_approval=true`。
- 不自动批准；不写 MidPlatform / Scene Delta / WorldModel。

## 输入

| 根目录 | 作用 |
|--------|------|
| `cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0` | fusion payload |
| `cross_modal_fusion_review_queue_smoke_v0` | review queue |
| `cross_modal_ai_interpretation_dryrun_smoke_v0` | interpretation |

## 评测

[LUNA_EVALUATION_CROSS_MODAL_SCENE_DELTA_CANDIDATE_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_SCENE_DELTA_CANDIDATE_DRYRUN_V0.md)

## 建议下一跳

**Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001**（见 [LUNA_CROSS_MODAL_SCENE_DELTA_GATE_EVALUATOR_DRYRUN_V0.md](./LUNA_CROSS_MODAL_SCENE_DELTA_GATE_EVALUATOR_DRYRUN_V0.md)）。
