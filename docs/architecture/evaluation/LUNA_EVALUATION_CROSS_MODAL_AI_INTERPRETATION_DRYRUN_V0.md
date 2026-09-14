# Luna — Evaluation: CrossModal AI Interpretation DryRun v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_ai_interpretation_dryrun_v0.py \
  --output-root /abs/path/_eval_out/cross_modal_ai_interpretation_dryrun_smoke_v0 \
  --review-queue-root /abs/path/_eval_out/cross_modal_fusion_review_queue_smoke_v0 \
  --fusion-candidate-dryrun-root /abs/path/_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_ai_interpretation_dryrun_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_ai_interpretation_dryrun_smoke_v0
```

GO / NO_GO：见 [LUNA_EVALUATION_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_AI_INTERPRETATION_DRYRUN_GO_NO_GO_PACK_V0.md)
