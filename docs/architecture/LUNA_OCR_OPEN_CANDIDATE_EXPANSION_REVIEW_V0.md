# LUNA — Open OCR Candidate Expansion & Reclassification Review v0

## Phase

- **Phase-ModelOCR-006D** — *Open OCR Candidate Expansion & Reclassification v0*

## Why expand the candidate pool

The unified GT benchmark (005B) and pre-decision reviews (006, 006A–006C) show that **no single stack** today clears both **latency** and **accuracy** bars for a navigation-adjacent realtime OCR default. Narrowing engineering effort to one provider (e.g. PaddleOCR-only hardening) **does not** address the product need: a **fast, auditable** realtime path plus **honest** baselines and **separate** tracks for complex documents.

## Phase-ModelOCR-006C — strict closure note

- **006C engineering deliverables:** accepted as **成立** (artifacts produced: runtime evidence hooks, output-shape notes, latency breakdown).  
- **006C audit verdict (strict):** **CONDITIONAL_GO**, **near NO_GO risk edge** — not because raw text is unusable, but because three **foundation** issues are not closed:
  1. **`runtime_model_path` still `unknown`** — cannot prove runtime det/rec equals manifest-pinned assets.  
  2. **BBox:** `rec_polys` is identified, but **batch evaluation does not close** (`bbox_present_rate=0.0`, `bbox_iou_avg=0.0`) — pipeline from raw output to evaluable boxes is incomplete.  
  3. **Latency:** dominant cost is **`per_frame_inference_ms` ≈ 2.3s class** — incompatible with realtime OCR regardless of path/bbox fixes alone.

**PaddleOCR current configuration — frozen labels:**

- `not_recommended_current_config`  
- **Realtime default candidacy:** **不成立**  
- **Default provider eligibility:** **不成立**  
- **Roles retained:** `offline_accuracy_candidate`, `complex_ocr_candidate` (see role reclassification doc).

**Important:** 006C closure does **not** “fail” PaddleOCR as a research/offline asset; it **fails** it as **realtime主线** until a different configuration (e.g. mobile ONNX via RapidOCR, or a future locked mobile Paddle path) is proven separately.

## Why not prioritize PaddleOCR-006C-Fix-001 immediately

**006C-Fix-001** (strong path lock + bbox eval closure) improves **auditability**, not **realtime suitability**. Even with perfect path proof and bbox IoU, **~2.3 s/frame inference** keeps PaddleOCR **off** the realtime chain. That fix can proceed **in parallel** as a **branch**; it must **not block** realtime candidate expansion.

## Direction (006D)

1. **Reclassify** all listed providers (RapidOCR variants, PaddleOCR, Vision, EasyOCR, Tesseract, complex-branch stacks).  
2. **Expand** the **realtime OCR** evaluation pool for the next benchmark phase (**006E**).  
3. **Split** **realtime OCR** decisions from **complex layout / reading-order / OCR-VL** futures — **no mixing** in a single default-provider gate.

## Boundaries

- No default OCR provider.  
- No YOLO, no mid-platform, no SceneTask/Fusion/Output.  
- No semantic interpretation, no navigation execution, no real TTS, no controlled live stream.

## Related documents

- Full role table: `LUNA_OCR_PROVIDER_ROLE_RECLASSIFICATION_V0.md`  
- Next benchmark plan: `LUNA_OCR_REALTIME_CANDIDATE_NEXT_BENCHMARK_PLAN_V0.md`  
- Complex branch: `LUNA_OCR_COMPLEX_LAYOUT_CANDIDATE_BRANCH_PLAN_V0.md`  
- Go/No-Go: `LUNA_OCR_OPEN_CANDIDATE_EXPANSION_GO_NO_GO_PACK_V0.md`
