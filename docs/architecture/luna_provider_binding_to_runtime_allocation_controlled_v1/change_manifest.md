# Change manifest

## Added

- Provider-only `ProviderBindingCandidateV1` contract。
- Runtime Executor-owned allocation and execution-instance preparation candidates。
- Controlled fixtures, engine, runner and verifier。
- 本阶段架构与责任文档。

## Modified

- Provider Binding Candidate input 增加显式 runtime/resource/execution requirement refs 的 carry-forward。
- Provider Binding validation 补充 target/contribution completeness。

## Reused

- Provider Governance owner 与既有 Provider Runtime Target Preparation。
- Runtime Executor owner、FPO、Observation Gateway、旧 Model+Provider contract 作为兼容性边界证据。
- Governance Rule Registry、Profile、Applicable Rule Resolver、Preflight/Postflight、Unified Final Decision。

## Not Modified

真实 Provider/Model runtime、FPO runtime、Observation Gateway、Model Manager、Provider Registry、Capability Registry、Scenario 12。

## Deferred

Binding Decision、Model Binding、Runtime Allocation、Execution Instance creation、Provider Session、Gateway admission/submission、resource/slot reservation、provider/model invocation、Observation Execution、Evidence Ingress/Fusion。
