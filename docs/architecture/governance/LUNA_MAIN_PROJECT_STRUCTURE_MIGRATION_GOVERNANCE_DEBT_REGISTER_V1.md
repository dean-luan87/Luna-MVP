## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_governance_debt_register_v1.py`
- **Status**: governance-debt-register-only（结构化登记；不修复、不授权、不执行）

## Intent

消费 Pre-Authorization Roadmap Decision **Route D** 信号，将本轮迁移与预授权链暴露的治理债登记为可追踪对象：

- 输入：Roadmap Decision `verifier=GO / boundary_ok=true / selected_route=Route D / ready_for_governance_debt_register=true`
- 输出：11 类 register 对象（policy / register / severity / source mapping / blocked rules / future mapping / verifier additions / doc sync plan / terminology table / automation matrix / readiness）
- 规范性引用：[LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md](./LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md)

## 登记的 9 类治理债

1. `permission_semantics_debt`（P0 / critical）
2. `boundary_object_debt`（P0 / high）
3. `evidence_chain_debt`（P1 / high）
4. `success_claim_debt`（P0 / critical）
5. `owner_operator_debt`（P0 / critical）
6. `test_harness_debt`（P1 / medium）
7. `documentation_sync_debt`（P1 / medium）
8. `terminology_debt`（P0 / critical）
9. `automation_candidate_debt`（P1 / medium）

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_READY_FOR_POST_REGISTER_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001`

## Non-Claims

- Register GO ≠ 治理债已修复（`fix_executed_now=false`）
- Register GO ≠ 真实 owner/operator approval 已授予
- Register GO ≠ execution window 已打开
- Register GO ≠ 真实 rollback rehearsal / migration / batch arming 可执行
- Register GO ≠ 文档已自动同步或 automation 已实施
- blocked progression rules 为登记规则，本阶段不执行 enforcement 修复

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001**: **GO**（702/420 checks）
- **Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001**: **GO**（483/420 checks）

## Downstream Handoff

- Register GO 仅表示 9 类治理债已结构化登记；**fix_executed_now=false**
- **Post-Review GO**（438/420）：登记可用性已审查；仍不等于债务已修复
- 下一阶段：`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001`（路线裁决；非 debt fix / 非真实授权）
