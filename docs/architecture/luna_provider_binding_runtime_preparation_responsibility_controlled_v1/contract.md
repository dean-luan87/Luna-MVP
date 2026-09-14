# Candidate contract

Canonical module：`capabilities/midplatform/provider_runtime_governance/provider_binding_runtime_preparation_v1.py`。

输入为 `ProviderRuntimeTargetPreparationCandidateV1` collection。输出为一对一的 `ProviderBindingRuntimePreparationCandidateV1` collection。

每个 output 保留：

- source Provider Target、FPO Compatibility、Routing、Demand、Capability Resolution refs；
- provider candidate/class 与 optional `source_model_ref`；
- observation target、constraints、expected contribution；
- cognitive lineage、context、provenance、trace。

Formation 只验证 upstream target 完整、candidate-only、read-only、non-truth、source state/problem/lineage coherent，然后 deterministic projection。不会重新 resolve capability、选择 Provider、推断 Model、修改 Demand 或生成新的 target。

所有 output 明确保持 `provider_bound=false`、`runtime_allocated=false`、`execution_instance_created=false`、`provider_session_started=false`、`gateway_submission=false`、`runtime_observation_created=false` 等边界标记。
