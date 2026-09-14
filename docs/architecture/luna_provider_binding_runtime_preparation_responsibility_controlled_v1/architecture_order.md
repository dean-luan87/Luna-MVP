# Architecture order

当前适用顺序：

`Provider Runtime Target Candidate`
→ `Provider Binding / Runtime Preparation Candidate`
→ `[future Model/Provider Binding when declarations are complete]`
→ `[future Runtime Allocation]`
→ `[future Execution Instance]`
→ `[future Provider Session / Runtime Observation]`
→ `Observation Gateway Runtime Admission`
→ `[future Evidence Ingress]`

Gateway 的 `ObservationGatewayRuntimeAdmissionV1` 是针对已经形成的 Runtime Observation ingress 的 Gateway-owned proof，不是本阶段创建的 execution-before permission grant。真正的 pre-execution authorization 仍需由既有 Provider/Runtime/Resource governance contracts 在后续阶段提供；本阶段不新建 super-owner。

Route C 原因：现有 Model↔Provider binding contract 需要 Model declaration，而当前 Provider Target 只保证 Provider candidate 与 observation lineage，Model 可选；直接调用已有 binding/runtime API 会越过本阶段边界。
