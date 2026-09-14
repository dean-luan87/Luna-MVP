# LUNA — OCR Provider Role Reclassification v0

## Phase

- **Phase-ModelOCR-006D** — *Open OCR Candidate Expansion & Reclassification v0*

## Purpose

Freeze **role** and **status** for each OCR-related stack so realtime navigation OCR, offline accuracy, system fallback, general comparison baselines, and **complex layout / VL** futures are **not conflated**. No default provider is assigned here.

## Mandatory role table (frozen)

| Provider / configuration | Role | Status | Notes |
|--------------------------|------|--------|--------|
| **RapidOCR — current** | `realtime_candidate` | `candidate_ready_needs_variant_benchmark` | Light near-realtime track; 005B-class latency ~**118 ms/frame**; needs **006E** variant + baselines. |
| **RapidOCR + PP-OCRv5 mobile ONNX** (det/rec) | `realtime_variant_candidate` | `to_evaluate` | Next benchmark (006E). |
| **RapidOCR + PP-OCRv4 mobile ONNX** (det/rec) | `realtime_variant_candidate` | `to_evaluate` | Next benchmark (006E). |
| **PaddleOCR — current workspace config** | `offline_accuracy_candidate` / `complex_ocr_candidate` | `not_recommended_current_realtime_config` | **Reasons:** `runtime_model_path_unknown`, `bbox_evaluation_not_closed`, `latency_too_high_for_realtime` (~**2340 ms/frame** class). Optional **006C-Fix-001** does not restore realtime suitability by itself. |
| **macOS Vision OCR** | `system_fallback` / `comparison_baseline` | `ready_but_not_realtime` | Reliable harness path; **~460 ms/frame** class — not realtime primary. |
| **EasyOCR** | `general_multilingual_comparison_candidate` | `to_evaluate` | **006E** general comparison; not presumed winner. |
| **Tesseract** | `classic_baseline_candidate` | `to_evaluate` | **006E** classic baseline. |
| **Surya OCR** | `layout_reading_order_candidate` | `complex_branch_future` | **Not** in 006E realtime pool. |
| **docTR** | `document_ocr_candidate` | `complex_branch_future` | **Not** in 006E realtime pool. |
| **PaddleOCR-VL / DeepSeek-OCR / OCR2-style** | `complex_document_future_candidate` | `future_branch` | Layout / VL / long-doc — **separate** from realtime default gate. |

## Split: realtime vs complex branch

- **Realtime OCR decision path:** RapidOCR line + EasyOCR + Tesseract for **006E** only (see `LUNA_OCR_REALTIME_CANDIDATE_NEXT_BENCHMARK_PLAN_V0.md`).  
- **Complex layout / reading-order / OCR-VL path:** Surya, docTR, PaddleOCR-VL, DeepSeek-OCR — see `LUNA_OCR_COMPLEX_LAYOUT_CANDIDATE_BRANCH_PLAN_V0.md`. **Do not** merge into realtime default eligibility without a dedicated phase.

## Non-goals

- Does **not** set default OCR provider.  
- Does **not** remove PaddleOCR from repo or stop **006C-Fix-001** as a **parallel** audit branch.  
- Does **not** declare RapidOCR production-default — **006E** required.

## Governance reminder

Raw-text harness boundaries, zero semantic leakage, zero downstream execution, zero real TTS, trace/replay/whitebox per module standard.
