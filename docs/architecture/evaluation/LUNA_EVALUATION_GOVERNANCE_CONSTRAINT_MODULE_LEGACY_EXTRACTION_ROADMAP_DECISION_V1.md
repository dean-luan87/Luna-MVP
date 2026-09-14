# Luna Evaluation — Governance Constraint Module Legacy Extraction Roadmap Decision v1

**Phase**：`Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/governance_constraint_module_legacy_extraction_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_legacy_extraction_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_legacy_extraction_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 471/420
- **boundary_ok**: true
- **selected_route**: Route A — Governance Constraint Module Generation Planning
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Planning-v1-001`

## 核心对象（9 类）

| 对象 | 产物 |
|------|------|
| LegacyExtractionRoadmapDecisionPolicy | `legacy_extraction_roadmap_decision_policy_v1.json` |
| CompletedLegacyExtractionChainReview | `completed_legacy_extraction_chain_review_v1.json` |
| LegacyExtractionRoadmapRouteCandidateMatrix | `legacy_extraction_roadmap_route_candidate_matrix_v1.json` |
| ConstraintModuleGenerationDependencyMatrix | `constraint_module_generation_dependency_matrix_v1.json` |
| ConstraintModuleGenerationPlanningScope | `constraint_module_generation_planning_scope_v1.json` |
| LegacyExtractionRoadmapNonReleaseMatrix | `legacy_extraction_roadmap_non_release_matrix_v1.json` |
| ConstraintModuleGenerationEntryReadinessRiskMatrix | `constraint_module_generation_entry_readiness_risk_matrix_v1.json` |
| LegacyExtractionRoadmapDecisionNonClaimsRegister | `legacy_extraction_roadmap_decision_non_claims_register_v1.json` |
| LegacyExtractionRoadmapReadinessDecision | `legacy_extraction_roadmap_readiness_decision_v1.json` |

## 边界冻结

- `governance_constraint_module_generation_planning_selected=true`
- `governance_constraint_module_generated_now=false`
- Route B/C/D/E/F/G deferred；Route H blocked
- 主线未恢复
