# Loop growth and future branch boundary

## Need-driven multi-capability use

A single Loop may use multiple capabilities, but each capability candidate
must originate from the current minimum Need or an explicitly reassessed
information gap. Every new capability candidate re-enters:

`Need → Requirement → Scope → Resolution → Resource → Permission → Safety → Observation admission`

`REQUEST_MORE_EVIDENCE` remains a future Observation Candidate. It never means
automatic Provider invocation, automatic retry, or camera activation.

## Anti-growth guards

The next implementation must reject or defer unnecessary Loop/capability
growth using candidate-only signals for:

- minimum sufficient cognition;
- resource envelope and budget;
- goal sufficiency threshold;
- state/Requirement staleness;
- diminishing information value;
- duplicate Requirement detection;
- already materialized Need or Observation candidate;
- completed, stopped, or waiting Loop state.

These are governance signals, not a utility optimizer or autonomous scheduler.

## Branch / sub-Loop reservation

The existing Cognitive Flow now also has a narrow candidate-only Branch
Formation boundary and a separate candidate-only Branch Governance boundary.
Formation may organize explicit governed Hypothesis alternatives, unresolved
Information Gaps, or other governed alternatives into distinct Branch
Candidates. Governance evaluates those candidates against explicit current
state refs and emits ADMITTED, DEFERRED, or REJECTED decisions. Neither
boundary executes, schedules, merges, closes, or reopens a branch.

Future contracts may reference:

- `parent_loop_ref`;
- `derived_from`;
- dependency refs;
- shared Context refs;
- inherited evidence refs;
- branch reason;
- supersede ref;
- merge candidate ref.

Loop → Loop derivation is allowed in principle, but Brain owns creation and
governance. No recursive autonomous Loop spawning, branch execution, or merge
algorithm is implemented here.

The current Cognitive Flow also has a bounded post-governance acquisition strategy
candidate boundary. An admitted Branch and its branch-local Need/Gap may be paired
with an explicit governed acquisition basis to form one or more immutable
`InformationAcquisitionStrategyCandidateV1` values. This formation does not infer a
strategy from Goal/Question text, does not coordinate or prioritize candidates, and
does not form Resource, Attention, Observation Demand, Capability, Task, or Action
semantics. Deferred or Rejected Branches do not produce active strategy candidates.
Strategy coordination and acquisition execution remain future boundaries.

## Closure and Experience reservation

The future bridge is:

`Runtime Trace → Loop Closure Record → Loop Package → Experience Candidate → Experience Governance → future Cognitive Prior`

The Loop Package is a data package, not a new owner. It may eventually report
successful/failed reasoning paths, capability or observation utility,
premature closure, unnecessary exploration, resource cost, emotion modulation
effects, and reconsideration quality. Experience mutation, Memory mutation,
Hive influence, and semantic compression remain deferred.
