# Information Acquisition Strategy Candidate Contract

## Owner

Formation owner 是现有 Cognitive Flow 内的 Information Acquisition Strategy
Candidate Formation。它只读取 `CognitiveBranchCandidateV1`、
`CognitiveBranchGovernanceDecisionV1`、`CognitiveNeedCandidateV1` 与显式
`GovernedAcquisitionBasisV1`，不取得这些对象的 mutation authority。

## Governed basis

`GovernedAcquisitionBasisV1` 是上游已明确声明的结构化 basis，不是 Strategy
本身。它可以携带：

- branch、Information Need / Gap refs；
- expected information contribution refs；
- explicit `acquisition_mode_candidate`；
- capability class refs、opportunity refs、dependency refs；
- provenance 与 candidate-only boundary。

mode 只保留已声明且受控的值：`PERCEPTION`、`RETRIEVAL`、`INTERACTION`、
`HYPOTHETICAL_REASONING`、`OTHER_GOVERNED`。缺失或不受支持的值归一为
`UNKNOWN`，不会通过字符串推测 mode。

## Strategy candidate

`InformationAcquisitionStrategyCandidateV1` 保留：

- strategy / branch / parent problem / source state refs；
- Information Need、Gap、basis、lineage、provenance、trace refs；
- expected information contribution refs；
- explicit acquisition mode；
- capability class、opportunity、dependency refs；
- `formation_status=FORMED_CANDIDATE`；
- `candidate_only=true`、`read_only=true`、`truth_declared=false`、
  `world_truth_declared=false`。

candidate identity 由 formation、branch、basis 与 source state 的稳定组合派生。
同一 admitted Branch / Need 的多个 distinct governed bases 可形成多个 candidates，
不执行 winner-take-all、priority 或 dedup。

## Formation input/result

`InformationAcquisitionStrategyFormationInputV1` 使用明确 collection：
`branch_candidates`、`governance_decisions`、`need_candidates` 与
`governed_acquisition_bases`。只有治理 status 为 `ADMITTED` 的 Branch 接受
basis 投影；`DEFERRED` / `REJECTED` Branch 的 basis 被排除但原 Candidate 保留。

`InformationAcquisitionStrategyFormationResultV1` 输出 strategy collection、
admitted/excluded branch refs、excluded basis refs、validation errors 与完整
非执行 markers。formation status 仅为 `FORMED_CANDIDATES`、
`NO_GOVERNED_ACQUISITION_BASIS`、`NO_ADMITTED_BRANCH` 或 `INVALID_INPUT`。

## Boundary

本阶段不形成 Strategy Governance lifecycle，不形成 Resource、Attention、
Observation Demand 或 Capability Requirement，不调用 Provider / Model，不写
Current World / Field / Memory / PCN，不产生 Truth、Decision、Task 或 Action。
`HYPOTHETICAL_REASONING` 仅是可携带的受治理 mode candidate；它不向 A-Route
Current World 写入结果。
