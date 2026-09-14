# Contract

## Bridge input

`GovernedObservationCapabilityRequirementMappingV1` 是显式的：

```text
Observation Demand → required capability class refs
```

V1 只允许恰好一个 capability class ref。Demand 不通过字符串、target 名称或
acquisition mode 推导 capability。

`ObservationDemandCapabilityRequirementAdapterV1` 只投影 requirement handoff，
并保留 Demand、Strategy、Branch、Need、Gap、problem、state、lineage 与 provenance。
它不是第二套 capability registry。

## Resolution

`GovernedCapabilityInventoryEntryV1` 是 controlled read-only inventory snapshot，
包含 capability candidate ref、class ref、availability、admission 与 eligibility。
解析规则为：

```text
required class == inventory class
AND availability == AVAILABLE
AND admission == ADMITTED
AND eligible == true
→ matched candidate
```

同一 Demand 的多个合法 inventory entries 全部输出。不同 Demand 即使请求同一
class 也分别输出，当前不做 Resource Merge。

## Result statuses

- `CAPABILITY_CANDIDATES_RESOLVED`
- `NO_CAPABILITY_REQUIREMENT`
- `NO_MATCHING_CAPABILITY`
- `CAPABILITY_UNAVAILABLE`
- `INVALID_INPUT`
- `UNSUPPORTED_REQUIREMENT_SHAPE`

所有输出 candidate-only、read-only、non-Truth；不携带 Provider/Model binding。
