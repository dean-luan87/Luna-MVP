# Assessment and Executable Candidate boundary

The source fails closed before assessment if a required record is missing,
owned by the wrong boundary, stale/superseded, mismatched, invalidated, or
missing provenance/version lineage.

Only `READY_FOR_EXECUTABLE_CANDIDATE` permits construction of
`ExecutableCapabilityCandidateV1`. A valid Capability↔Model or
Model↔Provider binding alone never creates an executable candidate.

The emitted assessment and executable candidate remain candidate-only. Their
execution flags are false. Runtime Admission does not perform Provider
Admission or invocation.
