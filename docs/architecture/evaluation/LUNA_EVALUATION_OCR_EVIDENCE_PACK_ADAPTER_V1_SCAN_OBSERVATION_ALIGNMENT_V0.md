# Luna — Evaluation: OCR Evidence Pack Adapter v1 Scan Observation Alignment v0

**Phase**：`Phase-OCR-Evidence-Pack-Adapter-v1-ScanObservation-Alignment-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_GO_NO_GO_PACK_V0.md)
