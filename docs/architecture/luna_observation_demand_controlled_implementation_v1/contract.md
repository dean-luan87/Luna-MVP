# Cognitive Observation Demand Contract

Owner: `Cognitive Flow Observation Demand Formation`。

## Input

`ObservationDemandFormationInputV1` 消费：

- `StrategyCoordinationResultV1`；
- 与 result 对齐的 immutable `InformationAcquisitionStrategyCandidateV1`；
- 显式 `GovernedObservationDemandMappingV1`。

Mapping 是受治理的 strategy → observation target 关系。Formation 不从 goal、
question、need 或 ref 字符串解析 target；缺少 mapping 时 fail closed。

## Output

`ObservationDemandCandidateV1` 保留：

- parent problem、source state、strategy、branch、Need、Gap；
- acquisition basis 与 expected information contribution；
- explicit observation class、target、constraint、context；
- lineage、provenance、trace。

当前只支持显式可映射的 `PERCEPTION` acquisition mode/class。其它 mode 返回
`UNSUPPORTED_ACQUISITION_MODE`，不猜测 Retrieval、Interaction 或 OCR 的执行方式。

## Formation semantics

```text
ADMITTED Strategy + explicit governed mapping
  → one Observation Demand Candidate

0 admitted strategies
  → NO_OBSERVATION_DEMAND
```

DEFERRED、SUPPRESSED_REDUNDANT、BLOCKED_DEPENDENCY、INCOMPATIBLE 均不会形成
active demand。独立 admitted strategies 不合并、不排序、不选 winner。

Demand 的 `candidate_only`、`read_only` 为 true，`truth_declared` 与
`world_truth_declared` 为 false；所有执行、Capability、Provider、Model、OCR、
Camera、SLAM、Attention、Decision、Task、Action flags 均为 false。
