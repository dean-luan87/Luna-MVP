# CognitiveWorkingEnvelopeV1 Contract

## Status

Candidate-only schema design. This document does not add or modify a Python
type.

## Purpose

CognitiveWorkingEnvelopeV1 is the bounded reference envelope passed into A
reasoning and, with a restricted view, into B contingency reasoning.

It carries references and source versions. It does not duplicate authoritative
state.

## Proposed fields

| Field | Meaning | Ownership |
|---|---|---|
| work_id | working context identity | envelope/candidate |
| concern_ref | admitted concern identity | Brain-owned ref |
| goal_refs | global goal refs | Brain-owned refs |
| intent_refs | Intent refs | Intent owner |
| role_refs | Role refs | Role owner |
| perspective_refs | Perspective refs | Role/Perspective owner |
| field_refs | Field refs | Field owner |
| context_refs | Context refs | Context owner |
| current_world_refs | Current World refs | Current World/State owner |
| cognitive_state_version_ref | source state version | State Formation/Flow |
| task_behavior_refs | Task/Behavior constraints | Task/Behavior owners |
| emotion_modulation_refs | modulation inputs | Emotion owner |
| experience_refs | prior candidate refs | Experience owner |
| safety_refs | safety gate refs | Safety owner |
| permission_refs | permission gate refs | Permission owner |
| resource_envelope_refs | resource constraints | Resource owner |
| current_need_ref | current minimum Need | A-owned local candidate |
| hypothesis_refs | active hypothesis refs | A/B reasoning with Hypothesis owner |
| expectation_refs | expectation refs | A/B reasoning / Outcome consumer |
| evidence_refs | evidence refs | source evidence owners |
| unresolved_gap_refs | unresolved information gaps | A-owned local candidate |
| temporal_continuity_refs | temporal continuity refs | source continuity refs |
| spatial_continuity_refs | spatial continuity refs | source continuity refs |
| trace_refs | trace links | source owners |
| provenance_refs | provenance links | source owners |

## Field classes

### authoritative_ref_fields

concern_ref, goal_refs, intent_refs, role_refs, perspective_refs, field_refs,
context_refs, current_world_refs, task_behavior_refs, emotion_modulation_refs,
safety_refs, permission_refs, resource_envelope_refs and experience_refs.

These are read-only references and source versions, never copied authority.

### source-owned candidate fields

evidence_refs, expectation_refs, attention-like relevance refs, current-world
candidate refs, capability outcome refs and observation admission refs.

Their source owners retain semantic authority.

### A-owned local fields

current_need_ref, hypothesis revision references, unresolved_gap_refs,
local expectation interpretation, local evidence relevance result and local
sufficiency/reconsideration candidates.

These remain candidate-only and concern-scoped.

### B-visible inherited fields

concern_ref, source state version, bounded goal/intent/role/field/context/world
refs, inherited evidence/hypothesis refs, reality constraints, scope/depth,
resource and stop-condition refs.

B receives a bounded view. B cannot write back into the envelope.

### Loop-stored mechanical fields

work_id, state version lineage, pending refs, Need/Requirement refs, pause/wait/
resume state, closure/freeze refs, trace/provenance refs and history boundary
refs.

Loop stores references and mechanical facts only.

## Non-duplication invariant

No envelope field may contain an authoritative copy of external state. A field
without a source owner is either an A-owned local candidate or a documented
contract gap; it must not silently become a new owner.
