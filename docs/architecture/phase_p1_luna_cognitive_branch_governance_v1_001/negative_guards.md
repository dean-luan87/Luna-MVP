# Negative Guards

本阶段必须保持：

- candidate input immutable；
- Governance 不执行 Branch Formation，不生成新 Branch；
- 不修改 Hypothesis、Information Need、Required Conditions、Current World、Field 或 Self；
- 不声明 World Truth / Field Truth；
- 不执行 winner-take-all；
- 不执行 Merge、Convergence、Close、Reopen 或其他 Branch Lifecycle；
- 不产生 execution priority、schedule 或 resource governance；
- 不形成 Resource Need、Observation Demand、Capability Requirement、Decision、Task 或 Action；
- 不调用 Provider / Model，不执行 Observation；
- 不调用 Memory / PCN mutation；
- 不使用 semantic string similarity、Goal string、Question string、scenario_id、case_id
  或 fixture name 驱动治理；
- Resource availability 变化不得改变 Branch 的认知治理结果。
- Need satisfied 不等于 Branch no longer required；没有明确 currently-not-needed
  governance signal 时不得仅凭 satisfaction defer/reject。

治理结果只表达当前 candidate 的认知治理状态。即使所有 Branch 都不是
`ADMITTED`，也不得由本模块自动触发 Stop；Stop 仍由既有 Sufficiency / Stop owner
负责。
