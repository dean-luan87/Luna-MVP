# Evaluation — Voice Dialogue Task Control Contract v1

**Phase**：`Voice-Dialogue-Task-Control-Contract-v1-001`  
**输出根目录**：`_eval_out/voice_dialogue_task_control_contract_v1_smoke_v0/`

## 命令

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min

python3 tools/evaluation/midplatform/run_voice_dialogue_task_control_contract_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_dialogue_task_control_contract_v1_smoke_v0 \
  --basic-loop-plan-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/luna_basic_functional_loop_stabilization_plan_v1_smoke_v0 \
  --voice-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_runtime_dryrun_v1_smoke_v0 \
  --vop-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0 \
  --user-clarification-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_clarification_prompt_runtime_dryrun_for_reading_v1_smoke_v0 \
  --user-clarification-parsing-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_clarification_response_parsing_dryrun_for_reading_v1_smoke_v0 \
  --task-scene-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_runtime_dryrun_v1_smoke_v0 \
  --task-scene-reevaluation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_reevaluation_dryrun_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_voice_dialogue_task_control_contract_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_dialogue_task_control_contract_v1_smoke_v0
```

## 输入 roots（必读）

- Basic Functional Loop Stabilization Plan
- Voice Guidance Runtime + VOP Adapter
- User Clarification Runtime + Parsing
- Task Scene Context Runtime + Reevaluation
- OCR Activation + STC
- System Health + Simulation (`developer_full`)

## 关键产物

- `voice_dialogue_task_control_contract_v1_summary.json`
- intent / command schema、handoff、policies、template matrix、FSM contract
- `voice_dialogue_task_control_final_decision_v1.json` → `VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_READY`

## GO 语义

- contract_only；无 ASR/LLM/TTS/VOP；无任务状态变更；`no_write_boundary_pass_rate=1.0`
- verifier `verdict=GO`

详见 [GO/NO-GO Pack](./LUNA_EVALUATION_VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_V1_GO_NO_GO_PACK_V0.md)。
