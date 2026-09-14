# Luna Evaluation — Pre-Authorization and Rollback Rehearsal Closure v1

**Phase**：`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1.py
```

## 通过条件

- Planning / DryRun / Post-Review 三阶段 GO；`completed_phase_count>=3`
- `pre_authorization_rollback_rehearsal_chain_closed=true`；`armed_batch_count=0`
- Semantic Clarification A 已记录；`rollback_success_claim_allowed=false`
- Verifier ≥ 260 checks；`boundary_ok=true`

## 下一 phase

`Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001` — 裁决下一步路线，仍不直接授权真实迁移。
