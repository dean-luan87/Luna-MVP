# LUNA — OCR Pre-Decision Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-006**

## GO

- at least 2 repeat runs completed
- all run verifiers pass
- governance leakage remains 0
- schema/artifact drift remains 0
- stability analysis artifacts generated
- dataset bias review generated
- PaddleOCR fairness caveat explicitly documented
- no default provider set

## CONDITIONAL_GO

- only 1 repeat run completed, but no leakage and no drift

## NO_GO

- governance leakage > 0
- schema/artifact drift exists
- provider repeated failures
- PaddleOCR unfairness not documented
- default provider set in this phase
