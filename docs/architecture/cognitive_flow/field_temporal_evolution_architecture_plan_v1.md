# Field Temporal Evolution Architecture Plan v1

## 1. Phase Position

- Phase: `Phase-A2.1-Field-Temporal-Evolution-Planning-v1-001`
- Execution Mode: Planning Only
- Parent domain: L1 Cognitive Flow / Field Kernel
- Status: architecture proposal pending human review

This phase defines the temporal architecture of Field Kernel. It creates no code, runtime, runner, verifier, persistence, database connection, model connection, or change to an existing module.

## 2. Module Position

Field Temporal Evolution describes how a Field, its Units, Relations, and governed States change over time. It answers:

> How did the current Field representation develop from earlier governed states?

It extends Current World Representation with a bounded change trajectory. It does not extend Field Kernel into World Understanding.

```text
Field State at time t0
  -> governed state transition
  -> Field State at time t1
  -> governed state transition
  -> Field State at time t2
  -> Current Field Snapshot + temporal trajectory
```

The current snapshot remains a derived read object. Temporal Evolution organizes its relationship to earlier governed State versions; it does not create another state store.

## 3. Required Non-Equivalences

| Concept | What it records | What it must not become |
| --- | --- | --- |
| Field Temporal Evolution | What changed in a Field representation, when, and under which governed State transition | Experience, causal explanation, prediction, or decision basis by itself |
| Field History | Readable past State and transition record for the Field | Knowledge judgement, case library, or memory-value system |
| Experience | Luna's reviewed understanding of a process, outcome, context, and applicability | automatic summary of all Field History |
| Hypothesis | Possible explanation of why a change occurred | State transition or temporal fact |
| Prediction | Candidate statement about a future State | active State update or scheduled truth |

Example:

```text
Allowed Field Temporal Evolution
2026-01: normal operation
2026-03: partial shop closure
2026-06: broad renovation state
2026-08: re-opened state

Forbidden Experience / Hypothesis content in this layer
"this mall is poorly operated"
"the closures were caused by financial distress"
"the mall will close again"
```

## 4. Temporal Object Planning

The following are future Field Kernel contract objects. They are planning names only; no schema or implementation is created in this phase.

| Planned object | Purpose | Required provenance boundary |
| --- | --- | --- |
| Field State Version | One Reducer-produced State in its effective time context | Reducer output, admitted-event references, evidence/source/trace lineage |
| State Transition Record | Declares the governed predecessor/successor relation between State versions | transition trigger, reducer reference, temporal basis, no causal claim |
| Field History Projection | Read-only ordered view of past State Versions and transitions | query scope, snapshot time, retained provenance |
| Temporal Uncertainty Descriptor | States what is unknown or estimated about time boundaries | unknown/estimated status and the evidence limitation that caused it |
| State Expiration Assessment | Describes whether a current State remains effective, is nearing expiry, or needs reconfirmation | State valid-time and existing temporal/reducer governance references |

None of these objects may independently mutate Field State. The State Transition Record is a representation of a transition that the existing Reducer has already governed; it is not a transition command.

## 5. Time Coordinate Model

The following time coordinates have distinct owners and meanings. They must never be silently substituted for each other.

| Time coordinate | Meaning | Principal owner / origin | Must not be used as |
| --- | --- | --- | --- |
| Event Time | When the reported event occurred in the represented world | Event Candidate, evaluated by Temporal Validity | Snapshot generation time or proof of State validity by itself |
| Observation Time | When an organ/user observed the condition | Observation / Evidence provenance | Event Time when the occurrence is unknown |
| Admission Time | When Admission evaluated and accepted the event | Field Event Admission | Event Time, State start time, or causal timestamp |
| State Valid Time | Interval in which the Reducer-produced State is effective | Reducer output using admitted temporal context | prediction period or Snapshot time |
| Snapshot Time | When a read representation was assembled | Field Kernel / Read Model query | State creation, observation, or event occurrence time |
| Transition Recorded Time | When the governed predecessor/successor relation is represented | Future temporal projection | the moment a real-world change necessarily occurred |

All timestamps must carry a clear timezone when their precise ordering is asserted. If a timestamp is absent, estimated, or non-comparable, the representation must retain that uncertainty rather than inventing an order.

## 6. State Transition Model

State transition is driven only by the existing governed ingress path:

