# LUNA Evaluation — PaddleOCR Manifest v1 Cache Materialize v0（Phase-PaddleOCR-ManifestV1-CacheMaterialize-001）

## 目标

将 **官方 det / rec / cls** 模型物料落到 **`model_root`**（见 candidate），完成 **hash pin 观测链**：**Fill → Snapshot → Snapshot verifier → Completion**，直至 **`completion_verdict == GO`**（等价于 snapshot 业务 **GO** + **pinning_complete** + **sha256** 齐）。

## 严禁

- **不** `PaddleOCR()`、**不** OCR 推理、**不**替换 RapidOCR、**不**进主线 / 白盒 / MidPlatform、**不**改 OCR routing、**不**设默认 provider。  
- **不**伪造 **sha256**、**不**把空目录标为 **`pinning_complete=true`**。

## 编排工具

```text
python3 tools/evaluation/ocr/run_paddleocr_manifest_v1_cache_materialize_v0.py \
  --repo-root /Users/luanlei/Desktop/Luna-Core \
  --prepare-root <ABS_CACHE_PREPARE_OUT> \
  [--output-root <ABS_MATERIALIZE_ROOT>] \
  [--copy-from <ABS_LOCAL_DET_REC_CLS_TREE>] \
  [--allow-download --download-url-manifest <ABS_URL_JSON>]
```

在 **`materialize_output_root`** 下生成 **`fill/`**、**`snapshot/`**、**`completion/`** 子目录及 **`paddleocr_manifest_v1_cache_materialize_summary.json`**。

## 验收工具

```text
python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_cache_materialize_v0.py \
  --materialize-root <ABS_MATERIALIZE_ROOT>
```

- **`verdict: GO`**：summary 中 **`materialize_verdict == GO`** 且无结构矛盾。  
- **`verdict: CONDITIONAL_GO`**：物料未齐或 completion 仍为 CONDITIONAL_GO，但产物与目录结构正常。  
- **`verdict: NO_GO`**：summary 宣称 GO 但与 pinning/sha/missing 矛盾，或缺关键产物。

## 与 Controlled Trial 的边界

**本 phase 结束于「缓存可 pin + completion GO」**；**不**进入 **Phase-PaddleOCR-Controlled-Trial-001**（trial 须单独闸门）。
