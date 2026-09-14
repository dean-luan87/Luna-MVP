# Observation Demand Controlled Implementation v1

Status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

本阶段在现有 Cognitive Flow 中建立受限的认知到感知需求边界：

```text
Strategy Coordination
  → candidate-only Cognitive Observation Demand
  → [future Capability Resolution / Perception Routing]
```

一个 `ADMITTED` acquisition strategy 形成一个 Observation Demand candidate。
Demand 只表达“需要观察什么”，不表达如何执行。它不是第二套 Loop，也不取得
Observation、Capability、Provider、Model、Task 或 Action ownership。

本阶段不修改 Information Need、Branch、Strategy Coordination、Sufficiency 或
Stop 的 owner。Sandbox integration 保持 `DEFERRED`，以避免把历史探索沙盒升级为
感知接口 owner。
