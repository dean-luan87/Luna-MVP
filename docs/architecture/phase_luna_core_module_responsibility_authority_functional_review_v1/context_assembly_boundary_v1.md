# Context Assembly Boundary v1

## Assembly rule

`source-owned projections + temporal scope + validity/version metadata + trace`
→ `Context Envelope Candidate`.

The assembly must preserve unknown, uncertain and multiple-candidate source
states. It must not resolve them into invented facts.

## What Context owns

- context-envelope identity and assembly version;
- temporal scope and validity of the assembled envelope;
- inclusion/exclusion of valid source refs for the requested situation frame;
- assembly trace, provenance and degraded/unknown markers;
- source-version alignment at the assembly level.

## What Context only references

Field, Current World, Observation, Memory, Self/identity, Role, Relationship,
Intent, Task, Emotion/user state, time/location and governance constraints.
The existing `ProjectionReferenceV1` is read-only/reference-only and explicitly
contains source owner, projection version, validity, unknown state and
provenance rather than source payload.

## Missing/stale behavior

Missing source → incomplete/degraded candidate with the missing ref recorded.
Stale source → stale/invalidated context candidate with source-version reason.
Conflicting source → contested/multiple-candidate context candidate. Context
does not choose the semantic winner; A decides the cognitive consequence and
Brain governs global constraints.

## Bypass prohibition

No direct Observation→Context authority without a governed projection/handoff;
no direct Current World→Field mutation; no Context→Intent/Task/A mutation. A
context candidate can be passed to the sibling Semantic Working Outline and
Cognitive Snapshot products through refs.
