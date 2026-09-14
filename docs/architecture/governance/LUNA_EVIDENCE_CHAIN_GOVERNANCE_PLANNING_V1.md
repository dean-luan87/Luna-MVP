## Phase

- **Phase ID**: `Phase-Evidence-Chain-Governance-Planning-v1-001`
- **Capability**: `capabilities/governance/evidence_chain_governance_planning_v1.py`
- **Status**: evidence-chain-governance-planning-only（规划 evidence 生命周期；非 evidence 生成）

## Intent

规划 Luna-Core 治理 phase 的 Evidence Chain 统一规则：evidence candidate、runtime/audit/success evidence、source chain、verifier_report、summary、boundary matrix、post-review report 的生命周期、可用边界、升级路径、acceptance policy、non-substitution、success claim eligibility 与 verifier usage。

## Source Chain

- **上游**: `Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001`（Route A selected）
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`

## Core Artifacts（12 类）

| # | 对象 | 输出文件 |
|---|------|----------|
| 1 | EvidenceChainGovernancePlanningPolicy | `evidence_chain_governance_planning_policy_v1.json` |
| 2 | EvidenceTypeLifecyclePlanningMatrix | `evidence_type_lifecycle_planning_matrix_v1.json` |
| 3 | EvidenceSourceChainPlanningMatrix | `evidence_source_chain_planning_matrix_v1.json` |
| 4 | EvidenceUsageScopePlanningMatrix | `evidence_usage_scope_planning_matrix_v1.json` |
| 5 | EvidenceUpgradePathPlanningMatrix | `evidence_upgrade_path_planning_matrix_v1.json` |
| 6 | EvidenceAcceptancePolicyPlanningMatrix | `evidence_acceptance_policy_planning_matrix_v1.json` |
| 7 | EvidenceBoundaryNonSubstitutionMatrix | `evidence_boundary_non_substitution_matrix_v1.json` |
| 8 | EvidenceToSuccessClaimEligibilityPlanningMatrix | `evidence_to_success_claim_eligibility_planning_matrix_v1.json` |
| 9 | EvidenceVerifierUsagePlanningMatrix | `evidence_verifier_usage_planning_matrix_v1.json` |
| 10 | EvidenceChainNonClaimsPlanningMatrix | `evidence_chain_non_claims_planning_matrix_v1.json` |
| 11 | EvidenceChainOutputPlan | `evidence_chain_output_plan_v1.json` |
| 12 | EvidenceChainGovernancePlanningReadinessDecision | `evidence_chain_governance_planning_readiness_decision_v1.json` |

## Core Rules

- **evidence_candidate / verifier_report / summary** 不得单独支撑 success claim
- **source_chain** 可作为 evidence chain 组成部分，但不得单独推出 success claim
- **success_evidence** 为 future 规则下可支撑 success claim 的类型，当前 `generation_allowed_now=false`
- verifier GO ≠ success claim；summary 记录 ≠ success evidence

## Final Decision

- `EVIDENCE_CHAIN_GOVERNANCE_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Evidence-Chain-Governance-DryRun-v1-001`

## Boundary Flags

```
evidence_chain_planning_only=true
evidence_generated_now=false
evidence_accepted_for_success_claim_now=false
success_claim_gate_generated_now=false
success_claim_allowed=false
```

## Implementation Status

- **Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001**: **GO**（466/420 checks）
- **Phase-Evidence-Chain-Governance-Planning-v1-001**: **GO**（502/420 checks）
- **Phase-Evidence-Chain-Governance-DryRun-v1-001**: **GO**（428/420 checks）
- **Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001**: **GO**（434/420 checks）
- **Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001**: **GO**（521/420 checks）

## Downstream Handoff

- **已完成**：Roadmap Decision → Owner/Operator Approval Protocol Planning
- 下一阶段：**Evidence Chain Governance Post-DryRun Review**
- 仍不得生成 evidence、不得让 evidence 支撑 success claim
