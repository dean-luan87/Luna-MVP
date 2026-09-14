# Cognitive Neural Provider Quality Assessment Model v1

## Input

`provider_quality_assessment_candidate` is formed only from:

- the CWO reference;
- the Evidence Candidate for this bounded observation;
- the Provider Status Candidate for the same invocation.

It records availability, observed text coverage, failure patterns, and a `quality_state_candidate`. It explicitly has `provider_reliability_fact=false`, `truth_claim=false`, and `cognitive_completion_decided=false`.

## Interpretation boundary

Neural Governance may determine whether the current Provider observation is sufficient, degraded, or unusable **for this specific information need**. It may not determine whether OCR is globally trustworthy, whether the visual world contains text, or whether a new Provider must execute.

## Replay policy

Provider latency remains in the trace as a status observation. Because local initialization and device scheduling make its bucket non-deterministic, only latency is excluded from the deterministic replay-identity signature. No quality, failure, evidence, authority, or adaptive-control field is excluded.

This prevents instantaneous telemetry from masking a genuine Candidate-flow change while preserving the raw status for diagnostics.
