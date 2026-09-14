# Luna Controlled Multi-Scenario Cognitive Exploration Sandbox v1-001

Status: `IMPLEMENTATION_READY_FOR_USER_EXECUTION`

这是一个 synthetic-only、controlled-only 的 integration / behavioral exploration
sandbox，不是新的 cognition owner，也不是第二套 Cognitive Loop。

它复用现有 canonical owner：

```text
Required Cognitive Condition Formation
→ Information Need Formation
→ Governed Cognitive Branch Formation
→ Cognitive Branch Governance
→ Information Acquisition Strategy Candidate Formation
```

Sandbox 只负责编排、注入受控 fixture、组织 round trace 和输出人工审阅材料。
它不重写上述模块的形成规则。

本阶段支持固定的 Round 0，以及仅由显式
`SandboxSimulatedAcquisitionReturnV1` 触发的可选 Round 1。模拟 return 不是
Observation、Provider Result 或真实 acquisition。

本阶段不实现 Strategy Coordination、Resource Merge、Attention、Observation
Demand、Capability Execution、Evidence Fusion、Decision、Task、Action、真实
Provider/Model、Memory/PCN 或 autonomous infinite loop。
