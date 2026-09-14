# Contracts

`ProviderBindingDecisionV1` 是 Provider Governance-owned authoritative binding
record，支持 `source_model_ref=None` 的 Provider-only binding；显式 model 只
carry-forward，不作 Model selection。

`RuntimeAllocationRecordV1` 是 Runtime Executor-owned authoritative allocation
record，状态为 `ALLOCATED`、`DENIED`、`RELEASED` 或 `FAILED`。controlled fixture
中的 resource/runtime refs 带有 synthetic/controlled/no-real-resource-effect
语义，不能解释为机器资源已经被占用。

`ExecutionInstanceV1` 由 valid Binding、valid fresh Grant、active Allocation 和
Execution Instance Preparation 共同形成。其 deterministic ref 由稳定 request、
allocation、binding refs 派生；不使用时间或随机数。模型可为空。
