# Cognitive Concept Layer Validation Contract v1

## Source input

The only input is `cognitive_concept_dryrun_result_v1.json`. It must be frozen fixture-only DryRun evidence and retain its DryRun phase/schema identity.

## Closure output

The output is a canonical validation record containing per-case schema, semantic mapping, Primitive/Context reference, provenance, lifecycle, provider-taxonomy, and trace results. It is validation evidence, not a Concept Candidate and not a world-state input.

## Provenance designation

For this v1 fixture contract, `candidate.provenance.source_refs` is the abstract Evidence Reference set defined by the Translation provenance contract. Closure evidence records it as `evidence_refs_v1`; no provider payload or real Evidence resolution is performed.

## Language boundary

`Concept Candidate -> Future Language Primitive` is a design interface only. Language Encoding, Generation, Mutation, Admission, and reverse `Language -> Concept` generation are prohibited.

## Blocker condition

Any missing Concept, Primitive, Translation, Evidence, Source Capability, or matching trace reference is a blocker. Any candidate-to-Fact/Decision/Action/State/Memory/Learning escalation is a blocker.
