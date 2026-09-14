# Luna Evaluation — Governance Constraint Module Generation Authorization Roadmap Decision v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 427/420
- **boundary_ok**: true
- **selected_route**: Route A — Governance Constraint Module Generation Authorization Request Planning
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_AUTHORIZATION_REQUEST_PLANNING`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001`（**GO**，588/420 checks）
- **下游 Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001`

## 核心对象（9 类）

| 对象 | 产物 |
|------|------|
| GovernanceConstraintModuleGenerationAuthorizationRoadmapDecisionPolicy | `governance_constraint_module_generation_authorization_roadmap_decision_policy_v1.json` |
| CompletedAuthorizationGovernanceChainReview | `completed_authorization_governance_chain_review_v1.json` |
| AuthorizationRoadmapRouteCandidateMatrix | `authorization_roadmap_route_candidate_matrix_v1.json` |
| AuthorizationRequestPlanningDependencyMatrix | `authorization_request_planning_dependency_matrix_v1.json` |
| AuthorizationRequestPlanningScope | `authorization_request_planning_scope_v1.json` |
| AuthorizationRoadmapNonReleaseMatrix | `authorization_roadmap_non_release_matrix_v1.json` |
| AuthorizationRequestEntryReadinessRiskMatrix | `authorization_request_entry_readiness_risk_matrix_v1.json` |
| AuthorizationRoadmapDecisionNonClaimsRegister | `authorization_roadmap_decision_non_claims_register_v1.json` |
| AuthorizationRoadmapReadinessDecision | `authorization_roadmap_readiness_decision_v1.json` |

## 边界冻结

- `governance_constraint_module_generation_authorization_request_planning_selected=true`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `governance_constraint_module_generation_authorization_request_generated_now=false`
- Route B/C/D/E/F/G deferred；Route H blocked
- 主线未恢复
