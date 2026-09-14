# Dataset Registry Relationship

## Inherited ownership

The Dataset Registry remains an evaluation-boundary concern under:

`capabilities/evaluation/dataset_registry/`

It is not implemented in this phase and does not belong to Model Manager.

## Sufficiency of prior proposal

The four proposed declarations remain sufficient as the foundation:

- `DatasetRegistryEntryV1`;
- `DatasetSampleManifestV1`;
- `AnnotationGroundTruthRefV1`;
- `BenchmarkSpecV1`.

The Evaluation Strategy adds required references, not a parallel registry:

- task/condition/data-distribution refs;
- expected observation requirement;
- cognitive-difficulty/strategy refs;
- annotation quality and GT applicability;
- Model Test Case and Execution Profile refs;
- TestBoard protected artifact refs.

These are revision recommendations for the next implementation phase, not
schema changes now.

## Boundary

Dataset entries describe inputs and evaluation validity. They do not declare
model fit, modify runtime bindings, create Evidence, or enter World Truth.
