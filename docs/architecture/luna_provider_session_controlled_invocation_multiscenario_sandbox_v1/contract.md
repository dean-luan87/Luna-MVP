# Contract

`create_provider_runtime_session()` 只接受已经存在且 lineage coherent 的：

- `ProviderBindingDecisionV1 = BOUND`
- fresh, authoritative `RuntimeExecutionGrantDecisionV1 = GRANTED`
- `RuntimeAllocationRecordV1 = ALLOCATED`
- `ExecutionInstanceV1` in `CREATED` or `READY`

session creation 生成 deterministic `session_ref`，状态为 `CREATED`，并保持
`execution_started=false`。

`start_controlled_provider_invocation()` 在 start 前再次验证上述四类输入。
它生成 deterministic invocation/result/payload refs；payload 是 opaque
synthetic reference，不包含 observation semantics。完成、失败、停止、撤销、
超时均是 controlled lifecycle outcomes。

`execution_started=true` 只在合法 invocation start 后出现。它不等于
`real_provider_invoked`，后者在本阶段始终为 `false`。
