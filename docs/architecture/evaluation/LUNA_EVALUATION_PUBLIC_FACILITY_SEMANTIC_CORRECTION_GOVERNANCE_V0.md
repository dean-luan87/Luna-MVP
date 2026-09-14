# Luna — Evaluation: Public Facility Semantic Correction Governance v0

```bash
python3 tools/evaluation/midplatform/run_public_facility_semantic_correction_governance_v0.py \
  --metrics-schema-root /abs/path/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_smoke_v0 \
  --output-root /abs/path/_eval_out/public_facility_semantic_correction_governance_smoke_v0

python3 tools/evaluation/midplatform/verify_public_facility_semantic_correction_governance_v0.py \
  --smoke-root /abs/path/_eval_out/public_facility_semantic_correction_governance_smoke_v0
```

GO/NO_GO：本阶段 governance-only；`default_ocr_mainline_allowed=false`；主证据非 OCRTextEvidence；audit 无 OCR/写入。
