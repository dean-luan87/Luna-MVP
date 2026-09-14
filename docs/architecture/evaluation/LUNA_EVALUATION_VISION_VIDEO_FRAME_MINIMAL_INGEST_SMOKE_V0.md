# Luna 评测 — Vision 视频帧最小 Ingest Smoke v0

**Phase**：`Phase-Vision-VideoFrame-Minimal-Ingest-001`  
**Verifier**：`tools/evaluation/vision/verify_video_frame_minimal_ingest_smoke_v0.py`

## CLI

**生成测试视频并 ingest（推荐本地自检）**

```bash
python3 tools/evaluation/vision/run_video_frame_minimal_ingest_smoke_v0.py \
  --repo-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --generate-test-video \
  --max-frames 10 \
  --sample-stride 2 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0
```

**指定已有 MP4（绝对路径）**

```bash
python3 tools/evaluation/vision/run_video_frame_minimal_ingest_smoke_v0.py \
  --repo-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --video /ABS/PATH/video.mp4 \
  --max-frames 10 \
  --sample-stride 1 \
  --max-width 1280 \
  --max-height 720 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0
```

`--repo-root` 可省略（默认使用 runner 推导的仓库根并加入 `PYTHONPATH`）。

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `video_frame_ingest_summary.json` | 汇总：`source_video_ref`、`stream_id`、帧计数、内嵌 audit 等 |
| `video_frame_sampling_report.json` | `total_frames_seen`、`sampled_frame_count`、`skipped_frame_count`、`sample_stride` / `sampling_stride`、`sampled_indices` |
| `video_frame_envelopes.jsonl` | 每行一个 `video_frame_envelope_v0` |
| `video_frame_matrix.json` | 采样帧的表格化摘要（`rows`） |
| `video_frame_audit_report.json` | 与 summary 中 audit 一致的独立报告 |
| `video_frame_ingest_notes.md` | 人类可读短说明 |
| `generated/video_frame_minimal_ingest_test.mp4` | 仅 `--generate-test-video` 时 |
| `frames/frame_XXXXXX.png` | 每采样帧一张 PNG |

## Verifier

```bash
python3 tools/evaluation/vision/verify_video_frame_minimal_ingest_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0
```

输出：`video_frame_minimal_ingest_verifier_report.json`。

GO / CONDITIONAL_GO / NO_GO 见：`LUNA_EVALUATION_VISION_VIDEO_FRAME_MINIMAL_INGEST_SMOKE_GO_NO_GO_PACK_V0.md`。

## Vision 主线顺序（评测侧对齐）

本 smoke 只覆盖「帧 ingest」；**不得**据此直接接视角识别。后续合法顺序与 **Input Governance / ROI stub** 见架构文档：[LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md](../vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md)。
