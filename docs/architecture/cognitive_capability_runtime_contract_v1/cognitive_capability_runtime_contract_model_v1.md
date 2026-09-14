# Cognitive Capability Runtime Contract Model v1

## Purpose and Constitution dependency

This phase defines how Luna requests an abstract Capability while preserving
the A Route Cognitive Constitution. It is a contract architecture, not a
Provider Runtime and not a Model Request implementation.

The canonical flow is:

```text
Observation Requirement
        ↓
Capability Request
        ↓
Capability Admission
        ↓
Provider Invocation Candidate
        ↓
Provider Output
        ↓
Raw Evidence Candidate
        ↓
Evidence Gateway
        ↓
Reality Update Candidate
        ↓
Reducer
```

The requester names a Capability and an Evidence expectation, never a model
identity. A Capability Request is not a Decision, Action, Goal, Situation,
Fact, or direct Model Request.

## Request authority

Capability Requests may originate from Attention, Observation Cycle, or a
Situation Requirement. Brain may govern Goal and authorization context but
does not directly call a Provider. Provider cannot create a request, trigger a
new need, create a Field, or modify a Goal. Runtime cannot create a need by
itself.

## Admission contract

Every request receives a candidate admission review:

- Requirement Match;
- Permission and Constitution boundary;
- Resource Budget;
- Current Capability State and Confidence;
- Risk Level;
- Evidence Expectation;
- provenance, expiry, and Unknowns.

Admission is a candidate, not execution. Resource denial, unavailable
Capability, or high risk returns a diagnostic/failure candidate.

## Provider isolation

Provider sees only the least-privilege input contract: request reference,
scoped input Evidence, capability parameters, resource envelope, and output
schema. Provider does not receive Goal, Brain Intent, full Field, Identity,
Value, Decision, or the complete cognitive state.

Provider output is not Reality or Situation. It must pass Evidence Gateway
validation for schema, provenance, confidence, timestamp, uncertainty, and
capability reference before a Reality Update Candidate exists.

## Resource and failure boundary

Resource requests declare camera/sensor, GPU/CPU, memory, latency, energy,
network, and storage requirements as candidates. The runtime contract never
executes allocation here.

Failure classes are unavailable, timeout, low_confidence, invalid_output,
resource_denied, protocol_error, and provider_error. Failure flows to
Diagnostics, Self Capability Update Candidate, Attention Adjustment Candidate,
or Alternative Capability Candidate. It never directly changes Reality,
Goal, Decision, or Self Identity.

## Prohibitions

No real model call, No OCR, No SLAM, No Camera, No Hardware, No Provider
Runtime, No Action Runtime, No automatic execution, No automatic learning, No
Provider-to-Brain path, No Provider-to-Decision path, and No B Route are
implemented in this phase.

The request is not an Action. Resource Cost is explicit. No Provider Runtime
is implemented.
