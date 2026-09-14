# Provider Binding → Runtime Allocation → Execution Instance

本 controlled phase 首次形成三个 execution-domain authoritative mechanical
record：`ProviderBindingDecisionV1`、`RuntimeAllocationRecordV1` 和
`ExecutionInstanceV1`。它们只使用受控 synthetic identity；不会启动进程、Provider
session、模型、设备、Gateway 或 Observation。

链路为：Provider Binding Candidate → Runtime Grant (GRANTED、fresh、未 revoke) →
Provider Binding Decision → Runtime Allocation Record → Execution Instance
(`CREATED`，但 `execution_started=false`)。Runtime Grant 是两个 mechanical steps
前都要重新检查的硬前置。
