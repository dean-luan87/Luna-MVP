# Capability Scope and Invocation Bridge

This controlled implementation extends the existing Universal Capability Slot
resolution surface with structured Module scope validation, explicit capability
gaps, readiness-aware resolution, and a candidate-only invocation handoff.

Canonical route:

`Need → CapabilityRequirement → ScopeAssessment → Official Module → Slot /
readiness → InvocationCandidate → existing Gateway/FPO execution boundary`.

No provider, model, camera, OCR, SLAM, or runtime execution occurs here.
