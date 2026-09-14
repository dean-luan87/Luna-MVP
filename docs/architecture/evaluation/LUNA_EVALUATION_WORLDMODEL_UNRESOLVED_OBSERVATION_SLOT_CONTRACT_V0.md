# Luna — Evaluation: WorldModel Unresolved Observation Slot Contract v0

**Phase**：`Phase-WorldModel-Unresolved-Observation-Slot-Contract-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_worldmodel_unresolved_observation_slot_contract_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0 \
  --ocr-evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --ocr-evidence-pack-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_update_smoke_v0 \
  --ocr-semantic-candidate-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_generator_dryrun_smoke_v0 \
  --readability-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --realvideo-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_reference_closure_smoke_v0 \
  --mixed-video-poster-batch-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_worldmodel_unresolved_observation_slot_contract_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_GO_NO_GO_PACK_V0.md)
