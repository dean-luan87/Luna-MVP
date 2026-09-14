## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_generation_authorization_request_planning_v1.py`
- **Status**: authorization-request-planning-only（授权 request 结构规划；非 request artifact / 非 request sent / 非 grant / 非 module generation / 非主线恢复）

## Intent

规划正式 **Governance Constraint Module Generation Authorization Request** 的结构、字段、source set 绑定、domain preservation 绑定、excluded scope、non-grant / non-generation statement、request lifecycle、review requirement、abort / revoke linkage 与 verifier usage。

Authorization Roadmap Decision 已选定 **Route A — Governance Constraint Module Generation Authorization Request Planning**。本阶段仅完成 planning，不生成 request artifact、不发起 request、不授予 grant。

## 三类防误读

| 误读 | 纠正 |
|------|------|
| request planning = request generated | planning GO 仅表示结构已规划 |
| request generated = request sent | artifact 存在 ≠ 已发送 |
| request sent = authorization granted | 发送 request ≠ 授予授权 |

## Planning Scope（12 类核心对象）

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

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001`

## Implementation Status

- Authorization Planning / DryRun / Post-DryRun Review / Roadmap Decision：GO
- **Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001**: **GO**（588/420 checks）

## Downstream Handoff

- **Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001**: **GO**（601/420 checks；见 `LUNA_GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_V1.md`）
- 下一阶段：**Governance Constraint Module Generation Authorization Request Post-DryRun Review**（审查 dry-run 完整性；非 request artifact / 非 request sent / 非 grant）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成 authorization request artifact
- 仍不得发起 authorization request
- 仍不得授予 authorization grant
- 仍不得生成正式 Governance Constraint Module
