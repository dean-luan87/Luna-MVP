# LUNA — OCR Stage-2 Provider Approval Gate v0

## Phase

- **Phase-Mainline-GuardedTrial-010** — *Provider Dependency / Credentials / Input Snapshot & Approval Gate v0*

## Purpose

Freeze **pre-execution** artifacts for an OCR Stage-2 provider-controlled trial:

- Dependency snapshot (import probes only; no OCR inference)
- Credential presence check (**keys only**, never secret values)
- Input sample metadata + SHA-256 (allowed image extensions; **no pixel decode**, no OCR)
- Fallback / `not_available` readiness (policy materials)
- Controlled provider runbook snapshot (from Phase-009 output)
- Approval gate report + trace/replay/whitebox

## Explicit non-scope

- Does **not** invoke OCR providers or OCR models
- Does **not** send network requests
- Does **not** open camera or video streams
- Does **not** enter MidPlatform / SceneDelta / WorldContextEvidence
- Does **not** integrate **full voice interaction** (output governance / RequestTrace shadow ≠ ASR / dialog main chain)

## Related tools

- `tools/prepare_ocr_stage2_provider_approval_gate_v0.py`
- `tools/verify_ocr_stage2_provider_approval_gate_v0.py`
