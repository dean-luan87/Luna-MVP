# Luna Evaluation — Main Project Structure Migration Guarded Closure v1

**Phase**：`Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001`  
**性质**：closure-only（状态冻结 / 边界冻结 / non-claims / carryover；不执行迁移、测试、回滚、owner 确认）  
**Capability**：`capabilities/governance/main_project_structure_migration_guarded_closure_v1.py`  
**Runner**：`tools/evaluation/governance/run_main_project_structure_migration_guarded_closure_v1.py`  
**Verifier**：`tools/evaluation/governance/verify_main_project_structure_migration_guarded_closure_v1.py`  
**输出目录**：`_eval_out/main_project_structure_migration_guarded_closure_v1_smoke_v0/`

## 运行方式（smoke）

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_guarded_closure_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_guarded_closure_v1.py
```

## 通过条件

- 四阶段 `completed_phase_count >= 4`，均为 GO
- `batch_count=8`；`simulated_pass_batch_count=8`；`gate_sequence_pass=true`
- 31 测试绑定 / 0 执行；8 rollback checkpoint / `rollback_executed=false`
- HumanApproval 占位；`final_owner_human_confirmed=false`
- `correction_record_status=recorded`；`correction_semantic_impact=no_permission_granted`
- `closure_allowed=true`；`real_migration_allowed=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE`
- Verifier：`passed == true`；`check_count >= 260`（smoke 275）

## Non-Claims（必须成立）

- Closure ≠ 可真实搬迁 / 可执行 post-migration tests / owner 已确认
- Closure ≠ protected / HR / DnAE 可处理
