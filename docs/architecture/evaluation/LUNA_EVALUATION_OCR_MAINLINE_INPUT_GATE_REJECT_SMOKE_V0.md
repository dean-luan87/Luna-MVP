# Luna Evaluation — OCR Mainline Input Gate Reject Smoke v0

**Phase**: `Phase-OCR-Mainline-InputGate-Reject-Smoke-001`

## 目的

在 **`allow_full_image=false`** 下，验证 **超限大图** 被 **ImageInputGate REJECT**，**不**调用 stub 以外的逻辑、**不**产生含 `MOCK_TEXT` 的误导性 evidence。

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_mainline_bridge_reject_smoke_v0.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_bridge_reject_smoke_v0 \
  --width 3000 \
  --height 5334
```

## 期望

- `input_gate.gate_verdict` = **REJECT**，`oversized` = **true**  
- `recommended_input_strategy` ∈ {**downscale_required**, **tile_required**}（由像素预算与 `max_megapixels_requires_tiling` 决定）  
- `status` = **rejected**；`bridge_pack.pack_status` = **rejected_no_evidence**  
- audit 全 false；verifier **GO**
