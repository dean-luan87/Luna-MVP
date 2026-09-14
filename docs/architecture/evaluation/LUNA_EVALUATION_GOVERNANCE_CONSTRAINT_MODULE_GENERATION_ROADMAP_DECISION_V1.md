# Luna Evaluation — Governance Constraint Module Generation Roadmap Decision v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 518/420
- **boundary_ok**: true
- **selected_route**: Route A — Governance Constraint Module Generation Authorization Planning
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_ROADMAP_DECISION_READY_FOR_GENERATION_AUTHORIZATION_PLANNING`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001`

## 核心对象（9 类）

| 对象 | 产物 |
|------|------|
| GovernanceConstraintModuleGenerationRoadmapDecisionPolicy | `governance_constraint_module_generation_roadmap_decision_policy_v1.json` |
| CompletedGovernanceConstraintModuleGenerationChainReview | `completed_governance_constraint_module_generation_chain_review_v1.json` |
| GovernanceConstraintModuleGenerationRoadmapRouteCandidateMatrix | `governance_constraint_module_generation_roadmap_route_candidate_matrix_v1.json` |
| GovernanceConstraintModuleGenerationAuthorizationDependencyMatrix | `governance_constraint_module_generation_authorization_dependency_matrix_v1.json` |
| GovernanceConstraintModuleGenerationAuthorizationPlanningScope | `governance_constraint_module_generation_authorization_planning_scope_v1.json` |
| GovernanceConstraintModuleGenerationRoadmapNonReleaseMatrix | `governance_constraint_module_generation_roadmap_non_release_matrix_v1.json` |
| GovernanceConstraintModuleAuthorizationEntryReadinessRiskMatrix | `governance_constraint_module_authorization_entry_readiness_risk_matrix_v1.json` |
| GovernanceConstraintModuleGenerationRoadmapDecisionNonClaimsRegister | `governance_constraint_module_generation_roadmap_decision_non_claims_register_v1.json` |
| GovernanceConstraintModuleGenerationRoadmapReadinessDecision | `governance_constraint_module_generation_roadmap_readiness_decision_v1.json` |

## 边界冻结

- `governance_constraint_module_generation_authorization_planning_selected=true`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `governance_constraint_module_generation_authorized_now=false`
- Route B/C/D/E/F/G deferred；Route H blocked
- 主线未恢复
