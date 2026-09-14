# Luna Evaluation — Main Project Structure Migration B0 Controlled Execution v1

## 目标

- B0 首次真实 controlled migration（三份文档索引/README/phase table）
- 生成 before/after manifest + operation plan/trace + guard/assertion 产物
- 成功后进入 Post-Migration Review（不再生成新授权链）

## 成功条件（GO）

- preflight 上游 GO
- 三份 candidate_paths 均存在且处理完成（unchanged / moved / renamed）
- 无 forbidden operation；无 protected/eval_out 触碰
- before/after manifest 与 operation_trace 完整
- `boundary_ok=true`

## 输出目录

- `_eval_out/main_project_structure_migration_b0_controlled_execution_v1_smoke_v0/`
