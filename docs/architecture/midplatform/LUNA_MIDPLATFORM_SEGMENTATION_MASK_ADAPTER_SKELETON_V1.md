# Luna Midplatform — Segmentation / Mask Adapter Skeleton v1

## Scope

Adapter Skeleton only. Based on Segmentation / Mask Smoke IO Inspection artifacts. No real segmentation execution.

## Pipeline

```
build_segmentation_mask_adapter_input_package
→ load_segmentation_mask_raw_output_candidate
→ normalize_segmentation_mask_output_to_candidates
→ build_object_boundary_candidates
→ build_freespace_candidates
→ assemble_segmentation_mask_adapter_result
```

## Output Candidates

- MaskObservationCandidate
- ObjectBoundaryCandidate
- FreeSpaceCandidate
- RegionObservationCandidate
- MaskQualityCandidate
- SegmentationMaskAdapterResultCandidate

## Execution Modes

- cached_output / adapter_stub (not real run)
- blocked_by_missing_weight / blocked_by_missing_dependency (no fabrication)
- local_real_model classification only when real output ref exists

## Prohibited

- Real segmentation execution / model download / weight download
- World model assembly
- Task reasoning / action output / navigation suggestion
- Field simulation
