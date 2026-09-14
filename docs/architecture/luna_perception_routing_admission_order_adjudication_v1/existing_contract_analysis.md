# Existing Contract Analysis

`ObservationGatewayRuntimeAdmissionV1` is a Gateway-owned admission proof,
not a candidate-only projection. Its required identity includes:

- gateway admission reference;
- runtime observation reference;
- execution instance reference;
- observation reference;
- evidence references;
- provenance and Gateway trace.

The existing `ObservationGatewayEngineV1` constructs this proof only when the
request uses `LIVE_RUNTIME` and supplies a valid
`RuntimeObservationEnvelopeV1`. The envelope requires concrete provider and
capability/runtime observation data. The engine does not select a provider or
model, but it is not a pure candidate-only admission API for the current
cognitive handoff.

`ObservationIngressRequestV1` is a runtime ingress contract and includes
provider/source/payload/runtime fields. It is not a legal direct target for a
candidate-only FPO compatibility object.

Therefore the current order is blocked before Runtime Admission. No Gateway
or FPO runtime call is made by this phase.

