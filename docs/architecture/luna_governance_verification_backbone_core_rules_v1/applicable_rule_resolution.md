# Applicable rule resolution

Canonical function：`resolve_applicable_governance_set`。

Resolver 读取 typed registry 与 profile，按 registry 顺序保留稳定结果；只进行 domain、owner、profile 和显式 contract-ref 的 exact matching，不使用 keyword、fuzzy、embedding、LLM 或动态加载。

输出 `ApplicableGovernanceSetV1`：resolved rules、blocker/warning refs、resolution basis、resolution status 和 validation errors。
