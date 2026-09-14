# Dataset and Ground-Truth Audit

## Dataset Registry

Canonical location: `capabilities/evaluation/dataset_registry/`.

`DatasetRegistryV1`, `DatasetRegistryEntryV1`, `DatasetSampleManifestV1`, `AnnotationGroundTruthRefV1`, and `BenchmarkSpecV1` are reusable canonical evaluation contracts. The registry owner is `Evaluation Governance`; records are `evaluation_only=True` and `runtime_allowed=False`.

`register_explicit_dataset_v1` is the relevant registration boundary. It requires explicit registration, rejects directory scanning and generated evaluation roots, and never loads media. This is suitable as the future ingress boundary. It is not evidence that a real dataset has been registered: `registry_declaration_v1.json` contains no entries, samples, annotations, or benchmarks.

## Supported metadata

The existing types cover dataset/sample identity and version, media references/type, source/provenance, source versions, content hash, license, annotation refs, environment/distribution/cognitive difficulty, expected observation refs, case refs, lifecycle, invalidation/supersession, and evaluation usage. They do not establish an integrated real-ingestion archive or file verification workflow.

## Ground-truth layers

The repository contains enough named/reference structure to preserve three layers, but not a complete real-world admission path:

1. World Ground Truth: objective scene/object/environment facts through annotation/GT references.
2. Observation Ground Truth: what is visible, occluded, outside ROI, ambiguous, or unavailable from a particular view; represented by Level-1 references and planned metadata rather than a demonstrated integrated runtime contract.
3. Cognitive Evaluation Assertions: `CognitiveEvaluationAssertionV1` and canonical assertion kinds in `level1_field_cognition_suite/types_v1.py`.

`AnnotationGroundTruthRefV1` explicitly carries `evaluation_ground_truth_only=True` and `world_truth=False`. Human correction assets (`ocr_manager_human_correction_adapter_v1.py` and OCR review packages) are candidate correction/review signals and explicitly do not authorize automatic fact or GT promotion.

## Generated inputs and outputs

`_tmp_eval_inputs`, `_tmp_eval_out`, `_eval_out`, Roboflow smoke summaries, Model Test Lens jobs, and TestBoard references are generated or execution evidence. They must remain evidence/input artifacts unless an explicit owner-controlled registration operation creates a Dataset Registry entry. The Roboflow RF-DETR summary is useful precedent for provider/evidence lineage, not a corpus source-of-truth.

## Readiness

Real dataset registration: `PARTIAL`. The explicit API and schema exist, but zero real datasets/samples are registered and no integrated GT admission/archive is present.

