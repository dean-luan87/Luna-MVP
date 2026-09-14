# Luna Evaluation — Controlled Frame File Metadata Boundary DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001`  
**输出目录**：`_eval_out/controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0/`

## 运行命令

```bash
python3 tools/evaluation/vision/run_controlled_frame_file_metadata_boundary_dryrun_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_file_metadata_boundary_dryrun_v1.py
```

## 通过判定

- `verifier=GO`
- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `scenario_count>=18`
- `metadata_decision_simulation_only=true`
- 全部文件操作边界字段为 `false`
