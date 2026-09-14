# Declaration and Binding Contract v1

## Existing Registry locations

| Domain | Registry | New declaration |
|---|---|---|
| Model Governance | `capabilities/midplatform/model_manager/registries/model_registry_v1.json` | `model-asset:rf-detr-small:roboflow-v1` |
| Capability Governance | `capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json` | `capability-model-binding:object-detection:rf-detr-small:v1` |
| Provider Governance | `capabilities/midplatform/model_manager/registry/provider_registry_v1.json` | existing `provider:roboflow:vision:poc:v1` extended with governed workflow binding |
| Provider Governance | `capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json` | `model-provider-binding:rf-detr-small:roboflow:custom-workflow:v1` |
| Model Contract Repository | `capabilities/midplatform/model_manager/model_contract_repository/model_contract_repository_registry_v1.py` | external workflow loader and Roboflow adapter contract |

## RF-DETR model declaration

The model is declared as an external/provider-managed model asset:

- model id: `rf-detr-small`
- asset ref: `model-asset:rf-detr-small:roboflow-v1`
- model version: `workflow-declared-v1`
- weights version: `provider-managed-declared-v1`
- capability: `object_detection`
- loader: `loader:roboflow:workflow-api:v1`
- execution mode: `external_api`
- evidence role: candidate visual detection evidence producer
- cognition ownership: false
- truth admission ownership: false

No checksum is computed and no local model path is asserted. The declared
weights path is a provider-managed reference only.

## Provider/workflow declaration

The existing Roboflow Provider entry remains candidate/pending and retains
Provider Governance ownership. Its workflow binding now declares:

- workspace ref: `workspace:roboflow:lei-luan:v1`
- workflow id: `custom-workflow`
- workflow ref: `workflow:roboflow:lei-luan:custom-workflow:v1`
- endpoint class: `serverless_cloud_api`
- transport: `transport:inference_sdk:InferenceHTTPClient:v1`
- input mapping: `input:image:v1`
- detection output mapping: `detections → $[0].model_output_3.predictions`
- credential requirement: external `ROBOFLOW_API_KEY` configuration only

Workflow lifecycle remains Provider Governance. Observation and Capability
layers receive refs, not a workflow selector or hardcoded workflow identity.

## Binding separation

```text
Capability/Slot
  ≠ Model identity
  ≠ Provider identity
  ≠ Workflow/deployment binding
```

The Capability↔Model binding and Model↔Provider binding remain separate,
candidate-only, versioned, provenance-aware, and non-admitting. Neither binding
implies Runtime Admission, Provider Admission, model loading, or invocation.

## Transport drift resolution

The Roboflow Provider declaration previously named `urllib` while the existing
PoC client imported `inference_sdk.InferenceHTTPClient`. The declaration now
uses `dependency:inference-sdk` and the existing Model Contract Repository
contains `loader:roboflow:workflow-api:v1` plus
`adapter:roboflow:vision-evidence:v1`.

The observed Serverless response is a one-image sequence whose first item has
`model_output`, `model_output_2`, and `model_output_3`; only
`model_output_3.predictions` is governed as the detection output.

No dependency was installed. No API key is stored.
