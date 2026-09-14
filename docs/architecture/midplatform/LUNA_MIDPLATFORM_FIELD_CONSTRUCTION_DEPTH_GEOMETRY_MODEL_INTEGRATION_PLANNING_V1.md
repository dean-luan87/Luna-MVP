# Luna Midplatform Field Construction Depth / Geometry Model Integration Planning v1

## Route Correction

YOLO detector ingestion skeleton is GO. This phase shifts focus from detector to **field construction models**.

## Priority Tiers

| Tier | Focus | Status |
|------|-------|--------|
| P0 | Depth Model Adapter (Depth Anything V2, UniDepth) | Near-term |
| P1 | Field Geometry Adapter (pseudo_3d, field_zone) | Near-term |
| P2 | SLAM candidates (LingBot-Map, MASt3R-SLAM, ORB-SLAM3) | Future review |
| P3 | Scene Graph (Hydra, HOV-SG, ConceptGraphs) | Future review |

## Minimal Chain

```
YOLO bbox + Depth estimate → object_depth_hint → pseudo_3d_position → field_zone → FieldSceneCandidate
```

## Next Phase

`Phase-Midplatform-Depth-Observation-Candidate-Ingestion-Skeleton-v1-001`
