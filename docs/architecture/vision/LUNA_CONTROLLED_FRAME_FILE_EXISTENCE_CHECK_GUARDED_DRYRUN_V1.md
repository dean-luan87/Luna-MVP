# Luna — Controlled Frame File Existence Check Guarded DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`  
**性质**：dry-run-only（只模拟 gate 决策与治理输出；不执行真实文件存在性检查）  
**输出目录**：`_eval_out/controlled_frame_file_existence_check_guarded_dryrun_v1_smoke_v0/`

## 阶段目标

本阶段对 `File Existence Check Guarded Planning v1` 做一次严格 dry-run（simulation-only），验证：

- existence-check gate 能否区分 `future_allowed / restricted / blocked` 路径
- 仅有路径字符串是否会被阻断（授权不足）
- 缺 `source_chain` / 缺隐私标签 / 缺 fixture registry ref 是否会被阻断
- user upload / system generated 授权是否不足以单独授权 existence check
- “authorized candidate” 在 dry-run 仍 **不会**触发真实 exists/stat
- gate denied / permission denied / missing file 等 failure mode 是否能落到安全 fallback
- audit trace 与 rollback 决策是否稳定生成
- no-file-operation / no-runtime / no-write / no-action / no-speech 边界是否保持成立

## 强边界（必须冻结）

- 不执行文件存在性检查；不调用 `os.path.exists` / `pathlib.Path.exists`
- 不 `stat/open/read`；不读 image/video 内容；不 hash；不 EXIF/probe；不解码/抽帧
- 不进入 runtime；不写 `WorldModel/Memory/Fact/Library`；不触发 action/speech

## 关键产物（概览）

runner 必须输出（详见 evaluation 文档）：

- schemas：dryrun case / request stub / gate decision / path scope / authorization / audit / failure mode / rollback / mapping / result
- `controlled_frame_file_existence_check_guarded_dryrun_scenario_matrix.json`（≥22 场景）
- `controlled_frame_file_existence_check_guarded_dryrun_results.json`（聚合结果）
- 各决策 results：gate / path_scope / authorization / audit / failure / rollback / mapping
- `file_existence_check_boundary_matrix.json`
- `next_phase_recommendation.json`
- `no_file_operation_boundary_report.json` / `no_runtime_boundary_report.json` / `no_write_boundary_report.json`

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`

## 实施状态

- **当前阶段结论**：`GO`
- **final_decision**：`CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **recommended_next_phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`
- **硬边界声明**：本阶段不调用 `exists/stat/open/read/hash`，不进入 runtime，不写 `WorldModel/Memory/Fact/Library`。

> 注：本阶段的通过并不意味着真实 `exists/stat` 已启用；下一阶段 `Post-DryRun Review` 与后续 `Closure` 仍将继续压死“simulation-only / no-file-operation”边界。

