# Phase P1 — Luna Roboflow RF-DETR Provider Declaration and Evidence Seam

本阶段只实现第一条 Roboflow external perception provider 的受治理声明、
binding、synthetic normalization 与 Observation/Gateway handoff candidate。

## 范围

```text
object_detection
  → rf-detr-small
  → Roboflow / lei-luan / custom-workflow
  → response[0].model_output_3.predictions
  → provider-native result (synthetic only)
  → VisualDetectionEvidenceCandidateV1
  → ObservationGatewayEvidenceHandoffCandidateV1
```

本阶段不执行 `InferenceHTTPClient.run_workflow`，不加载模型、不调用网络、
不执行 Observation/Action、不写 Current World/Field authoritative state。

## Canonical owners

- Capability/Slot：Capability Governance
- `object_detection ↔ rf-detr-small` binding lifecycle：Capability Governance
- Model identity/declaration：Model Governance
- Roboflow identity/workflow/provider binding：Provider Governance
- Provider request/normalization translation：Roboflow integration adapter
- Evidence semantics/admission：既有 Luna Evidence/Gateway boundary

## Subsequent real RF-DETR smoke record

The implementation phase itself did not invoke the SDK. A subsequent,
user-executed one-image smoke reached the governed normalization and handoff
boundaries with:

- provider: `provider:roboflow:vision:poc:v1`
- workflow: `workflow:roboflow:lei-luan:custom-workflow:v1`
- model: `model-asset:rf-detr-small:roboflow-v1`
- extraction: `$[0].model_output_3.predictions`
- observed detections: `15` for this test image only
- real normalization: pass
- Observation Gateway handoff: candidate-only, admission false
- Luna cognitive outputs: Current World Candidate, Hypothesis Candidate, and
  Sufficiency Candidate (`SUFFICIENT`)
- next target: `Decision Governance`; this adapter did not create a Decision

The count `15` is an observation result, not a fixed model-output contract.
The smoke remained candidate-only: no World Truth, Field mutation, Task, or
Action was produced.

## 结果

复用既有 `VisualDetectionEvidenceCandidateV1`、
`ObservationGatewayEvidenceHandoffCandidateV1`、
`ProviderAdapterContractV1` 与现有 Roboflow PoC request/result 类型；没有创建
新的 Provider、Model、Capability 或 Evidence hierarchy。

## 文档

- [declaration_binding_contract_v1.md](declaration_binding_contract_v1.md)
- [normalization_evidence_boundary_v1.md](normalization_evidence_boundary_v1.md)
- [synthetic_fixture_and_verification_v1.md](synthetic_fixture_and_verification_v1.md)
- [change_manifest.md](change_manifest.md)
