# Luna Midplatform — Tracking / Optical Flow Adapter Skeleton v1

## Scope

Adapter Skeleton only. Based on Smoke IO Inspection artifacts. No real tracker/flow execution.

## Pipeline

```
build_tracking_opticalflow_adapter_input_package
→ load_tracking_opticalflow_raw_output_candidate
→ normalize_tracking_opticalflow_output_to_candidates
→ build_object_persistence_candidates
→ build_motion_candidates
→ assemble_tracking_opticalflow_adapter_result
```

## Output Candidates

- ObjectTrackCandidate
- ObjectPersistenceCandidate
- MotionCandidate
- TrackingQualityCandidate
- TrackingOpticalFlowAdapterResultCandidate

## Prohibited

- Real tracker / optical flow execution
- World model assembly
- Task reasoning / action output
- Field simulation
