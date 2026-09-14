# Evaluation — OCR StaticReading Poster RealVideo Regression Route Compliance v1

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_ocr_staticreading_poster_realvideo_regression_route_compliance_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0 \
  --closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_software_mainline_closure_v1_smoke_v0 \
  --staticreading-ocrrequest-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_staticreading_v1_smoke_v0 \
  --memory-handoff-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/confirmed_text_evidence_memory_handoff_dryrun_v1_smoke_v0 \
  --hardware-adapter-stub-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_runtime_adapter_implementation_stub_v1_smoke_v0 \
  --rrd-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_runtime_dryrun_v1_smoke_v0 \
  --realvideo-frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --realvideo-ocr-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_evidence_readonly_consumer_smoke_v0 \
  --realvideo-text-bearing-planning-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_text_bearing_sample_planning_smoke_v0 \
  --poster-layout-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_layout_segmentation_governance_smoke_v0 \
  --poster-fusion-policy-gate-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_policy_gate_dryrun_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --testboard-metrics-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_schema_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_ocr_staticreading_poster_realvideo_regression_route_compliance_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0
```

## GO/NO-GO Pack

[LUNA_EVALUATION_OCR_STATICREADING_POSTER_REALVIDEO_REGRESSION_ROUTE_COMPLIANCE_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_STATICREADING_POSTER_REALVIDEO_REGRESSION_ROUTE_COMPLIANCE_V1_GO_NO_GO_PACK_V0.md)
