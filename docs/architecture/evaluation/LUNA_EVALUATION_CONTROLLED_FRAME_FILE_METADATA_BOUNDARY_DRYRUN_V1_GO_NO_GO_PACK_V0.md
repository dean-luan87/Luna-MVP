# Luna Evaluation — Controlled Frame File Metadata Boundary DryRun v1 — GO / NO-GO Pack v0

## GO 条件

- `file_metadata_boundary_planning_input_loaded=true`
- 全部 schema 与 dryrun results 齐全
- `scenario_count>=18`，18 个必需场景 ID 均存在
- `metadata_decision_simulation_only=true`
- `file_stat_invoked=false`、`exif_parsed=false`、`video_probe_invoked=false`、`real_file_hash_computed=false`
- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`

## NO-GO 条件

- planning 输入缺失或 final_decision 不匹配
- 任一真实文件操作标记为 true
- `recommended_next_phase` 不是 Post-DryRun Review phase

## Verifier 阈值

- `MIN_CHECKS >= 220`
- `BASELINE_REQUIREMENT = 180`
