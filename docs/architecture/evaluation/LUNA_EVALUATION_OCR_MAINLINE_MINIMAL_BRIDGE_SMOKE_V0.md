# Luna Evaluation — OCR Mainline Minimal Bridge Smoke v0

**Phase**: `Phase-OCR-Mainline-Minimal-Bridge-001`

## 命令

```bash
python3 tools/evaluation/ocr/run_ocr_mainline_bridge_smoke_v0.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_bridge_smoke_v0
```

可选：`--image /ABS/path.png`（未提供时在 output_root 生成 512×512 PNG）。

## 产物

- `ocr_mainline_bridge_smoke_summary.json`  
- `ocr_mainline_bridge_request.json`  
- `ocr_mainline_bridge_result.json`  
- `ocr_mainline_bridge_audit_report.json`  
- `ocr_mainline_bridge_notes.md`  
- `ocr_mainline_bridge_smoke_verifier_report.json`（verifier 写入）

## 语义

Smoke **GO** 表示「stub 骨架链路可跑通」；**不**表示 OCR 生产可用。
