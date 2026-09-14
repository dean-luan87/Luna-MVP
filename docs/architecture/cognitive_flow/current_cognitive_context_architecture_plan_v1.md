# Current Cognitive Context Architecture Plan v1

## 1. Phase Position

- Phase: `Phase-A2.5-Current-Cognitive-Context-Layer-Planning-v1-001`
- Execution Mode: Planning Only
- Layer: L1 Cognitive Flow / Current World Representation Interface
- Status: contract proposal pending human review

Current Cognitive Context is placed between Field Snapshot and Cognitive Analysis:

```text
Field Event Admission
  -> Field State Reducer
  -> Field Kernel
  -> Field Snapshot
  -> Current Cognitive Context
  -> Cognitive Analysis
```

It is not Field State, Field Snapshot, Read Model, Hypothesis, Decision, Experience, Memory, World View, or a new fact source.

## 2. Canonical Definition

**Canonical Name:** Current Cognitive Context  
**中文名称：** 当前认知上下文

Current Cognitive Context is a read-only, derived, traceable, minimum-sufficient cognitive input composed from a Field Snapshot, Temporal Context, Subject Context, Task Context, Goal Context, Attention Context, Evidence References, and Schema References.

It answers:

> For this subject, task, and goal, which governed parts of the current world need to enter Cognitive Analysis now?

It does not answer why something happened, what will happen, what should be done, what is good or bad, or which Hypothesis is true.

## 3. Difference from Field Snapshot

| Field Snapshot | Current Cognitive Context |
| --- | --- |
| Complete governed read view of one Field at a snapshot time. | Task-, subject-, goal-, and attention-bounded subset of the Snapshot and linked sources. |
| Stable world-representation query surface. | Derived cognitive-analysis input boundary. |
| May include all relevant Units, Relations, States, and temporal context in Field scope. | Includes only minimum-sufficient selected content plus explicit exclusions and gaps. |
| Does not depend on one subject's current task. | May differ for multiple subjects/tasks using the same Snapshot. |
| Is not a Hypothesis. | Is also not a Hypothesis; it selects and organizes information only. |

Context does not replace the Snapshot. All selected and excluded entries retain recoverable source references to the Snapshot, History Projection, and/or Evidence Reference.

## 4. Design Principles

1. **Derived Only** — Context derives only from governed inputs and cannot become a new fact source.
2. **Read Only** — It cannot modify Field State, Temporal Evolution, Snapshot, Evidence, Task State, or source objects.
3. **Minimum Sufficient Representation** — It contains the least information sufficient for the declared analysis boundary, not merely the smallest payload.
4. **Traceable Selection** — Every inclusion and exclusion carries a reason and source reference.
5. **Unknown Preservation** — Unknown remains Unknown; missing time, location, entity, relation, or evidence is never auto-filled.
6. **Multi-Context Support** — One Snapshot may yield multiple valid Contexts under different subject/task/goal/attention inputs.
7. **Non-Exclusive Interpretation** — Context claims no single correct understanding; it is an analysis input boundary.
8. **No Silent Information Loss** — Compression is recoverable by source reference and does not permanently delete unselected information.

## 5. Legal Inputs

| Input | Required minimum content | Context use | Prohibited use |
| --- | --- | --- | --- |
| Field Snapshot | `snapshot_ref`, Field scope, Units, Relations, States, provenance, snapshot time | Primary current-world source | bypassing Snapshot to read raw State/Event data |
| Temporal Context | `current_time_reference`, `valid_time_scope`, `history_window_reference`, `temporal_uncertainty`, `stale_state_reference` | Scope current/historical relevance and retain uncertainty | inventing event time or future state |
| Subject Context | `subject_ref`, role, location reference, capability constraints, permission scope | Bound relevance and permitted view | personality/value judgement in this phase |
| Task Context | `task_ref`, type, stage, priority, constraints, status | Bound task relevance | treating task priority as safety level or truth confidence |
| Goal Context | `goal_ref`, primary goal, secondary goals, success/stop conditions | Bound sufficiency and gap relevance | decision or action authorization |
| Attention Context | scope, targets, priority, exclusions, reason references | Bound selection and exclusion | treating attention priority as truth confidence |
| Evidence Reference | evidence/source/trace references | Preserve source basis without copying all raw evidence | treating evidence as Fact |
| Schema Reference | declared cognitive schema reference | Organize selection categories | forcing information to fit a preset fact template |

