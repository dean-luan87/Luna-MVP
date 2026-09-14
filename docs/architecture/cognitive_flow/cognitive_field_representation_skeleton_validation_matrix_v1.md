# Cognitive Field Representation Skeleton Validation Matrix v1

| Validation | Static evidence | Failure condition |
| --- | --- | --- |
| Schema | Versioned immutable dataclass and candidate identity | Unknown schema or missing identity |
| Reference integrity | Context required; all reference tuples well-formed; Primitive or Concept lineage exists | Missing/malformed source reference |
| Temporal boundary | Non-empty declared temporal scope | Invented temporal value is not represented as a reference scope |
| Spatial boundary | Non-empty declared spatial scope | Spatial scope omitted or used as State authority |
| Traceability | Provenance source references and matching trace | Trace missing/mismatched |
| Candidate boundary | candidate-only, not-state, not-fact, no authority fields | Any State/Fact/Decision/Action/Memory authority |
| Relevance | Only declared scoped/recoverable relevance classes | Attention/relevance becomes truth, deletion, or action |
| Execution boundary | Skeleton flags all false | Any runtime/model/provider/reducer/mutation operation |

This phase permits static import/file checks only. It creates no runner or verifier execution.
