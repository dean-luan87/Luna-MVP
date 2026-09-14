# Luna Evaluation — Governance Constraint Module Generation Authorization Planning v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_planning_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 522/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001`

## 核心对象（12 类）

| 对象 | 产物 | 覆盖 |
|------|------|------|
| GovernanceConstraintModuleGenerationAuthorizationPlanningPolicy | `governance_constraint_module_generation_authorization_planning_policy_v1.json` | 阶段总策略 |
| ModuleGenerationAuthorizationRequestSchemaPlanning | `module_generation_authorization_request_schema_planning_v1.json` | ≥12 fields |
| ModuleGenerationAuthorizationGrantSchemaPlanning | `module_generation_authorization_grant_schema_planning_v1.json` | ≥12 fields |
| SourceSetFinalApprovalAuthorityPlanning | `source_set_final_approval_authority_planning_v1.json` | ≥12 components |
| DomainSpecificPreservationApprovalPlanning | `domain_specific_preservation_approval_planning_v1.json` | ≥12 domains |
| ModuleGenerationAuthorityPlanningMatrix | `module_generation_authority_planning_matrix_v1.json` | ≥12 authorities |
| FutureIntegrationBoundaryPlanning | `future_integration_boundary_planning_v1.json` | ≥10 boundaries |
| PostGenerationReviewAuthorityPlanning | `post_generation_review_authority_planning_v1.json` | ≥12 review authorities |
| ModuleGenerationAbortAndRollbackAuthorityPlanning | `module_generation_abort_and_rollback_authority_planning_v1.json` | ≥12 authorities |
| ModuleGenerationAuthorizationVerifierUsagePlanning | `module_generation_authorization_verifier_usage_planning_v1.json` | ≥12 checks |
| ModuleGenerationAuthorizationNonClaimsPlanning | `module_generation_authorization_non_claims_planning_v1.json` | ≥10 scenarios |
| GovernanceConstraintModuleGenerationAuthorizationPlanningReadinessDecision | `governance_constraint_module_generation_authorization_planning_readiness_decision_v1.json` | readiness |

## 边界冻结

- `governance_constraint_module_generation_authorization_planning_only=true`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `governance_constraint_module_generation_authorized_now=false`
- `source_set_final_approved_now=false`
- `domain_specific_preservation_approved_now=false`
- 所有 planned output `not_generated_now=true`
- 主线未恢复