## 6. Output Boundary

The planned output is `CurrentCognitiveContextV1`, plus Inclusion Records, Exclusion Records, Information Gaps, and a Sufficiency Result. These outputs are candidate/read-interface objects only.

Context may produce:

- Context;
- Context Inclusion Record;
- Context Exclusion Record;
- Information Gap;
- Context Sufficiency Result.

Context must not produce Fact, Field State, Transition Record, Hypothesis, Decision, Experience, Value, action command, or a replacement Snapshot.

## 7. Lifecycle and Invalidation

```text
Context Requested
  -> Context Built
  -> Context Validated
  -> Context Active
  -> Context Refreshed
  -> Context Superseded
  -> Context Archived
```

- **Requested:** caller declares subject, task, goal, attention, and source scope.
- **Built:** a new derived Context version is assembled from source references.
- **Validated:** selection trace, unknown preservation, provenance, and sufficiency are assessed.
- **Active:** Context is available as a read-only Cognitive Analysis input.
- **Refreshed:** a new Context version is derived from new Snapshot/Task/Goal/Attention inputs; old Context is not overwritten.
- **Superseded:** a later Context version is linked using `superseded_by_ref`.
- **Archived:** prior Context is retained only under future retention governance.

Required version fields are `context_version`, `previous_context_ref`, and `superseded_by_ref`.

The following invalidate a Context: `source_snapshot_changed`, `field_state_changed`, `task_stage_changed`, `goal_changed`, `subject_changed`, `attention_scope_changed`, `temporal_scope_expired`, `critical_evidence_revoked`, and `permission_scope_changed`.

Invalidation may mark `stale`, `superseded`, or `refresh_required`; it never updates Field State or silently rewrites an existing Context.

## 8. Existing Module Relationship

| Module | Relationship to Current Cognitive Context |
| --- | --- |
| Field Kernel | Supplies governed structure, current State, and temporal representation boundaries. |
| Field Snapshot | Supplies the complete current governed read view. |
| Read Model | Supplies authorized Snapshot and future Historical View queries. |
| Observation Attention | May supply Attention Context candidate inputs; it has no fact or State authority. |
| Task Manager | May supply Task Context candidate inputs; it has no cognitive-truth authority. |
| Evidence Layer | Supplies Evidence References and source/trace lineage. |
| Cognitive Analysis | Read-only Context consumer. |
| Experience | May later influence selection-policy candidates; it must not write Field State. |
| Self | May later supply subject/constraint/preference candidates; no value adjudication is introduced here. |
| Hive | May later supply experience/schema candidates; it cannot control an individual Context. |

## 9. Cognitive Analysis Interface Reservation

Future Cognitive Analysis receives:

```text
Current Cognitive Context + necessary source references
```

It may later emit Hypothesis Candidate, Interpretation Candidate, Information Gap Refinement, or Decision Candidate under its own contracts. It cannot directly write Context or Field State. Any result that seeks world-state change must become an Event Candidate and return through:

```text
Admission -> Reducer -> Field Kernel
```

## 10. Terminology Governance

No existing canonical definition is modified. The following are `terminology_change_candidates` for a future Terminology Registry Amendment:

| Candidate | Reason |
| --- | --- |
| Current Cognitive Context / 当前认知上下文 | Required formal L1 interface term; absent from the current registry. |
| Context Inclusion Record | Required traceable-selection record. |
| Context Exclusion Record | Required recoverable exclusion record, not an error/deletion term. |
| Context Sufficiency Result | Required bounded-analysis readiness term, distinct from Fact admission. |
| Minimum Sufficient Field Representation | Required selection principle, distinct from Snapshot completeness. |

The prohibited alternatives are not adopted as formal terms: Working Memory, Situation State, Active World, Context Brain, Cognitive Snapshot, Attention World, Mini World, and Current Reality.

## 11. Phase Boundary

This document creates no runtime, code, runner, verifier, database, model, real data path, Hypothesis, Decision, Experience, Self, Hive, or modification to Field Kernel, Reducer, Admission, Read Model, Registry, Manifest, Baseline, Lifecycle, or Protocol governance.
