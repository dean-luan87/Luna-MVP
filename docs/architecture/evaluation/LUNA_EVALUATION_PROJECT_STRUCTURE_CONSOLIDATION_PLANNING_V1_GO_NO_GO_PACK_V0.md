## GO

- 五类 plan register（merge/archive/split/keep/defer）齐全
- 每条 plan row 含非空 `future_life_system_mapping`
- `consolidation_batch_sequence` ≥ 6 批次，全部 `execution_status=planning_only`
- `no_file_move_boundary_report.actual_file_move_executed == false`
- verifier `passed == true`，`check_count >= 260`

## NO-GO

- 缺少 life-system 映射
- 发生或声称发生文件移动/合并执行
- verifier 失败
