# Cognitive State Formation Architecture Plan v1

## Phase
- Phase: Phase-Luna-Cognitive-State-Formation-Architecture-And-Controlled-Implementation-Planning-v1-001
- Mode: Planning Only (V0 static checks only)
- Previous phase decision: GO

## Module Definition
- Single complete module: Cognitive State Formation Module
- Internal chain: Attention Selection -> Hypothesis Space -> Current World Candidate
- Upstream references: Context, PCN, Intent, Field, Observation, Risk, Task, Role, Memory
- Downstream references: Causal candidate input, Decision context reference

## Existing Asset Reuse (Read-Only)
- Reuse as mainline owners:
  - Context Foundation
  - Personal Cognitive Network Governance
  - Intent Governance
  - Causal Governance
  - Field State Reducer
- Reuse as candidate pattern reference:
  - capabilities/midplatform/core/information_integration_types_v1.py
  - capabilities/midplatform/core/information_integration_skeleton_v1.py
- Architecture references:
  - docs/architecture/cognitive_hypothesis_belief_architecture_v1/
  - docs/architecture/cognitive_global_state_representation_v1/
  - docs/architecture/luna_cognitive_state_machine_architecture_v1/
  - docs/architecture/luna_cognitive_dynamic_function_architecture_v1/

## Hidden/Implicit Existing Implementations
- Found candidate-like assets for attention/world composition in Information Integration:
  - PriorityAttentionMapCandidate
  - LiveWorldStateCandidate
  - ConflictCandidate
  - DecisionContextCandidate
- Interpretation: these are reusable candidate skeleton patterns, not canonical owner declarations for this phase target module.

## Controlled Implementation Planning Scope
- Define canonical owner boundary for module.
- Define attention/hypothesis/current world schemas and contracts.
- Define deterministic candidate flow and minimum scenarios.
- Define gap registry A/B/C/D without modifying existing modules.

## Out of Scope
- No runtime execution.
- No field mutation.
- No intent mutation.
- No causal mutation.
- No decision/action/task execution.
- No module implementation in this phase.
