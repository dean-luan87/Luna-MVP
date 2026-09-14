# CognitiveWhiteBoxTraceV1 Contract

## Node coverage

The node vocabulary covers Goal, Intent, Concern, Context, Role, Field,
Attention, Information Need, Observation Demand/Request, Capability
Requirement/Resolution, External Capability Invocation, Observation, Evidence,
Evidence Relevance/Conflict/Missing/Uncertainty, Current World Candidate,
Hypothesis/Revision, Sufficiency, Information Gap, Re-observation, Stop Reason,
Decision Governance Handoff, and Result Closure.

## Node fields

Each node carries identity, kind, observability status, owner/source refs,
parent/predecessor/successor refs, task/goal/concern refs, cycle and sequence
indices, provenance, source versions, invalidation, candidate/authoritative
flags, and bounded metadata.

Raw Provider payload, credentials, binary/image data, and World Truth are not
accepted in bounded metadata.

## Observability

The contract distinguishes `currently_observable`, `partially_observable`,
`planned`, and `unavailable`. A missing canonical runtime asset is represented
as a status, never manufactured as a node.

## Authority

The trace is an observation record. It cannot modify Attention, Observation,
Evidence, Current World, Hypothesis, Sufficiency, Re-observation, or Decision.
