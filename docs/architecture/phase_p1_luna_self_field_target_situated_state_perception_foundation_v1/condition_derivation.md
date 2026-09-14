# Condition Derivation

The first scope is deliberately limited to the conditions already used by
text-recognition minimum-condition resolution:

| Condition | Input candidate | Derivation |
|---|---|---|
| `condition:target-visible:v1` | `target_visibility_candidate` | `VISIBLE` → `SATISFIED`; `NOT_VISIBLE`/`PARTIAL` → `UNSATISFIED`; otherwise `UNKNOWN` |
| `condition:target-complete:v1` | `target_completeness_candidate` | `COMPLETE` → `SATISFIED`; incomplete/partial/insufficient → `UNSATISFIED`; otherwise `UNKNOWN` |
| `condition:target-scale-adequate:v1` | `target_scale_candidate` | `ADEQUATE` → `SATISFIED`; small/inadequate → `UNSATISFIED`; otherwise `UNKNOWN` |
| `condition:stable-relation:v1` | `stability_candidate` and relative motion | `STABLE`/low motion → `SATISFIED`; `UNSTABLE`/high motion → `UNSATISFIED`; otherwise `UNKNOWN` |

`UNKNOWN` is never added to `satisfied_condition_refs`.  The generic
Feasibility evaluator treats required unknown conditions as not feasible and
includes them in the condition-gap path.
