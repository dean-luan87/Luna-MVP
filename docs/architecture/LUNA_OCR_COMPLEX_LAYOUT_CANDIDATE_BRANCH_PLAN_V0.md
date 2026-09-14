# LUNA — Complex Layout OCR Candidate Branch Plan v0

## Phase

- **Phase-ModelOCR-006D** (branch definition) — execution **after** realtime 006E baseline is stable

## Purpose

**Isolate** long-horizon, **layout-heavy** OCR stacks from **realtime navigation OCR** decisions. Mixing these into the same “default OCR” gate produces false conclusions: they optimize **reading order, structure, tables, and VL-style understanding**, not **low-latency raw text** for a single frame.

## Candidates on this branch (not in 006E realtime benchmark)

| Stack | Role ID | Status |
|-------|---------|--------|
| **Surya OCR** | `layout_reading_order_candidate` | `complex_branch_future` |
| **docTR** | `document_ocr_candidate` | `complex_branch_future` |
| **PaddleOCR-VL** | `complex_document_future_candidate` | `future_branch` |
| **DeepSeek-OCR / OCR2 / similar VL-doc** | `complex_document_future_candidate` | `future_branch` |

## Intended use cases (future)

- Reading order and block grouping  
- Layout analysis  
- Table recognition  
- Long-form / multi-column text  
- Complex documents, screens, announcements, posters  
- OCR-VL and multimodal document understanding  

## Rules

1. **Do not** use this branch’s results to justify **realtime default** OCR without a **separate** harness and latency budget.  
2. **Do not** merge complex-branch scores into **006E** realtime tables.  
3. **PaddleOCR (current workspace config)** may overlap “complex” usage in the future, but remains **`not_recommended_current_realtime_config`** until re-proven on a **new** configuration — tracked separately from this branch’s VL tools.

## Governance

Same raw-text and no-downstream boundaries apply when these are eventually harnessed; semantic interpretation policies for VL outputs are **out of scope** for ModelOCR raw-text phases unless explicitly opened in a future phase.
