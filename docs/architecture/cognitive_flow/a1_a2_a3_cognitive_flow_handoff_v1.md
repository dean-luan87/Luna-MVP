# A1 to A2 to A3 Cognitive Flow Handoff v1

## Frozen flow

```text
A1 Field Foundation
  -> A2 Current World Representation
  -> A3 Cognitive Analysis
```

| Stage | Frozen responsibility | May not do |
| --- | --- | --- |
| A1 Field Foundation | Govern world-state mutation, structure, versioning, temporal transition, history projection, and snapshot foundation. | Explain, hypothesize, decide, act, or bypass Admission/Reducer. |
| A2 Current World Representation | Read, organize, select, and compress governed representation into a read-only Context and Envelope. | Write state, infer causes, conclude truth, or decide action. |
| A3 Cognitive Analysis | Generate analysis candidates from a Context and explicit uncertainty. | Mutate world representation or treat candidates as facts. |

## A3 read boundary

A3's direct input is **Current Cognitive Context**. The Context must retain
traceable references to:

- `source_snapshot_ref`;
- selected field references;
- inclusion records;
- exclusion records;
- Information Gap records;
- Context Sufficiency records;
- provenance;
- `trace_ref`.

A3 may use these references to form analysis candidates. It must not directly
write Field State, State Version, Transition Record, History Projection, Field
Snapshot, Read Model result, Current Cognitive Context, or Current World
Representation Envelope.

## Candidate-only A3 outputs

Future A3 outputs may include Hypothesis Candidate, Interpretation Candidate,
Competing Hypothesis Set, Gap Refinement, Analysis Result, and Decision
Candidate. None of these is a Fact, Field State, or automatic action.

When an analysis result identifies a possible world change, the only permitted
return route is:

```text
Analysis Result
  -> Event Candidate
  -> Admission
  -> Field State Reducer
  -> Field State
```

Direct `Cognitive Analysis -> Field State` is prohibited.

## Insufficiency and unknown-data guardrails

- If Context Sufficiency is not met, A3 must not produce a valid analysis
  conclusion.
- Unknown information must remain unknown; it cannot be silently filled as
  fact.
- Missing information may produce only Gap Refinement or an Observation
  Request Candidate. It must not automatically create or update Field State.

## Handoff status

A1 supplies governed world-state representation. A2 supplies a scoped,
read-only representation of that world. A3 remains a future analysis boundary;
it has no writeback path and no implementation authority in this handoff.

This document does not activate runtime integration, production readiness, or
any decision/action capability.
