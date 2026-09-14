# Cognitive Flow Domain Model v1

## Semantic Separations

| Separation | Meaning |
| --- | --- |
| Event != State | An event records something received or asserted; state is a governed temporal projection derived from admitted events. |
| Evidence != Fact | Evidence supports review and reasoning; it does not establish truth by itself. |
| Hypothesis != Conclusion | A hypothesis is a falsifiable explanation or prediction with assumptions and alternatives. |
| Analysis != Decision | Analysis produces structured candidates; a decision requires a separate authority and policy boundary. |
| Experience != Value Judgment | Experience captures situated outcomes and reusable patterns; it does not establish individual or Hive values. |

## Core Objects

| Object | Identity and minimum content | Owner | Allowed lifecycle | Prohibited interpretation |
| --- | --- | --- | --- | --- |
| Observation Event | event id, source, observed/received time, payload, trace | Perception Admission | received, normalized, rejected, retained | fact or state write |
| Evidence | evidence ref, source chain, artifact ref, provenance, quality/uncertainty | Evidence governance boundary | candidate, reviewed, retained, retracted | truth by existence |
| Field | field ref, anchors, scope, identity confidence, lineage | Field Kernel | proposed, resolved, unresolved, superseded | global immutable ontology |
| Field State | state ref, field ref, temporal validity, admitted event refs, provenance | Field State Reducer | candidate, revised, suspended, expired, revoked | direct organ/model output |
| Entity | entity ref, observed properties, field relation refs, evidence refs | Field Kernel planning | observed candidate, linked, unresolved | stable fact without admission |
| Relation | relation ref, endpoints, relation type, scope, evidence and time refs | Field Kernel planning | proposed, supported, conflicted, retired | automatic causal truth |
| Hypothesis | hypothesis id, question, claims, assumptions, alternatives, evidence refs | Cognitive Analysis | proposed, tested, supported, weakened, retired | conclusion or action order |
| Information Gap | gap id, missing condition, relevance, requested evidence/capability | Cognitive Analysis | identified, requested, satisfied, deferred, expired | permission to invoke tools |
| Experience Episode | episode id, context, delivery/outcome links, evidence, reflection | Experience System | captured, reviewed, retained, withdrawn | universal rule or value |
| Experience Kernel | kernel id, abstraction, applicability, counterexamples, provenance | Experience System | proposed, reviewed, reusable, deprecated | model weight, policy override, fact |
| Experience Branch | branch id, episode/kernel refs, relation/conflict rationale, local scope | Experience System / Hive association | proposed, linked, conflicted, retired | consensus or vote |

## Required Shared Fields

Every object must have a stable object reference, source or provenance references, trace reference, creation/evaluation time with timezone, lifecycle status, version/revision reference, and explicit uncertainty where applicable. Objects that may affect current world understanding additionally preserve Field scope and temporal assessment.

## Object Relation Sketch

```text
Observation Event -> Evidence -> admitted Field Event -> Field State
Field State + Evidence -> Hypothesis / Difference Point / Information Gap
Hypothesis + Gap + constraints -> Cognitive Delivery candidate
Delivery or authorized exploration -> Outcome Event -> Experience Episode
Reviewed Episodes -> Experience Kernel -> Experience Branch
```

No relationship in this sketch performs a fact promotion, action execution, or global value decision.

