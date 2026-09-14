# Luna — Semantic Candidate v3 BBoxExpansionAware GO/NO_GO Pack v0

## GO

- 4 EP v3 → 4 Semantic Candidate v3；`entity_confirmed_count=0`
- bank-like 仅 `bank_sign_candidate`；noisy English 不提交 correction/completion
- `padding_medium` + `contextual_expand` 重复「建银银行」记为 `strategy_repeat`，非 consensus
- 不执行 Source Validation v2；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- EP v3 数量与 smoke 不一致但边界完整；部分 `unknown_text_candidate`

## NO_GO

- 确认银行实体；自动纠错/补全为 China Construction Bank
- 重复 strategy 输出当 independent consensus
- Source Validation v2 执行；写 fact/WorldModel/SceneDelta
- benchmark/provider comparison claim；改 runtime routing
