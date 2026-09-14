# Proposed Minimum Schema Set

This is a planning contract for the next phase. It is not an implementation
and does not create canonical types in this phase.

## 1. DatasetRegistryEntryV1

Required concepts:

- `dataset_id`, `dataset_version`, lifecycle;
- class: public benchmark, Luna scenario, or future real observation;
- modality/task/capability refs;
- source, license/consent, provenance, source-chain refs;
- split declarations and declared sample counts;
- annotation/ground-truth schema refs and quality/review status;
- `evaluation_only=true`, `runtime_allowed=false`;
- registry source version, trace/provenance, invalidation/supersession refs.

It references Capability Governance and Model/Provider registries; it does not
embed their declarations.

## 2. DatasetSampleManifestV1

Required concepts:

- `sample_id`, dataset ref/version, split;
- media/input refs using the existing asset-ref vocabulary;
- media type and optional frame/timestamp/ROI/sequence refs;
- source/provenance, hash/size/dimensions when available;
- annotation/ground-truth refs;
- scenario/case refs and privacy/consent state where applicable;
- candidate/evaluation-only and runtime-forbidden flags.

The future schema should reuse `input_asset_refs` and local asset manifest
semantics rather than define a second media reference object.

## 3. AnnotationGroundTruthRefV1

Required concepts:

- annotation/GT ID and version;
- sample ref, task/capability ref;
- format/schema ref and taxonomy/label-set ref;
- payload/file/ref location;
- completeness, quality, review, and human-correction provenance;
- source version, provenance, invalidation/supersession;
- explicit evaluation-GT scope; never World Truth or semantic closure.

Task-specific payloads should remain adapters (for example OCR text/boxes,
COCO-like boxes/masks, depth maps, trajectories), not be embedded into one
overloaded universal payload.

## 4. BenchmarkSpecV1

Required concepts:

- benchmark ID/version and dataset/split refs;
- task/capability and model/provider registry refs;
- required GT/annotation quality;
- metric definitions, aggregation, comparison baseline, and reproducibility;
- evaluation mode and resource assumptions;
- trace/provenance and TestBoard artifact refs;
- no runtime/mainline side effects.

Where possible this should extend the existing TestBoard/MUEP benchmark
surfaces rather than introduce a second metric result hierarchy.

## Reused references instead of new schemas

- Model Test Case Manifest for test-case identity and inputs.
- Model Test Result Envelope for candidate outputs and metrics.
- Model Test Trace for stage/attempt/execution flags.
- EvaluationReportV0 for evaluation reports.
- ModelBenchmarkRecordV1 for model-specific benchmark result records.
- TestBoard protected artifacts for durable evidence.
- Human Correction records for review provenance.

## Version and invalidation

There is no global dataset/model state version. Dataset version,
sample/annotation version, model version, capability/binding version, and
evaluation-run version remain separate and are linked by refs. A stale or
invalidated dataset, annotation, model, or binding must invalidate the
affected evaluation use; it must not be silently refreshed or treated as
current.
