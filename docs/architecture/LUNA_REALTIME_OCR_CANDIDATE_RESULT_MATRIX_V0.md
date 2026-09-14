# LUNA — Realtime OCR Candidate Result Matrix v0

## Phase

- **Phase-ModelOCR-006E**

## Matrix dimensions

Populate from `logs/realtime_ocr_candidate_benchmark_006e_*/metric_tables/` and `per_provider_summaries/`:

| Row \ Col | Accuracy (exact/CER) | Latency (avg/p95) | BBox (IoU/precision) | Confidence | Governance | Asset status |
|-----------|----------------------|-------------------|----------------------|------------|------------|--------------|
| rapidocr_current | | | | | | |
| rapidocr_ppocrv4_mobile | | | | | | |
| rapidocr_ppocrv5_mobile | | | | | | |
| easyocr | | | | | | |
| tesseract | | | | | | |

## Interpretation

- **accuracy_risk_flag** when `text_exact_match_rate` &lt; 0.2 (recorded in metrics).
- **Latency**: suggest budget — ≤150 ms avg “优”; ≤300 ms avg “conditional”; see benchmark notes.
- **BBox**: if unusable for spatial tasks, do not treat as spatial OCR primary.

Concrete numbers are **run-specific** — fill after each `output_root` execution.
