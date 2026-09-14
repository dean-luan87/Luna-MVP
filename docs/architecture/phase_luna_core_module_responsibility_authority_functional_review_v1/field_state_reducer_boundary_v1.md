# Field State Reducer Boundary v1

## Canonical role

The Field State Reducer is the narrow transition authority for Field state. It
consumes **admitted** field events and produces deterministic transition or
read-projection candidates with replay and provenance lineage.

## Required boundary

`Observation/Evidence → Field Event Admission → Reducer candidate → governed
Field state transition/read model`.

The event-admission contract (`field_event_admission_api_v1.py`) validates
structure, temporal order, duplicate identity and reducer eligibility. The
reducer must not receive raw observation payloads. A reducer-eligible event is
still marked candidate/not-fact until the applicable Field state admission and
persistence contract is satisfied.

## What the reducer may do

- validate structural and temporal transition inputs;
- preserve event ordering, conflict, revocation, expiration and supersession
  metadata;
- construct a deterministic state-transition candidate;
- preserve state/version/provenance/replay lineage;
- produce a read-model projection candidate.

## What it may never do

- infer the cognitive meaning of a state;
- decide Need, Hypothesis, Sufficiency, Reconsideration or Next-step;
- fuse a Current World candidate as authoritative Field state;
- assemble Context or a Semantic Working Outline;
- execute Observation, Provider, Action or Task work;
- perform external lookup, model recall or scheduler work;
- declare World Truth.

## Current evidence and gap

The current skeleton explicitly sets `reducer_is_single_mutation_authority =
True`, but also sets `runtime_implemented = False`, `direct_state_write_allowed =
False`, and returns `state_mutation_executed = False`. Therefore the architecture
has an owner boundary, not a production runtime claim. The future implementation
must preserve this separation between transition authority and cognition.

## Failure ownership

The reducer owns invalid event ordering, invalid transition shape, stale
acceptance within its contract, replay inconsistency, lost provenance and
cross-Field contamination. It reports rejection/degradation; it does not
provide semantic recovery advice. A owns the consequence of a Field change for
local reasoning.
