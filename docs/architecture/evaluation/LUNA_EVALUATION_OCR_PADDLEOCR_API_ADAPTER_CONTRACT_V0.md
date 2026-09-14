# LUNA Evaluation — PaddleOCR Current API Adapter Contract v0（Phase-PaddleOCR-API-Adapter-Contract-001）

## 定位

在 **Controlled-Trial-001** 已证明可构造、可推理的前提下，将 **current API** 的调用与返回整理为 **evaluation-only adapter contract**：

- **优先 `predict()`**；失败或未暴露时 **受控回退 `ocr()`**，并记录 **`call_method`** 与 **`fallback_reason`**。  
- 将 raw 结果规范化为 **最小 normalized OCR evidence**（含 **`rec_texts` → `text_items` / `text_joined`** 等），供后续 provider adapter 对齐。

**不**：进主线、改 routing、替换 RapidOCR、白盒 / MidPlatform、benchmark、中台语义、扩大样本（**≤3**）。

## 前置

- **materialize_root**：`paddleocr_manifest_v1_cache_materialize_summary.json` 中 **`materialize_verdict == GO`**。  
- **pinned manifest**：`pinning_complete`、**sha256** 等与 CacheMaterialize 一致。

## 工具

```text
python3 tools/evaluation/ocr/paddleocr_current_api_adapter_contract_v0.py \
  --repo-root <ABS_Luna-Core> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  [--trial-root <ABS_PRIOR_TRIAL_ROOT>] \
  [--output-root <ABS_ADAPTER_OUT>] \
  [--constructor-only] \
  [--no-use-angle-cls] \
  [--image <ABS_IMG> ...]
```

```text
python3 tools/evaluation/ocr/verify_paddleocr_api_adapter_contract_v0.py \
  --adapter-root <ABS_ADAPTER_OUT> \
  [--materialize-root <ABS_MATERIALIZE_ROOT>]
```

## 产物

`paddleocr_api_adapter_*` JSON / `paddleocr_api_adapter_notes.md`；verifier 写 **`paddleocr_api_adapter_verifier_report.json`**。
