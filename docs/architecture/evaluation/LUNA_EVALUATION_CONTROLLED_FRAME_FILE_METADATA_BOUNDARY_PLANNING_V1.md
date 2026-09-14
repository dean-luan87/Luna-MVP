# Luna Evaluation — Controlled Frame File Metadata Boundary Planning v1

**Phase**：`Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_metadata_boundary_planning_v1_smoke_v0/`

## 运行命令

```bash
python3 tools/evaluation/vision/run_controlled_frame_file_metadata_boundary_planning_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_file_metadata_boundary_planning_v1.py
```

## 通过判定

- `verifier=GO`
- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001`
- `scenario_count>=16`
- 全部文件操作边界字段为 `false`
