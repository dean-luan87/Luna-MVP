# LUNA — OCR Provider Decision Risk Register v0

## Phase

- **Phase-ModelOCR-007**

## Mandatory risks (must not be ignored)

| ID | Risk | Mitigation / gate |
|----|------|-------------------|
| R1 | **Sample size = 30** — minimum bar only, not population proof | Stratified expansion; stability runs; do not over-claim generalization |
| R2 | **Exact match ceiling ~0.2** — metric may be strict; OCR “default” must stay **conservative** | Add **task-relevant** scoring (e.g. CER, partial match, sign-type subsets) in future phases — **not** in Phase-007 code |
| R3 | **GT / stratum gaps** — e.g. exit_sign / warning_text classes historically noted as thin | Continue GT expansion per dataset plan |
| R4 | **PP-OCRv5 mobile ONNX** — **community export** (`ilaylow/PP_OCRv5_mobile_onnx` + dict from `monkt/paddleocr-onnx`); **not** Paddle official HF Paddle-format chain | Treat as **experimental**; `FUTURE_REVIEW_REQUIRED`; optional official export + hash audit |
| R5 | **Complex OCR / VL** — must not leak into **realtime default** decision | Keep 006D branch boundary; separate harness |
| R6 | **Default provider temptation** — evidence ≠ permission to flip runtime | Phase-007 **forbids** code default; Phase-008 policy definition **still** no forced runtime switch unless explicitly approved later |

## Evidence linkage

- 006E-Fix: `logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`  
- 006D role split: complex vs realtime  
- 006C: Paddle path/bbox/latency audit gaps for realtime

## Owner note

This register is **living**; re-open when GT ≥ next threshold or when new models enter the realtime pool.
