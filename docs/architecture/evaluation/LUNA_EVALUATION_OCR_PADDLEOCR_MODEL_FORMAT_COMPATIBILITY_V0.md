# LUNA Evaluation — PaddleOCR Model Format Compatibility v0（Phase-PaddleOCR-ModelFormat-001）

## 目标

在 **不下载模型、不 `PaddleOCR()`、不 OCR 推理、不改 OCR routing、不进主线/白盒/MidPlatform** 的前提下，完成 **PaddleOCR 已安装版本 + `PaddleOCR.__init__` 静态签名 + Luna manifest v0 期望格式** 的兼容性评审，并输出 **格式兼容性矩阵** 与 **A/B/C 后续路线选项**。

## 冻结事实（输入）

- **Readiness-001** = GO（历史结论；本 phase 不重复跑 readiness）。  
- **Weights-003** = CONDITIONAL_GO；本地发现链：**无**成对 `inference.pdmodel` / `inference.pdiparams`。  
- **Manifest v0**：仍要求旧式 **Paddle Inference** 六文件（det/rec/cls × pdmodel + pdiparams）。  
- **PP-OCRv5**：官方/社区包格式**可能**与上述旧式结构**不完全一致**，不得假设「下载 v5 即满足 manifest」。

## 工具

```text
python3 tools/evaluation/ocr/review_paddleocr_model_format_compatibility_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  [--output-root <ABS_DIR>]

python3 tools/evaluation/ocr/verify_paddleocr_model_format_review_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --review-root <上一步 output_root>
```

默认 `output-root`：`~/LunaRuntime/logs/evaluation/paddleocr_model_format_review_001_<UTC>/`

## 产出文件

| 文件 | 作用 |
|------|------|
| `paddleocr_model_format_review_summary.json` | 总摘要、`constraints`、artifact 索引、`review_verdict`。 |
| `paddleocr_installed_version_report.json` | distribution / import 版本与包路径。 |
| `paddleocr_api_signature_report.json` | `PaddleOCR.__init__` 参数表（仅 inspect）。 |
| `paddleocr_manifest_format_compatibility_matrix.json` | manifest / 格式风险 / API 表面对齐说明。 |
| `paddleocr_model_format_route_options.json` | 路线 A/B/C（旧 inference / 新格式适配 / v4v3 降级）。 |
| `paddleocr_model_format_review_notes.md` | 人类可读摘要。 |

## 验收口径（摘要）

- **GO**：本机可 import `paddleocr` 且能解析 `PaddleOCR.__init__` 签名；矩阵与路线齐全；verifier **GO**；`constraints` 全为「未下载、未实例化、未推理、未改 routing」。  
- **CONDITIONAL_GO**：包未安装或签名无法解析时，仍以 manifest 与路线 JSON 落盘，但 `review_verdict` 可能为 CONDITIONAL_GO；**需人工**对照官方 PP-OCRv5 实际发布物。  
- **NO_GO**：若 verifier 发现缺输出、缺 A/B/C、或 `constraints` 被伪造为已下载/已构造等（本工具链正常情况下不应出现）。
