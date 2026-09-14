# Luna Evaluation — OCR ROI Coordinate Lift Smoke v0

**Phase**: `Phase-OCR-ROI-Evidence-Coordinate-Lift-001`

## 目的

在 **ROI `processing_policy.strategy=roi`** 且 `coordinate_transform.mode=roi_crop` 的前提下，将 RapidOCR 返回的 **ROI-local** 多边形 / 框，按

`original = offset + local / scale`

抬升到 **原图坐标系**，写入 `ocr_evidence.text_items` 与 `bridge_pack.eligible_text_evidence`，并在 audit 中记录 lift 与 geometry 可用性。  
**不**改 routing；**不**进 MidPlatform；**不**启 PaddleOCR；**不**伪造无 provider 时的 original 几何。

## 前置

- `Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001` = GO  
- `Phase-OCR-ImageInput-Normalization-Pipeline-001` = GO  

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_roi_coordinate_lift_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_roi_coordinate_lift_smoke_v0 \
  --reference-roi-smoke-root /ABS/PATH/_eval_out/ocr_lightweight_provider_roi_input_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_roi_coordinate_lift_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_roi_coordinate_lift_smoke_v0
```

`--reference-roi-smoke-root` 仅写入摘要备注，可省略。

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_roi_coordinate_lift_governance.json` | 本次 run 使用的治理（与 ROI smoke 对齐）。 |
| `ocr_roi_coordinate_lift_canvas.png` | 合成大图 + ROI 内文字。 |
| `ocr_roi_coordinate_lift_summary.json` | 摘要（含 `coordinate_transform` 与 audit lift 字段）。 |
| `ocr_roi_coordinate_lift_items.json` | `ocr_evidence.text_items`（含 local / original 几何与 `coordinate_lift_applied`）。 |
| `ocr_roi_coordinate_lift_bridge_pack.json` | `bridge_pack`（含 `eligible_text_evidence`）。 |
| `ocr_roi_coordinate_lift_audit_report.json` | 扁平 audit。 |
| `ocr_roi_coordinate_lift_notes.md` | 短说明。 |
| `ocr_roi_coordinate_lift_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** 与 **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
