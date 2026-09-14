# Field Capability Integration Go/No-Go v1

## Readiness checks

- Cognitive Field produces a provider-neutral Observation Requirement.
- Capability Registry admits only declared Evidence capabilities.
- Model Manager and Provider boundaries preserve A Route and Brain authority.
- Evidence Gateway validates provenance, confidence, uncertainty, timestamp,
  capability reference, and request reference.
- Provider replacement changes Evidence Quality Candidate only.
- Human Feedback enters through the Evidence Gateway.
- Provider failure follows Capability Failure → Diagnostics → Self Capability
  Candidate. The output is a Self Capability Candidate, not a direct Self
  mutation.
- No capability creates a Field, modifies Reality, changes Goal, or triggers
  Action.

## Explicit prohibitions

This phase has No real model execution, No real OCR, No real SLAM, No Hardware
Runtime, No Action Runtime, No B Simulation Runtime, no online learning, no
automatic model switching, no direct model call from Cognitive Field, and no
automatic Reality mutation.

The lower-case boundary terms are also explicit: no Hardware Runtime, no
automatic model switching, and no automatic Reality mutation.

Exact prohibitions: no Hardware Runtime; no automatic model switching; no
automatic Reality mutation.

no Hardware Runtime; no automatic model switching; no automatic Reality mutation.

No Hardware Runtime is prohibited in this architecture-only phase.

The phase is architecture-only. It does not grant Runtime permission and does
not declare GO. The user must run the Final Phase Verifier and return all
required output sections.

## Stop status

After V0 static checks, the agent stops at
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.
