# Luna Evaluation — Controlled Frame File Stat Guarded Planning v1

**Phase**：`Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001`  
**性质**：planning-only（policy/schema/simulation-plan only；不允许任何真实 stat/exists/open/read/hash/runtime）  
**Runner**：`tools/evaluation/vision/run_controlled_frame_file_stat_guarded_planning_v1.py`  
**Verifier**：`tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_planning_v1.py`  
**输出目录**：`_eval_out/controlled_frame_file_stat_guarded_planning_v1_smoke_v0/`

## 运行方式（smoke）

在 `Luna-Core` 根目录执行：

```bash
python3 tools/evaluation/vision/run_controlled_frame_file_stat_guarded_planning_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_file_stat_guarded_planning_v1.py
```

## 验证要点（必须满足）

- **输入 roots**：必须加载 `post_file_existence_check_roadmap_decision` + `file_existence_check_guarded` 链（planning/dryrun/post-review/closure）以及更早的 `file_metadata_boundary` 链与基础闭环（sample/input/safety/MRI/OCR）。  
- **policy/schema 定义完整**：gate/scope/auth/privacy/audit/failure/rollback/mapping 全部落盘。  
- **场景矩阵**：≥24，并包含“future allowed / blocked / restricted / metadata boundary / failure / rollback”关键场景。  
- **边界冻结**：`stat_allowed_now=false` 且 `stat_invoked=false`；同时 `exists/open/read/hash/EXIF/probe/runtime/write` 全部 false。  
- **不产生事实**：所有产物保持 `fact_status=not_fact`、`write_allowed=false`（candidate-only）。  
- **裁决**：`final_decision=CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN`；推荐进入 `Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001`（仍 simulation-only）。

## 产物清单（runner 输出）

见：`docs/architecture/vision/LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_V1.md` 的“结构化产物”章节。

