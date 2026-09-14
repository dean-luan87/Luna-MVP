# Luna — Evaluation: CrossModal Vision OCR TestBoard v0 Closure

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_v0_closure_v0.py \
  --testboard-expansion-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_expansion_smoke_v0 \
  --full-chain-3-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_runner_smoke_v0 \
  --lowquality-partial-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_lowquality_partial_smoke_v0 \
  --full-chain-5-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_5cases_smoke_v0 \
  --mixed-cnen-falsepositive-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_smoke_v0 \
  --full-chain-7-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_7cases_smoke_v0 \
  --duplicate-conflicting-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_duplicate_conflicting_smoke_v0 \
  --non-text-rejection-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_non_text_roi_rejection_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_v0_closure_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_v0_closure_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V0_CLOSURE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_V0_CLOSURE_GO_NO_GO_PACK_V0.md)
