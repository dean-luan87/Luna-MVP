# LUNA — Realtime OCR Candidate Next Benchmark Plan v0

## Phase

- **Phase-ModelOCR-006E** — *Realtime OCR Candidate Benchmark v0* (planned execution; 006D defines scope only)

## Objective

Run a **single-GT, raw-text-only** comparison across **five** realtime-track candidates on the existing **30-sample** manifest:

`datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json`

## Candidates in scope for 006E

| # | Stack | Role (006D) | Notes |
|---|--------|-------------|--------|
| 1 | **RapidOCR — current default** | `realtime_candidate` | Baseline; status `candidate_ready_needs_variant_benchmark`. |
| 2 | **RapidOCR + PP-OCRv5 mobile ONNX** (det + rec) | `realtime_variant_candidate` | `to_evaluate`; pinned ONNX paths per repo policy. |
| 3 | **RapidOCR + PP-OCRv4 mobile ONNX** (det + rec) | `realtime_variant_candidate` | `to_evaluate`. |
| 4 | **EasyOCR** | `general_multilingual_comparison_candidate` | `to_evaluate`; general comparison, not presumed default. |
| 5 | **Tesseract** | `classic_baseline_candidate` | `to_evaluate`; classic baseline. |

## Explicitly **out of scope** for 006E

The following stay on the **complex layout / future** branch — **not** scored in 006E for realtime default:

- Surya OCR  
- docTR  
- PaddleOCR-VL  
- DeepSeek-OCR / OCR2-style stacks  

(See `LUNA_OCR_COMPLEX_LAYOUT_CANDIDATE_BRANCH_PLAN_V0.md`.)

## Harness requirements (all five)

- Same GT, same metrics schema family as 005B (exact/normalized, CER/WER, latency, fps, bbox/conf where applicable).  
- **Raw text candidates** only — no semantic interpretation.  
- **Governance:** `semantic_interpretation_enabled=false`, `allows_execute_now=false`, `real_tts_invoked=false`, `downstream_invoked=false`.  
- **Observability:** trace / replay / whitebox per existing OCR module standard (extend adapters where missing — engineering work under 006E, not 006D).  
- **No** default provider flag in output.  
- **No** downstream integration.

## Reference metrics (context from 005B — illustrative)

- RapidOCR class: avg latency **~118 ms/frame** order, `bbox_iou_avg` **~0.28** class, `text_exact_match_rate` **~0.2** — **variant + extra baselines** needed before provider decision.

## Deliverables (006E)

- Five timestamped `output_root` directories + verifiers.  
- Summary table: latency + accuracy + bbox + governance.  
- Explicit statement: **no default OCR** until a separate **provider decision review** phase.
