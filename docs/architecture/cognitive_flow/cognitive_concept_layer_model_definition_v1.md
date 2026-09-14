# Luna Cognitive Concept Layer Model Definition v1

## Concept Candidate

`ConceptCandidate` is planned with `concept_id`, `concept_type`, `primitive_refs`, `context_refs`, `relation_refs`, `semantic_pattern`, confidence, uncertainty, provenance, trace reference, and candidate status. It is fixed as `candidate_only=true` and `fact_status=not_fact`.

It must not contain `fact_id`, `decision_id`, `action_id`, `state_write_target`, or `memory_target`.

## Pattern Model

```text
Primitive Cluster
        ↓
Pattern Candidate
        ↓
Concept Candidate
```

For example, Person Entity + Approaching State/Event + Near Relation + Night Context may express `unknown_approach_pattern`. The Pattern remains a possible interpretation, retains primitive/evidence references and uncertainty, and does not establish risk, intent, identity, or world truth.

## Concept Compression

Compression is a future representation structure, not an inference engine:

`person detected + distance 3m + speed increasing + unknown identity`
→ `unknown person approaching` candidate
→ `possible risk` candidate.

Each layer preserves its primitive/evidence lineage, uncertainty, alternatives, and candidate status. Compression cannot remove uncertainty or promote a high-level label to Fact/Decision.

