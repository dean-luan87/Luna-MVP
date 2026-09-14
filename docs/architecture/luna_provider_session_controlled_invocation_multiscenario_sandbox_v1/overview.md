# Provider Session Controlled Invocation Multi-Scenario Sandbox v1

本阶段把已创建的 `ExecutionInstanceV1` 推进到受治理的 Provider Runtime
Session 与 synthetic controlled invocation。它只模拟 execution lifecycle
记录，不产生真实 Provider、Model、网络或操作系统 runtime effect。

链路为：

`ExecutionInstanceV1 → ProviderRuntimeSessionV1 → ProviderInvocationRecordV1`

后续的 `RuntimeObservationEnvelopeV1`、Observation Gateway、Evidence 与
Current World 仍然 deferred。
