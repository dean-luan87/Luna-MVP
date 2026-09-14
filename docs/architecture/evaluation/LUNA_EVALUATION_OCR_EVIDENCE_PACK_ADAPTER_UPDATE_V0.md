# Luna — Evaluation: OCR Evidence Pack Adapter Update v0

**Phase**：`Phase-OCR-Evidence-Pack-Adapter-Update-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_ocr_evidence_pack_adapter_update_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_update_smoke_v0 \
  --ocr-evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --realvideo-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_closure_smoke_v0 \
  --realvideo-reference-update-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_update_smoke_v0 \
  --realvideo-readonly-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_evidence_readonly_consumer_smoke_v0 \
  --realvideo-gated-submission-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_request_gated_submission_smoke_v0 \
  --poster-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_reference_closure_smoke_v0 \
  --poster-reference-update-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_reference_update_smoke_v0 \
  --poster-readonly-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_readonly_consumer_smoke_v0 \
  --poster-gated-execution-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_gated_execution_smoke_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_ocr_evidence_pack_adapter_update_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_update_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_UPDATE_GO_NO_GO_PACK_V0.md)
