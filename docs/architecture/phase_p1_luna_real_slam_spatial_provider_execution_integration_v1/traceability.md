# Traceability Assessment

## 未来 Route A 的最小 lineage

```text
Evidence
  → RuntimeObservation
  → ProviderRuntimeResult
  → ProviderRuntimeRequest
  → Provider / Model
  → Capability Requirement / Capability Resolution
  → Provider session / execution instance
  → sequence / frame / sensor source
```

SLAM 还必须额外保留 frame identity、timestamp、session identity、state reset/carryover
关系、map/trajectory reference、tracking state 和 provider provenance（实际提供时）。

## 当前证据边界

当前可追踪的只有 registry declaration、schema、fixture、sample、file source 和
controlled adapter lineage。它们不能形成真实的 Provider Request → native invocation
→ Provider Result lineage。

以下 synthetic/recorded refs 不得被升级成当前真实 identity：

- `provider:slam:runtime-result`；
- `capability:slam-spatial-mapping`；
- `provider-output:slam:exit-geometry`；
- `provider-runtime:slam-001`。

它们来自 fixture，不是 canonical live binding。未来真实接入必须重新产生并验证
`capability_requirement_ref`、`capability_ref`、`provider_ref`、`model_ref`、
`provider_request_ref`、`provider_result_ref`、`execution_instance_ref`、
`runtime_observation_ref` 和 `evidence_ref`。
