# LUNA Evaluation — PaddleOCR Quality & Runtime Benchmark v0（Phase-PaddleOCR-Evaluation-Benchmark-001）

## 定位

在 **evaluation-only** 条件下，基于 **pinned manifest** 与 **Materialize = GO**，对 **≤20 张** 本地样本运行 **PaddleOCR current API**（优先 `predict`），输出 **raw / normalized / evidence 形态摘要**、**质量指标**（有 ground truth 时）与 **运行时分位数**，并形成可复现报告。

**只做**：小样本评测、指标汇总、审计、verifier。

**不做**：替换 RapidOCR、改 routing、进 runtime / 白盒 / MidPlatform、写世界模型、中台语义、provider 切换、**下载模型**、**修改 pinned cache**、无边界批量评测；**不把 benchmark GO 当作上线许可**。

## 前置

- **`materialize_root`**：`paddleocr_manifest_v1_cache_materialize_summary.json` 中 **`materialize_verdict == GO`**。  
- **`--pinned-manifest`**：与 Materialize 产物一致的 **pinned JSON**。  
- **`--sample-manifest`**：`schema_version: paddleocr_benchmark_sample_manifest_v0`，**1–20** 条样本，`image_path` 为**可读绝对路径**。

## 工具

```text
python3 tools/evaluation/ocr/run_paddleocr_evaluation_benchmark_v0.py \
  --repo-root <ABS_Luna-Core> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  --sample-manifest <ABS_SAMPLE_MANIFEST_JSON> \
  [--output-root <ABS_BENCHMARK_OUT>] \
  [--no-use-angle-cls]
```

```text
python3 tools/evaluation/ocr/verify_paddleocr_evaluation_benchmark_v0.py \
  --benchmark-root <ABS_BENCHMARK_OUT>
```

## 样本清单示例

`configs/evaluation/ocr/paddleocr_benchmark_sample_manifest_v0.example.json`

## 产物

见 `paddleocr_benchmark_*.json`、`paddleocr_benchmark_notes.md`、`paddleocr_benchmark_verifier_report.json`。

## Contract 复用

归一化与 **`predict` / `ocr` fallback** 与 **`paddleocr_current_api_adapter_contract_v0.py`** 对齐（运行期通过 `importlib` 加载同文件中的实现）。
