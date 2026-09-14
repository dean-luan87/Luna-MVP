# Ownership and authority

| Concern | Existing owner / boundary |
|---|---|
| Provider identity and registry view | Model Manager Provider Registry / Provider Governance boundary |
| Provider lifecycle, admission and health governance | Provider Runtime Governance |
| Capability inventory and slot lifecycle | Universal Capability Slot / Capability Governance |
| Provider binding | Provider Governance |
| Model binding and model asset declarations | Model Governance / Model Manager binding contracts |
| Execution instance and runtime observation identity | Runtime Observation / Observation Gateway runtime boundary |
| Provider session / invocation | Provider runtime ingress or concrete runtime owner |
| Active-observation semantic authorization | FPO / Active Observation Control |

FPO does not select a Provider. Observation Gateway validates runtime ingress and produces runtime admission proof only after an existing runtime observation envelope is available; it does not make this preparation candidate into a runtime request. The existing provider registry loader and provider governance skeleton are reused as ownership evidence, but their selection/scoring paths are not called by this phase.

`ProviderRuntimeTargetPreparationCandidateV1` is therefore a new contract in the existing Provider Governance namespace, not a new owner. It consumes explicit controlled mapping entries and never creates `execution_instance_ref`.
