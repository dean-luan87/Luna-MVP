# CrossModal Vision-OCR RealVideo FrameSample Smoke v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001`  
**定位**：在 RealVideo CaseRegistry 与 Vision ingest/trace/governance 产物之上，建立 **帧采样索引 smoke**（非识别阶段）。

**核心原则**：只采样帧、生成样本索引与质量 placeholder、case coverage 与 poster/facility 候选映射；**不** 运行 OCR / Vision provider / YOLO / VLM；**不** 生成 OCRRequest / CrossModal reference / fusion；**不** 写事实层。

**实现**：
- `capabilities/midplatform/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0.py`
- `tools/evaluation/midplatform/run_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0.py`
- `tools/evaluation/midplatform/verify_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0.py`

**后续**：ROI-to-OCR reference-only 见 [LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_ROI_TO_OCR_REFERENCE_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_REALVIDEO_ROI_TO_OCR_REFERENCE_V0.md)。
