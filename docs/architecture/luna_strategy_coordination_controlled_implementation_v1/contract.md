# Strategy Coordination Contract

## Canonical owner

Owner: `Cognitive Flow Strategy Coordination`。

Input 复用：

- `InformationAcquisitionStrategyCandidateV1`；
- `CognitiveBranchGovernanceDecisionV1`；
- strategy 的 Need / Gap / basis / dependency / lineage / provenance refs。

新增最小 contract：

- `GovernedStrategyCoordinationRelationV1`；
- `StrategyCoordinationInputV1`；
- `StrategyCoordinationDecisionV1`；
- `StrategyCoordinationResultV1`。

## Status semantics

每个 eligible strategy 只产生一个独立 decision：

- `ADMITTED`：进入后续认知 consideration；
- `DEFERRED`：合法但当前暂缓；
- `SUPPRESSED_REDUNDANT`：仅在显式 governed redundancy relation 下抑制重复表示；
- `BLOCKED_DEPENDENCY`：显式 dependency 未在当前 satisfied dependency refs 中；
- `INCOMPATIBLE`：显式 governed incompatibility，相关策略均保持未决，不选 winner。

空输入或没有来自 ADMITTED Branch 的策略返回 `NO_STRATEGY_CANDIDATES`；非法
输入 fail closed 为 `INVALID_INPUT`。

原始 strategy candidate 与 Branch Governance decision 均 immutable。协调结果是
candidate-only、read-only、non-Truth；不形成 execution plan，不赋 priority、
不排序、不调度、不获取资源。
