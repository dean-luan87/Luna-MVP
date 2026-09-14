# Luna Midplatform Tracking / Optical Flow Model Smoke IO Inspection v1

P1 model smoke + IO inspection. No adapter skeleton. No world model assembly.

## Upstream

Requires SLAM Task Collaboration Planning GO.

## Fixed Order

```
Model Smoke + IO Inspection (this) → Adapter Skeleton → Task Collaboration → World Model (deferred)
```

## Scope

- Tracking: track_id, bbox sequence, object continuity
- Optical Flow: motion vector, flow map summary
- Mapping feasibility: ObjectTrackCandidate, ObjectPersistenceCandidate, MotionCandidate

## Next Phase

`Phase-Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-v1-001`
