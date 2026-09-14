# LUNA — Open OCR Candidate Expansion Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-006D** — *Open OCR Candidate Expansion & Reclassification v0*

## GO

All of the following are true:

- **PaddleOCR downgrade rationale** is documented (006C strict: path unknown, bbox eval not closed, inference latency ~2.3s class → **not realtime**, **`not_recommended_current_config`**).  
- **OCR provider role reclassification** is complete in `LUNA_OCR_PROVIDER_ROLE_RECLASSIFICATION_V0.md`.  
- **Realtime OCR candidate pool** is explicit (RapidOCR current + v5/v4 mobile variants + EasyOCR + Tesseract for 006E).  
- **Complex layout branch** is explicit and **separated** from realtime decisions.  
- **Next benchmark plan** is explicit (`LUNA_OCR_REALTIME_CANDIDATE_NEXT_BENCHMARK_PLAN_V0.md`).  
- **No default OCR provider** is set.  
- **No downstream** integration (YOLO, mid-platform, SceneTask, Fusion, Output, navigation, real TTS, controlled live stream).

## CONDITIONAL_GO

- Role table is complete but **006E harness adapters** for EasyOCR/Tesseract are not yet implemented — acceptable for **006D closure** if the **plan** and **scope split** are frozen; track as engineering follow-up.

## NO_GO

- **PaddleOCR current config** is still treated as **realtime primary candidate** without documenting the three 006C blockers.  
- **Complex layout** and **realtime** OCR are **mixed** in a single default-provider decision.  
- A **default OCR provider** is set in this phase.  
- **PaddleOCR risks** (path/bbox/latency) are not registered.  
- This phase **enters downstream** systems.

## Suggested verdict (documentation phase)

When the five 006D documents and README index are merged: **GO** for **006D scope** (strategy + taxonomy + plans only).

## Hard blockers (project-level, carried forward)

- PaddleOCR **runtime model path** not proven against manifest.  
- PaddleOCR **bbox** not evaluable at batch level despite `rec_polys` hint.  
- **Inference latency** excludes PaddleOCR current config from realtime chain.

## Soft follow-ups

- Implement **006E** harnesses for EasyOCR and Tesseract.  
- Acquire and pin **PP-OCRv5 / v4 mobile** ONNX for RapidOCR variants.  
- Optional parallel: **006C-Fix-001** for Paddle audit path (does not unblock realtime by itself).

## Recommended next phase

- **Phase-ModelOCR-006E — Realtime OCR Candidate Benchmark v0**  
  Evaluates **only**: RapidOCR current, RapidOCR + PP-OCRv5 mobile ONNX, RapidOCR + PP-OCRv4 mobile ONNX, EasyOCR, Tesseract.  
  **Does not** include: Surya, docTR, PaddleOCR-VL, DeepSeek-OCR (complex branch).

## Boundaries (repeat)

This phase is **only** OCR candidate expansion and role reclassification. **No** default OCR, **no** semantic distillation, **no** YOLO, **no** mid-platform, **no** downstream, **no** navigation execution, **no** real TTS.
