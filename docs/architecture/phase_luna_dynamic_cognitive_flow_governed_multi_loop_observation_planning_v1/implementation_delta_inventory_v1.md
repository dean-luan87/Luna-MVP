# Minimum implementation delta inventory

Status: candidate-only implementation complete; user-terminal verification pending.

## Already reusable

- `DynamicCognitiveFlowEngineV1` and dynamic loop candidate input/output types;
- `CognitiveStateVersionCandidateV1` and explicit state-version lineage;
- `ReconsiderationCandidateV1`;
- `SuspendCandidateV1` and `ResumeCandidateV1`;
- `ReobserveCandidateV1` and Observation Gateway candidate types;
- Need → Capability Requirement Bridge;
- Capability Scope, Resolution, and Invocation Candidate types;
- `CycleSnapshotV1` for read-only Context/Field/World/Attention/Hypothesis refs;
- Task Manager readiness vocabulary and Intent resource references;
- `ExperienceCandidateV1` and `MemoryCandidateV1` as future boundary refs;
- Brain Golden Baseline and existing Safety / Resource governance.

## Reusable with minimal extension

1. Add a candidate-only Loop identity envelope around existing Dynamic Flow
   input/output without duplicating authoritative data.
2. Add a lifecycle disposition mapping for `ACTIVE`, `WAITING`, and `STOPPED`
   while reusing `SUSPENDED`, `DEFER`, and `COMPLETED`.
3. Add a Resume Assessment candidate carrying the six continuity signals and
   current authoritative source versions.
4. Add loop-scoped references to Need, Requirement, Observation, evidence,
   priority, resources, safety, trace, and provenance.
5. Add a candidate-only Cognitive Outcome / Loop Closure package reference.
6. Add future branch reservation fields without implementing derivation.

## Implemented in this controlled phase

- Loop identity envelope and Brain materialization guard;
- loop-local state/provenance isolation fixture;
- KEEP / SUPERSEDE / REPLAN / COMPLETE / WAITING resume assessment fixture;
- six-signal continuity comparison fixture;
- Need-driven multi-capability reservation and growth guards;
- Brain/Loop non-duplication guard;
- Cognitive Outcome Candidate and future Experience bridge reservation checks.

## Remaining candidate-only work for a later phase

- direct adapter to a concrete Brain materialization source;
- richer authoritative state comparison beyond reference candidates;
- explicit Task/Behavior continuity owner handoff;
- static schema validation beyond the controlled Verifier;
- real multi-capability execution, which remains deferred.

## Deferred

- real multi-capability execution;
- real second YOLO/provider invocation;
- autonomous scheduling or arbitration;
- optimal resource allocation and utility scoring;
- capability acquisition/install/uninstall;
- Learning, Memory, Experience mutation, Hive runtime influence;
- semantic folding/expansion;
- Action execution.

## Lifecycle closure implementation delta

- `ClosureAssessmentCandidateV1` separates a closure suggestion from
  lifecycle acceptance.
- `ClosureDecisionCandidateV1` records Brain/Cognitive Flow governance.
- `LifecycleClosureCandidateV1` leaves local state `OPEN` until acceptance.
- `FinalStateFreezeCandidateV1` freezes references and disposes outstanding
  Requirements/Observation Candidates without copying authoritative state.
- `BrainAssimilationCandidateV1` keeps outcome assimilation candidate-only.
- `LoopPackageCandidateV1` and `HistoryBoundaryCandidateV1` reserve bounded
  handoff/history semantics without compression.
- 28 focused `LC-*` scenarios cover closure reasons, final-state integrity,
  assimilation, package/history, branch, and negative boundaries.

## Conflicts found and resolved in planning

- A Loop Brain or Loop Manager would duplicate Brain/Cognitive Flow ownership;
  rejected.
- Loop-owned Intent, Field, Emotion, Safety, Resource, Memory, or Provider
  identity would duplicate canonical authority; rejected.
- Treating every thought or plan candidate as a Loop would create unnecessary
  persistent state; rejected.
- Treating Loop completion as Experience or Truth would bypass Brain
  assimilation; rejected.
