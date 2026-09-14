# Perception Routing to Runtime Admission — Order Adjudication v1

Status: `ARCHITECTURE_ORDER_ADJUDICATED` / waiting for user terminal verification.

Repository reconnaissance found that the existing Observation Gateway runtime
admission proof is created only on the runtime ingress path. The current
candidate-only FPO compatibility object cannot be converted into that proof
without provider/runtime-observation data. This phase therefore records Route
B: Provider/Model Governance and runtime-target preparation precede Gateway
runtime admission.

This phase does not implement runtime admission, a new admission owner, a
Gateway adapter, Provider/Model binding, or observation execution.

