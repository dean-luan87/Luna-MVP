# Luna Midplatform SLAM Spatial Mapping Adapter Skeleton v1 (Revision)

Adapter skeleton based on Smoke IO Inspection results. Not Field Simulation. No world model assembly.

## Upstream

Requires `Phase-Midplatform-SLAM-Spatial-Mapping-Model-Adapter-Smoke-IO-Inspection-v1-001` Verifier=GO.

## Fixed Onboarding Order

1. Model Smoke + IO Inspection
2. **Adapter Skeleton (this phase)**
3. Task Collaboration Planning
4. World model assembly (deferred)

## Scope

- Load raw output from inspection-confirmed smoke runs
- Normalize to CameraPose / Trajectory / Anchor / LocalMap / MapQuality candidates
- Declare task collaboration mapping and later world model readiness only

## Prohibited

No real SLAM, no WorldModelCandidate assembly, no WorldModelEntry, no Fact Admission, no Task Reasoning.

## Next Phase

`Phase-Midplatform-SLAM-Spatial-Mapping-Task-Collaboration-Planning-v1-001`
