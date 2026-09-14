# Luna — OCR Source Validation DryRun v1 GO/NO_GO Pack v0

## GO

- 各分支 intake + 规则 + 链完整性 + 可靠性评估完整
- `source_validation_passed_count=0`；`validation_satisfied_for_fact_count=0`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 候选数量随输入变化但 policy/boundary 完整

## NO_GO

- `source_validation_passed_count>0`；SQ_E/scan 通过 fact validation；批准或写 fact/WM/Scene Delta
