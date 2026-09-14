# Luna — Evaluation: RealVideo OCR Readability Governance v0

**Phase**：`Phase-RealVideo-OCR-Readability-Governance-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_realvideo_ocr_readability_governance_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --text-bearing-sample-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_text_bearing_sample_planning_smoke_v0 \
  --realvideo-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_closure_smoke_v0 \
  --realvideo-reference-update-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_update_smoke_v0 \
  --realvideo-readonly-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_evidence_readonly_consumer_smoke_v0 \
  --existing-video-candidate-scan-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_text_bearing_existing_video_candidate_scan_complex_6m42s_v0 \
  --poster-fusion-gate-chain-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_gate_chain_closure_smoke_v0 \
  --public-facility-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_runtime_dryrun_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_realvideo_ocr_readability_governance_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_REALVIDEO_OCR_READABILITY_GOVERNANCE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_REALVIDEO_OCR_READABILITY_GOVERNANCE_GO_NO_GO_PACK_V0.md)
