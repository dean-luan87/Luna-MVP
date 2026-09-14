# LUNA — OCR Candidate Archive & Exclusion Policy v0

## Phase

- **Phase-ModelOCR-007A** — *OCR Candidate Archive & Exclusion Policy v0* (**documentation and governance classification only**)

## Purpose

Move providers that **do not** belong in the **active realtime default decision pool** into **archived / comparison / complex / future-review** categories — **without deleting** code, historical documents, or benchmark artifacts.

This phase answers: *what stays “active candidate” vs “demoted but preserved,”* and *why deletion is the wrong move.*

## Why we do not delete “failing” candidates

Current “not suitable for realtime default” conclusions are **phase-bound** (e.g. **30-sample** GT, **current** config, **current** hardware). Removing them would destroy three kinds of engineering assets:

1. **Negative evidence** — Why EasyOCR, Tesseract, or PaddleOCR (current config) failed this bar prevents repeated mistakes and supports audits.
2. **Comparison / sanity-check baselines** — Tesseract, macOS Vision, etc. remain useful as **classic baseline**, **system fallback reference**, or **A/B sanity checks** even when not primary.
3. **Future branch assets** — PaddleOCR, Surya, docTR, DeepSeek-OCR, OCR-VL stacks may be wrong for **short realtime text** but right for **complex layout, long text, reading order, document OCR** — they stay in a **complex / offline** lane, not erased.

## Hard exclusions (this phase)

This document phase **must not**:

- Delete or gut **provider implementation code** (adapters, harnesses).
- Delete **historical architecture / benchmark write-ups**.
- Delete **benchmark output roots** under `logs/` or equivalent.
- Set or imply a **runtime default OCR provider** in code or config.
- Wire **YOLO**, **mid-platform**, **SceneTask / Fusion / Expression**, **semantic condensation**, **navigation execution**, **real TTS**, or **controlled live stream** — **not in scope**.

## Evidence baseline (frozen)

- **006E-Fix** completed: five harness candidates **success**; primary realtime narrative aligns with **007** decision review.
- **Benchmark root (authoritative for 006E-Fix):**  
  `logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`
- **Realtime primary narrative (documentation):**  
  `rapidocr_ppocrv4_mobile_onnx` and/or `rapidocr_current` — see **007** matrix.

## Active vs demoted (conceptual)

| Intent | Meaning |
|--------|---------|
| **Active realtime candidate pool** | Providers allowed to be discussed as **future** realtime default / primary-secondary policy **targets** (still **no** code default in 007A). |
| **Archived / demoted from active pool** | **Not** deleted — **downgraded** to comparison, baseline, complex branch, or future review; **must not** be promoted to realtime default without **re-entry criteria** (see `LUNA_OCR_CANDIDATE_REENTRY_CRITERIA_V0.md`). |
| **Default chain (when it exists)** | **Must not** silently call providers that are **excluded** from realtime default per this policy; adapters and benchmarks **remain** for **explicit** invocation / replay. |

## Classification reference

Authoritative tabular breakdown: **`LUNA_OCR_PROVIDER_ACTIVE_ARCHIVE_STATUS_MATRIX_V0.md`**.

## Related documents

- `LUNA_OCR_PROVIDER_DECISION_REVIEW_V0.md` — Phase-007 evidence and recommendations.
- `LUNA_OCR_REALTIME_PROVIDER_RECOMMENDATION_MATRIX_V0.md` — recommendation grades (007).
- `LUNA_OCR_PROVIDER_ACTIVE_ARCHIVE_STATUS_MATRIX_V0.md` — **007A** active/archive status matrix.
- `LUNA_OCR_CANDIDATE_REENTRY_CRITERIA_V0.md` — **007A** re-entry conditions.
- `LUNA_OCR_CANDIDATE_ARCHIVE_GO_NO_GO_PACK_V0.md` — **007A** closure pack.
