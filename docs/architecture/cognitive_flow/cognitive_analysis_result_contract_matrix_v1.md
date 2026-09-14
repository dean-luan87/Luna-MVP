# A3 Cognitive Analysis Result Contract Matrix v1

| dimension | contract requirement | permitted meaning | prohibited meaning |
| --- | --- | --- | --- |
| Input | `input_reference` and `evidence_reference` are required and traceable | governed Context/Question and Evidence references | raw model output, raw Field State access, or evidence mutation |
| Processing Boundary | contract Validator is pure structural validation | field presence, reference presence, uncertainty/provenance, authority flags | Runtime execution, inference, model call, State write |
| Output | `Analysis Result Candidate` includes candidate output, uncertainty, provenance, confidence, warning | candidate cognitive signal | Fact, Event, Field State, Decision, Action, Memory update |
| Consumer | future Cognitive Flow reader under separate handoff governance | read a candidate with its limits | treat confidence as truth, execute an Action, or update State |
| Authority | all forbidden authority flags are explicitly false | no mutation authority | Fact creation/mutation, Decision creation, Action execution, State mutation, Memory update |