```text
Event Temporal Validity
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> predecessor / successor State relationship
  -> Field Temporal Evolution projection
  -> Field Snapshot / Field History query
```

An admitted event may cause the Reducer to produce:

- an initial State;
- a successor State with a different value;
- a State with changed validity information;
- an Uncertain State when governed information is insufficient for a more precise current description;
- no State change.

The transition layer records only the result and its governed temporal basis. It must not infer the cause of a sequence, select a future state, or make model prediction an active State.

Illustrative value path, not a mandated universal state machine:

```text
operating
  -> renovating
  -> closed
  -> operating
```

The values are domain descriptions. Their transition is only valid when a new Admitted Event is reduced by the existing Reducer.

## 7. Field History Boundary

Field History is a read-only, time-ordered projection of prior governed State Versions and transition records for a Field. It permits statements such as:

- “the shopping mall had a broad renovation State in June 2026”; and
- “the entrance State changed from accessible to closed between two governed State versions.”

It prohibits:

- “the shopping mall is poorly operated”;
- “this sequence proves a cause”;
- “similar Fields will behave this way”; and
- an Experience, policy, or value judgement generated from the record.

History retention, archival storage, replay format, and cross-Field comparison remain deferred. A2.1 defines the semantics only, not a history database or event log.

## 8. State Expiration and Reconfirmation

A State's `valid_time` is distinct from its event and observation times. A future implementation must support these planned representation outcomes:

| Condition | Planned representation outcome | Required boundary |
| --- | --- | --- |
| Current time remains inside known valid interval | State remains Active in current representation | No prediction implied. |
| Known valid interval ends without successor State | State becomes Expired or requires reconfirmation | Expiry does not fabricate a replacement value. |
| Temporary condition has short explicit validity, such as a two-hour closure | Reconfirmation need becomes visible after expiry | No automatic “open” state. |
| Longer condition has estimated duration, such as renovation | Estimated end is represented as uncertainty/estimate | No automatic future re-opening. |
| Validity is missing or incomplete | State remains temporally Uncertain | No default Active/Expired conclusion. |

Expiration is temporal representation governance, not causal interpretation. A State can be historically retained after it is no longer active, without being treated as current.

## 9. Temporal Uncertainty

Temporal Evolution must represent uncertainty as an explicit condition rather than a hidden fallback.

| Uncertainty form | Meaning | Allowed representation |
| --- | --- | --- |
| Unknown Start Time | A condition is observed but its actual beginning is not known | Observation/Admission times may be retained; State Valid Time start is marked unknown. |
| Unknown End Time | A condition is known but no end can safely be asserted | Open-ended or unknown valid-time end; no predicted closure. |
| Estimated Duration | A duration is supplied as an estimate | Retain estimate source, scope, and uncertainty; do not convert it to a future State. |
| Ordering Ambiguity | Two observations/events cannot safely be ordered | Preserve unresolved ordering; do not construct a false transition. |
| Reconfirmation Required | Current validity has degraded or elapsed | Surface a need for later governed input; do not dispatch work automatically. |

## 10. Existing Module Relationship

| Module | Temporal responsibility |
| --- | --- |
| Field Event Admission / Temporal Validity | Event ingress: timestamp sufficiency, ordering, duplication, expiry, and eligibility before admission. |
| Field State Reducer | Sole State mutation authority; produces State from Admitted Events and remains owner of governed State change. |
| Field Temporal Evolution | Post-reduction representation of State Versions, transitions, validity, expiry, uncertainty, and History projection. |
| Field State Read Model | Read-only access to current temporal State and future History/Snapshot projections. |
| Cognitive Analysis | Later read-only consumer that may formulate Hypotheses from a trajectory; it cannot write a temporal State or transition. |
| Experience System | Later owner of reviewed learning from outcomes; it cannot be inferred or written by Field History. |

## 11. Reserved Future Extensions

- Temporal Graph;
- State Transition Graph;
- Field Evolution Pattern.

These names reserve compatibility only. They do not authorize predictive models, causal analysis, cross-Field pattern claims, Experience construction, or autonomous action.

## 12. Phase Boundary

This plan modifies no existing Field Kernel, Reducer, Read Model, Admission, Temporal Validity, database, registry, manifest, baseline, lifecycle, protocol, or runtime behavior. Human architecture review is required before a temporal-evolution implementation phase.
