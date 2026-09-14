# Luna Evaluation — Real Rollback Rehearsal Pre-Authorization Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1.py
```

## 通过条件（摘要）

- 必须读取上游 Post-DryRun Review 输出，并确认 `verifier=GO / boundary_ok=true / ready_for_pre_authorization_roadmap_decision=true`
- 必须生成 9 类 roadmap decision 对象
- `roadmap_decision_only=true`；所有真实授权与执行权限保持 false
- 至少 7 条 route candidate；**Route D** `selected_now=true`；**Route G** `blocked_now=true`
- **GovernanceDebtSignalMatrix** 至少 9 类债务信号
- **PermissionAuthorizationNonReleaseMatrix** 全部 pass
- final decision 必须指向 **Governance Debt Register**，不得指向真实 pre-auth request / owner approval / real rehearsal / migration / batch arming
- Verifier ≥ 420 checks（baseline 340）

## 规范性引用

后续 verifier 必须引用：[LUNA_EVALUATION_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_V1.md](./LUNA_EVALUATION_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_V1.md)

## Smoke 结果

- **verifier**: GO
- **checks**: 690/420
- **selected_route**: `Route D — Governance Debt Register`
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_GOVERNANCE_DEBT_REGISTER`
- **Next**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`
