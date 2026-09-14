# Runtime Path Assessment

## 目标 canonical path

若未来 Route A 成立，应复用
`capabilities/midplatform/core/provider_runtime_to_observation_ingress/`：

```text
Spatial Observation Demand
  → spatial_mapping Capability Requirement
  → Capability / Provider Resolution
  → canonical identity
  → ProviderRuntimeRequestV1
  → Runtime Admission / LIVE_RUNTIME
  → real SLAM sequence/session invocation
  → native pose/map/trajectory result
  → SLAM adapter / normalizer
  → ProviderRuntimeResultV1
  → RuntimeObservationEnvelopeV1
  → Observation Gateway
  → Spatial Evidence Candidate
  → A-Route / CState
  → Sufficiency / Information Gap / Stop
```

当前仓库只具备其中的 capability mapping、shared contracts、Gateway modality 和
recorded fixture path。`provider_runtime_to_observation_ingress/fixtures_v1.py`
中的 `SLAM_PROVIDER_RESULT_TO_COGNITION` 是 recorded provider-result bridge；它不
调用 SLAM Provider。`observation_runtime_ingress/fixtures_v1.py` 中的
`REAL_RUNTIME_SLAM_REFERENCE` 也是 Gateway reference fixture，不能作为 real
execution evidence。

## 当前缺失

- real SLAM/VIO native invocation function；
- ProviderRuntime entrypoint；
- local backend dependency / binary / package；
- camera calibration and sequence/session input;
- real video, RGB-D, stereo or RGB+IMU source;
- provider session start/reset/carryover ownership;
- native tracking state and partial-result emission path;
- SLAM-specific adapter from native output into shared Runtime Result。

因此本阶段不生成 `ProviderRuntimeRequest` 的 live execution 实例，不生成真实
`ProviderRuntimeResult`、RuntimeObservation、Gateway admission 或 Spatial Evidence。
