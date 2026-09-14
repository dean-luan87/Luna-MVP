## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_governance_debt_register_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（路线裁决；非 debt fix / 非 canonicalization 实施）

## Intent

对 Governance Debt Register + Post-Review 做路线裁决，选中 **Route A — Permission Semantics Canonicalization Planning** 作为后续治理债处理入口。

Route A 不仅是字段语义解释，还必须同步规划：

- 字段命名规范、状态流转规范
- verifier 必查规范、forbidden state combination
- non-claims / readiness decision / final decision 规范
- planning / dry-run / review / roadmap / register / authorization / execution 分层规则
- 后续 phase 如何引用 `governance_constraints_ref` 与 canonical semantics

**强绑定依赖**：Route B（Terminology）、Route C（Success Claim Gate）为 Route A 的 required dependency。

## Selected Route

**Route A — Permission Semantics Canonicalization Planning**（P0）

### 暂缓 / 阻断

- Route D–H：deferred（P1）
- Route I — Direct Debt Fix Execution：`blocked_now=true`

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING`
- **Next**: `Phase-Permission-Semantics-Canonicalization-Planning-v1-001`

## Non-Claims

- Roadmap GO ≠ permission semantics 已 canonicalized（`canonicalization_executed_now=false`）
- Route A 选中 ≠ debt fixed / verifier modified / automation implemented
- Route B/C 绑定 ≠ terminology 或 success claim 债务已修复
- Roadmap GO ≠ owner/operator approval / real rehearsal / migration / batch arming

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001**: **GO**（438/420 checks）
- **Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001**: **GO**（432/420 checks）
- **Phase-Permission-Semantics-Canonicalization-Planning-v1-001**: **GO**（420/420 checks）

## Downstream Handoff

- **已完成**：Permission Semantics Canonicalization Planning（14 类规范蓝图；`not_enforced_now=true`）
- 下一阶段：**Permission Semantics Canonicalization DryRun**（模拟规范能否被 verifier 与 phase template 消费；仍不 enforced）
- 仍不得进入 canonicalization execution、debt fix、verifier 改造、phase template 改造、automation 或真实授权链
