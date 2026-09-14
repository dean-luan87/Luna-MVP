# LUNA — Realtime OCR Candidate Replacement Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-006D**

## Intent

Decide whether the project may **proceed** from “three-provider parity benchmark” to a **realtime主线 refocus** (RapidOCR variants) without selecting a default OCR provider.

## GO

All of the following are satisfied:

- **PaddleOCR role downgrade** is documented with clear reasons (latency class, bbox/path audit gap, no abandonment of Paddle as offline/complex track).  
- **RapidOCR realtime主线** is explicit: primary candidate **class** for realtime evaluation is RapidOCR/ONNXRuntime, pending **006E** variant runs.  
- **New candidate combinations** are enumerated: A default, B PP-OCRv5 mobile ONNX, C PP-OCRv4 mobile ONNX, D Paddle offline.  
- **No default OCR provider** is set in any runtime or config as part of 006D.  
- **No downstream integration** (YOLO, mid-platform, SceneTask, Fusion, Output, navigation execution, real TTS, controlled live stream) is introduced in this phase.

## CONDITIONAL_GO

- Role reclassification is agreed, but **006E** pinning locations or weight acquisition for B/C is still open — proceed to 006E with a **weight acquisition sub-step** called out in the evaluation plan.

## NO_GO

- Ambiguity remains whether PaddleOCR is still treated as realtime default candidate **without** documented rationale.  
- RapidOCR realtime主线 is not stated, or PP-OCR variant plan is missing.  
- Any **default OCR provider** flag or routing change is introduced without a separate provider decision phase.  
- Downstream or semantic scope creep (navigation actions, TTS, fusion) appears in the same change set as 006D docs.

## Verdict placeholder

For the **full** 006D expansion (open candidate pool + role table + complex branch), use **`LUNA_OCR_OPEN_CANDIDATE_EXPANSION_GO_NO_GO_PACK_V0.md`**.

Record the actual verdict when 006D is closed in the project log:

- **Verdict:** _TBD_  
- **Closed at:** _TBD_  
- **Owner note:** 006D is documentation/strategy only; **006E** executes benchmarks.

## Next phase

- **Phase-ModelOCR-006E — RapidOCR Model Variant Benchmark v0** (see `LUNA_RAPIDOCR_MODEL_VARIANT_EVALUATION_PLAN_V0.md`).
