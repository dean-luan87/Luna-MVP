# A3 Evidence Context Translation Layer Controlled DryRun Validation Matrix v1

| validation area | required condition | failure condition |
| --- | --- | --- |
| Evidence reference | each case has one traceable Evidence reference | missing/empty/reference substitution |
| Translation output | Skeleton returns a primitive candidate envelope | missing envelope or primitive type mismatch |
| Candidate-only | `candidate_only=true`, `fact_status=not_fact`, `translation_not_executed` | Fact/confirmed/active claim |
| Provenance | source refs, source capability refs, and trace retained | missing/hidden source or trace |
| Traceability | candidate → request/translation record → Evidence → source capability is reconstructable | broken chain |
| Permission boundary | all execution, external, Fact, Decision, Action, State, and Memory flags are false | any forbidden flag true |
| Negative Guard | Guards 1–5 are declared and structurally validated | guard absent or violated |
| Deterministic output | canonical JSON equals its normalized serialization | formatting/order drift |
