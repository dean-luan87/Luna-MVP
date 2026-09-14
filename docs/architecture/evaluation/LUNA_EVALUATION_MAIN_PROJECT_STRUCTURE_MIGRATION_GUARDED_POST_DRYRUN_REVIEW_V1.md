# Luna Evaluation — Main Project Structure Migration Guarded Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001`  
**性质**：review-only（不执行真实搬迁、不执行迁移后测试、不执行回滚、不确认 owner）  
**Capability**：`capabilities/governance/main_project_structure_migration_guarded_post_dryrun_review_v1.py`  
**Runner**：`tools/evaluation/governance/run_main_project_structure_migration_guarded_post_dryrun_review_v1.py`  
**Verifier**：`tools/evaluation/governance/verify_main_project_structure_migration_guarded_post_dryrun_review_v1.py`  
**输出目录**：`_eval_out/main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0/`

## 运行方式（smoke）

在 `Luna-Core` 根目录执行：

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_guarded_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_guarded_post_dryrun_review_v1.py
```

## 通过条件（必须满足）

- **输入**：guarded dryrun / guarded planning / readiness / PAHR closure / consolidation closure / structure map / gate taxonomy 全部 loaded
- **批次**：`reviewed_batch_count=8`；`simulated_pass_batch_count=8`；`simulated_blocked_batch_count=0`；`no_batch_executed=true`
- **Gate**：`reviewed_gate_count=10`；`gate_sequence_pass=true`；`human_approval_checkpoint_is_placeholder=true`；`runtime_granted=false`
- **Candidate / Exclusion**：`migration_candidate_scope_count=8`；`candidate_scopes_execution_allowed=false`；`migration_exclusion_scope_count>=17`；protected / HR / DnAE 等排除 flag 全为 true
- **测试 / 回滚 / 审批**：31 绑定、0 执行；8 rollback checkpoint、未执行 rollback；`final_owner_human_confirmed=false`；`human_approval_is_placeholder_only=true`
- **边界**：无 file move/delete/rename/merge；无 runtime；无 stat/exists/open/read；`boundary_ok=true`
- **Readiness**：`ready_for_closure=true`；`ready_for_real_migration=false`
- **裁决**：`final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- **Verifier**：`passed == true`；`check_count >= 300`（smoke 当前 377）
