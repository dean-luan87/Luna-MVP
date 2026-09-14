# LUNA — Realtime OCR Candidate Replacement Review v0

## Phase

- **Phase-ModelOCR-006D**

## Note (breadth)

For the **expanded** 006D scope (EasyOCR, Tesseract, complex-branch split, strict 006C verdict), see **`LUNA_OCR_OPEN_CANDIDATE_EXPANSION_REVIEW_V0.md`**. This document remains valid as a **RapidOCR-centric** replacement narrative.

## Scope

This document records a **strategy-level** review only: which OCR stacks are suitable for **realtime / near-realtime** navigation-adjacent use versus **offline / complex-document** use. It does **not** select a default OCR provider, does **not** wire downstream systems, and does **not** run new benchmarks (benchmark execution belongs to **Phase-ModelOCR-006E**).

## Current facts (frozen inputs)

- **PaddleOCR (006A/006B/006C evidence path)**  
  - Real inference runs and produces usable raw text in the harness.  
  - Observed end-to-end latency on the 30-sample GT run is on the order of **~2.2–2.5 s/frame** (order of magnitude; exact numbers live in run artifacts under `logs/`).  
  - Bbox/traceability and **runtime model path lock** remain insufficient for treating bbox IoU as a reliable capability signal.  
  - **Conclusion for realtime default candidacy:** not suitable as the primary realtime OCR candidate under the current configuration.

- **RapidOCR / ONNXRuntime (004C/005B)**  
  - Latency is **~106–118 ms/frame** class on comparable sampled runs (see closure notes), clearly faster than Vision and PaddleOCR in this workspace.  
  - Trace / replay / whitebox paths are in place per harness design.  
  - On the same 30-sample raw-text benchmark, **exact match** remains low (e.g. **~0.2**), so RapidOCR is **not** eligible for “default provider” decision on accuracy grounds alone.

- **macOS Vision OCR (004A)**  
  - Suitable as **system fallback / comparator**; latency ~**460 ms/frame** class — too slow for realtime primary in this product posture.

## External product facts (reference only)

Official Paddle / PP-OCR materials distinguish **mobile** vs **server** detection models (CPU latency differs by tier) and note that **PP-OCRv5** recognition uses a larger dictionary and can be slower than **PP-OCRv4** in some setups. RapidOCR is positioned as an ONNXRuntime-friendly, deployment-oriented OCR stack with speed as a design emphasis. These facts support **moving the realtime evaluation主线 toward RapidOCR + PP-OCR ONNX variants** without abandoning Paddle for offline/complex scenarios.

## Directional decision (review, not runtime switch)

1. **Downgrade** PaddleOCR from “realtime default candidate” to **offline / complex-document / accuracy exploration** candidate.  
2. **Elevate** the **RapidOCR + ONNXRuntime** line as the **primary realtime evaluation主线** (model variant benchmarking next).  
3. **Retain** macOS Vision as **fallback / baseline** comparator.  
4. **Do not** set a default OCR provider until **006E** (and any follow-on gates) complete.

## Candidate set for the next benchmark phase (006E)

| ID | Description |
|----|-------------|
| **Candidate A** | RapidOCR — current default bundled models |
| **Candidate B** | RapidOCR + **PP-OCRv5 mobile** ONNX det/rec (pinned paths TBD in 006E) |
| **Candidate C** | RapidOCR + **PP-OCRv4 mobile** ONNX det/rec (pinned paths TBD in 006E) |
| **Candidate D** | PaddleOCR — **offline / complex** track only (not realtime default) |

## Recommended next phase

- **Phase-ModelOCR-006E — RapidOCR Model Variant Benchmark v0**  
  Same 30-sample GT dataset; compare A/B/C on raw text metrics + latency + governance; then reassess readiness for provider decision review.

## Boundaries

- No default OCR provider.  
- No YOLO, no mid-platform wiring, no SceneTask/Fusion/Output integration.  
- No semantic interpretation, no navigation execution, no real TTS, no controlled live stream.
