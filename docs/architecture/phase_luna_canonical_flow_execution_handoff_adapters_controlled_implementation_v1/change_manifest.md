# Change Manifest

## Created

Implementation package:

`capabilities/midplatform/core/cognitive_flow/integration/canonical_execution_handoff_adapters_controlled/`

Documentation package:

`docs/architecture/phase_luna_canonical_flow_execution_handoff_adapters_controlled_implementation_v1/`

## Reused

- `ACognitiveRequirementCandidateV1`
- `AttentionCandidateV1` family as the downstream Attention contract
- `RuntimeAdmissionAssessmentCandidateV1`
- `ExecutableCapabilityCandidateV1`
- existing Decision, Task and Action handoff families
- `EdgeObservabilityCandidateV1`

## Not changed

No canonical source module, owner, enum, runtime, Provider, Observation,
Action, Field, Current World, Brain, Task or Decision authoritative state was
modified.

## Execution policy

The agent did not run Python, `py_compile`, pytest, Runner, Verifier,
Observation, Action, Provider, model or runtime probes.

