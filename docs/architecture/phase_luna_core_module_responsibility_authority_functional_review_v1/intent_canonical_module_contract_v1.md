# Intent Governance — Canonical Module Contract v1

## Canonical purpose

Intent Governance is the canonical owner of a governed directed purpose or
orientation: it qualifies and governs Intent candidates, preserves their
provenance and lifecycle, and exposes versioned Intent references and
handoffs to cognition, without becoming Brain governance, A reasoning, Task
execution, Capability resolution, Provider selection, or Loop mechanics.

## Why this owner exists

Without an independent Intent owner, directed purpose would be recreated by
Brain, A, Task, Context, or a route orchestrator. That would make a local Need
look like a purpose, make Task completion look like Intent completion, and
allow source modules to mutate a commitment they do not own. Intent Governance
provides the missing identity, admission, coexistence, provenance, version,
and lifecycle boundary.

## Core responsibilities

| Responsibility | Classification | Contract |
|---|---|---|
| qualify Potential Intent and Intent candidates | CORE | preserve source refs, uncertainty and provenance |
| admit and maintain governed Intent identity/version | CORE | only Intent Governance mutates admitted Intent |
| coexistence, conflict and temporary dominance | CORE | return governed lifecycle/interaction decisions or candidates |
| carryover, suspension, resumption and supersession | CORE | semantic lifecycle, not Loop persistence |
| handoff to Concern governance or cognition | SUPPORTING | candidate/ref handoff; Brain remains Concern authority |
| priority/resource interaction | SUPPORTING | local Intent relation is candidate; Brain owns global priority |
| semantic construction | OUT_OF_SCOPE | Semantic Module responsibility |
| Need, Sufficiency or Reconsideration | OUT_OF_SCOPE | A responsibility |
| Task/Capability/Provider execution | OUT_OF_SCOPE | downstream owners |

## Authority and responsibility

Intent Governance may decide whether a candidate is an admissible Intent,
which Intent versions coexist, and which Intent lifecycle transition is valid.
It is responsible for identity collisions, unauthorized mutation, provenance
loss, invalid version transitions, cross-Intent contamination, and invalid
carryover or handoff. It is not responsible for the Goal that motivated the
Intent, the Concern-local judgment of A, or downstream execution.

## Current implementation evidence

The repository has `IntentCandidateV1`, `PotentialIntentCandidateV1`,
`IntentInteractionCandidateV1`, `IntentStateTransitionCandidateV1`, and
`IntentToCausalHandoffCandidateV1`. `IntentGovernanceSkeletonV1` constructs
candidate-only outputs with `runtime_executed=False` and
`source_mutation_executed=False`. The ownership guard requires the Intent
owner, read-only refs, provenance, and no decision/action/task output.

These assets prove the boundary and controlled candidate seam. They do not
yet constitute a unified runtime that writes or serves an authoritative
admitted Intent record.

## Disposition and timing

**KEEP.** The owner is irreducible. Implementation timing is
`CONTRACT_ONLY / DEFER_RUNTIME`; the next implementation should add the
admission/lifecycle bridge without moving authority to another module.
