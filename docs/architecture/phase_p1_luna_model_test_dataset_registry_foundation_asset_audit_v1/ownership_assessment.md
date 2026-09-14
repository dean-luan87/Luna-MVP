# Ownership Assessment

## Decision

Dataset declaration, sample provenance, annotation/ground-truth quality, and
benchmark membership are evaluation-domain concerns. They are not model
identity, capability identity, provider identity, runtime admission, or
world-state authority.

The recommended owner is the existing **Model Test / Evaluation subsystem**,
under `capabilities/evaluation/`, with an explicit evaluation-only dataset
registry boundary. Model Test Lens consumes the registry; it does not own it.

This is a bounded extension of an existing owner, not a new top-level Luna
owner and not a new Manager.

## Why not Model Manager?

Model Manager owns model assets, model lifecycle, capability contracts, and
model/provider declarations. Its `ModelBenchmarkRecordV1` and evaluation
profiles describe model evaluation results, not the provenance, split,
annotation, licensing, and sample lifecycle of datasets. A dataset registry
inside Model Manager would conflate what is evaluated with the model being
evaluated.

## Why not an independent Dataset Governance subsystem?

The repository already has an offline evaluation boundary with dataset
manifests, ground truth, reports, failure bundles, human review, and TestBoard
evidence. A new top-level owner would duplicate that boundary. The next phase
should add a narrow `capabilities/evaluation/dataset_registry/` surface and
keep it evaluation-only.

## Authority boundaries

| Domain | Owner | Dataset Registry relationship |
|---|---|---|
| Model identity/version | Model Governance | Reference `model_registry_v1.json`; never duplicate model declarations. |
| Capability/slot identity | Capability Governance | Reference capability and slot IDs/contracts. |
| Provider identity/binding | Provider Governance | Reference provider/model-binding records for evaluation provenance. |
| Dataset/sample/annotation declaration | Evaluation Governance | Own the future registry entries and their validation lifecycle. |
| Evaluation run/result evidence | Evaluation Tools/TestBoard | Consume dataset refs; persist protected run evidence. |
| Human correction | Human Correction Layer | Produce review/correction candidates; no automatic GT promotion. |
| Current World/Field/Truth | Canonical source owners | Never owned or mutated by Dataset Registry. |

## Direct answers

1. No canonical generic Dataset Registry exists.
2. No canonical generic Benchmark Registry exists; benchmark result and OCR
   provider registries are narrower.
3. A reusable test-case schema exists in Model Test Lens, but it needs a
   bounded dataset/sample reference extension.
4. Ground truth exists for OCR and several dry-run formats, but no generic
   multimodal representation exists.
5. Media references are fragmented but reusable through `input_asset_refs`,
   local asset manifests, and image/video/frame/timestamp fields.
6. Dataset Registry should reuse source/version refs, provenance, hashes,
   annotation versions, license/source-chain records, trace refs, and
   TestBoard protected-artifact refs.
7. It must reference Model Registry, Capability Registry, Provider Registry,
   Model Contract Repository, and existing binding records.
8. Model Test Lens should consume dataset/sample/annotation refs and emit
   result/trace envelopes; it should not become dataset authority.
9. Human Correction should remain review evidence/correction candidates and
   require explicit review before a version is accepted as evaluation GT.

## Conflicts to preserve as gaps

- OCR registry vocabulary is domain-specific and cannot be promoted unchanged.
- Model Test Lens case manifests support `detection_tracking`, while MUEP
  input vocabulary does not explicitly include object detection.
- `RawFrameReferenceV1` is referenced by contracts but was not found as a
  complete canonical class in the audited scope.
- Historical Roboflow documentation predates the current RF-DETR declarations.
