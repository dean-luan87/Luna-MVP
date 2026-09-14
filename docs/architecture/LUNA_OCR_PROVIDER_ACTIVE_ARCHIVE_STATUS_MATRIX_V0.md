# LUNA — OCR Provider Active / Archive Status Matrix v0

## Phase

- **Phase-ModelOCR-007A** — complements **Phase-ModelOCR-007** (decision review) with **pool membership** and **exclusion-from-default** semantics.

## Status taxonomy (007A)

| Tag | Meaning |
|-----|---------|
| `ACTIVE_REALTIME_CANDIDATE` | In the **active** pool for **realtime default policy** discussion (still **no** automatic code default). |
| `COMPARISON_ONLY` | Keep for **benchmarks, multilingual comparison, sanity checks** — **not** realtime default. |
| `SYSTEM_FALLBACK_BASELINE` | System API / stable local path — **fallback or comparison**, not realtime primary. |
| `COMPLEX_OR_OFFLINE_BRANCH` | Layout / long text / document / OCR-VL — **separate branch** from realtime short-text default. |
| `FUTURE_REVIEW_REQUIRED` | Retain code & assets; **re-evaluate** when re-entry criteria met. |
| `NOT_RECOMMENDED_CURRENT_CONFIG` | **Current** config + **current** evidence bar — **not** suitable for realtime default **as-is**; **not** a directive to delete code. |
| `CLASSIC_BASELINE` | Legacy engine value (e.g. Tesseract) for **classic** comparisons. |
| `SOURCE_RISK_COMMUNITY_ONNX` | Model provenance is **community export** — extra audit before any promotion. |

A provider may carry **multiple** tags (e.g. comparison + not recommended for default).

## Matrix (initial 007A fill-in)

| Provider / stack | Pool & tags | Role summary |
|------------------|-------------|----------------|
| `rapidocr_ppocrv4_mobile_onnx` | `ACTIVE_REALTIME_CANDIDATE` | Primary **documentation** candidate; auditable ONNX paths; ~equivalent to current on 006E-Fix metrics. |
| `rapidocr_current` | `ACTIVE_REALTIME_CANDIDATE` | Secondary **documentation** candidate; ~equivalent to v4 mobile on current GT. |
| `easyocr` | `COMPARISON_ONLY`, `NOT_RECOMMENDED_CURRENT_CONFIG` | Retain for multilingual comparison; poor accuracy/latency on current GT for realtime default. |
| `tesseract` | `COMPARISON_ONLY`, `CLASSIC_BASELINE`, `NOT_RECOMMENDED_CURRENT_CONFIG` | Classic OCR baseline; weak on zh / natural scene for this GT. |
| `macos_vision_ocr_system_v0` | `SYSTEM_FALLBACK_BASELINE`, `COMPARISON_ONLY` | Slower but stable, local, system API — not realtime primary. |
| `paddleocr_current` (workspace config) | `COMPLEX_OR_OFFLINE_BRANCH`, `NOT_RECOMMENDED_CURRENT_CONFIG` | Not for current realtime config; keep for offline / complex accuracy / future model swap. |
| `rapidocr_ppocrv5_mobile_onnx` | `FUTURE_REVIEW_REQUIRED`, `NOT_RECOMMENDED_CURRENT_CONFIG`, `SOURCE_RISK_COMMUNITY_ONNX` | No gain vs v4; weaker bbox; community ONNX — audit before promotion. |
| **PaddleOCR-VL** | `COMPLEX_OR_OFFLINE_BRANCH` | Document / OCR-VL lane — not realtime default. |
| **DeepSeek-OCR** | `COMPLEX_OR_OFFLINE_BRANCH` | Complex / VL lane — not realtime default. |
| **Surya** | `COMPLEX_OR_OFFLINE_BRANCH` | Layout / reading order candidate — not realtime default. |
| **docTR** | `COMPLEX_OR_OFFLINE_BRANCH` | Layout / document lane — not realtime default. |

## Active realtime candidate pool (explicit)

Only these are in **`ACTIVE_REALTIME_CANDIDATE`** for **realtime default policy** work (008+):

- `rapidocr_ppocrv4_mobile_onnx`
- `rapidocr_current`

All others in the table are **out of** that pool for **default** purposes until **re-entry** is satisfied (`LUNA_OCR_CANDIDATE_REENTRY_CRITERIA_V0.md`).

## Non-goals

- This matrix **does not** delete adapters or harnesses.
- This matrix **does not** set `default_ocr_provider` in code.
