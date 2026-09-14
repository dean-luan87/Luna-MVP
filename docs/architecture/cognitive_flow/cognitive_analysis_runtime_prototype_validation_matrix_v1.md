# A3 Cognitive Analysis Runtime Prototype Validation Matrix v1

| validation area | required check | failure condition | authority effect |
| --- | --- | --- | --- |
| Input trace | Context, every Evidence reference, and Analysis Question reference are preserved in order | missing, changed, or untraceable reference | block candidate output |
| Output contract | Result Candidate passes the existing Result Contract Validator | missing candidate field, evidence, uncertainty, provenance, warning, or candidate boundary | block candidate output |
| Permission boundary | all prototype write/external/authorization flags are false | any model, network, database, Fact, Decision, Action, State, Memory, Training, or authorization flag is true | blocker |
| Authority boundary | candidate authority flags remain false despite local prototype execution | Fact/Decision/Action/State/Memory authority appears | blocker |
| Determinism | canonical serialization is defined and result declares deterministic output | non-canonical or non-deterministic declaration | block candidate output |

`runtime_executed=true` is valid only in the fixture-only prototype envelope; it is not an authority flag and cannot enable a write path.
