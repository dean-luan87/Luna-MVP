# Luna — OCR Review Queue Runtime DryRun v1 GO/NO_GO Pack v0

## GO

- 47 个 queue candidate 全部 intake；分类/排序/状态/出队 dry-run 完整
- `decision_committed=false`；`approval_granted_count=0`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- candidate 数量与 policy 一致但非 47；无越界

## NO_GO

- candidate 被丢弃；`approval_granted=true`；`review_decision_committed=true`
- WM attach / Scene Delta / 写 fact / benchmark claim / 改 routing
