# Luna — Evaluation: OCR MidPlatform Gated Runtime Path Alignment v0

**Phase**：`Phase-OCR-MidPlatform-Gated-Runtime-Path-Alignment-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_ocr_midplatform_gated_runtime_path_alignment_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_midplatform_gated_runtime_path_alignment_v0 \
  --mixed-video-poster-batch-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 \
  --mixedvideo-linebox-trace-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --readability-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --ocr-evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_ocr_midplatform_gated_runtime_path_alignment_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_midplatform_gated_runtime_path_alignment_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_MIDPLATFORM_GATED_RUNTIME_PATH_ALIGNMENT_GO_NO_GO_PACK_V0.md)
