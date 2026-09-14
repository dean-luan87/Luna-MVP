# Luna Midplatform SLAM Spatial Mapping Task Collaboration Planning v1

Planning only: how SLAM participates in 2–3 model task groups under midplatform control.

## Upstream

Requires Adapter Skeleton GO from `_tmp_eval_out/slam_spatial_mapping_adapter_skeleton_v1_smoke_v0/`.

## Fixed Order

```
Smoke IO Inspection → Adapter Skeleton → Task Collaboration Planning (this) → Tracking Smoke IO (next)
```

## Scope

- 4 task groups: field_construction, indoor_navigation_context, return_to_location_context, path_memory_context
- ModelInvocationControlPolicy (reuse, no new protocol)
- TaskEvidenceBundleCandidate pattern (planning structures only)

## Prohibited

No Task Reasoning execution, no actions, no navigation suggestions, no world model assembly.

## Next Phase

`Phase-Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-v1-001`
