# Cognitive Concept Layer Provenance Closure v1

## Required chain

`Concept Candidate -> Primitive Reference -> Translation Reference -> Evidence Reference -> Source Capability`.

The chain is structural and candidate-only. It does not resolve real Evidence, prove factual truth, or authorize Field State update.

## v1 fixture mapping

| Chain element | Serialized location |
| --- | --- |
| Concept Candidate | `candidate.concept_id` |
| Primitive Reference | `candidate.primitive_refs` |
| Translation Reference | `candidate.provenance.translation_refs` |
| Evidence Reference | `candidate.provenance.source_refs` |
| Source Capability | `candidate.provenance.source_capability_refs` |
| Trace continuity | `candidate.provenance.trace_ref == candidate.trace_ref` |

Missing any element or mismatching trace is a blocker. Provider identity remains provenance only and is prohibited from the Concept taxonomy.
