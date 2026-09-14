# Negative Guards

本阶段必须保持以下边界：

- `scenario_id`、`case_id`、Goal string、Question string 和 fixture name 不驱动 branch semantics；
- 不使用 keyword / substring 生成 Branch；
- 单一充分解释不强制生成多个 Branch；
- Conflict 只能引用已有 explanation / hypothesis alternatives，不能凭空生成新 hypothesis；
- Branch Formation 不修改 Hypothesis、Information Need、Current World、Field 或 Self；
- Branch Candidate 不声明 World Truth 或 Field Truth；
- 不执行 Branch admission、rejection、priority、merge、dormant、close、reopen；
- 不申请或获取 Cognitive Resource；
- 不形成 Observation Demand、Capability Requirement、Task、Decision 或 Action；
- 不调用 Provider / Model / Observation Runtime；
- 不调用 Memory / PCN mutation；
- 不创建 autonomous child loop runtime；
- 不改变现有 Sufficiency、Stop、Re-observation owner 与语义。

所有 Branch 输出必须保持 candidate-only、read-only、non-Truth，并保留
parent、basis、derived-from、lineage、trace 与 provenance。
