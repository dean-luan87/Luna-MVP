# Cognitive Analysis Controlled Skeleton README v1

## Module position

This is the A3 **Controlled Skeleton Implementation**. It expresses immutable,
serializable, provenance-aware and trace-aware Analysis candidate objects. It
does not perform cognitive reasoning; fixture construction is explicit object
assembly only.

## Objects

- Cognitive Analysis Admission Result
- Cognitive Analysis Frame
- Hypothesis Candidate
- Competing Hypothesis Set
- Analysis Evidence Assessment
- Information Gap Refinement
- Observation Request Candidate
- Cognitive Analysis Sufficiency Result
- Cognitive Analysis Result

## Context-only input and compatibility mapping

The direct input boundary is `CurrentCognitiveContextV1`. A3 does not import,
copy, or create a parallel Context type. The actual A2 fields map as follows:

| A2 actual field | A3 skeleton use |
| --- | --- |
| `context_id`, `context_version` | source Context identity/version references |
| `snapshot_ref` | traceable source Snapshot reference through Context |
| nested subject/task/goal/attention/temporal contexts | declared read-only scope references |
| selected refs, inclusion/exclusion, gaps, sufficiency | candidate-analysis inputs only |
| `provenance`, `trace` | A3 `provenance`, `trace_ref` lineage fields |

## Permission and output boundary

The skeleton emits only fixture candidate objects. It cannot mutate Context,
Snapshot, Read Model, Field State, State Version, Transition, or History. The
Field State Reducer remains the sole Field State mutation authority.

`HypothesisCandidateV1` is not Fact. `CognitiveAnalysisResultV1` is not
Decision or Action. `ObservationRequestCandidateV1.execution_admitted` is
always `false` in this phase.

## Fixture-only declaration

The fixture builder creates eight fixed-ID cases for structural coverage:
supported, competing, contradicted, insufficient, revoked, temporal-unknown,
gap-request, and state-writeback-denied. It uses no runtime Context, model,
network, database, system time, random source, UUID generation, or external
I/O.

`runtime_executed = false`, `simulation_only = true`,
`decision_boundary_admitted = false`, and `state_writeback_admitted = false`
are immutable boundary requirements for every fixture result.

## Static validation and future route

The static validator checks references, controlled enums, admission/sufficiency
consistency, competing-hypothesis rules, revoked-evidence handling,
candidate-only observation requests, result flags, provenance/trace presence,
and AST-level forbidden runtime imports/calls.

The next possible route is a separately authorized A3 Controlled DryRun phase.
It must add its own runner/verifier and must not reinterpret this skeleton as
runtime, production readiness, Fact admission, Decision execution, or State
writeback permission.
