# Luna Evaluation — Governance Constraint Module Generation Authorization Request Roadmap Decision v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_request_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_request_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 438/420
- **boundary_ok**: true
- **selected_route**: Route A — Authorization Request Artifact Generation Planning
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_ROADMAP_DECISION_READY_FOR_ARTIFACT_GENERATION_PLANNING`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001`

## 核心对象（9 类）

| 对象 | 产物 |
|------|------|
| AuthorizationRequestRoadmapDecisionPolicy | `authorization_request_roadmap_decision_policy_v1.json` |
| CompletedAuthorizationRequestChainReview | `completed_authorization_request_chain_review_v1.json` |
| AuthorizationRequestRoadmapRouteCandidateMatrix | `authorization_request_roadmap_route_candidate_matrix_v1.json` |
| AuthorizationRequestArtifactGenerationPlanningDependencyMatrix | `authorization_request_artifact_generation_planning_dependency_matrix_v1.json` |
| AuthorizationRequestArtifactGenerationPlanningScope | `authorization_request_artifact_generation_planning_scope_v1.json` |
| AuthorizationRequestRoadmapNonReleaseMatrix | `authorization_request_roadmap_non_release_matrix_v1.json` |
| AuthorizationRequestArtifactEntryReadinessRiskMatrix | `authorization_request_artifact_entry_readiness_risk_matrix_v1.json` |
| AuthorizationRequestRoadmapDecisionNonClaimsRegister | `authorization_request_roadmap_decision_non_claims_register_v1.json` |
| AuthorizationRequestRoadmapReadinessDecision | `authorization_request_roadmap_readiness_decision_v1.json` |

## 边界冻结

- `authorization_request_artifact_generation_planning_selected=true`
- `governance_constraint_module_generation_authorization_request_artifact_generated_now=false`
- Route H blocked；Route B–G deferred
- 主线未恢复
