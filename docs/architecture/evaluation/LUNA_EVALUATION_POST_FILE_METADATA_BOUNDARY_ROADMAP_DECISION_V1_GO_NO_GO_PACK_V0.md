# Luna Evaluation — Post File Metadata Boundary Roadmap Decision v1 — GO / NO-GO Pack v0

**Phase**：`Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001`

## GO 条件（必须全部满足）

- 输入 roots required 全部 `loaded=true`，且 `summary.final_decision` 与前置 phase 的预期一致
- 产物完整：`route_option_matrix / priority_ranking / boundary_freeze / non_claims / governance_debt` 等文件齐全
- 路线数量与分层满足：
  - `route_option_count >= 10`
  - `p0_route_count >= 3`
  - `p1_route_count >= 4`
  - `p2_route_count >= 2`
- **选中路线**必须为：
  - `selected_route = File Existence Check Guarded Planning`
  - `recommended_next_phase = Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`
- File Metadata Boundary 当前状态总结必须明确：
  - `file_metadata_boundary_closed=true`
  - `metadata_decision_simulation_only=true`
  - `file_existence_check_readiness_claimed=false`
  - `real_metadata_readiness_claimed=false`
  - `real_hash_readiness_claimed=false`
  - `real_image_readiness_claimed=false`
  - `visual_runtime_claimed=false`
  - `production_readiness_claimed=false`
- 强边界必须全部成立（no-runtime / no-write / no-action / no-speech / no-file-existence-check / no-file-stat / no-file-open / no-image-read / no-video-decode 等）

## NO-GO 条件（任一触发即 NO_GO）

- 任一 required root 缺失或 `final_decision` 不匹配预期
- 输出中出现任何越界主张或行为标记为 true：
  - `file_existence_check_invoked / file_stat_invoked / file_opened / file_content_read`
  - `image_opened / video_opened / image_content_read / video_content_read`
  - `video_decoded / frame_extracted / exif_parsed / video_probe_invoked`
  - `real_file_hash_computed / perceptual_hash_computed`
  - `camera_invoked / visual_model_invoked / ocr_provider_invoked / map_api_invoked / tracking_runtime_invoked / crossing_runtime_invoked`
  - `world_model_written / memory_written / fact_written / library_written`
- `recommended_next_phase` 不是 `Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

## Verifier 阈值

- `MIN_CHECKS >= 200`
- `BASELINE_REQUIREMENT = 150`

## 预期最终裁决

- `final_decision=POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

