# Evaluation — Static Reading ISRC Localization Runtime DryRun v1

**Phase ID**：`Static-Reading-Information-Source-Localization-Runtime-DryRun-v1-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_static_reading_information_source_localization_runtime_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_runtime_dryrun_v1_smoke_v0 \
  --tsc-reevaluation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_reevaluation_dryrun_v1_smoke_v0 \
  --response-parsing-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_clarification_response_parsing_dryrun_for_reading_v1_smoke_v0 \
  --information-source-policy-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_policy_v1_smoke_v0 \
  --readable-region-policy-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_guidance_policy_v1_smoke_v0 \
  --task-scene-policy-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_policy_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_static_reading_information_source_localization_runtime_dryrun_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_runtime_dryrun_v1_smoke_v0
```

## GO 要点

- 4 条 query intake；candidate source area matrix；exclusion + ranking placeholder  
- ranked source area candidates + RRD handoff；`final_decision=READY_FOR_READABLE_REGION_DISCOVERY_RUNTIME_LATER`  
- no-write boundary；verifier GO

## 架构说明

[LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md](../midplatform/LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md)

## GO/NO-GO Pack

[LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md)
