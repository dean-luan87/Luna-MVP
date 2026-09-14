# Luna — Evaluation: TestBoard LowQuality PartialText Execution v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-LowQuality-PartialText-Execution-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_lowquality_partial_execution_v0.py \
  --testboard-expansion-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_expansion_smoke_v0 \
  --full-chain-runner-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_runner_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_lowquality_partial_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_lowquality_partial_execution_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_lowquality_partial_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_LOWQUALITY_PARTIAL_EXECUTION_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_LOWQUALITY_PARTIAL_EXECUTION_GO_NO_GO_PACK_V0.md)
