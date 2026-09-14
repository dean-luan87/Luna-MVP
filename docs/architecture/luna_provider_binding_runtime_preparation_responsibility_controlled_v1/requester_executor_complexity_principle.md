# Requester owns requirement complexity; executor owns execution complexity

正式原则：

`REQUESTER_OWNS_REQUIREMENT_COMPLEXITY`

提出 Requirement / Demand 的 owner 负责表达其语义、目标、约束、必要条件与 lineage。Provider Governance 不负责重新解释用户问题，也不从 observation text 推断 Provider、Model 或 capability。

对应的防止反向泄漏原则是：

`EXECUTOR_OWNS_EXECUTION_COMPLEXITY`

Runtime / Resource / Gateway owner 分别承担 allocation、execution identity、runtime ingress validation 等复杂度；这不回流到 Cognitive Demand owner。

因此“谁提需求，谁复杂”不表示 requester 负责所有下游执行，而是 requester 负责需求语义复杂度，执行 owner 负责执行复杂度。
