# Phase-Luna-System-Integration-Validation-Planning-v1-001

## Scope

This planning phase defines the minimal controlled system integration validation path for promoted midplatform modules only.

Constraints:

- candidate-only
- no real model execution
- no runtime loop
- no real Field State write
- no Final Phase Verifier
- no runner creation in this phase

## Validation Module Range

Primary system chain:

1. luna.task_manager
2. luna.field_perception_orchestrator
3. luna.vision_manager
4. luna.model_manager
5. luna.observation_manager
6. luna.field_state_reducer

Supporting dependency context already registered:

- luna.permission_and_admission_manager
- luna.protocol_manager
- luna.ocr_manager

## Main Chain Order

Planned minimal verification order:

1. Task request candidate formation in Task Manager
2. Field context handoff into Field Perception Orchestrator
3. Visual invocation planning and budget degradation decision
4. Vision request candidate handoff into Vision Manager
5. Provider selection and eligible model binding through Model Manager
6. Observation request candidate formation in Observation Manager
7. Admitted-event-shaped downstream input contract into Field State Reducer
8. Field state candidate update contract check without real persistence

System chain statement:

Task Manager
-> Field Perception Orchestrator
-> Vision Manager
-> Model Manager
-> Observation Manager
-> Field State Reducer

## Reusable Runners

Existing module runners that should be reused as prevalidated components:

1. tools/evaluation/midplatform/run_task_manager_module_integration_v1.py
2. tools/evaluation/midplatform/run_field_perception_visual_handoff_integration_v1.py
3. tools/evaluation/midplatform/run_vision_manager_module_integration_v1.py
4. tools/evaluation/midplatform/run_model_manager_module_integration_v1.py
5. tools/evaluation/midplatform/run_observation_manager_module_integration_v1.py
6. tools/evaluation/midplatform/run_field_state_reducer_module_integration_v1.py

Expected reuse mode:

- use existing runner contracts as component baselines
- do not duplicate their scenario coverage in full
- only add cross-module assertions in the future system-level runner

## Missing System-Level Runner

No registered end-to-end runner currently validates the full system chain above in one controlled pass.

Minimal missing asset:

- tools/evaluation/midplatform/run_system_integration_validation_v1.py

Planned responsibility of the missing runner:

- stitch module input/output contracts only
- reuse candidate outputs from upstream module as downstream controlled inputs
- validate reference preservation across task_id, field_snapshot_ref, information_gap_ref, trace_ref, replay_key
- confirm boundary flags remain false across the whole chain

## Planned Scenario Groups

### Group A: Happy Path Handoff

- task-driven visual request with sufficient governance context
- field perception creates handoff_ready visual invocation
- model provider resolution succeeds
- observation request candidate is formed
- field state reducer receives controlled downstream candidate input contract

### Group B: Budgeted Degradation

- constrained budget keeps minimal viable visual capability path
- critical budget keeps minimum safety observation path only
- downstream chain still preserves references and candidate-only boundary

### Group C: No-Invocation / Reuse Path

- no_visual_invocation_required from field perception
- duplicate_suppressed path
- fresh_evidence_reused path
- confirm downstream modules are not forced into invalid execution branches

### Group D: Provider/Eligibility Failure Path

- no_eligible_model remains contained inside controlled handoff
- observation request is not fabricated when eligible model binding fails
- failure diagnostics remain local and deterministic

### Group E: Evidence-to-State Contract Path

- observation-manager output shape is sufficient to define the synthetic downstream state-reducer input bridge
- no persistence or admitted fact promotion occurs

## Cross-Module Assertions

Future system-level validation should assert:

1. task_id preserved across all stages
2. field_snapshot_ref preserved from Field Perception to Observation handoff and synthetic state update input
3. information_gap_ref preserved across visual handoff chain
4. trace_ref and replay_key present at every stage
5. candidate-only boundary preserved at every stage
6. no real model execution
7. no real visual evidence creation
8. no Field State write
9. no runtime loop activation

## Baseline And Manifest Usage

Planning assumptions based on current metadata:

- all six primary chain modules have manifests
- field_perception_orchestrator baseline is calibration-only
- baseline assets are governance/calibration references only, not runtime config inputs

## Boundary And Stop Conditions

Boundary:

- do not invoke real model runtime
- do not invoke camera runtime
- do not write Field State
- do not promote facts
- do not execute actions
- do not start continuous observation loop

Stop conditions for the future system validation execution phase:

1. a single system-level runner is defined
2. runner inputs are synthetic and contract-bounded
3. all cross-module references are asserted
4. any first failure gate is localized to one module handoff boundary
5. stop immediately on first need for real runtime, real evidence generation, or real persistence

## Recommended Next Phase

Recommended next phase:

Phase-Luna-System-Integration-Validation-Controlled-Runner-Build-v1-001

Minimal target of the next phase:

- create exactly one controlled system-level runner
- reuse existing module contracts and readiness evidence
- verify the primary chain without reworking business logic