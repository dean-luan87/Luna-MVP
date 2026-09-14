# LUNA — PaddleOCR Real Inference Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-006A**

## GO

- real inference path runs
- same 30-sample GT set evaluated
- raw text schema valid
- metrics complete
- governance leakage = 0
- trace/replay/whitebox complete
- fairness review updated

## CONDITIONAL_GO

- partial sample failures but fail-closed honest outputs
- metrics complete with caveats
- cls missing_optional keeps orientation not_claimed

## NO_GO

- real inference cannot start
- fake success while dependencies/models missing
- semantic/navigation leakage appears
- downstream invoked
- observability artifacts missing
