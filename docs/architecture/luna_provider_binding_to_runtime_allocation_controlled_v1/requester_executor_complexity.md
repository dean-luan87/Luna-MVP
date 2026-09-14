# Requester / executor complexity

`REQUESTER_OWNS_REQUIREMENT_COMPLEXITY` 约束上游负责完整表达目标、约束、必要 capability 和 lineage；Provider/Runtime 层不得根据自然语言补齐需求。

`EXECUTOR_OWNS_EXECUTION_COMPLEXITY` 约束 Runtime/Resource owner 负责 allocation、execution identity 和执行失败；Requester 不承担 GPU、slot、process、session 等内部细节。

需求不完整、Provider 不可用、binding 失败、resource 失败和 execution 失败分别归属其 authority owner；不得通过 `UPSTREAM_INVALID` 转移责任。
