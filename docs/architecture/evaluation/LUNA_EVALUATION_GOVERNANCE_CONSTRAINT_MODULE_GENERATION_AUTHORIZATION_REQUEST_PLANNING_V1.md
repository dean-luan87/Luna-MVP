# Luna Evaluation — Governance Constraint Module Generation Authorization Request Planning v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_request_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_request_planning_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_request_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 588/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001`（**GO**，601/420 checks）
- **下游 Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001`

## 核心对象（12 类）

| 对象 | 产物 |
|------|------|
| AuthorizationRequestPlanningPolicy | `authorization_request_planning_policy_v1.json` |
| AuthorizationRequestIdentityPlanning | `authorization_request_identity_planning_v1.json` |
| AuthorizationRequestSourceSetBindingPlanning | `authorization_request_source_set_binding_planning_v1.json` |
| AuthorizationRequestDomainPreservationBindingPlanning | `authorization_request_domain_preservation_binding_planning_v1.json` |
| AuthorizationRequestScopeAndExclusionPlanning | `authorization_request_scope_and_exclusion_planning_v1.json` |
| AuthorizationRequestNonGrantAndNonGenerationStatementPlanning | `authorization_request_non_grant_and_non_generation_statement_planning_v1.json` |
| AuthorizationRequestLifecyclePlanning | `authorization_request_lifecycle_planning_v1.json` |
| AuthorizationRequestReviewRequirementPlanning | `authorization_request_review_requirement_planning_v1.json` |
| AuthorizationRequestAbortRevokeLinkagePlanning | `authorization_request_abort_revoke_linkage_planning_v1.json` |
| AuthorizationRequestVerifierUsagePlanning | `authorization_request_verifier_usage_planning_v1.json` |
| AuthorizationRequestPlanningNonClaimsPlanning | `authorization_request_planning_non_claims_planning_v1.json` |
| AuthorizationRequestPlanningReadinessDecision | `authorization_request_planning_readiness_decision_v1.json` |

## 边界冻结

- `authorization_request_planning_only=true`
- `governance_constraint_module_generation_authorization_request_generated_now=false`
- `governance_constraint_module_generation_authorization_request_sent_now=false`
- `governance_constraint_module_generation_authorized_now=false`
- lifecycle 仅 `planning_defined`；不得进入 `request_sent` / `grant_issued`
- 主线未恢复
