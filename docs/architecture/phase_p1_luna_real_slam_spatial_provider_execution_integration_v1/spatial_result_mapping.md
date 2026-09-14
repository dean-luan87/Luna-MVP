# Spatial Result Mapping Assessment

## 已有 candidate mapping 能力

现有 adapter / normalizer 资产已经能描述下列候选类型：

- `camera_pose_candidate`；
- `camera_trajectory_candidate`；
- `spatial_anchor_candidate`；
- `local_map_candidate`；
- `map_quality_candidate`；
- motion、health、drift、relocalization candidate。

`slam_spatial_mapping_adapter_core_v1.py`、`spatial_mapping_output_normalizer_v1.py`
和 `slam_spatial_evidence_adapter/` 可以对 smoke/cached/file payload 做候选形状
转换，但不能证明 native SLAM 输出真实产生。其 output 必须继续保持：

```text
native pose/map/trajectory/health
  → spatial candidate payload
  → ProviderRuntimeResultV1
  → RuntimeObservationEnvelopeV1
  → Gateway spatial evidence
```

## 不可补造

真实 Provider 未提供时，不得补造 pose、rotation、translation、scale、covariance、
map point、keyframe、tracking confidence、loop closure 或 traversability。
尤其不能在 tracking lost 时把最后一个 pose 重复标记为当前 pose。

## 当前阻断

因为没有真实 native result，本阶段不存在可填写的 `provider_result_ref`、
`execution_instance_ref`、`runtime_observation_ref` 或 `evidence_ref`。已有 sample
字段只可作为 schema/reference 使用。
