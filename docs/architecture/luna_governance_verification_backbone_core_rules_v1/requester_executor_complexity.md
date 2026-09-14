# Requester / Executor responsibility

`REQUESTER_OWNS_REQUIREMENT_COMPLEXITY`：Requirement/Demand requester 负责语义、目标、约束、必要条件与 lineage；下游不得发明或重新解释需求。

`EXECUTOR_OWNS_EXECUTION_COMPLEXITY`：Runtime、Resource、Provider、Gateway 等执行 owner 负责各自 operational complexity；Requester 不承担 provider health、resource allocation 或 execution failure。

这不是让 requester 包办执行，而是建立 semantic responsibility 与 operational responsibility 的边界。
