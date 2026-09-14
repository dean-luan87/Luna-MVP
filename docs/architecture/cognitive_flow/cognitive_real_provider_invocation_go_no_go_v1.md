# Cognitive Real Provider Invocation Go/No-Go v1

## Execution mode

V1 controlled real-provider adapter skeleton. This document records component evidence only. It does not issue final phase approval.

## Validation evidence

Three fixed, offline English fixtures were each executed twice and compared through `verify_real_ocr_provider_adapter_skeleton_result_v1.py`.

| Case | Input condition | Component verifier |
|---|---|---|
| A | Clear text | 46/46 checks passed; replay consistent. |
| B | Partial occlusion | 46/46 checks passed; replay consistent. |
| C | Low-quality text | 46/46 checks passed; replay consistent. |

The verifier asserts Brain/Neural non-execution, Middleware session ownership, Evidence Adapter use, Provider Status propagation to Feedback, evidence non-truth, failure traceability, lifecycle order, and deterministic replay.

## Result summary

| Field | Result |
|---|---|
| `blocker_count` | `0` |
| `warning_count` | `1` |
| `provider_boundary_check` | `PASS` |
| `evidence_boundary_check` | `PASS` |
| `replay_check` | `PASS` for all three fixtures |

## Recorded warning

The locally supplied PP-OCRv5 Mobile configuration did not yield usable text on two fixture executions with the installed local RapidOCR runtime. The Adapter emitted `preferred_provider_no_text_output` and transparently used the local RapidOCR fallback. This is a Provider Status candidate and an integration/calibration follow-up, not a hidden success or an architectural boundary violation.

## Boundary result

- Brain did not directly invoke OCR.
- Neural Governance did not execute OCR.
- Middleware created the six-stage session trace and did not decide cognitive completion.
- Provider output became Evidence only through the Evidence Adapter.
- OCR evidence did not claim Reality, Truth, Decision, Action, or state mutation.
- No camera, hardware, UI, scheduler, legacy runtime change, Model Manager main-logic change, or Reducer mutation occurred.

`final_candidate_decision: COMPONENT_VALIDATION_PASSED_WITH_PROVIDER_FALLBACK_NOTE`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
