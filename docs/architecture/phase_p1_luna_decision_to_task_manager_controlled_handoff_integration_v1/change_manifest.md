# Change Manifest

Created the narrow integration package:

- `decision_to_task_manager_handoff_types_v1.py`
- `engine_v1.py`
- `runner_v1.py`
- `verifier_v1.py`

The following narrow compatibility correction was also made in the existing
Task Manager input boundary:

- `capabilities/midplatform/core/task_manager_static_validators_v1.py`
  now reads the existing trace/fact/risk fields from either canonical objects
  or mappings. This preserves the validator and fixes its proven mismatch
  with `task_manager_module_input_adapter_v1.py`, which supplies a mapping.
- `capabilities/midplatform/core/task_manager/module/task_manager_module_input_adapter_v1.py`
  preserves the existing generated trace fallback and accepts the optional
  caller-provided trace propagated by this integration.

No cognition, Decision Governance, Action, Archive, Evaluation, or White-box
implementation was modified. This Task Manager change does not remove or
weaken admission checks.

Recorded findings:

- `decision_to_task_manager_missing_canonical_trace_admission_mapping` —
  integration/compatibility mismatch resolved by trace propagation plus
  object/mapping-compatible validation.
- `negative_task_handoff_rejection_result_semantics_mismatch` — integration
  result-semantics defect resolved by deriving rejection from the actual
  rejected handoff and canonical error.
- `task_manager_cognition_execution_ref_truncation` — integration provenance
  mapping corrected to retain the full `a-route-execution:` reference.
