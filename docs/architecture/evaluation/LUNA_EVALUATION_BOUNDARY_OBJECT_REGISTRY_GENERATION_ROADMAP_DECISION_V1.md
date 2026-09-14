# Luna Evaluation — Boundary Object Registry Generation Roadmap Decision v1

**Phase**：`Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/boundary_object_registry_generation_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_boundary_object_registry_generation_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_boundary_object_registry_generation_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 431/420
- **boundary_ok**: true
- **selected_route**: Route A — Registry Generation Authorization Planning
- **final_decision**: `BOUNDARY_OBJECT_REGISTRY_GENERATION_ROADMAP_DECISION_READY_FOR_REGISTRY_GENERATION_AUTHORIZATION_PLANNING`
- **Next**: `Phase-Registry-Generation-Authorization-Planning-v1-001`（**已暂停**；见 Governance Constraint Module Legacy Extraction 收束链）

## 核心对象（9 类）

| 对象 | 产物 |
|------|------|
| RegistryGenerationRoadmapDecisionPolicy | `registry_generation_roadmap_decision_policy_v1.json` |
| CompletedRegistryGenerationChainReview | `completed_registry_generation_chain_review_v1.json` |
| RegistryGenerationRoadmapRouteCandidateMatrix | `registry_generation_roadmap_route_candidate_matrix_v1.json` |
| RegistryGenerationAuthorizationDependencyMatrix | `registry_generation_authorization_dependency_matrix_v1.json` |
| RegistryGenerationAuthorizationPlanningScope | `registry_generation_authorization_planning_scope_v1.json` |
| RegistryGenerationRoadmapNonReleaseMatrix | `registry_generation_roadmap_non_release_matrix_v1.json` |
| RegistryGenerationAuthorizationEntryReadinessRiskMatrix | `registry_generation_authorization_entry_readiness_risk_matrix_v1.json` |
| RegistryGenerationRoadmapDecisionNonClaimsRegister | `registry_generation_roadmap_decision_non_claims_register_v1.json` |
| RegistryGenerationRoadmapReadinessDecision | `registry_generation_roadmap_readiness_decision_v1.json` |

## 边界冻结

- `registry_generation_authorization_planning_selected=true`
- `registry_generation_authorization_request_sent_now=false`
- `registry_generation_authorized_now=false`
- registry 未生成；entry 未生成/未 commit；source 未 final validated
