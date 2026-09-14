# Luna — Evaluation: CrossModal Vision OCR Fusion Candidate DryRun v0

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_fusion_candidate_dryrun_v0.py \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0 \
  --text-bearing-sample-root /abs/path/_eval_out/vision_roi_text_bearing_ocr_sample_smoke_v0 \
  --rapidocr-reference-only-root /abs/path/_eval_out/cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_fusion_candidate_dryrun_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0
```

GO / NO_GO：见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_FUSION_CANDIDATE_DRYRUN_GO_NO_GO_PACK_V0.md)
