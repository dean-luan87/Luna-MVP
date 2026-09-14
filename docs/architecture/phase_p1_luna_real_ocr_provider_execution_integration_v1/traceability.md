# Traceability

The execution identity is carried through:

`observation_demand_ref → capability_requirement_ref → provider_request_ref
→ provider_result_ref → execution_instance_ref → runtime_observation_ref
→ gateway_admission_ref → evidence_refs → a_route_execution_ref
→ sufficiency_ref / information_gap_ref / stop_ref`.

The request preserves the canonical capability requirement identity. The
normalized provider-runtime requirement identity is diagnostic-only and is not
substituted into the canonical admission field. Registry, adapter, source,
provider trace, and native runtime references remain in provenance/trace lists.

The Runner summary records both canonical and native identities plus the full
native candidate payload. The Verifier checks request/result identity,
provenance retention, Gateway admission, OCR candidate-only semantics, and the
absence of downstream execution.
