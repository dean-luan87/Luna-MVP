# Luna — Evaluation: Vision ROI → OCRRequest Bridge v0

**Phase**：`Phase-Vision-ROI-to-OCR-Request-Bridge-001`

## 输入

- `vision_roi_proposal_candidate.json`
- `vision_provider_input_pack.json`
- `vision_roi_proposal_audit_report.json`（可选引用）

默认 proposal root：`_eval_out/vision_roi_proposal_stub_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/vision/run_vision_roi_to_ocr_request_bridge_v0.py \
  --output-root /abs/path/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0 \
  --vision-roi-proposal-root /abs/path/_eval_out/vision_roi_proposal_stub_smoke_v0

python3 tools/evaluation/vision/verify_vision_roi_to_ocr_request_bridge_v0.py \
  --smoke-root /abs/path/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `vision_roi_to_ocr_request_candidates.json` | OCRRequest 候选列表 |
| `vision_roi_to_ocr_request_candidate_matrix.json` | 候选矩阵 |
| `vision_roi_to_ocr_rejection_matrix.json` | 未触发 OCR 的 ROI |
| `vision_roi_to_ocr_request_bridge_audit_report.json` | 边界审计 |
| `vision_roi_to_ocr_request_bridge_verifier_report.json` | Verifier 结论 |

## GO / NO_GO

见 [LUNA_EVALUATION_VISION_ROI_TO_OCR_REQUEST_BRIDGE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_ROI_TO_OCR_REQUEST_BRIDGE_GO_NO_GO_PACK_V0.md)
