# Luna — Evaluation: MixedVideo OCR Scan LineBox Trace + Source Quality Gate v0

**Phase**：`Phase-MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --mixed-batch-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 \
  --readability-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --p0-video-path /Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0
```

## 输入 roots

| Root | 用途 |
|------|------|
| `cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0` | selected frame plan、video pack、scan preview |
| `realvideo_ocr_readability_governance_smoke_v0` | 可读性治理参考 |
| `ocr_evidence_pack_spatiotemporal_semantic_contract_v0` | Evidence Pack 合同 |
| `cross_modal_vision_ocr_benchmark_real_values_smoke_v0` | benchmark 链接（不更新分数） |
| `system_health_center_governance_v0` | system health 链接 |
| `simulation_lab_minimal_harness_v0/developer_full` | simulation context |

## GO / NO_GO

见 [LUNA_EVALUATION_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_GO_NO_GO_PACK_V0.md)
