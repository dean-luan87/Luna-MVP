# Evidence Gateway Validation Model v1

## Required path

```text
Provider Output
    ↓
Evidence Candidate
    ↓
Evidence Validation
    ↓
Reality Cognition
```

Provider output never enters A Route or Brain directly.

## Evidence Candidate contract

Every candidate carries `request_id`, `capability_reference`, `provider_reference`,
`source`, `raw_output_reference`, `text_candidates`, `region_candidates`,
`confidence`, `uncertainty`, `provenance`, `timestamp`, and `trace_reference`.

Validation checks schema completeness, provenance, timestamp, capability reference,
confidence range, uncertainty declaration, and limitation compatibility. Invalid
or incomplete evidence remains a candidate and is routed to Diagnostics; it does
not become Reality.

## Governance boundary

The gateway validates and routes evidence. It does not interpret Reality, make a
Decision, change Self, or execute a Provider. Reality Cognition remains the sole
consumer that may form a Reality Candidate from admitted evidence.
