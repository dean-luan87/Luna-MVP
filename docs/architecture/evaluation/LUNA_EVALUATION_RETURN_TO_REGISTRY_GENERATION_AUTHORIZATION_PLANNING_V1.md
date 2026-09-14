# Luna Evaluation — Return To Registry Generation Authorization Planning v1

**Phase**：`Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001`  
**输出**：`_eval_out/return_to_registry_generation_authorization_planning_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_return_to_registry_generation_authorization_planning_v1.py
python3 tools/evaluation/governance/verify_return_to_registry_generation_authorization_planning_v1.py
```

## Upstream

- `governance_constraint_module_branch_closure_v1_smoke_v0`（Branch Closure GO）

## Artifacts

1. `return_to_registry_generation_authorization_planning_policy_v1.json`
2. `branch_closure_input_review_v1.json`
3. `deferred_governance_constraint_module_source_pack_reference_v1.json`
4. `mainline_resume_target_binding_v1.json`
5. `return_non_release_matrix_v1.json`
6. `registry_generation_authorization_planning_reentry_scope_v1.json`
7. `return_to_mainline_non_claims_register_v1.json`
8. `return_to_registry_generation_authorization_planning_readiness_decision_v1.json`
9. `summary.json`
10. `verifier_report.json`

## Expected Verdict

- `verifier=GO`
- `final_decision=RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_READY`
- `recommended_next_phase=Phase-Registry-Generation-Authorization-Planning-v1-001`
- `mainline_resume_target=Phase-Registry-Generation-Authorization-Planning-v1-001`
