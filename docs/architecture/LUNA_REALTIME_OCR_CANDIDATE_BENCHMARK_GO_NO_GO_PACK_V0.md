# LUNA — Realtime OCR Candidate Benchmark Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-006E**

## GO

- `rapidocr_current` runs (**success** or **partial** on samples).
- At least **two** of the other four candidates report **success** or **partial**.
- All five candidates have **run_status** and **asset reports**.
- Metric tables + governance metrics + trace/replay/whitebox present.
- `forbidden_gt_field_count == 0`, governance leakage **0**, **no** default provider flag.
- **No** complex-branch providers in the run list.

## CONDITIONAL_GO

- `rapidocr_current` OK but only **one** additional candidate succeeds — expand harness/deps and re-run.
- **PP-OCRv5 mobile** remains **not_available** (missing ONNX) — acceptable if documented; does not alone fail 006E if other gates pass.

## NO_GO

- `rapidocr_current` cannot run.
- Any **fake** success for a failed provider.
- Governance leakage ≠ 0.
- Missing asset report bundle or observability files.
- Default OCR provider set in summary.
- Forbidden provider keys appear in the run.

## Recommended next phase

- If no candidate clears accuracy + latency: adopt **short-text / low-frequency RapidOCR** strategy and route **complex/long** to **future layout branch** (per 006D plan) — **without** setting default OCR until a dedicated provider decision review.
