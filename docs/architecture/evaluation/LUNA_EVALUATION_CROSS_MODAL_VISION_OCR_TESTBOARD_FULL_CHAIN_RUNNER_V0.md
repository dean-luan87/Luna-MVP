# Luna — Evaluation: CrossModal Vision OCR TestBoard Full-Chain Case Runner v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_full_chain_runner_v0.py \
  --testboard-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_expansion_smoke_v0 \
  --output-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_runner_smoke_v0

python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_testboard_full_chain_runner_v0.py \
  --smoke-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_full_chain_runner_smoke_v0
```

## 环境

与 TestBoard expansion 相同：`.venv-tx`、`LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0=true`、`LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0=true`、`LUNA_OCR_SUBMISSION_EVAL_ONLY=true`。

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_TESTBOARD_FULL_CHAIN_RUNNER_GO_NO_GO_PACK_V0.md)
