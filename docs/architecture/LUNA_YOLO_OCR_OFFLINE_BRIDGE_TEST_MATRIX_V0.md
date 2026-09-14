# LUNA — YOLO × OCR Offline Bridge Test Matrix v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-002**

## Verifier coverage (`tools/verify_yolo_ocr_offline_bridge_v0.py`)

- A. input samples readable
- B. `OCRCropProposal` schema valid
- C. crop region clamped to image bounds
- D. original bbox preserved
- E. max proposals per frame respected
- F. OCR source policy used
- G. YOLO attribution present
- H. OCR attribution present
- I. raw text candidates schema valid or honest empty
- J. `candidate_only=true`
- K. `semantic_interpretation_enabled=false`
- L. `allows_execute_now=false`
- M. `real_tts_invoked=false`
- N. `downstream_invocation_count=0`
- O. trace/replay/whitebox present
- P. delta placeholder fields present
- Q. no SceneTask/Fusion/Output invocation markers

## Sample evidence

- `logs/yolo_ocr_offline_bridge_002_20260429_151332` → verifier verdict **GO**.
