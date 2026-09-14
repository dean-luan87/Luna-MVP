# Luna Evaluation — OCR Lightweight Provider Multi-ROI Smoke v0

**Phase**: `Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001`

## 目的

验证 **`input_type=roi_list`** 时：中台生成 **多个 `unit_type=roi` 的 input_units**；RapidOCR lightweight **按 unit 受控循环调用**；每条 `text_item` 绑定 **`unit_id` / `roi_id` / `source_unit_ref`**；**ROI 坐标抬升**按各 unit 的 `coordinate_transform` 分别执行；`bridge_pack.eligible_text_evidence` 合并输出；`reading_order_candidate` 仅为 **`roi_order_then_provider_order`** 占位（**不做版面语义推断**）。  
**不**改 routing；**不**进 MidPlatform；**不**启 PaddleOCR；**不接** Scene Delta；**不做**自动视角分割 ROI。

## 前置

- `Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001` = GO  
- `Phase-OCR-ROI-Evidence-Coordinate-Lift-001` = GO  
- `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001` = GO  
- `Phase-OCR-ImageInput-Normalization-Pipeline-001` = GO  

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_lightweight_provider_multi_roi_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_lightweight_provider_multi_roi_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_lightweight_provider_multi_roi_governance.json` | 治理快照。 |
| `ocr_lightweight_provider_multi_roi_original.png` | 2200×2200 合成原图（三 ROI 内文字）。 |
| `ocr_lightweight_provider_multi_roi_request.json` | `OCRRequestV0`（`roi_list` + 多条 `roi_refs`）。 |
| `ocr_lightweight_provider_multi_roi_input_pack.json` | `ocr_provider_input_pack`（`strategy=roi_list`，多 unit）。 |
| `ocr_lightweight_provider_multi_roi_result.json` | 主线完整结果。 |
| `ocr_lightweight_provider_multi_roi_bridge_pack.json` | `bridge_pack`（含 `eligible_text_evidence`）。 |
| `ocr_lightweight_provider_multi_roi_coordinate_lift_matrix.json` | 坐标变换矩阵 + 证据几何摘要。 |
| `ocr_lightweight_provider_multi_roi_smoke_summary.json` | 摘要。 |
| `ocr_lightweight_provider_multi_roi_audit_report.json` | 扁平 audit。 |
| `ocr_lightweight_provider_multi_roi_notes.md` | 短说明。 |
| `ocr_lightweight_provider_multi_roi_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO** / **CONDITIONAL_GO**：**0**；**NO_GO**：**2**。
