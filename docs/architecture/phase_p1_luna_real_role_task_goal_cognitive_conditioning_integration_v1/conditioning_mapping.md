# Conditioning Mapping

共享链路为：

`Goal / Task / Role → Information Need / required information →
ProviderObservationIngressCaseV1 → existing RealOCRProviderExecutionEngineV1 →
ProviderRuntimeResultV1 → RuntimeObservation → Observation Gateway → A-Route →
Cognitive State Formation`。Runtime ingress 同时传递只读的
`evidence_information_refs`（Evidence ref → provider-declared information refs）和
跨轮的 `inherited_information_refs`；这两个字段只用于把 relevance 与 coverage 对齐，
不改变 native Evidence。

evaluation 层只定义 side context 并比较 canonical CState proof；不创建新的
conditioning owner、Sufficiency owner、Information Gap owner 或 Stop owner。

现有 CState engine 的 conditioning fields：

- `role_refs`
- `task_refs`
- `goal_refs`
- `concern_refs`
- `information_need_refs`
- admitted `evidence_refs`
- `required_information_refs` / `available_information_refs` / support bindings
- `relation_refs`

允许变化的是 attention、relevance、relation interpretation、hypothesis、Current World
Candidate、sufficiency、gap 和 stop candidate。存在 support binding 时，只有 `RELEVANT`
Evidence 才能覆盖其声明的 required information；`IRRELEVANT` 只保留为 candidate。
Physical Field、native result、Runtime Observation 与 Evidence raw content 不随
conditioning 变化。
