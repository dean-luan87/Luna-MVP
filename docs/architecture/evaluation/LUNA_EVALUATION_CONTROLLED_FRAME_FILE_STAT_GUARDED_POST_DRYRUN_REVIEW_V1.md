# Luna Evaluation — Controlled Frame File Stat Guarded Post-DryRun Review v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001`  
**性质**：review-only（不新增能力；不执行任何 `stat/exists/open/read/hash`）  
**Runner**：`tools/evaluation/vision/run_controlled_frame_file_stat_guarded_post_dryrun_review_v1.py`  
**Verifier**：`tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_post_dryrun_review_v1.py`  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_post_dryrun_review_v1_smoke_v0/`

## 运行方式（smoke）

在 `Luna-Core` 根目录执行：

```bash
python3 tools/evaluation/vision/run_controlled_frame_file_stat_guarded_post_dryrun_review_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_post_dryrun_review_v1.py
```

## 通过条件（必须满足）

- inputs：必须加载 file stat dryrun + planning，并加载 existence-check chain 与 metadata boundary chain 的历史闭环输入  
- 覆盖：`reviewed_scenario_count>=28`，required scenario ids 全覆盖  
- 边界：`stat/exists/open/read/hash/EXIF/probe` 全部未发生；runtime/write/action/speech 全部未触发  
- readiness：`ready_for_closure=true` 且 `ready_for_real_stat=false`  
- 裁决：`final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`

