# Existing Trial Inventory

| Asset | Current role |
|---|---|
| `run_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1.py` | CLI, 22 RCT cases, structured summary/artifacts |
| `dynamic_cognitive_flow_real_capability_trial_adapter_v1.py` | Trial orchestration and post-evidence cognitive handoff |
| `dynamic_cognitive_flow_real_capability_trial_types_v1.py` | Trial result record |
| `dynamic_cognitive_flow_real_capability_trial_fixture_v1.py` | RCT-01…RCT-22 definitions |
| `real_capability_runtime_admission_compatibility_adapter_v1.py` | New trial-local terminal → logical/runtime candidate bridge |
| `field_perception_real_vision_provider_adapter_v1.py` | Existing Provider admission and invocation |
| `yolo11n_external_provisioning_types_v1.py` | Existing model asset/checksum/dependency admission candidate |
| `real_visual_evidence_gateway_adapter_v1.py` | Observation/evidence admission |
| `ContextWorldStateControlledIntegrationEngineV1` | Current World candidate construction |
| `interpret_for_a()` | Dynamic Flow compatibility → A semantic interpretation |

Before modification, line counts were: adapter 443, Runner 230, Verifier 122,
fixture 50, types 48, package init 7. The new compatibility helper keeps the
large adapter from absorbing the migration logic.

