# Luna — Evaluation: TestBoard Full-Chain Runner Update 5 Cases v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_full_chain_runner_update_5cases_v0.py \
  --lowquality-partial-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_lowquality_partial_smoke_v0 \
  --previous-full-chain-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_runner_smoke_v0 \
  --testboard-expansion-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_expansion_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_5cases_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_full_chain_runner_update_5cases_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_5cases_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_UPDATE_5CASES_GO_NO_GO_PACK_V0.md)
