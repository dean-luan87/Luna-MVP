# Current Cognitive Context Controlled Skeleton Implementation v1

## 1. Module Position

Current Cognitive Context is a derived, read-only interface between Field Snapshot and future Cognitive Analysis. It assembles caller-selected, minimum-sufficient Field references under Subject, Task, Goal, Temporal, and Attention Contexts.

**Current Cognitive Context is not Field State.**  
**Current Cognitive Context is not Field Snapshot.**  
**Current Cognitive Context is not Hypothesis.**  
**Current Cognitive Context is not Decision.**  
**Current Cognitive Context cannot mutate Field Kernel.**

## 2. Object Relationship

```text
Caller-provided Snapshot / context inputs / selected references
  -> ContextInclusionRecord / ContextExclusionRecord
  -> InformationGap / ContextSufficiencyResult
  -> CurrentCognitiveContextV1
  -> future read-only Cognitive Analysis input
```

The module stores only references to Field Units, Relations, States, History, and Evidence. It does not copy a complete Snapshot or read raw Field State.

## 3. Inputs and Outputs

Inputs are immutable Subject, Task, Goal, Attention, and Temporal Context objects plus explicit Snapshot/Field references, selected references, selection records, gaps, sufficiency result, provenance, and trace.

Output is immutable `CurrentCognitiveContextV1`. It includes context/version lineage, selected references, recoverable exclusions, Information Gaps, sufficiency result, invalidation reasons, and source lineage.

## 4. Builder Boundary

`build_current_cognitive_context_v1()` validates only explicit caller input:

- required Field, Snapshot, Context, trace, and source references;
- duplicate selected references;
- Inclusion Record reference membership in explicit selected references;
- recoverable/current-context-only Exclusion Record flags;
- Exclusion Record Snapshot consistency.

It does not select objects, score relevance, infer task intent, create gaps, revise sufficiency, query Snapshot/Field State, invoke a model, or fill unknown information.

## 5. Inclusion and Exclusion Semantics

Inclusion represents a traceable current-context selection. Exclusion means only that an object is not selected for this Context. Every Exclusion is required to be recoverable, current-context-only, and linked to its source Snapshot; it does not mark an object as erroneous or delete source data.

## 6. Information Gap Boundary

`InformationGapV1` describes missing, stale, conflicting, restricted, or insufficiently resolved information. Its `recommended_observation_scope` is a candidate scope for later observation only. It does not issue an action, navigation command, model request, final decision, Event Candidate, or Hypothesis.

## 7. Sufficiency Boundary

`ContextSufficiencyResultV1` is explicitly caller-assembled. It states only whether a Context is adequate for a bounded next analysis stage: sufficient, conditionally sufficient, insufficient, or unknown. It does not determine world facts, Hypothesis status, decision safety, or Fact Admission.

## 8. Lifecycle and Versioning

The lifecycle validator supports:

```text
requested -> built -> validated -> active
active -> refreshed | superseded
refreshed -> active | superseded
superseded -> archived
```

It rejects archived reactivation, superseded reactivation, requested direct activation, and built direct archival. It validates transitions only and does not change a Context. New Context versions use explicit `context_version`, `previous_context_ref`, and `superseded_by_ref`; refresh never overwrites an older Context.

## 9. Fixed Simulation Fixtures

Non-executing fixed constructors cover airport pickup, shopping-mall shop-status observation, indoor navigation for a blind user, and three distinct Contexts sharing the same airport Snapshot reference. They use no system time, random ID, model, database, network, real Snapshot query, or Reducer call.

## 10. Snapshot and Cognitive Analysis Boundaries

Field Snapshot remains the complete governed source view. Context is a recoverable, task-scoped selection surface and cannot bypass Snapshot/Read Model to access raw State or Event data.

Future Cognitive Analysis may read Context plus necessary source references and produce its own candidates. It has no Context or Field Kernel write-back path. Any world-state change candidate must return through Admission and Reducer.

## 11. Current Non-Goals

This skeleton implements no relevance scoring, attention model, automatic selection/exclusion, task interpretation, State explanation, Hypothesis, Interpretation, Decision, Experience, Self, Hive, persistence, model call, network, database, runtime, runner, verifier, or test.

## 12. Stop Condition

Stop after these isolated skeleton assets exist. Do not execute simulation or static checks in this phase; request user terminal review before any DryRun or integration work.
