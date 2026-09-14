# Luna Evaluation — Governance Constraint Module Generation Authorization Request Post-DryRun Review v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_authorization_request_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_authorization_request_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_authorization_request_post_dryrun_review_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 552/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001`（**GO**，438/420 checks）
- **下游 Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001`

## 核心对象（12 类）

| 对象 | 产物 |
|------|------|
| AuthorizationRequestPostDryRunReviewPolicy | `authorization_request_post_dryrun_review_policy_v1.json` |
| AuthorizationRequestDryRunCompletenessReview | `authorization_request_dryrun_completeness_review_v1.json` |
| AuthorizationRequestArtifactNonGenerationReview | `authorization_request_artifact_non_generation_review_v1.json` |
| AuthorizationRequestNonSentReview | `authorization_request_non_sent_review_v1.json` |
| AuthorizationGrantNonIssuedReview | `authorization_grant_non_issued_review_v1.json` |
| SourceAndDomainApprovalNonExecutionReview | `source_and_domain_approval_non_execution_review_v1.json` |
| RequestLifecycleNonAdvanceReview | `request_lifecycle_non_advance_review_v1.json` |
| ScopeAndExclusionBoundaryReview | `scope_and_exclusion_boundary_review_v1.json` |
| AbortRevokeLinkageNonExecutionReview | `abort_revoke_linkage_non_execution_review_v1.json` |
| RequestVerifierUsageNonModificationReview | `request_verifier_usage_non_modification_review_v1.json` |
| AuthorizationRequestNonClaimsReview | `authorization_request_non_claims_review_v1.json` |
| AuthorizationRequestPostDryRunReviewReadinessDecision | `authorization_request_post_dryrun_review_readiness_decision_v1.json` |

## 边界冻结

- `post_dryrun_review_only=true`
- `review_only=true`
- `request_ready_now=false` / `request_sent_now=false` / `grant_issued_now=false`
- `lifecycle_planning_defined_only=true`
- 主线未恢复
