# Luna — OCR TTL Gate v1 GO/NO_GO Pack v0

## GO

- 全部 ttl_review_queue 项已评估；`ttl_gate_passed_count=0`；`approval_granted=false`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- ttl 项数量与 policy 一致但非 2；无越界

## NO_GO

- ttl 直接批准或 `ttl_gate_passed_count>0` 无后续 gate；提交 decision；写 fact/WM/Scene Delta
