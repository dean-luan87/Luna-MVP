# Luna Evaluation — OCR Lightweight Real Provider Adapter Smoke v0

**Phase**: `Phase-OCR-Lightweight-Real-Provider-Adapter-001`

## 目的

验证 **RapidOCR 轻量 adapter** 在 **显式 flag** 下可被选中并 **受 input_pack 边长策略约束**；默认 stub；Paddle runtime 关闭；超大图/不可用路径 **不得伪造真实成功**。

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_lightweight_real_provider_adapter_smoke_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_lightweight_real_provider_smoke_v0

python3 tools/evaluation/ocr/verify_ocr_lightweight_real_provider_adapter_smoke_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_lightweight_real_provider_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `ocr_lightweight_provider_adapter_smoke_summary.json` | A/B/C/D 摘要。 |
| `ocr_lightweight_provider_registry_snapshot.json` | `real`+`rapid` 开启时的 registry 快照。 |
| `ocr_lightweight_provider_selection_report.json` | Case B 的 `provider_selection_report`。 |
| `ocr_lightweight_provider_result.json` | Case B 完整 bridge 结果。 |
| `ocr_lightweight_provider_bridge_pack.json` | Case B `bridge_pack`。 |
| `ocr_lightweight_provider_audit_report.json` | Case B `audit`。 |
| `ocr_lightweight_provider_case_*.json` | 各用例结果。 |
| `ocr_lightweight_provider_notes.md` | 短说明。 |
| `ocr_lightweight_provider_verifier_report.json` | Verifier 输出。 |

## 用例摘要

- **A**：默认 flag → stub。  
- **B**：`LUNA_ENABLE_OCR_REAL_PROVIDER_V0=true` + `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0=true`，512×512；若 Rapid 可用则 **real_provider_invoked=true**，否则带 **unavailable / import** 类 reason 回退 stub。  
- **C**：在 B 基础上 `LUNA_OCR_RAPIDOCR_FORCE_UNAVAILABLE_V0=true` → 必须 **stub** + `provider_runtime_unavailable`。  
- **D**：同 B flag，3000×5334 + `allow_full_image` → 轻量策略 **拒绝**真实调用（`edge_exceeds_lightweight_cap`）或 gate **rejected**。
