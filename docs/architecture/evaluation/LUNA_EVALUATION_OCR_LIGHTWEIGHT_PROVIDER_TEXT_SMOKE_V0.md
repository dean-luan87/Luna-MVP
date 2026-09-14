# Luna Evaluation — OCR Lightweight Provider Text Smoke v0

**Phase**: `Phase-OCR-Lightweight-Provider-Text-Smoke-001`

## 目的

在 **不改 routing、不进 MidPlatform、不启 PaddleOCR** 的前提下，用 **带简单文字的小图**（默认 ≤512×512）验证：在显式 flag 下 **RapidOCR** 能产出 **非空** `text_items` / `text_joined`，并进入 **bridge_pack**（**非 benchmark**，不做质量结论）。

## 前置

- `Phase-OCR-Lightweight-Real-Provider-Adapter-001` = GO  
- 参考 adapter 说明：[LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md](../ocr/LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md)

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_lightweight_provider_text_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_lightweight_provider_text_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_lightweight_provider_text_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_lightweight_provider_text_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `ocr_lightweight_provider_text_input.png` | 白底黑字测试图。 |
| `ocr_lightweight_provider_text_request.json` | `OCRRequestV0` 快照。 |
| `ocr_lightweight_provider_text_result.json` | 主线 bridge 完整结果。 |
| `ocr_lightweight_provider_text_bridge_pack.json` | `bridge_pack`。 |
| `ocr_lightweight_provider_text_audit_report.json` | `audit`。 |
| `ocr_lightweight_provider_text_smoke_summary.json` | 摘要。 |
| `ocr_lightweight_provider_text_notes.md` | 短说明。 |
| `ocr_lightweight_provider_text_verifier_report.json` | Verifier 输出（`verdict`: `GO` \| `CONDITIONAL_GO` \| `NO_GO`）。 |

## 说明

- **GO**：本机 RapidOCR 可用，且识别出 **非空** 文本。  
- **CONDITIONAL_GO**：RapidOCR **不可用**，走 **stub** 且 `provider_selection_reason_codes` 含可解释的 unavailable/import 等；**不得**伪造非空真实 OCR。  
- 退出码：`GO` 与 `CONDITIONAL_GO` 为 **0**；`NO_GO` 为 **2**。
