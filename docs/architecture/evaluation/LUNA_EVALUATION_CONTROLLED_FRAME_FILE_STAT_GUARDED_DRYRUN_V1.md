# Luna Evaluation — Controlled Frame File Stat Guarded DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`  
**性质**：dryrun-only / simulation-only（只模拟 gate 决策与候选链；不调用任何真实 `stat/exists/open/read/hash`）  
**Runner**：`tools/evaluation/vision/run_controlled_frame_file_stat_guarded_dryrun_v1.py`  
**Verifier**：`tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_dryrun_v1.py`  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_dryrun_v1_smoke_v0/`

## 运行方式（smoke）

在 `Luna-Core` 根目录执行：

```bash
python3 tools/evaluation/vision/run_controlled_frame_file_stat_guarded_dryrun_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_dryrun_v1.py
```

## 验证要点（必须满足）

- **输入 roots**：必须加载 file stat planning、post roadmap、existence-check chain、metadata boundary chain、以及 sample/input/safety/MRI/OCR 的闭环输入。  
- **场景矩阵**：`scenario_count>=28` 且包含 required scenario ids。  
- **统计与覆盖**：包含 future allowed / restricted / blocked / auth failure / metadata exposure / failure mode / rollback / mapping。  
- **边界冻结**：`stat_invoked=false` 且 `exists/open/read/hash/EXIF/probe/runtime/write` 全部为 false。  
- **裁决**：`final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`，推荐进入 post-dryrun review（review-only）。

