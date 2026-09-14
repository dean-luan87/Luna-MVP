# Luna Evaluation — OCR Lightweight Provider ROI Input Smoke v0

**Phase**: `Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001`

## 目的

验证 **大图 + 指定 ROI → 中台裁剪（`unit_type=roi`）→ Provider Input Pack → RapidOCR lightweight** 的最小真实链路：  
`source_image_ref` 指向原图，ROI 像素写入独立 `image_ref`；`coordinate_transform` 记录 **crop offset**（`offset_x` / `offset_y`）及 ROI 内可选 **二次缩放**（当 ROI 最长边超过 `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`，默认 512）。  
**非 benchmark**；不进 MidPlatform；不写 WorldModel；不启 PaddleOCR；不改 routing；不把 RapidOCR 设为默认 provider。

## 前置

- `Phase-OCR-Lightweight-Provider-Text-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Real-Provider-Adapter-001` = GO  
- `Phase-OCR-ImageInput-Normalization-Pipeline-001` = GO  
- `Phase-OCR-Input-Size-Governance-001` = GO  

## 治理配置

- 默认与 normalized input smoke 相同：仓库 `configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json`；若缺失则 runner 内嵌等价 JSON（含 `preferred_max_side=512`，用于整图 gate 语义；**ROI 分支**在裁剪后可再按轻量 cap 缩放）。

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_lightweight_provider_roi_input_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_lightweight_provider_roi_input_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_lightweight_provider_roi_input_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_lightweight_provider_roi_input_smoke_v0
```

可选：`--roi 400,500,1200,800`（默认与阶段说明一致）。

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_lightweight_provider_roi_input_governance.json` | 本次 run 使用的治理快照。 |
| `ocr_lightweight_provider_roi_input_original.png` | 原图（默认 2200×2200，ROI 外留白）。 |
| `ocr_lightweight_provider_roi_input_roi.png` | 从 pack 中 `image_ref` 复制的裁剪/缩放后 ROI 图。 |
| `ocr_lightweight_provider_roi_input_request.json` | `OCRRequestV0`（`input_type=roi`，`roi_refs`）。 |
| `ocr_lightweight_provider_roi_input_result.json` | 主线完整结果。 |
| `ocr_lightweight_provider_roi_input_pack.json` | `ocr_provider_input_pack`（单 unit，`roi`）。 |
| `ocr_lightweight_provider_roi_input_bridge_pack.json` | `bridge_pack`。 |
| `ocr_lightweight_provider_roi_input_audit_report.json` | 扁平 `audit`。 |
| `ocr_lightweight_provider_roi_input_summary.json` | 摘要。 |
| `ocr_lightweight_provider_roi_input_notes.md` | 短说明。 |
| `ocr_lightweight_provider_roi_input_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** 与 **CONDITIONAL_GO**：退出码 **0**；**NO_GO**：**2**。
