# Dynamic relative observation state

`RelativeObservationStateV1` records a candidate relation at one temporal
point: `Self ↔ Target ↔ Field ↔ Observation Requirement`. It contains target
visibility, completeness, scale, relative orientation, relative motion,
stability, and occlusion candidates plus source/provenance references.

The same target, field, and requirement can have different relative states at
`t0` and `t1`. A state change can therefore change feasibility without changing
the physical evidence contract or inventing spatial truth. The phase uses
controlled states only; it does not implement tracking, camera capture, IMU,
SLAM, or exact geometry.

