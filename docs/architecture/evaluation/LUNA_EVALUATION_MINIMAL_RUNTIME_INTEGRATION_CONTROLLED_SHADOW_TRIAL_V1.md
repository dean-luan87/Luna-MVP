# Evaluation — Minimal Runtime Integration Controlled Shadow Trial v1

**Phase**：`Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001`  
**输出**：`_eval_out/minimal_runtime_integration_controlled_shadow_trial_v1_smoke_v0/`

本阶段执行的是 controlled shadow trial，不是 live runtime。  
runner 仅生成 candidate trace、Speech Gate shadow decision、VOP shadow event、abort/boundary report 和 observability trace。

关键产物：

- `controlled_trial_input_trace.json`
- `shadow_execution_steps.json`
- `shadow_candidate_trace.json`
- `speech_gate_shadow_decisions.json`
- `vop_shadow_events.json`
- `controlled_shadow_abort_checks.json`
- `observability_trace.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

见同目录 [GO/NO_GO Pack](./LUNA_EVALUATION_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_V1_GO_NO_GO_PACK_V0.md)。
