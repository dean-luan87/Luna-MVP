# Runtime Contract

`ProviderRuntimeRequestV1` is a bounded request carrying the selected
capability/provider, source, execution identity, modality, and trace/provenance
refs. It does not carry Luna's full cognitive state.

`ProviderRuntimeResultV1` is a candidate-only result with explicit status:
`SUCCESS`, `UNAVAILABLE`, `REJECTED`, or `ERROR`. A successful recorded result
is normalized by `provider_result_adapter_v1.py` into the existing
`RuntimeObservationEnvelopeV1`. The adapter rejects malformed results and does
not convert unavailable results into Evidence.

`provider_runtime_contract_verified=true` means the request/result/envelope
contract and downstream ingress path were exercised by recorded fixtures.
`provider_real_execution_verified=false` remains explicit until a later,
user-authorized provider runtime phase.

The later real-provider phase may set provider/model invocation flags on a
result only when its request is `LIVE_RUNTIME`. Recorded results must continue
to leave those flags false. `EMPTY_SUCCESS` is a valid executed result with no
detections and is distinct from `UNAVAILABLE` or `ERROR`.

`execution_mode=LIVE_RUNTIME` identifies the real-runtime ingress contract; it
does not assert that a provider, sensor, or camera was invoked by this
recorded-fixture Runner. `live_observation_execution=false` remains explicit.

The re-observation bridge is intentionally request-only: the existing Field
Perception Orchestrator next-cycle ingress is carried into a new
`ProviderRuntimeRequestV1` candidate, while no provider result, Gateway
admission, or second cognition execution is fabricated or invoked.
