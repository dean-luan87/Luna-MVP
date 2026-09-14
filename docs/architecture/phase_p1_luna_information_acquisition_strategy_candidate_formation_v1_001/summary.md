# Summary

本阶段在现有 Cognitive Flow owner 内加入最小的 governed acquisition strategy
candidate formation：

```text
Required Cognitive Conditions
→ Minimum Relevant Cognitive View
→ Information Need
→ Branch Formation
→ Branch Governance
→ Governed Exploration Branch Set
→ Information Acquisition Strategy Candidates
```

Formation 复用既有 Branch Candidate、Branch Governance Decision、Cognitive Need
与 provenance/trace 模式。新增 `GovernedAcquisitionBasisV1` 作为显式上游 basis，
并以 `InformationAcquisitionStrategyCandidateV1` 只读投影它。一个 admitted
Branch / Need 可以形成 0、1 或 N 个 candidates；不做 winner-take-all。

本阶段只完成 basis-driven candidate representation。Strategy Coordination 已由
后续独立 controlled boundary 承担；本阶段自身仍不拥有该治理语义，也没有
Resource Need、Resource Merge、Priority、Scheduling、Pre-observation Attention、
Observation Demand、Capability Resolution、Evidence return、Branch lifecycle 或
独立 General Cognitive Exploration Loop runtime。

当前状态：`WAITING_FOR_USER_TERMINAL_VERIFICATION`。
