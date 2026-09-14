## Phase

- **Phase ID**: `Phase-Luna-Project-Structure-Consolidation-Planning-v1-001`
- **Capability**: `capabilities/governance/luna_project_structure_consolidation_planning_v1.py`
- **Status**: planning-only（不执行真实迁移）

## Intent

在 **Structure Map DryRun** 完成 7391 条资产归位表之后，本阶段把 `merge / archive / split / keep / defer` 计划冻结为可审计的 consolidation 规划，并定义批次顺序与依赖图。

每条计划行必须保留 **`future_life_system_mapping`**，确保 consolidation 仍按 Luna 终局 life-system 方向推进，而非纯目录整理。

## Inputs

- `luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0`（required）
- `luna_project_structure_governance_and_modularization_planning_v1_smoke_v0`（required）
- `gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0`（optional）

## Outputs

`_eval_out/luna_project_structure_consolidation_planning_v1_smoke_v0/`：

- `merge_plan_register.json` / `archive_plan_register.json` / `split_plan_register.json` / `keep_plan_register.json` / `defer_plan_register.json`
- `consolidation_batch_sequence.json` — B0–B6 批次（keep → dev backend → midplatform → capability → cognition → legacy → docs）
- `consolidation_dependency_graph.json`
- `life_system_consolidation_matrix.json`
- `developer_backend_consolidation_plan.json` / `midplatform_consolidation_plan.json` / `cognition_placeholder_consolidation_plan.json` / `client_boundary_consolidation_plan.json`
- `consolidation_risk_register.json`
- `no_file_move_boundary_report.json`

## Final Decision

- `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN`
- **Next**: `Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001`

## Implementation Status

- **Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001**: **GO**（dry-run 已完成；见 `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_V1.md`）
- **Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001**: **GO**（review 已完成；见 `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_V1.md`）
- **Phase-Luna-Project-Structure-Consolidation-Closure-v1-001**: **GO**（closure 已完成；见 `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSURE_V1.md`）
- **Recommended next**: `Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`

## Non-Claims

- 不声称已执行任何 merge/archive/split 或文件移动。
- 计划行均为 `fact_status=not_fact`。
