# Cognitive Analysis System Architecture v1

## 1. Position

The Cognitive Analysis System is the A3 L1 Cognitive Flow layer. It reads a
governed **Current Cognitive Context** and produces governed analysis
candidates: possible explanations, alternative hypotheses, evidence
assessments, information-gap refinements, sufficiency outcomes, and an
analysis result.

It answers what the currently governed information may mean, which
explanations are reasonable, which evidence supports or contradicts them,
which alternatives remain open, and whether the available information is
sufficient for a provisional analysis result.

It does not explain the world as a fact owner, choose or execute an action,
write Experience, or modify Self or Hive.

```text
Cognitive Analysis != Current World Representation
Hypothesis Candidate != Field Fact
Analysis Result != Decision
Information Gap Refinement != Observation Execution
```

## 2. Main chain

```text
Current Cognitive Context
  -> Cognitive Analysis Admission
  -> Cognitive Analysis Frame
  -> Hypothesis Candidate + Analysis Evidence Assessment
  -> Competing Hypothesis Set + Information Gap Refinement
  -> Cognitive Analysis Sufficiency Result
  -> Cognitive Analysis Result
  -> Decision Admission Boundary (future, separate authority)
```

Every arrow is reference-preserving and read-only with respect to A1 and A2.
The analysis chain neither creates Field State nor replaces the A1 admission
and reducer path.

## 3. Direct input boundary

The only direct input object is `CurrentCognitiveContextV1`. A3 may read only
the Context and its declared fields/references:

- `context_id`, `context_version`, `snapshot_ref` / `source_snapshot_ref`;
- field, subject, task, goal, attention, and temporal scopes;
- selected Field, Relation, State, History, and Evidence references;
- inclusion and exclusion records;
- Information Gaps and Context Sufficiency Result;
- lifecycle, invalidation, refresh, provenance, and trace data.

A3 must not bypass Context to read Raw Observation, raw model output, Field
Event Candidate, Reducer-internal state, mutable Field State, databases,
cameras, OCR, SLAM, network models, or other external capabilities. A Context
reference is provenance, not permission to dereference an underlying mutable
store.

## 4. Layered responsibilities

| Layer | Responsibility | Explicit non-authority |
| --- | --- | --- |
| Analysis Admission | Determine whether the supplied Context is analyzable. | Does not repair or refresh Context. |
| Analysis Frame | Define a traceable, short-lived read boundary for one analysis. | Is not Working Memory, a Context copy, or long-term storage. |
| Hypothesis / Evidence | Represent candidate explanations and their support, contradiction, and uncertainty. | Does not alter Evidence or turn confidence into Fact. |
| Competing / Gap | Preserve alternatives and refine material missing information. | Does not force one answer or execute observation. |
| Sufficiency / Result | Govern whether a result may be emitted and record its provisional status. | Is not truth validation, Decision, or Action. |
| Decision Boundary | Reserve a future handoff for eligible analysis results. | Does not select, authorize, or execute a decision in A3. |

## 5. Admission and output governance

`CognitiveAnalysisAdmissionResultV1` evaluates Context existence, lifecycle
status, staleness, refresh requirement, Context Sufficiency, critical gaps,
read permission, provenance, trace, and source-Snapshot traceability. Its
states are `admitted`, `conditionally_admitted`, `rejected`, `blocked`, and
`unknown`.

An insufficient Context cannot yield a valid analysis conclusion. A stale
Context cannot silently be treated as current. Revoked Evidence must lower
admission or require refresh; it may not be removed from history to simulate
validity.

## 6. A1, A2, and Decision relationship

| System | Role for A3 | A3 may not do |
| --- | --- | --- |
| A1 Field Foundation | Owns governed world-state mutation, versioning, history, and snapshot foundations. | Read it directly or write any A1 object. |
| A2 Current World Representation | Supplies the sole direct input: a scoped, read-only Context. | Mutate Context, Snapshot, Envelope, or Read Model result. |
| Future Decision | Receives only sufficiently governed candidate outputs through a separate admission boundary. | Be selected, authorized, or executed by A3. |

If a future analysis identifies a possible world change, it must return only
through the already frozen path:

```text
Analysis Result
  -> Field Event Candidate
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

## 7. Non-responsibilities

A3 must not:

- claim a Hypothesis Candidate or Interpretation Candidate is a Fact;
- mutate Field State, State Version, Transition Record, History Projection,
  Snapshot, Read Model result, Context, or Envelope;
- perform causal truth confirmation, prediction, decision selection, action,
  device control, TTS, navigation, or external output;
- invoke observation, Camera, OCR, SLAM, Network, Model, database, or runtime;
- create Experience, update a model, modify Self, or coordinate Hive.

## 8. Status

This is architecture planning only. It creates no runtime, contract schema,
implementation, runner, verifier, real inference, model call, database, or
network connection.
