# Cognitive Loop continuity contract

Continuity is a set of signals used by Resume Assessment. It is not a new
owner and it is not a duplicated authoritative state model.

## Signals

| Signal | Source owner | Resume question | Loop treatment |
|---|---|---|---|
| Intent continuity | Intent Governance | Does the same governed Intent still apply? | Read-only Intent refs and versions |
| Task / Behavior continuity | Task Manager / Behavior governance | Is the related task or behavior context still the same? | Read-only task/behavior refs; no Task mutation |
| Temporal continuity | Context / Field / Outcome owners | Is the observation and requirement still within its valid time window? | Compare temporal refs and source versions |
| Spatial continuity | Field / Current World owners | Is the relevant spatial context still the same? | Compare spatial and Current World refs |
| Field continuity | Field State owner | Has authoritative Field state changed or been superseded? | Reassess Need and Requirement |
| Role / Perspective continuity | Role / Perspective governance | Does the same role and perspective still govern relevance? | Read-only role/perspective refs |

Emotion modulation, Attention, Safety, Resource, Context, Hypothesis, and
Current World are additional assessment inputs. They do not become Loop-owned
authoritative state.

## Resume rule

```text
PAUSED / WAITING
  -> Resume Assessment
  -> compare Intent / Task-Behavior / Temporal / Spatial / Field / Role-Perspective
  -> compare current authoritative Context / Current World / State Version
  -> reassess Need and Requirement
  -> KEEP | SUPERSEDE | REPLAN | COMPLETE | WAITING
```

`KEEP` means the current minimum Need and Requirement remain valid for the
current source state. `SUPERSEDE` means an old Requirement is stale and cannot
resume Provider invocation. `REPLAN` means changed continuity or evidence
changes the candidate path. `COMPLETE` means this Loop is sufficient. `WAITING`
means no dependency has become admissible.

No resume path may bypass Scope, Resolution, Permission, Resource, Safety, or
Observation admission.

