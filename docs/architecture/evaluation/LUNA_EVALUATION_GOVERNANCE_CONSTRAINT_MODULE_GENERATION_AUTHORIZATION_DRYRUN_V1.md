# Luna Evaluation — Governance Constraint Module Generation Authorization DryRun v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_dryrun_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_dryrun_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 575/420
- **boundary_ok**: true
- **simulated**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001`

## 核心对象（12 类）

| 对象 | 产物 | 覆盖 |
|------|------|------|
| GovernanceConstraintModuleGenerationAuthorizationDryRunPolicy | `governance_constraint_module_generation_authorization_dryrun_policy_v1.json` | 阶段总策略 |
| AuthorizationRequestSchemaConsumptionDryRun | `authorization_request_schema_consumption_dryrun_v1.json` | ≥12 fields |
| AuthorizationGrantSchemaConsumptionDryRun | `authorization_grant_schema_consumption_dryrun_v1.json` | ≥12 fields |
| SourceSetFinalApprovalAuthorityDryRun | `source_set_final_approval_authority_dryrun_v1.json` | ≥12 components |
| DomainSpecificPreservationApprovalDryRun | `domain_specific_preservation_approval_dryrun_v1.json` | ≥12 domains |
| ModuleGenerationAuthorityDryRun | `module_generation_authority_dryrun_v1.json` | ≥12 authorities |
| FutureIntegrationBoundaryDryRun | `future_integration_boundary_dryrun_v1.json` | ≥10 boundaries |
| PostGenerationReviewAuthorityDryRun | `post_generation_review_authority_dryrun_v1.json` | ≥12 review authorities |
| AbortAndRollbackAuthorityDryRun | `abort_and_rollback_authority_dryrun_v1.json` | ≥12 authorities |
| AuthorizationVerifierUsageDryRun | `authorization_verifier_usage_dryrun_v1.json` | ≥12 checks |
| AuthorizationNonClaimsGenerationDryRun | `authorization_non_claims_generation_dryrun_v1.json` | ≥10 scenarios |
| GovernanceConstraintModuleGenerationAuthorizationDryRunReadinessDecision | `governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json` | readiness |

## 边界冻结

- `governance_constraint_module_generation_authorization_dryrun_only=true`
- `simulated=true`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `governance_constraint_module_generation_authorized_now=false`
- `source_set_final_approved_now=false`
- `domain_specific_preservation_approved_now=false`
- `module_generation_authority_released_now=false`
- 主线未恢复

## Non-Claim

DryRun GO 只表示授权结构可模拟消费，不等于 authorization request 已发起、authorization 已授予、或 module generation 可以开始。
