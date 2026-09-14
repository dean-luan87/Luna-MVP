# Luna Midplatform — Field Continuity Detection Planning v1

## Phase

`Phase-Midplatform-Field-Continuity-Detection-Planning-v1-001`

## Core Question

当前场与上一时刻的场：同一个场、偏移后的同一场，还是新场？

## Pipeline

`FieldSceneCandidate(t-1)` + `FieldSceneCandidate(t)` → `FieldContinuityDecisionCandidate`

## Boundaries

Planning only — no tracking, no video inference, no runtime, candidate-only outputs.

## Next Phase

`Phase-Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001`
