# Luna Evaluation — Controlled Frame File Metadata Boundary Planning v1 — GO / NO-GO Pack v0

## GO 条件

- 全部 required input roots `loaded=true`
- 全部 policy/schema 产物齐全
- `scenario_count>=16`，且 16 个必需场景 ID 均存在
- `file_existence_check_allowed_now=false`、`real_hash_computation_allowed_now=false`、`external_metadata_read_allowed_now=false`
- `file_stat_invoked=false`、`file_opened=false`、`exif_parsed=false`、`video_probe_invoked=false`、`real_file_hash_computed=false`
- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN`

## NO-GO 条件

- 任一 required root 缺失
- 出现真实文件操作或内容读取标记为 true
- `recommended_next_phase` 不是 DryRun phase

## Verifier 阈值

- `MIN_CHECKS >= 200`
- `BASELINE_REQUIREMENT = 160`
