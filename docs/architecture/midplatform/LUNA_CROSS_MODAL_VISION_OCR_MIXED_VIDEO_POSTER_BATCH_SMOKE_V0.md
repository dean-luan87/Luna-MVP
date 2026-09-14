# Luna — CrossModal Vision OCR Mixed Video + Poster Batch Smoke v0

**Phase**：`Phase-CrossModal-Vision-OCR-Mixed-Video-Poster-Batch-Smoke-001`

## 目的

混合 **8 路视频 + 10 张 fixtures 图片**，验证新版 OCR → Evidence Pack → Semantic Candidate 主线能否端到端跑通（smoke only）。

## 边界

- 允许 RapidOCR 扫描 / 抽帧 / 图片 OCR
- 生成 OCRTextEvidencePack + OCRSemanticCandidate dry-run
- **不写** MidPlatform fact / Scene Delta / WorldModel；不改 routing

## 实现

- Capability：`capabilities/midplatform/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0.py`
- Runner：`tools/evaluation/midplatform/run_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0.py`

## 评测

[LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_CROSS_MODAL_VISION_OCR_MIXED_VIDEO_POSTER_BATCH_SMOKE_V0.md)

## 后续阶段

**Phase-MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001**（见 [LUNA_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md](./LUNA_MIXEDVIDEO_OCR_SCAN_LINEBOX_TRACE_SOURCE_QUALITY_GATE_V0.md)）已补视频 scan linebox trace 与 OCR Source Quality Gate。

## 后续阶段

v2 **Gated Path Only** 见 [LUNA_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_V0.md](./LUNA_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_V0.md)（替代本阶段直连 RapidOCR）。

## 建议下一跳

以 v2 作为 mixed batch 主 smoke；继续 ROI crop / SystemHealth provider mask。
