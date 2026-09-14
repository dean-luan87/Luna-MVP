# Luna — Evaluation: OCR Semantic Candidate Generator DryRun v0

**Phase**：`Phase-OCR-Semantic-Candidate-Generator-DryRun-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_ocr_semantic_candidate_generator_dryrun_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_generator_dryrun_smoke_v0 \
  --ocr-evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --ocr-evidence-pack-adapter-update-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_update_smoke_v0 \
  --realvideo-readability-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --poster-fusion-gate-chain-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_gate_chain_closure_smoke_v0 \
  --public-facility-runtime-dryrun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/public_facility_runtime_dryrun_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_ocr_semantic_candidate_generator_dryrun_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_generator_dryrun_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_DRYRUN_GO_NO_GO_PACK_V0.md)
