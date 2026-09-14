# Branch Candidate Contract

## Canonical contract

`CognitiveBranchCandidateV1` 位于现有 Cognitive Flow ownership tree 中。
它通过 refs 关联既有 `CognitiveHypothesisCandidateV1`、Information Need、
Information Gap、Evidence 和 Conflict，不复制这些对象的语义 ownership。

每个 Branch Candidate 保留：

- `branch_ref`、parent cognitive problem ref、source state ref；
- formation basis 与 basis ref；
- hypothesis / need / gap / evidence / conflict refs；
- derived-from、lineage、trace 与 provenance refs；
- `formation_status=FORMED_CANDIDATE`；
- `candidate_only=true`、`read_only=true`、`truth_declared=false`。

Formation basis 只允许来自：

- `HYPOTHESIS_ALTERNATIVE`；
- `UNRESOLVED_INFORMATION_GAP`；
- `EXPLICIT_GOVERNED_ALTERNATIVE`。

空 basis 产生 `NO_EXPLICIT_BRANCH_BASIS`，不会强制 fan-out。

## Formation boundary

`form_governed_cognitive_branches(...)` 是 deterministic、read-only、
candidate-only 的形成函数。Branch identity 由 parent problem、basis kind 和
basis ref 稳定派生，不读取 `scenario_id`、`case_id`、goal/question 字符串，
也不执行 substring 或 fixture mapping。

它不拥有：

- branch admission / rejection / priority；
- resource proposal / merge / acquisition；
- observation、capability、task 或 action；
- Current World / Field / Memory / PCN mutation；
- Truth、Decision 或 autonomous child runtime。

`INVALID_INPUT` 仅表示 formation input contract invalid，不表示 Branch
Governance 的 rejection decision。
