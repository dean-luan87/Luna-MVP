# Governance Boundary

Allowed in this phase:

- controlled Situated-State transitions;
- candidate Need/Feasibility/Gap/Adjustment/Opportunity/Eligibility states;
- existing eligibility-gated real RapidOCR execution;
- downstream Observation, Evidence, A-Route, CState, and Sufficiency readout.

Forbidden:

- Camera, IMU, SLAM, movement, navigation, or device control;
- Decision, Task, Action, or Runtime Executor execution;
- Field mutation, Memory mutation, or World Truth declaration;
- background loops, sleep/polling, Provider fallback, or multi-provider
  orchestration.

Self describes Self state; Field/Target/Relation provide candidate situated
inputs; the existing Capability Preconditions owner evaluates capability
conditions. No new Brain or action owner is created.
