# Luna Evaluation — Controlled Frame File Existence Check Guarded DryRun v1 — GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

## GO 条件（必须全部满足）

- required roots 全部 `loaded=true`
- `scenario_count >= 22` 且关键场景均存在（future_allowed / restricted / blocked / missing_* / auth_insufficient / rollback）
- dry-run 产物齐全（schema + results + boundary reports）
- 强边界全部成立（必须全部为 false）：
  - `file_existence_check_invoked`
  - `os_path_exists_invoked` / `pathlib_exists_invoked`
  - `file_stat_invoked` / `file_opened` / `file_content_read`
  - `image_content_read` / `video_content_read`
  - `exif_parsed` / `video_probe_invoked`
  - `real_file_hash_computed` / `perceptual_hash_computed`
  - 任一 runtime/write/action/speech 标志
- 最终输出必须为：
  - `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
  - `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001`

## NO-GO 条件（任一触发即 NO_GO）

- 任一 required root 缺失或 `final_decision` 不匹配
- 任一越界标志为 true（exists/stat/open/read/hash/exif/probe/runtime/write/action/speech 任一）
- `boundary_ok=false` 或 `violations` 非空
- `recommended_next_phase` 不符合预期

## Verifier 阈值

- `MIN_CHECKS >= 240`
- `BASELINE_REQUIREMENT = 200`

