# Candidate contract

新增/使用的最小 contracts：

- `ProviderBindingCandidateV1`：Provider Governance-owned，1:1 从既有 Provider Binding Runtime Preparation Candidate 投影；不是 Binding Decision。
- `RuntimeAllocationPreparationCandidateV1`：Runtime Executor-owned，携带显式 `runtime_requirement_refs`、`resource_class_refs`、`execution_class_refs`，不携带具体分配身份。
- `ExecutionInstancePreparationCandidateV1`：Runtime Executor-owned，描述未来 execution envelope shape；`execution_instance_created=false`，不产生 `execution_instance_ref`。

所有 candidate 都保持 candidate-only/read-only/non-truth。多个 Provider 不排序、不评分、不选 winner；同 Provider 服务多个 Demand 时保留独立 lineage。
