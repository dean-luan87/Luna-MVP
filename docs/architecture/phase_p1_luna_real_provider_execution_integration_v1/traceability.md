# Traceability

The terminal result must resolve:

`observation_demand_ref → capability_requirement_ref → capability_ref →`
`provider_request_ref → provider_ref/model_ref → provider_result_ref →`
`runtime_observation_ref → gateway_admission_ref → evidence_refs →`
`a_route_execution_ref → sufficiency_ref or information_gap_ref/stop_ref`.

Provider and model invocation flags are execution facts. Provenance and trace
references from the request are retained in the provider result and runtime
observation. No unavailable reference is synthesized.

Each Runner invocation creates a new execution-instance reference; the
provider request/result and downstream observation identities carry that same
execution identity.

Vision detection boxes remain traceable to the provider frame and retain the
provider's original-image pixel coordinate space. For the current local input,
the source image is 5712x4284; raw-frame metadata and provider detection
`frame_dimensions` therefore use 5712x4284 rather than 640x480.
