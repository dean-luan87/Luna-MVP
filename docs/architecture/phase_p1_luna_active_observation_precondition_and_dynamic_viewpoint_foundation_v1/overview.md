# Phase-P1 Luna Active Observation Precondition and Dynamic Viewpoint Foundation v1

Status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

This phase adds the controlled, candidate-only precondition layer between an
Observation Demand and Observation Capability eligibility:

`Observation Necessity → Minimum Conditions → Self Viewpoint State → Relative Observation State → Feasibility → Observation Window → Capability Eligibility`

It does not invoke OCR or any other provider. It does not implement camera,
IMU, SLAM, geometry, movement, navigation, Decision, Task, or Action.

The implementation reuses the existing Field Perception Orchestrator / Active
Observation Control owner and the existing Self State Awareness boundary.
Controlled dynamic states demonstrate that the same requirement can open or
close an observation window as the relative state changes. They are not a
`REAL_DYNAMIC_VIEWPOINT_VERIFIED` claim.

