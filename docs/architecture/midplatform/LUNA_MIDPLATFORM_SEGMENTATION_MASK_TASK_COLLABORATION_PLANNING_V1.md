# Luna Midplatform — Segmentation / Mask Task Collaboration Planning v1

## Scope

Task collaboration planning only. Based on Segmentation / Mask Adapter Skeleton artifacts.

## Model Groups

1. navigation_passability — YOLO + Depth/Geometry + Segmentation/Mask
2. obstacle_avoidance_context — YOLO + Depth/Geometry + Segmentation/Mask
3. door_area_detection — YOLO + Segmentation/Mask + Depth optional
4. object_interaction_boundary — YOLO + Segmentation/Mask + Depth optional

## Segmentation Responsibilities

- MaskObservationCandidate — mask observation evidence
- ObjectBoundaryCandidate — object boundary evidence
- FreeSpaceCandidate — passable region evidence (not navigation permission)
- RegionObservationCandidate — semantic region evidence
- MaskQualityCandidate — quality / degradation signals

## Prohibited

- Task Reasoning execution
- Action / navigation output
- World model assembly
- Field simulation
- Real segmentation execution
