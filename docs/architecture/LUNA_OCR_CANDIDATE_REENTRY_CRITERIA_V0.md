# LUNA — OCR Candidate Re-Entry Criteria v0

## Phase

- **Phase-ModelOCR-007A** — defines when a **demoted** or **non-active** provider may **re-enter** the **active realtime candidate pool** for **policy** discussion and **benchmark admission** (still subject to **no silent default** until a later explicit phase).

## General rules

- Re-entry is **evidence-driven**: re-run the **same or stricter** harness (e.g. realtime OCR candidate benchmark) with **pinned assets**, **documented hardware**, and **verifier GO**.
- **Governance**: `governance leakage = 0` for any promotion discussion.
- **Sample size**: minimum **30** GT remains a **floor**; broader categories (e.g. exit_sign, warning_text) may require **additional** stratified samples before **default** consideration.

---

## EasyOCR

May be reconsidered for **active realtime candidate** evaluation when **all** hold:

- Dependencies and model **weights pinned** (reproducible versions + hashes where applicable).
- On **≥30** GT (same or superset), **exact match / CER** shows **clear** advantage over **RapidOCR** primary line (`rapidocr_ppocrv4_mobile_onnx` / `rapidocr_current`) under agreed metrics — not marginal noise on n=30.
- **Average latency** ≤ **300 ms** per frame (or product-updated budget) on reference hardware.
- **Governance leakage = 0**.

Until then: **`COMPARISON_ONLY`** + **`NOT_RECOMMENDED_CURRENT_CONFIG`**.

---

## Tesseract

May be reconsidered when **all** hold:

- **Chinese language pack / preprocessing strategy** completed and documented (no ad-hoc ambiguity).
- Demonstrable **advantage** on agreed slices (e.g. **digit**, **doorplate**, **English short text**) vs RapidOCR line — with numbers.
- **Latency** acceptable for the **realtime_region_ocr** budget on reference hardware.
- **Governance leakage = 0**.

Until then: **`CLASSIC_BASELINE`** / **`COMPARISON_ONLY`** — **not** realtime default.

---

## PaddleOCR (current workspace configuration)

Either:

**Path A — Re-enter realtime candidate evaluation**

- **Runtime model path locked** and auditable (hash / manifest).
- **BBox / evaluability** gaps **closed** (raw structure, coordinate system, GT alignment).
- **Latency** **significantly** improved vs historical ~2.3s/frame class **or** product accepts a higher budget with written rationale.
- Verifier-clean benchmark run.

**Path B — Stay in complex / offline only**

- Explicitly **scoped** to **offline accuracy**, **complex layout**, or **document** branch — **no** merge into realtime default pool without Path A evidence.

---

## RapidOCR PP-OCRv5 mobile ONNX

May be reconsidered for **active** pool when **all** hold:

- **Official auditable model source** or a **trusted export chain** with **pinned** artifacts and **hashes** (not “community ONNX” without lineage).
- **Accuracy and bbox** **clearly** better than **v4 mobile / current** on the same GT + agreed task-relevant scores.
- Asset manifest complete in repo or controlled cache per project rules.

Until then: **`FUTURE_REVIEW_REQUIRED`** + **`SOURCE_RISK_COMMUNITY_ONNX`**.

---

## macOS Vision

Typically **does not** “re-enter” as **realtime primary** — it remains **`SYSTEM_FALLBACK_BASELINE`**.  
Re-entry to **active primary** would require a **product charter change** and **new latency/accuracy** evidence (out of scope for default 007A assumption).

---

## Complex-branch stacks (Surya, docTR, PaddleOCR-VL, DeepSeek-OCR, …)

**Re-entry to realtime default** is **not** the normal path. They **graduate** within **`COMPLEX_OR_OFFLINE_BRANCH`** via **layout / document / OCR-VL** benchmarks and policies — **not** by merging into short-text realtime default without a **separate** phase and **explicit** scope.
