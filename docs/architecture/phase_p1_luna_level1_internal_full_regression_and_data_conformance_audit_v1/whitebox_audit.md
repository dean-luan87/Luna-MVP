# White-box Audit

The audit reuses and inspects `CognitiveWhiteBoxTraceV1`,
`LunaCognitiveExecutionProfileV1`, and `CognitiveFailureGapRefV1` payloads.

It checks trace/profile/run/case linkage, unique node IDs, transition refs,
cycle representation, revision and loop node visibility, owner fields,
candidate-only/non-authoritative flags, and explicit unavailable metrics.
Profile values marked unavailable, not observed, or planned must not carry a
fabricated numeric value. Trace/Profile data is observational and must not
claim cognition or Field mutation ownership.
