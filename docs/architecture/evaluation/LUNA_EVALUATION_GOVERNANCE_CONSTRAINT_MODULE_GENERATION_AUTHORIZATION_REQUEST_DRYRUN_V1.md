# Luna Evaluation — Governance Constraint Module Generation Authorization Request DryRun v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_request_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_request_dryrun_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_request_dryrun_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 601/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001`（**GO**，552/420 checks）
- **下游 Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001`

## 核心对象（12 类）

| 对象 | 产物 |
|------|------|
| AuthorizationRequestDryRunPolicy | `authorization_request_dryrun_policy_v1.json` |
| AuthorizationRequestIdentityDryRun | `authorization_request_identity_dryrun_v1.json` |
| AuthorizationRequestSourceSetBindingDryRun | `authorization_request_source_set_binding_dryrun_v1.json` |
| AuthorizationRequestDomainPreservationBindingDryRun | `authorization_request_domain_preservation_binding_dryrun_v1.json` |
| AuthorizationRequestScopeAndExclusionDryRun | `authorization_request_scope_and_exclusion_dryrun_v1.json` |
| AuthorizationRequestNonGrantAndNonGenerationStatementDryRun | `authorization_request_non_grant_and_non_generation_statement_dryrun_v1.json` |
| AuthorizationRequestLifecycleDryRun | `authorization_request_lifecycle_dryrun_v1.json` |
| AuthorizationRequestReviewRequirementDryRun | `authorization_request_review_requirement_dryrun_v1.json` |
| AuthorizationRequestAbortRevokeLinkageDryRun | `authorization_request_abort_revoke_linkage_dryrun_v1.json` |
| AuthorizationRequestVerifierUsageDryRun | `authorization_request_verifier_usage_dryrun_v1.json` |
| AuthorizationRequestNonClaimsDryRun | `authorization_request_non_claims_dryrun_v1.json` |
| AuthorizationRequestDryRunReadinessDecision | `authorization_request_dryrun_readiness_decision_v1.json` |

## 边界冻结

- `authorization_request_dryrun_only=true`
- `simulated=true`
- `governance_constraint_module_generation_authorization_request_generated_now=false`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `lifecycle_planning_defined_only=true`
- 主线未恢复
