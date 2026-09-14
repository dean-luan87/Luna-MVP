# LUNA — RapidOCR Model Variant Evaluation Plan v0

## Phase

- **Phase-ModelOCR-006E** (planned; execution deferred until 006D review is accepted)

## Scope note

The **canonical 006E benchmark scope** (five realtime candidates, complex branch excluded) is **`LUNA_OCR_REALTIME_CANDIDATE_NEXT_BENCHMARK_PLAN_V0.md`**. This file remains a **narrow** RapidOCR-only variant plan for historical reference.

## Objective

Run a **controlled, same-GT** comparison of RapidOCR under three model configurations on the existing **30-sample** `ocr_raw_text_benchmark_v0` manifest:

1. **Variant A — RapidOCR default**  
   Current default det/rec (as shipped by the project’s RapidOCR dependency / adapter defaults).

2. **Variant B — PP-OCRv5 mobile ONNX**  
   RapidOCR configured to use **PP-OCRv5 mobile** detection and recognition ONNX weights (paths pinned in manifest or adapter profile; acquisition follows existing pinned-weights policy).

3. **Variant C — PP-OCRv4 mobile ONNX**  
   RapidOCR configured to use **PP-OCRv4 mobile** det/rec ONNX weights (same pinning discipline).

**Variant D** (PaddleOCR offline/complex) is **out of scope** for this benchmark phase — it remains on the offline track per **006D** role reclassification.

## Dataset and harness

- **Manifest:** `datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json`  
- **Metrics:** align with existing raw-text benchmark metrics (exact/normalized match, CER/WER, latency percentiles, fps, confidence where available, governance counters).  
- **Boundaries:** raw text only; no semantic labels; no downstream; no default provider selection in the tool output.

## Engineering tasks (checklist)

- [ ] Define three RapidOCR **config profiles** (or manifest entries) that differ only by ONNX model paths / RapidOCR init kwargs.  
- [ ] Acquire and pin **PP-OCRv5 mobile** and **PP-OCRv4 mobile** ONNX assets with file-level hashes (reuse `models/ocr/` + manifest pattern from ModelOCR-003).  
- [ ] Extend or duplicate `evaluate_rapidocr_raw_text_v0.py` entry points to accept `--model-profile` (or equivalent) without changing GT.  
- [ ] Run three full passes; archive `output_root` per variant with timestamps.  
- [ ] Optional: short note on **mobile vs server** ONNX choice rationale (reference: official PP-OCR tables — mobile for realtime experiments).

## Success criteria (for proceeding to provider decision review)

- All three variants **complete** on 30 samples without fail-closed mass failure.  
- **Comparable** latency and accuracy tables (same metrics schema).  
- **Governance leakage = 0** per verifier.  
- Explicit statement whether any variant clears a **pre-agreed** accuracy + latency bar (bar is defined in provider decision pack, not in this plan).

## Explicit non-goals

- No PaddleOCR realtime tuning marathon.  
- No default OCR provider flag in runtime config.  
- No integration with YOLO, mid-platform, SceneTask, Fusion, or Expression.
