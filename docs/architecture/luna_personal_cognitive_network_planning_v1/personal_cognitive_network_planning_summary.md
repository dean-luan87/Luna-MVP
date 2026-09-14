# PLANNING_CANDIDATE

## PCN Positioning

Personal Cognitive Network (PCN) is a personal relatedness and activation projection network over source object references. It is not Memory, not Knowledge Graph, not Causal Engine, and not Decision Engine.

## Object Model

PCN stores only source references, cognitive links, activation states, and context-bounded projections. Source object ownership, persistence, and mutation remain with source owners.

## Link Model

Link schema supports relation_type, activation_state, strength_state, provenance, confidence, and uncertainty. Strength is subjective salience and is not equivalent to objective truth.

## Growth Model

New information and experience may create link growth candidates when existing links are insufficient. Reinforcement, weakening, and dormancy are resource-governed; inactivity does not auto-delete links.

## Activation Model

Activation starts from Context and selectively activates related Field/Role/Relationship/Memory/State references, then performs bounded propagation to produce active projection candidates.

## Dormancy Model

States include ACTIVE, WEAK, DORMANT, and REACTIVATED. Transitions are relevance-based and resource-aware, not fixed-time-threshold driven.

## Subjective Cognition Boundary

PCN preserves subjective, biased, contradictory, and emotion-driven personal associations when traceable in personal cognition. PCN does not perform forced truth correction.

## Context Relationship

Context Foundation provides read-only handoff and constraints to PCN. PCN cannot overwrite Context source state.

## Memory Boundary

Memory owns admission, persistence, retrieval, and consolidation. PCN only references Memory projections for activation and context projection.

## Causal Boundary

PCN handles relatedness/association/activation. Causal handles why/cause/effect/alternative explanation. PCN cannot generate causal facts.

## Resource Boundary

Activation scope and propagation are bounded by resource budgets and can degrade projection scope under pressure without deleting network state.

## Nested Constraints

The planning model explicitly records:
Context <-> PCN, Resource <-> PCN, Memory <-> PCN, Field <-> PCN, Role <-> PCN, Relationship <-> PCN, Emotion <-> PCN, and future Intent/Causal/Experience <-> PCN.

## Future Skeleton Entry

Future skeleton phase may start from:
1. Context handoff adapter for PCN activation candidate intake.
2. Reference-only link candidate registry in controlled skeleton mode.
3. Projection candidate output path to Intent/Causal consumers.

## Stop Condition

This phase answers what PCN should be and how it should be implemented in future phases. No runtime, persistence, algorithm, or migration implementation is started.
