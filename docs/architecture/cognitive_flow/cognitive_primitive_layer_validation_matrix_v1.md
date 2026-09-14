# Luna Cognitive Primitive Layer Validation Matrix v1

| validation class | assertion | failure condition | boundary result |
| --- | --- | --- | --- |
| Schema Validation | required primitive identity/type, source/context refs, provenance, trace, candidate status, uncertainty are present | missing required reference or hidden source/trace | blocker candidate |
| Semantic Boundary Validation | Primitive family is Entity/Relation/State/Event/Situation candidate and does not state final world truth | Fact/confirmed identity/causal certainty/Decision meaning | blocker candidate |
| Traceability Validation | Translation/Evidence → Primitive source, Context, provider provenance, and trace chain remain visible | source substitution, provider identity converted to Entity, trace loss | blocker candidate |
| Negative Guard: Evidence ingress | Evidence/Model output cannot enter internal Primitive core without Translation reference boundary | raw payload/provider output used as Primitive authority | blocker candidate |
| Negative Guard: Fact | Primitive cannot create, mutate, or imply Fact | Fact status/authority flag or implicit promotion | blocker candidate |
| Negative Guard: Decision | Primitive cannot gain Decision/Action permission | Decision/Action field, command, or authority | blocker candidate |
| Negative Guard: State | Primitive cannot mutate Field State, Snapshot, or Context | writeback request or alternate mutation path | blocker candidate |
| Determinism / evolution | extension preserves stable taxonomy/version, candidate semantics, and compatibility evidence | provider-schema-driven taxonomy drift or unreviewed breaking change | review/blocked candidate |

Validation produces boundary evidence only. It does not admit a Primitive, execute Runtime, write State, or authorize a consumer.

