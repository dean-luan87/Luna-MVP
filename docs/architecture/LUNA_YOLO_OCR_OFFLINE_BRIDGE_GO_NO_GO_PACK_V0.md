# LUNA — YOLO × OCR Offline Bridge Skeleton Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-002** — *YOLO × OCR Offline Bridge Skeleton v0*

## GO

All true:

- Bridge skeleton executable in offline mode.
- Proposal schema and result schema validated.
- OCR source policy is invoked.
- Crop clamp/padding rules respected.
- YOLO + OCR attribution complete.
- candidate-only / raw-text-only constraints preserved.
- trace/replay/whitebox artifacts present.
- Verifier A-Q passes.
- No runtime / MidPlatform / downstream integration.

## CONDITIONAL_GO

- Some samples may have no OCR-worthy detections.
- Some OCR results may be empty but honest (`no_text_detected` / explicit blocker).

## NO_GO

- Semantic interpretation or navigation suggestion appears in bridge outputs.
- SceneTask/Fusion/Output or TTS is invoked.
- Crop out-of-bounds not clamped.
- Source attribution missing.
- OCR source policy bypassed.
- Trace/replay/whitebox missing.
- YOLO/OCR closed_v0 baselines modified.
- Product runtime path touched.

## Recommended next phase

- **Phase-ModelOCR-YOLO-Bridge-003 — YOLO × OCR Offline Bridge Evidence Run v0**
