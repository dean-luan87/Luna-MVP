# Evaluation — WorldModel Lookup for Reading Framework v1

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_worldmodel_lookup_for_reading_framework_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_lookup_for_reading_framework_v1_smoke_v0 \
  --ocr-mainline-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_governance_closure_v1_smoke_v0 \
  --software-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_software_mainline_closure_v1_smoke_v0 \
  --tsc-reevaluation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_reevaluation_dryrun_v1_smoke_v0 \
  --isrc-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_runtime_dryrun_v1_smoke_v0 \
  --rrd-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_runtime_dryrun_v1_smoke_v0 \
  --worldmodel-unresolved-slot-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0 \
  --memory-governance-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/confirmed_text_evidence_memory_governance_contract_v1_smoke_v0 \
  --memory-handoff-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/confirmed_text_evidence_memory_handoff_dryrun_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_worldmodel_lookup_for_reading_framework_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_lookup_for_reading_framework_v1_smoke_v0
```

## GO/NO-GO Pack

[LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1_GO_NO_GO_PACK_V0.md)
