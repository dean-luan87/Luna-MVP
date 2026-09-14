# Luna Evaluation — Controlled Frame Sample DryRun v1

**Phase**：`Phase-Controlled-Frame-Sample-DryRun-v1-001`  
**性质**：manifest-metadata-only dry-run（不读内容、不打开文件、不解码、不抽帧）  
**输出目录**：`_eval_out/controlled_frame_sample_dryrun_v1_smoke_v0/`

## 运行命令（smoke）

runner：

```bash
python3 tools/evaluation/vision/run_controlled_frame_sample_dryrun_v1.py
```

verifier：

```bash
python3 tools/evaluation/vision/verify_controlled_frame_sample_dryrun_v1.py
```

## 通过标准

通过 verifier（GO）时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`

本阶段强制保证：

- `manifest_metadata_only=true`
- `file_opened/image_opened/video_opened=false`
- `file_content_read/image_content_read/video_content_read=false`
- `video_decoded=false`、`frame_extracted=false`、`real_file_hash_computed=false`
- 不生成 `VisualObservation/SceneSketch/OCRActivationResult/TrackingResult`
- 不触发 runtime/write/action/speech

