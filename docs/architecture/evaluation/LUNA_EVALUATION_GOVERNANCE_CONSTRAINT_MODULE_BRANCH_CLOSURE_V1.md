# Luna Evaluation — Governance Constraint Module Branch Closure v1

**Phase**：`Phase-Governance-Constraint-Module-Branch-Closure-v1-001`  
**输出**：`_eval_out/governance_constraint_module_branch_closure_v1_smoke_v0/`

## Run

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_branch_closure_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_branch_closure_v1.py
```

## Upstream

- `governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0`（Request Roadmap Decision GO）

## Artifacts

1. `governance_constraint_module_branch_closure_policy_v1.json`
2. `completed_governance_constraint_module_branch_chain_review_v1.json`（16 phases × 4 branches）
3. `deferred_capability_register_v1.json`
4. `source_pack_register_v1.json`
5. `recursive_expansion_stop_decision_v1.json`
6. `mainline_return_readiness_matrix_v1.json`
7. `branch_non_release_matrix_v1.json`
8. `branch_closure_non_claims_register_v1.json`
9. `governance_constraint_module_branch_closure_readiness_decision_v1.json`
10. `summary.json`
11. `verifier_report.json`

## Expected Verdict

- `verifier=GO`
- `boundary_ok=true`
- `final_decision=GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase=Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001`
- `main_migration_resume_target=Phase-Registry-Generation-Authorization-Planning-v1-001`
