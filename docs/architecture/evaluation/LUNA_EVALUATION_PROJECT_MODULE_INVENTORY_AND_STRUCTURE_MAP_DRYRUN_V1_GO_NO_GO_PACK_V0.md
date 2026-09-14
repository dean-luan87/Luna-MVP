## Scope

`Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`

## GO 条件

- 全套 JSON 产物齐全（含 9 张核心映射表 + boundary report）。
- **每条 inventory / map row 均含非空 `future_life_system_mapping`**。
- `life_system_mapping_matrix.json` 覆盖全部 14 个 life-system layer。
- `no_file_move_boundary_report.json` 中 `actual_file_move_executed == false`。
- `migration_risk_register.json.assets_missing_life_system_mapping == 0`。
- `final_decision` / `recommended_next_phase` 匹配合同。
- verifier `passed == true` 且 `check_count >= 260`。

## NO-GO 条件

- 任一资产缺少 `future_life_system_mapping`（退化为纯工程目录整理）。
- 发生或声称发生文件移动/重命名/删除/模块合并。
- 把 dry-run 映射当作已完成迁移或 production readiness。
- verifier 失败或 checks 不足。

## Notes

- 本 phase 的 inventory 为 **planning 信号**（`fact_status=not_fact`），不是事实资产清单。
