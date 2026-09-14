## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（路线裁决；不发起真实授权、不执行、不 batch arming）

## Intent

对已完成的 **Pre-Authorization Planning → DryRun → Post-DryRun Review** 链做路线裁决（只读上游 Post-DryRun Review 结果）：

- 输入：Post-DryRun Review `verifier=GO / boundary_ok=true / ready_for_pre_authorization_roadmap_decision=true`
- 输出：9 类 roadmap decision 对象（policy / chain review / route matrix / governance debt signals / dependencies / selected route / non-release / non-claims / readiness）
- 关键约束：**不释放任何真实授权或真实执行权限**（owner/operator approval、execution window、rehearsal / migration / batch arming 均保持 false）

## Selected Route

**Route D — Governance Debt Register**（P0）

### 理由

- 迁移过程显影出权限语义、边界对象、证据链、success claim、owner/operator、术语等治理债
- 在更接近真实授权之前，必须先结构化登记治理债，降低“词义误读”与“边界对象缺失”风险
- Route D 的 `allowed_now` 仅表示 **登记允许**，不是 authorization allowed / execution allowed

### 暂缓路线

- **Route A** Real Pre-Authorization Request Planning — deferred
- **Route B** Owner/Operator Approval Workflow Planning — deferred
- **Route C** Sandbox / Branch Preparation Planning — deferred
- **Route E** Test Harness / Documentation Automation — 可并入 Route D 下游
- **Route F** Pause and Return to Capability Work — optional/deferred

### 阻断路线

- **Route G** Direct Real Rollback Rehearsal Execution — `blocked_now=true`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_GOVERNANCE_DEBT_REGISTER`
- **Next**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`

## Non-Claims

- Roadmap Decision GO ≠ 真实预授权申请已批准
- Roadmap Decision GO ≠ owner/operator approval 已授予
- Roadmap Decision GO ≠ execution window 已打开
- Roadmap Decision GO ≠ sandbox/branch 可创建 / restore map 可生成 / restore 可执行
- Roadmap Decision GO ≠ verifier 可 rerun / evidence 可生成 / rollback 已成功
- Roadmap Decision GO ≠ 真实迁移 / batch arming 可执行
- Governance Debt Register 选择不永久阻断未来 rehearsal；仅 gate 不安全推进

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001**: **GO**（531/360 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001**: **GO**（604/420 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001**: **GO**（560/420 checks）
- **Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001**: **GO**（702/420 checks）
- **Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001**: **GO**（483/420 checks；见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_V1.md`）

## Downstream Handoff

- Route D 已消费：Register GO 表示 9 类治理债已结构化登记；**fix_executed_now=false**
- **开发约束清单**：[LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md](./LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md)
- 下一阶段：`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001`（审查登记；仍不修复、不授权、不执行）
