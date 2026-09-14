# Cognitive Analysis A1/A2 Alignment v1

## 1. Alignment map

```text
A1 Field Foundation
  governed Field Event -> Admission -> Reducer -> Field State
  state/version/transition/history/snapshot foundations
                 |
                 v
A2 Current World Representation
  Read Model/Snapshot view -> Current Cognitive Context
  selection, exclusion, gap, sufficiency, provenance, trace
                 |
                 v
A3 Cognitive Analysis
  admission -> frame -> candidate analysis objects -> future Decision Boundary
```

| Layer | Owned output | A3 relationship |
| --- | --- | --- |
| A1 | Field State, State Version, Transition Record, History Projection, Snapshot foundation. | No direct read or write; A3 receives only their Context-selected references. |
| A2 | Current Cognitive Context, inclusion/exclusion, Information Gap, Context Sufficiency, Envelope. | Sole direct read boundary. A3 may not mutate or rebuild it. |
| A3 | Admission, Frame, Hypothesis Candidate, Competing Set, Evidence Assessment, Gap Refinement, Analysis Sufficiency, Analysis Result. | Candidate-only outputs; no A1/A2 mutation authority. |
| Future Decision | Decision admission and Decision Candidate handling. | Separate downstream authority; A3 only reaches its boundary. |

## 2. Object mapping

| A2 Context source | A3 planned use | Boundary |
| --- | --- | --- |
| `context_id` / `context_version` | Identity and immutable source version for all A3 objects. | No replacement or overwrite. |
| `snapshot_ref` / source snapshot reference | Traceability anchor for analysis. | No direct Snapshot read or mutation. |
| selected Field/Relation/State/History/Evidence refs | Declared analysis scope and evidence selection. | No new source selection from raw stores. |
| inclusion/exclusion records | Explain scoped availability and recoverability. | No record mutation or deletion. |
| Information Gaps | Input to Gap Refinement. | No auto-observation. |
| Context Sufficiency | Analysis Admission prerequisite. | Cannot be promoted by A3. |
| lifecycle, invalidation, refresh, provenance, trace | Staleness, reassessment, and lineage governance. | Cannot be suppressed. |

## 3. Forbidden bypasses and bidirectional boundary

Forbidden direct paths include:

- Raw Observation / Model output -> A3;
- Field Event Candidate -> A3;
- Reducer internal State / mutable Field State -> A3;
- A3 -> Context, Snapshot, Read Model, State Version, Transition, History, or
  Field State;
- A3 -> Camera, OCR, SLAM, network, model, database, device, or action.

The only permitted future return toward world change is candidate re-entry:

```text
Analysis Result
  -> Field Event Candidate
  -> Field Event Admission
  -> Field State Reducer
  -> Field State
```

An Observation Request Candidate similarly stays a candidate. It needs a
separate future observation/permission authority before any external
capability may be considered.

## 4. Cognitive-flow mapping

- **Context**: A2 Current Cognitive Context, never a Hypothesis or decision.
- **Schema**: future A3 Frame and planned object contracts, not an A2 rewrite.
- **Attention**: A2 `attention_context` is read-only A3 scope input.
- **Hypothesis**: A3 Hypothesis Candidate and Competing Hypothesis Set.
- **Current World**: A2 Current World Representation, not A3-owned understanding.
- **Decision**: a future downstream admission boundary only.
- **Learning**: prohibited in A3; no Experience or model update.

## 5. Terminology candidates

The following candidates are recorded for later Terminology Registry change
control only; this phase does not amend the registry:

- Cognitive Analysis System
- Cognitive Analysis Admission
- Cognitive Analysis Frame
- Hypothesis Candidate
- Competing Hypothesis Set
- Analysis Evidence Assessment
- Information Gap Refinement
- Cognitive Analysis Sufficiency Result
- Cognitive Analysis Result
- Decision Admission Boundary

`terminology_registry_amendment_status = deferred`.

## 6. Status

This alignment defines A3's read boundary and candidate return route only. It
does not implement A3, activate runtime, or grant any Decision, Fact, State,
Experience, Self, Hive, model, or external-capability authority.
