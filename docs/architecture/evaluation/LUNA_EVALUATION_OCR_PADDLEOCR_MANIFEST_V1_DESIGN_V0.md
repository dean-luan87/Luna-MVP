# LUNA Evaluation — PaddleOCR Manifest v1 Design v0（Phase-PaddleOCR-ManifestV1-Design-001）

## 目标

定义 **`paddleocr_current_api_model_manifest_v1`** 设计面：与 **当前 `PaddleOCR.__init__` 参数 / model dir 惯例** 对齐，并显式保留 **legacy 六文件 manifest** 为可选路线；**不**下载模型、**不** `PaddleOCR()`、**不** OCR 推理、**不**改 OCR routing、**不**替换 RapidOCR、**不设默认 provider**。

## 冻结事实

- **Readiness-001** = GO  
- **Weights-003** = CONDITIONAL_GO（本机无旧式六文件）  
- **ModelFormat-001** = GO（已产出 A/B/C 路线选项）  
- **Legacy**：`paddleocr_evaluation_readiness_manifest_v0.json` + `paddleocr_ppocrv5_model_files_manifest_v0.json` 仍为 **paddle_inference_legacy** 规划入口。

## 仓库内产物

| 路径 | 作用 |
|------|------|
| `configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json` | v1 字段示例（占位符，非 runtime 默认）。 |
| `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V1_DESIGN_V0.md` | v1 adapter 输出形状草案（设计-only）。 |

## 工具

```text
python3 tools/evaluation/ocr/review_paddleocr_manifest_v1_design_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  [--v1-example-relative configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json] \
  [--output-root <ABS_DIR>]

python3 tools/evaluation/ocr/verify_paddleocr_manifest_v1_design_v0.py \
  --repo-root <ABS_LUNA_CORE> \
  --design-root <上一步 output_root>
```

默认 `output-root`：`~/LunaRuntime/logs/evaluation/paddleocr_manifest_v1_design_001_<UTC>/`

## 设计原则（摘要）

1. **v1** 以 **`model_root` + `det_model_ref` / `rec_model_ref` / `cls_model_ref`** 描述离线缓存布局，语义上映射到 `PaddleOCR(det_model_dir=..., rec_model_dir=..., cls_model_dir=...)` 或等价官方推荐写法（以签名与文档为准）。  
2. **`model_format`**：`paddleocr_current_api` | `paddle_inference_legacy`，与 ModelFormat A/B/C 对齐。  
3. **`legacy_manifest_ref`**：始终可指回 v0 readiness，便于双轨与迁移说明。  
4. **治理字段**：`offline_cache_required`、`network_required`、`download_authorized`、`sha256_required`、`evaluation_candidate`、`runtime_default_enabled`、`mainline_provider`。

## 验收

见 `LUNA_EVALUATION_OCR_PADDLEOCR_MANIFEST_V1_GO_NO_GO_PACK_V0.md` 与 `verify_paddleocr_manifest_v1_design_v0.py`。
