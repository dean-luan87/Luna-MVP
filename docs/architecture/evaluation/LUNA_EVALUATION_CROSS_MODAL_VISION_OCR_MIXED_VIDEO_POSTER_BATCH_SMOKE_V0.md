# Luna — Evaluation: CrossModal Vision OCR Mixed Video Poster Batch Smoke v0

**Phase**：`Phase-CrossModal-Vision-OCR-Mixed-Video-Poster-Batch-Smoke-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 \
  --fixtures-root /Users/luanlei/Desktop/Luna-Workspace-Min/fixtures \
  --sample-interval-sec 3.0 \
  --max-selected-frames 12
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_GO_NO_GO_PACK_V0.md)
