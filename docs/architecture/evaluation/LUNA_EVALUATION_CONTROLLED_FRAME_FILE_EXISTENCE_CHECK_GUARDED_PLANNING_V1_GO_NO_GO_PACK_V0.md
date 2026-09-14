# Luna Evaluation — Controlled Frame File Existence Check Guarded Planning v1 — GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

## GO 条件（必须全部满足）

- required 输入 roots 全部 `loaded=true`，且 `summary.final_decision` 与前置 phase 预期一致
- 产物完整：policy / gate / scope / authorization / audit / failure / rollback / schema / matrix / boundary / next phase 文件齐全
- 场景矩阵满足：
  - `scenario_count >= 18`
  - 必含场景：repo_fixture / eval_out_fixture / registered_fixture / controlled_test_asset / user_upload_restricted / symlink_restricted / traversal_blocked 等
- 计数满足：
  - `future_allowed_path_candidate_count >= 4`
  - `blocked_path_candidate_count >= 6`
  - `restricted_path_candidate_count >= 2`
- 治理要求满足：
  - `authorization_required=true`
  - `audit_trace_required=true`
  - `rollback_required=true`
  - `source_chain_required=true`
  - `fixture_registry_authorization_required=true`
  - `user_upload_authorization_insufficient_alone=true`
  - `system_generated_path_insufficient_alone=true`
- 强边界全部成立（必须全部为 false）：
  - `file_existence_check_invoked`
  - `os_path_exists_invoked`
  - `pathlib_exists_invoked`
  - `file_stat_invoked`
  - `file_opened`
  - `file_content_read`
  - `image_content_read` / `video_content_read`
  - `exif_parsed` / `video_probe_invoked`
  - `real_file_hash_computed` / `perceptual_hash_computed`
  - 任一 runtime/write/action/speech 标志
- 最终输出必须为：
  - `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN`
  - `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

## NO-GO 条件（任一触发即 NO_GO）

- 任一 required root 缺失或 `final_decision` 不匹配
- 任一越界标志为 true（exists/stat/open/read/hash/exif/probe/runtime/write/action/speech 任一）
- `boundary_ok=false` 或 `violations` 非空
- `recommended_next_phase` 不是 `Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

## Verifier 阈值

- `MIN_CHECKS >= 200`
- `BASELINE_REQUIREMENT = 160`

