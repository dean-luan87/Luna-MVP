## Evaluation Target

- **Phase**: `Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001`
- **Goal**: 验证本阶段为 planning-only 的项目结构治理规划，且严格遵守硬边界；输出的结构化 JSON 产物齐全并通过 verifier。

## What This Evaluation Must Prove

- **Inputs**：上游根目录被正确加载，并且其 `summary.final_decision` 与链路合同一致。
- **Planning artifacts**：所有规划对象（目标结构模型、模块域分类、版本策略、文档重组、developer backend 抽离、midplatform 器官模型、未来占位等）均生成。
- **Hard boundaries**：所有 boundary report 均为 conservative（禁止 runtime / 禁止 file ops / 禁止写入持久层 / 禁止动作）。
- **Decision contract**：`final_decision` 与 `recommended_next_phase` 精确匹配合同。

## Commands

在 `Luna-Core` 根目录执行（如果遇到权限问题，需用更高权限重试）：

```bash
python tools/evaluation/governance/run_luna_project_structure_governance_and_modularization_planning_v1.py
python tools/evaluation/governance/verify_luna_project_structure_governance_and_modularization_planning_v1.py
```

## Output Location

- `_eval_out/luna_project_structure_governance_and_modularization_planning_v1_smoke_v0/`

## Pass Criteria (GO)

- `verifier_report.json.passed == true`
- `verifier_report.json.check_count >= 260`
- `summary.json.final_decision == LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN`
- `summary.json.recommended_next_phase == Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`
- 所有 `*_boundary_report.json` 中关键禁止项为 `false`，且 `boundary_ok == true`

## Fail Criteria (NO-GO)

- 任一上游 required 输入缺失/不一致
- 出现任何 runtime / action / persistent write / user media file read 的迹象或声称
- `final_decision` / `recommended_next_phase` 不匹配合同
- verifier 未达到最低 checks 或 `passed == false`

