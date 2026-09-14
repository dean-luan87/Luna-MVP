# Ownership and Boundaries

| Layer | Responsibility | This phase |
|---|---|---|
| Information Need | 缺少什么认知信息 | upstream, unchanged |
| Cognitive Flow Strategy Coordination | 哪些 strategy 可进入 downstream consideration | upstream, unchanged |
| Observation Demand Formation | 将 admitted strategy 表达为 what-to-observe candidate | owner |
| Capability Resolution / Perception Routing | 用什么能力满足 demand | deferred |
| FPO / Provider / Model / OCR / Camera | 运行时获取与返回 evidence | deferred/downstream |

历史 `Task-Driven Observation Request`、`cognitive_analysis` 的
`ObservationRequestCandidateV1`、FPO active-observation demand/request 与
Observation Gateway ingress 不能反向成为本阶段 Cognitive Flow owner。它们包含
task/field/capability/provider 或运行时语义，属于后续 adapter 或执行边界。

Demand 不声明事实、不写 Current World/Field，不形成 Attention，不生成
Capability Requirement，也不改变任何上游 candidate 或 coordination decision。
