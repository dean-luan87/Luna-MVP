# Phase-Luna-Recent-Integration-Unified-Final-Verifier-Preparation-v1-001

## Execution Mode

Controlled verifier preparation only.

## Scope

Prepare a unified final verifier for three completed integration tracks without executing any final verifier and without running any integration runner.

Covered tracks:

1. Model Manager Provider Registry Alignment
2. Field Perception Visual Handoff
3. System Integration Validation

## Fixed Asset Inputs

Registry:

- capabilities/registry/luna_capability_registry_v1.json
- capabilities/registry/luna_capability_dependency_map_v1.json
- capabilities/registry/luna_capability_module_baseline_registry_v1.json

System Integration:

- capabilities/registry/manifests/system_integration_validation_manifest_v1.json
- capabilities/registry/baselines/system_integration_validation_baseline_v1.json
- tools/evaluation/midplatform/run_system_integration_validation_v1.py
- _tmp_eval_out/system_integration_validation_v1_smoke_v0/system_integration_validation_v1.json

Field Perception:

- capabilities/registry/manifests/field_perception_orchestrator_manifest_v1.json
- capabilities/registry/baselines/field_perception_orchestrator_module_baseline_v1.json
- tools/evaluation/midplatform/run_field_perception_visual_handoff_integration_v1.py
- _tmp_eval_out/field_perception_visual_handoff_integration_v1_smoke_v0/field_perception_visual_handoff_integration_v1.json

Model Manager:

- capabilities/registry/manifests/model_manager_manifest_v1.json
- capabilities/registry/baselines/model_manager_module_baseline_v1.json
- tools/evaluation/midplatform/run_model_manager_module_integration_v1.py
- _tmp_eval_out/model_manager_module_integration_v1_smoke_v0/model_manager_module_integration_v1.json
- capabilities/midplatform/model_manager/registry/provider_registry_v1.json

## Deliverables

1. tools/evaluation/midplatform/verify_recent_integration_unified_final_v1.py
2. tools/evaluation/midplatform/recent_integration_unified_final_verifier_plan_v1.md

## Verifier Contract

Output fields:

- module
- verifier
- checked_scope
- passed_checks
- failed_checks
- blocker_count
- failed_items
- boundary_preserved
- evidence_refs
- final_decision_candidate
- verifier_executed

Allowed final_decision_candidate values:

- READY_FOR_USER_TERMINAL_VERIFICATION
- BLOCKED_BY_VERIFIER_PREPARATION

Verifier invariant:

- verifier_executed is always false in verifier output.

## Required Check Coverage

The verifier implements 35 checks:

A. Registry and promotion checks (1-6)

- Required capability records exist.
- Manifest paths exist and JSON is readable.
- Baseline paths exist and JSON is readable.
- Baseline registry flags are aligned.

B. Model Manager checks (7-13)

- provider_registry includes detection_v1 and slam_v1.
- latest report asserts integration_pass and deterministic replay.
- boundary flags and failed case conditions pass.
- report path is under Luna-Workspace-Min.

C. Field Perception Visual Handoff checks (14-19)

- total_cases, passed_cases, failed_cases constraints.
- boundary_preserved and deterministic_replay.
- unhandled_exceptions constraint.

D. System Integration checks (20-28)

- integration pass summary conditions.
- degraded_budget scenario field_perception_status assertion.
- per-scenario trace_replay_preserved and boundary_preserved constraints.

E. Governance boundary checks (29-35)

- manifest explicit boundary declarations.
- baseline runtime load constraint.
- verifier self-read-only guard.
- verifier no real-model import or execution guard.

## Non-Execution Rules

The preparation phase does not:

- run verify_recent_integration_unified_final_v1.py
- run any integration runner
- run any Final Phase Verifier
- modify any business module, runner, registry, manifest, or baseline

## Allowed Validation In This Phase

- one py_compile for verify_recent_integration_unified_final_v1.py

## User Terminal Execution (Next Step)

After preparation approval, user may run:

- /Users/luanlei/Desktop/Luna-Workspace-Min/.venv-tx/bin/python tools/evaluation/midplatform/verify_recent_integration_unified_final_v1.py
