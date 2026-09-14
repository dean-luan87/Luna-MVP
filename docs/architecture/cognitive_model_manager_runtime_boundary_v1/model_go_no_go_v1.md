# Model Manager Runtime Boundary Go / No-Go v1

## Required readiness checks

- Model Manager is an asset governance manager, not Brain, reasoning center,
  Task scheduler, Decision maker, or cognitive subject.
- Model Registry records Identity, Version, Provider, Capability Binding,
  Resource Requirement, Hardware Compatibility, Performance Profile, Health,
  and Permission.
- Capability and Model remain separate: Capability → Implementation Options →
  Models.
- Model Admission checks capability declaration, boundaries, resources,
  Evidence output, Hardware Compatibility, Permission, Health, and Protocol.
- Model Runtime receives Capability Request and outputs Evidence Candidate only.
- Model Cognitive Scope allows local analysis/candidate generation but not Goal,
  Decision, Action, Value, or Authority.
- Evidence Output contains Source, Confidence, Limitation, Unknown, and
  Provenance and must pass Evidence Gateway.
- Model Replacement does not change Identity, Field, Task, or Goal.
- Hardware limitation returns Model Unavailable/Degradation Candidate.
- Attention selects Capability and Model Manager provides implementation
  options; automatic model switching is disabled.

## Explicit prohibitions

No real model, No GPT, No VLM, No OCR, No SLAM, No ASR, No Provider Runtime, No
automatic model switching, No automatic learning, No Action, No B, No Emotion,
No Role, No direct Reality mutation, No direct Goal mutation, and No direct
Decision mutation.

The Agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

Capability → Implementation Options → Models is mandatory. Model Degradation
Candidate is a candidate only. Attention provides implementation options.
No direct Decision mutation is permitted.

Model Degradation Candidate is a candidate only and is not a runtime decision.
