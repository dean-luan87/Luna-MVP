# Cognitive Concept–Field Mapping Matrix v1

| Concept type | Eligible Field-facing reference | Context / temporal binding | Spatial binding | Representation effect | Forbidden conversion |
| --- | --- | --- | --- | --- | --- |
| Pattern Candidate | `concept_ref` attached to a bounded query annotation | Context/snapshot and source window retained | Existing Unit/Relation refs only | Candidate pattern context in Cognitive Query View | Pattern -> Fact/State/Event |
| Situation Candidate | Contextual scene interpretation reference | Task/attention/temporal scope and uncertainty retained | Existing Field/Unit scope only | Candidate situation annotation | Situation -> world conclusion/Decision |
| Relationship Candidate | Candidate relationship interpretation reference | Source context and relation scope retained | Existing declared relation refs only | Query-side relation meaning context | Candidate relation -> structural relation or causal claim |
| Risk Candidate | Candidate risk-pattern reference | Staleness, coverage, and uncertainty mandatory | Existing target/location refs only | Candidate warning context; no action authority | Risk -> safety Fact/Decision/Action |
| Context Candidate | Candidate context interpretation reference | Binds to immutable Context version | Existing scope references only | Selection/analysis context annotation | Context -> Context/Snapshot writeback |
| Goal Candidate | Candidate goal-related interpretation reference | Goal Context reference and limitation retained | Existing target refs only | Bounded query context only | Goal -> task command/Decision/Action |

## Binding eligibility

Only a `validated_candidate` may be offered as a Field-facing reference. Validation demonstrates contract integrity, traceability, and boundary preservation only. It does not make the Concept true, admitted, or State-eligible.

## Confidence and uncertainty matrix

| Metadata | Propagates to binding | May influence Field State/Snapshot | May become admission authority |
| --- | --- | --- | --- |
| Candidate confidence | Yes, unchanged and labelled candidate metadata | No | No |
| Candidate uncertainty | Yes, unchanged and explicit | No | No |
| Temporal uncertainty/staleness | Yes, as source scope limitation | No | No |
| Evidence/provenance trace | Yes, append-only reference chain | No | No |

## Trace mapping

`Concept Ref -> Primitive Refs -> Translation Refs -> Evidence Refs -> Source Capability Refs -> Context/Snapshot Scope -> FieldConceptReferenceBindingCandidate`.

Any missing element, trace mismatch, unknown authorization scope, or attempt to materialize a binding as State blocks future binding admission.
