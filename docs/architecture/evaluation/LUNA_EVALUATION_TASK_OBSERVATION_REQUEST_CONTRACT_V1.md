# Evaluation — Task Observation Request Contract v1

**Phase**：`Task-Observation-Request-Contract-v1-001`  
**输出**：`_eval_out/task_observation_request_contract_v1_smoke_v0/`

## 命令

见同目录 [GO/NO-GO Pack](./LUNA_EVALUATION_TASK_OBSERVATION_REQUEST_CONTRACT_V1_GO_NO_GO_PACK_V0.md)。

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_task_observation_request_contract_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_observation_request_contract_v1_smoke_v0 \
  --basic-loop-audit-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/basic_functional_loop_runtime_logic_audit_correction_v1_smoke_v0 \
  --task-manager-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_manager_runtime_dryrun_v1_smoke_v0 \
  --task-manager-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_manager_contract_v1_smoke_v0 \
  --midplatform-task-state-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_task_state_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_governance_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --voice-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_runtime_dryrun_v1_smoke_v0 \
  --vop-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0 \
  --hardware-stub-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_runtime_adapter_implementation_stub_v1_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
python3 tools/evaluation/midplatform/verify_task_observation_request_contract_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/task_observation_request_contract_v1_smoke_v0
```
