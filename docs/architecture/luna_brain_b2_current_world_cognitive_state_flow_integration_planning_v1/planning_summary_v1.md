# B2 Current World → Cognitive State / Cognitive Flow Planning

## Decision

The planned route is:

`B1 CurrentWorldCandidateV1` → read-only State Formation adapter → existing `CognitiveStateFormationEngineV1` → attention/hypothesis/cognitive-state candidates → existing `CognitiveFlowInputV1` / `CognitiveFlowEngineV1` → future Decision boundary.

This reuses the existing Cognitive State Formation and Cognitive Flow owners. It does not create a brain-side parallel owner.

## Ownership

- Context Foundation assembles read-only source projections.
- Field State Reducer remains the sole Field State mutation authority.
- Current World is a candidate representation owned by Cognitive State Formation / Current World representation.
- Cognitive State Formation owns candidate attention, hypotheses, competition, cognitive state vector, and candidate Current World formation.
- Cognitive Flow owns lifecycle, transitions, reconsideration, and module handoff candidates; it does not own state, Field, Context, Intent, or Decision commitment.
- Field Perception Orchestrator owns observation need and re-observation control.
- Intent Governance remains the sole Intent owner.
- Decision Governance / Decision Arbitration remains the Decision boundary.

## Important contract gap

`CognitiveFlowInputV1` has an explicit `current_world_ref`, while `CognitiveStateFormationInputV1` does not. This planning phase does not overload an unrelated field or modify the canonical type. Before B2 implementation, the owner must decide whether a versioned first-class `current_world_ref` is required or whether an explicitly typed read-only adapter is sufficient.

## Semantics

World State is not Cognitive State. Evidence is not Hypothesis, Hypothesis is not Fact, provider confidence is not cognitive confidence, and attention priority is not truth probability. Unknowns, alternatives, contradictions, uncertainty, temporal references, trace, and provenance remain explicit.

## Deferred

Dynamic cognitive functions, cognitive parameter genome, self-regulation, semantic compression, online learning, and downstream Decision/Task/Action execution remain deferred.

## Status

Planning candidate only. No implementation was changed and no runtime or validation command was executed.
