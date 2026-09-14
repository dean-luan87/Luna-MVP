# Runtime and Gateway relationship

Runtime Executor owns allocation realization, execution identity, session
lifecycle, and execution failure. This phase only consumes its preparation
candidate contracts. It does not call the Runtime Executor execution engine,
allocate a resource, reserve a slot, create an execution instance, or start a
provider session.

Observation Gateway remains downstream. Its
`ObservationGatewayRuntimeAdmissionV1` is an ingress/admission proof for an
already formed runtime observation envelope with observation, result/evidence,
provider, and execution identity references. It is not a pre-execution grant
and is not called here.
