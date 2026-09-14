# Legacy retirement safety levels

| Candidate | Level | Reason |
|---|---|---|
| Dynamic Flow semantic-looking output fields | R1–R2 | A wrapper exists, but direct fixtures/adapters still consume fields |
| Dynamic Flow `_select_next_need` | R1 | A Need bridge exists; caller cutover not complete |
| Dynamic Flow `_reconsideration` | R1 | A/B candidate types exist; old fixtures still depend on construction |
| Loop `_local_disposition` | R1 | semantic replacement is documented, not runtime-cut over |
| Loop resume decision derivation | R1 | Resume candidate implementation still derives decisions |
| Loop growth semantic decisions | R2 | guard structures exist, owner split still requires adapter cutover |
| Loop closure package/history mechanics | R2 | candidate-only closure and package boundary verified |
| A Route stage orchestration | R2 | handoff behavior is verified and remains useful |
| Product Loop semantic feedback | R1 | existing tests and downstream routes still consume it |
| Trace helper duplication | R0 | documentation/consolidation issue only |

No current candidate is R5. R5 requires R3 dependent fixture migration and R4 runtime caller migration.

