# Phase-P1 Luna Cognitive Branch Governance v1-001

Status: `GO — VERIFIED — PHASE CLOSED`

本阶段是现有 Minimum Sufficient Cognition Loop 的扩展，不创建第二套
Cognitive Loop，也不抽取独立 General Cognitive Exploration Loop runtime。

当前新增边界：

```text
Cognitive Branch Candidates
→ Governance Decisions
→ Governed Exploration Branch Set
```

Branch Governance 只评估已经形成的 Branch Candidate 是否仍具备当前有效的
cognitive basis、是否与当前问题一致、是否具有独立探索依据，以及当前是否需要
继续探索。当前仓库没有 canonical equivalence contract，因此不会人工进行
semantic dedup。它不形成新 Branch，不修改原 Candidate。

V1 只产生三类治理结果：

- `ADMITTED`：允许进入当前认知探索集合，不表示 executing、scheduled 或 resource granted；
- `DEFERRED`：当前暂不进入 Active Exploration Set，但候选身份、lineage、provenance
  与 recoverability 保留；
- `REJECTED`：当前 basis 或 candidate contract 不满足治理条件，不删除历史，也不声明
  World Truth。

Formation 与 Governance 严格分离。Governance 不拥有 Resource Governance、
Sufficiency、Stop、Decision、Task、Action 或 Branch Lifecycle。

本阶段成熟度限定为 `Governed Branch Governance`。用户终端已真实验证通过，
`COGNITIVE_BRANCH_GOVERNANCE_GAP = CLOSED`。

下一尚未解决的边界为：

```text
Governed Exploration Branch
→ Information Acquisition Continuity
→ one or more acquisition paths
→ coordination
→ Attention / Observation Demand
```

本 closure 不决定 Resource Need、Acquisition Strategy、Strategy Governance、
Priority、Scheduling、Attention 或 Observation Demand contract。
