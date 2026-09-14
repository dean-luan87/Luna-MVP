# CrossModal Vision-OCR RealVideo ROI-to-OCR Reference v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001`  
**定位**：基于 RealVideo FrameSample 与 Vision ROI / OCR bridge 产物，建立 **reference-only** 引用视图（frame → ROI → OCRRequest candidate）。**不提交 OCRRequest，不运行 OCR。**

**严禁**：提交 OCRRequest；运行 RapidOCR/PaddleOCR/Vision/YOLO/VLM；生成 OCR evidence / fusion / Scene Delta；写事实层；改 routing。

**实现**：`capabilities/midplatform/cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0.py`

**后续**：Gated OCRRequest submission 见 [LUNA_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md](../ocr/LUNA_REALVIDEO_OCR_REQUEST_GATED_SUBMISSION_V0.md)；readonly consumer 见 [LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md](../ocr/LUNA_REALVIDEO_OCR_EVIDENCE_READONLY_CONSUMER_V0.md)；reference update 见 [LUNA_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md](./LUNA_REALVIDEO_OCR_REFERENCE_UPDATE_V0.md)。

Regression Comparison 见 [LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_REGRESSION_COMPARISON_V0.md](./LUNA_CROSS_MODAL_VISION_OCR_TESTBOARD_V1_REGRESSION_COMPARISON_V0.md)。
