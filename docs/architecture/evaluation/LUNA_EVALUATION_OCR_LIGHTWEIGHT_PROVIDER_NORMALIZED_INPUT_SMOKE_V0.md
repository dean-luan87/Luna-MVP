# Luna Evaluation — OCR Lightweight Provider Normalized Input Smoke v0

**Phase**: `Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001`

## 目的

验证 **大图 → ImageInputGate（CONDITIONAL_ALLOW + downscale）→ Normalization → `downscaled_full_image` input_pack → RapidOCR lightweight** 全链路：**原图不直通**真实 provider；归一化后 **边长 ≤ `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`（默认 512）**；**非 benchmark**，不进 MidPlatform，不改 routing，不启 Paddle。

## 前置

- `Phase-OCR-Lightweight-Provider-Text-Smoke-001` = GO  
- `Phase-OCR-Lightweight-Real-Provider-Adapter-001` = GO  
- `Phase-OCR-ImageInput-Normalization-Pipeline-001` = GO  
- OCR Input Size Governance（评测索引）  
- 参考 text smoke 产物：`_eval_out/ocr_lightweight_provider_text_smoke_v0`（仅索引，不强制同次运行）

## 治理配置

- 仓库内默认：`configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json`（`preferred_max_side` / `fallback_max_side` = **512**）。  
- Runner 会将治理 **复制** 到 `--output-root/ocr_lightweight_provider_normalized_input_governance.json`；若仓库路径不可用则写入 **内嵌等价 JSON**（保证 `preferred_max_side=512`）。

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_lightweight_provider_normalized_input_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_lightweight_provider_normalized_input_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_lightweight_provider_normalized_input_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_lightweight_provider_normalized_input_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_lightweight_provider_normalized_input_governance.json` | 本次 run 使用的治理（512 边 downscale）。 |
| `ocr_lightweight_provider_normalized_input_original.png` | 大图输入（默认 2200×2200）。 |
| `ocr_lightweight_provider_normalized_input_request.json` | 请求快照。 |
| `ocr_lightweight_provider_normalized_input_result.json` | 主线完整结果。 |
| `ocr_lightweight_provider_normalized_input_pack.json` | `ocr_provider_input_pack`（单 unit，`downscaled_full_image`）。 |
| `ocr_lightweight_provider_normalized_input_bridge_pack.json` | `bridge_pack`。 |
| `ocr_lightweight_provider_normalized_input_audit_report.json` | 扁平 `audit`。 |
| `ocr_lightweight_provider_normalized_input_summary.json` | 摘要（含 `coordinate_transform` 摘要）。 |
| `ocr_lightweight_provider_normalized_input_notes.md` | 短说明。 |
| `ocr_lightweight_provider_normalized_input_verifier_report.json` | Verifier（`GO` / `CONDITIONAL_GO` / `NO_GO`）。 |

## Verifier 退出码

- **GO** 与 **CONDITIONAL_GO**：退出码 **0**；**NO_GO**：**2**。
