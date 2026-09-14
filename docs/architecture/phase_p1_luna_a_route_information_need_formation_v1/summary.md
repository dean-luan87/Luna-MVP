# Summary

本 Phase 为 A-Route 增加了最小、只读、candidate-only 的 Information Need
Formation adapter。它复用 `CognitiveNeedCandidateV1`，从已有
`GoalContextV1.success_condition_refs` 与明确 governed condition signals
形成 required cognitive conditions，再减去 Current World 的认知覆盖，输出
necessary unknowns。

已覆盖的 controlled 设计包括：相同 Goal 的不同 Current World、完整满足、部分
覆盖、不同 governed Role、无关 Context 稳定性以及不同 Goal。它证明 Need 对
当前认知状态敏感，而不是简单消费上游 `information_need_ref`。

用户终端已真实验证 99/99 checks 通过：`all_checks_passed=true`、
`cognitive_logic_result=PASS`、`operational_result=PASS`、
`failed_checks=[]`、`final_decision=GO`。因此：
`INFORMATION_NEED_FORMATION_GAP = CLOSED`，阶段状态为
`GO — VERIFIED — PHASE CLOSED`。

边界保持：Need 不是 Information Gap，也不是 Observation Demand；本阶段不
形成观察请求、不解析 Capability、不执行 Provider/Model、不修改 Field/World，
不进入 Memory、PCN、Decision、Task 或 Action。

后续成熟度边界保持冻结：Self-conditioned objective formation、Goal-conditioned
Minimum Self/External View、required condition 的更上游自主形成、
pre-observation Attention 与 Observation Demand Formation 均未在本 Phase 实现，
不启动 `OBSERVATION_DEMAND_FORMATION_GAP` implementation。
