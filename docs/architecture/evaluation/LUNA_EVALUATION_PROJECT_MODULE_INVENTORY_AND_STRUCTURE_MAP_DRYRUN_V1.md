## Evaluation Target

- **Phase**: `Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`
- **Goal**: 验证结构映射 dry-run 产出完整资产归位表，且每条记录含 `future_life_system_mapping`；严格遵守 no-file-move 边界。

## Commands

```bash
python3 tools/evaluation/governance/run_luna_project_module_inventory_and_structure_map_dryrun_v1.py
python3 tools/evaluation/governance/verify_luna_project_module_inventory_and_structure_map_dryrun_v1.py
```

## Pass Criteria (GO)

- `verifier_report.json.passed == true`
- `check_count >= 260`
- `summary.all_entries_have_future_life_system_mapping == true`
- `summary.assets_missing_life_system_mapping == 0`
- `summary.actual_file_move_executed == false`
- `final_decision == LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING`
- `recommended_next_phase == Phase-Luna-Project-Structure-Consolidation-Planning-v1-001`

## Required Artifacts

- `module_inventory.json` — 每条含 `future_life_system_mapping`
- `current_to_target_structure_map.json`
- `life_system_mapping_matrix.json`
- `developer_backend_extraction_map.json`
- `midplatform_subsystem_mapping.json`
- `future_module_placeholder_mapping.json`
- `client_boundary_mapping.json`
- `migration_risk_register.json`
- `no_file_move_boundary_report.json`
