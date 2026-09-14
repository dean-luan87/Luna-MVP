# Current Cognitive Context Candidate Skeleton Validation Matrix v1

| Area | Static requirement | Protected boundary |
| --- | --- | --- |
| Schema | All declared reference fields and frozen schema version exist | Unstructured context cannot enter the skeleton |
| Context type | One of six candidate classifications | Classification remains non-Fact and non-Decision |
| Candidate flags | All six fixed flags are true | No Fact, State, Decision, Action, or Memory promotion |
| Reference boundary | Required references are non-empty declarations | No lookup, inference, or source mutation occurs |
| Negative input guard | Raw model/provider, Memory, Fact, Decision, Action, Reducer, and State fields are rejected | No authority bypass |
| Field boundary | No Field/State/Snapshot authority field exists | Context cannot mutate the environment |
| Attention/language boundary | Neither attention authority nor language control field exists | Context is not controlled by either layer |
| Serialization | Sorted-key canonical JSON only | Stable read-only representation |

Static import, schema validation capability, and negative-guard capability are in scope. Context generation, model inference, and real-environment execution are not.
