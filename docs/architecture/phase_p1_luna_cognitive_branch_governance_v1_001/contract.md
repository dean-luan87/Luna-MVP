# Cognitive Branch Governance Contract

## Canonical owner

治理 owner 为 `Cognitive Flow Branch Governance`。它消费既有
`CognitiveBranchCandidateV1` 与显式 current governed state refs，输出独立的
`CognitiveBranchGovernanceDecisionV1` 和 `CognitiveBranchGovernanceResultV1`。

原始 Branch Candidate 保持 immutable：

```text
CognitiveBranchCandidateV1 (FORMED_CANDIDATE)
        ↓ read-only evaluation
CognitiveBranchGovernanceDecisionV1
        ↓ aggregate
CognitiveBranchGovernanceResultV1
```

治理结果不是新的 Branch，也不复制 Hypothesis、Information Need、Gap 或
Current World 的 semantic ownership。

## Explicit governance inputs

`CognitiveBranchGovernanceInputV1` 只接受：

- parent problem 与 current source state refs；
- formed Branch Candidates；
- 当前 hypothesis / information need / information gap / conflict / governed alternative refs；
- currently satisfied need refs 与 explicitly currently-not-needed branch refs；
- context、trace 与 provenance refs。

它不包含 resource availability、budget、provider、model、execution order 或
priority 输入。资源可用性不属于 Branch Cognitive Governance。

## Decision semantics

`CognitiveBranchGovernanceDecisionV1` 至少保留：

- `branch_ref`；
- `governance_status`；
- `reason_code`；
- governance basis refs；
- candidate lineage 与 candidate provenance refs；
- parent/source state refs；
- trace/provenance；
- candidate retained / recoverable semantics。

受控 reason codes 包括：

- `VALID_CURRENT_BASIS`；
- `BASIS_NOT_CURRENT`；
- `CURRENTLY_NOT_NEEDED`；
- `INVALID_CANDIDATE`；
- `PROBLEM_REF_MISMATCH`；
- `SOURCE_STATE_NOT_CURRENT`。

`DEFERRED != REJECTED`，`ADMITTED != EXECUTING`。
多个有效 Branch 可以同时 `ADMITTED`；治理不执行 winner-take-all。
Need satisfaction alone does not suppress a Branch or make it rejected；只有当前
governed state 明确给出 `currently_not_needed_branch_refs`，且其关联 Need
确实已满足时，才允许产生 `DEFERRED`。
当前仓库没有 canonical equivalence/same-basis contract；因此没有语义 dedup
路径。缺少已证明的 equivalence 不等于已证明相同，候选必须保留为独立 Branch。

## Boundary

本 Contract 不实现：

- Resource Governance / Resource Need / Resource Merge；
- priority、rank、schedule、budget 或 execution order；
- merge、convergence、close、reopen、supersede；
- Observation Demand、Capability Requirement、Task、Action；
- Sufficiency、Stop 或 Decision Governance；
- Field / Current World / Hypothesis / Information Need mutation；
- Truth promotion、Provider / Model invocation 或 child runtime。
