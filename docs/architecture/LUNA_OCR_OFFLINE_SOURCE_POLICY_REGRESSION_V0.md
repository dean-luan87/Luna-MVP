# LUNA — OCR Offline Source Policy Regression v0

## Phase

- **Phase-ModelOCR-010** — *OCR Offline Source Policy Regression & Closure v0* (read-only evidence validation)

## Tool

- `tools/run_ocr_offline_source_policy_regression_v0.py` — consumes **009** evidence roots; writes regression artifacts.
- `tools/verify_ocr_offline_source_policy_regression_v0.py` — validates regression output (cases A–L).

## Frozen inputs (009 evidence)

| Run | Path |
|-----|------|
| Normal | `logs/ocr_offline_source_policy_009_normal_20260429_124053` |
| Fallback | `logs/ocr_offline_source_policy_009_fallback_20260429_124053` |

## Example regression output root (010)

- `logs/ocr_offline_source_policy_regression_010_20260429_124628`

## Generated artifacts

| File | Purpose |
|------|---------|
| `ocr_offline_source_policy_regression_summary.json` | Verdict, hard gates, governance, boundary pointer |
| `ocr_offline_source_policy_regression_matrix.json` | Normal/fallback matrix (no large payload) |
| `ocr_offline_source_policy_audit_field_matrix.json` | Audit key presence across runs |
| `ocr_offline_source_policy_boundary_summary.json` | Closure / non-runtime marker |
| `regression_notes.md` | Human-readable gate dump |

## Hard checks (must pass for GO)

- `provider_selected` normal = `rapidocr_ppocrv4_mobile_onnx`, `fallback_used=false`
- `provider_selected` fallback = `rapidocr_current`, `fallback_used=true`, `fallback_reason=rapidocr_ppocrv4_disabled`
- `source_policy_id` = `ocr_default_offline_raw_text_source_policy_v0`, `policy_applied=true`
- `governance_leakage=0` (both)
- Forbidden default-chain providers not selected
- `trace` / `replay` / `whitebox` artifacts non-empty for each run

## Allowed vs forbidden drift

- **May drift:** OCR accuracy, latency, exact match, bbox IoU (metrics not gates for 010).
- **Must not drift:** Selected provider, fallback reason, policy id, governance leakage, forbidden selections, audit presence, trace/replay/whitebox.

## Verifier

- Example: **GO**, `governance_leakage=0`, `hard_blockers=[]` (see `verify_ocr_offline_source_policy_regression_v0.py` output).
