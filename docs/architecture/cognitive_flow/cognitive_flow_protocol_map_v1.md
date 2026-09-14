# Cognitive Flow Protocol Map v1

## Protocol Principles

Every protocol is versioned, candidate-preserving, traceable, and explicitly owned. A protocol may describe a decision candidate without authorizing decision execution. No protocol grants an external model, Hive, or capability attachment fact authority.

| Protocol | Input | Output | Authority | Lifecycle | Mutable? | May influence Decision? |
| --- | --- | --- | --- | --- | --- | --- |
| Observation Event Protocol | organ/model/user observation candidate, source, time | Observation Event candidate | Perception Admission | received → normalized → retained/rejected | original event immutable; correction is a new event | indirect only, as evidence input |
| Evidence Reference Protocol | artifact refs, source chain, provenance, quality signals | Evidence Reference candidate | Perception Admission / Evidence governance | proposed → reviewed → retained/retracted | references append/retract by new records; no silent rewrite | indirect only |
| Field Identity Protocol | field anchors, scope candidates, evidence refs | Field identity candidate | Field Kernel | proposed → resolved/unresolved → superseded | identity history append-only | indirect only |
| Field State Protocol | admitted events, temporal snapshot, policy snapshot | Field State candidate, read projection candidate | Field State Reducer only | candidate → revised/suspended/expired/revoked | only Reducer can produce state transition candidates | indirect only through governed reads |
| Hypothesis Protocol | Field State read, evidence refs, questions, assumptions | Hypothesis candidate with alternatives | Cognitive Analysis | proposed → tested/supported/weakened/retired | status changes are new analysis records | yes, as a bounded delivery input, never decisive alone |
| Difference Point Protocol | expected vs observed state, evidence refs | Difference Point candidate | Cognitive Analysis | detected → investigated → explained/unresolved | append investigation history | yes, as an analysis signal |
| Information Gap Protocol | hypothesis, field read, task context | Information Gap candidate | Cognitive Analysis | identified → requested → satisfied/deferred/expired | append resolution evidence | yes, to request exploration, not action |
| Exploration Request Protocol | information gaps, safety/task constraints, available capability refs | exploration request candidate | Cognitive Analysis; Task Manager governs execution | proposed → authorized/rejected/deferred → outcome-linked | only lifecycle transitions by owning governance boundary | yes, only after authorization |
| Cognitive Delivery Protocol | hypotheses, gaps, alternatives, task/self constraints | explanation/recommendation/clarification candidate | Cognitive Analysis | drafted → reviewed → delivered/superseded | delivery record immutable; revision creates new record | yes, but never directly executes action |
| Outcome Event Protocol | executed/delivered result, observation/evidence refs, trace | outcome event candidate | Perception Admission / authorized executor boundary | received → admitted/deferred/rejected → episode-linked | event immutable; correction is new event | indirect only, for learning |
| Experience Record Protocol | outcome events, context, hypotheses, evidence, review | Experience Episode candidate | Experience System | captured → reviewed → retained/withdrawn | append review/retraction records | indirect only, as reuse input |
| Experience Branch Protocol | episodes/kernels, similarity/conflict/lineage refs | Experience Branch candidate | Experience System or Hive association boundary | proposed → related/conflicted/merged-as-reference → retired | links are versioned; no destructive collapse | indirect only; never a decision vote |

## Cross-Protocol Guards

- Protocol outputs retain `candidate_only` until an explicitly authorized owning process changes their lifecycle.
- Evidence references never become facts by being repeated, vectorized, or associated with a model output.
- A Hypothesis may request more information but may not mutate Field State or launch a tool.
- Cognitive Delivery may explain alternatives and uncertainty but may not bypass Task Manager or human authorization.
- Hive receives experience references only through explicit branch protocols; it cannot write backward into local decisions.

