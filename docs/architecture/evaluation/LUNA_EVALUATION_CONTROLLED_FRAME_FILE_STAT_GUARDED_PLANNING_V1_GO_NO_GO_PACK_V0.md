# Luna Evaluation — Controlled Frame File Stat Guarded Planning v1 GO / NO-GO Pack v0

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001`

## 判定口径

本包只对 **planning-only** 的治理定义是否完备、边界是否冻结、验证是否通过进行裁决；**不**代表真实 `stat` 能力已启用。

## GO 条件（必须全部满足）

1. **verifier=GO**  
2. `final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN`  
3. `recommended_next_phase=Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`  
4. **硬边界冻结**（所有为 false）：
   - `stat_allowed_now/os_stat_allowed_now/pathlib_stat_allowed_now/lstat_allowed_now`
   - `stat_invoked/os_stat_invoked/pathlib_stat_invoked/lstat_invoked`
   - `exists_allowed_now/file_existence_check_invoked/os_path_exists_invoked/pathlib_exists_invoked`
   - `open_allowed_now/file_opened/content_read_allowed_now/file_content_read/image_content_read/video_content_read`
   - `hash_allowed_now/real_file_hash_computed/perceptual_hash_computed`
   - `exif_parsed/video_probe_invoked/video_decoded/frame_extracted`
   - `no_runtime_executed=true` 且所有 runtime/action/speech/write 相关字段为 false
5. **场景矩阵**：`scenario_count>=24` 且覆盖 24 个 required scenario id
6. **metadata 暴露边界**：allowed/restricted/blocked-or-deferred 三类均存在且计数满足最低门槛
7. **candidate-only**：所有产物保持 `fact_status=not_fact` 与 `write_allowed=false`

## NO-GO 触发条件（任一即 NO-GO）

- 任何真实文件操作迹象：`stat_invoked=true` / `os_stat_invoked=true` / `pathlib_stat_invoked=true` / `lstat_invoked=true`
- 出现 `exists/open/read/hash/EXIF/probe/decode/frame_extract` 任一被调用迹象
- 出现 runtime 或写入迹象：`camera_opened`/`ocrrequest_submitted`/`world_model_written`/`memory_written`/`fact_written`/`library_written`
- 场景矩阵不足（<24）或关键场景缺失
- verifier 未达最低 checks 要求或存在 failed checks

## 通过后的含义（non-claims）

- **不等于** 真实 `stat` 已可用  
- **不等于** 可以读取内容、计算 hash、解析 EXIF 或 probe video  
- **不等于** 可以写入 `WorldModel/Memory/Fact/Library`  

