# SOP v1 Compatibility Assessment

## 共享部分可复用性

SOP v1 的 candidate-only、canonical identity、ProviderRuntime、RuntimeObservation、
Observation Gateway、trace/provenance 和下游 ownership boundary 对 Spatial Provider
仍然适用。现有 Gateway 已支持 `SLAM_SPATIAL` / `slam_spatial_evidence`，shared
Runtime contracts 也有 `spatial_refs`。

## 尚未验证的 SLAM 生命周期

本阶段没有真实 backend，因此没有把下列事项宣称为已验证的 SOP gap；它们是未来
Route A 必须观察的 compatibility probes：

- persistent provider lifecycle；
- continuous observation；
- multi-frame / video / RGB-D / stereo input；
- temporal state 与 pose sequence；
- accumulated map state；
- provider session identity、reset 和 state carryover；
- partial result emission；
- `INITIALIZING`、`TRACKING`、`TRACKING_LOST`、`NO_MAP`、`NO_POSE` 等 native state。

## 当前判断

SOP v1.0 足以规定“真实输出必须经过统一 Runtime → Observation → Gateway →
Evidence 边界”，但当前有限的 `request → provider invocation → finite result`
验证来源不足以证明它能直接承载 persistent/continuous SLAM lifecycle。

这被记录为 **SOP_GAP_CANDIDATE / PENDING REAL VALIDATION**，不是 v1.1 已建立的
contract，也不触发当前 SOP 版本升级。只有真实 SLAM 接入暴露不可表达的需求时，
才按 canonical SOP Change History 提升版本。
