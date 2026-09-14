# Evaluation — Task Manager Runtime DryRun v1

**Phase**：`Task-Manager-Runtime-DryRun-v1-001`  
**输出**：`_eval_out/task_manager_runtime_dryrun_v1_smoke_v0/`

## 命令

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min

python3 tools/evaluation/midplatform/run_task_manager_runtime_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_manager_runtime_dryrun_v1_smoke_v0 \
  --task-manager-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_manager_contract_v1_smoke_v0 \
  --midplatform-task-state-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_task_state_runtime_dryrun_v1_smoke_v0 \
  --voice-dialogue-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_dialogue_task_control_runtime_dryrun_v1_smoke_v0 \
  --basic-loop-plan-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/luna_basic_functional_loop_stabilization_plan_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_task_manager_runtime_dryrun_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_manager_runtime_dryrun_v1_smoke_v0
```

## 期望

- `final_decision=TASK_MANAGER_RUNTIME_DRYRUN_READY_FOR_VISION_OCR_INGEST_AND_NAVIGATION_LOOP`
- 12 task state + 12 lifecycle candidates intake
- enrichment / verification / execution support candidates 生成
- `allowed_now=false`；`no_write_boundary_pass_rate=1.0`

详见 [GO/NO-GO Pack](./LUNA_EVALUATION_TASK_MANAGER_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md)。
