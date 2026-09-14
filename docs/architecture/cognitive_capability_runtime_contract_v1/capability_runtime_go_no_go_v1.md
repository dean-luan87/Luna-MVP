# Capability Runtime Contract Go / No-Go v1

## Required readiness checks

- Capability Request is abstract and is not a Model Request.
- Requests originate from Attention, Observation Cycle, or Situation
  Requirement; Provider and Runtime cannot create a need.
- Admission checks Requirement Match, Permission, Constitution Boundary,
  Resource Budget, Capability State, Risk Level, and Evidence Expectation.
- Provider input is least-privilege and excludes Goal, Brain Intent, full Field,
  Identity, Value, Decision, and complete Self Model.
- Provider output is Raw Evidence Candidate and must pass Evidence Gateway.
- Reality Update Candidate reaches the Reducer; Provider cannot modify Reality.
- Resource request includes camera/sensor, GPU/CPU, memory, latency, energy,
  network, storage, and explicit Resource Cost as candidates.
- Failure classes include unavailable, timeout, low_confidence, invalid_output,
  resource_denied, protocol_error, and provider_error.
- Failure returns Diagnostics, Self Capability, Attention, or Alternative
  Capability candidates without direct Goal, Decision, Reality, or Identity
  mutation.
- Provider replacement cannot change A Route cognition or Self Identity.

## Explicit prohibitions

No real model call, No OCR, No SLAM, No Camera, No Hardware, No Provider
Runtime, No Action Runtime, No automatic execution, No automatic learning, No
Provider-to-Brain, No Provider-to-Decision, No Provider-to-Goal, No B, No
Emotion, No Role, No Social Runtime, No direct Reality mutation, No direct Goal
mutation, and No direct Decision mutation.

The Agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

Situation Requirement is an allowed request origin. Alternative Capability is
a candidate only. No Provider Runtime and No Provider-to-Brain are enabled.
No Emotion and No direct Goal mutation are permitted.
