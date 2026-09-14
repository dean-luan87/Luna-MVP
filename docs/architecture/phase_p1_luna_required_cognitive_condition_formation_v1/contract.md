# Required Cognitive Condition Formation Contract v1

## Reused boundary

- `GoalContextV1` remains a governed Goal input and is not mutated。
- `CurrentWorldCandidateV1`、Minimum Relevant Cognitive View 的 selected
  refs，以及 Self/External selected information can provide the current
  situation as explicit signals。
- `ARouteMinimumRelevantCognitiveViewCandidateV1` continues to own minimum
  view selection。
- `ARouteInformationNeedFormationRequestV1` and its existing adapter continue
  to own Information Need formation。

新增的 `GovernedObjectiveConditionRuleV1` 是 objective governance 到 A-Route
formation 的薄语义输入，不是 Condition Ontology。规则以显式 references
表达适用目标、activation、suppression、satisfaction 和 minimum-set 语义。

## Formation algorithm

```text
objective_refs
  = exact refs of Goal / Intent / Concern
situation_refs
  = selected coverage / explicit current-world condition signals
    + governed Self / External / Role / Context / Field signals

requirement status
  = objective applies
  + activation_all ⊆ situation_refs
  + activation_any intersects situation_refs (when declared)
  - suppression intersects situation_refs

satisfaction status
  = ANY alternative_satisfaction_basis_refs ∩ situation_refs
    when governed alternative bases are declared
  = satisfaction_coverage_refs ⊆ situation_refs
    otherwise (legacy exact-coverage compatibility)

actual satisfaction coverage
  = only the matched current coverage refs that caused satisfaction

active required set
  = lowest selection_rank candidate per governed minimum_set_ref
```

The engine operates on exact references and never derives meaning from a string.
An opaque Context, Current World, or Minimum View envelope ref is retained as
context/provenance only; only an explicit governed condition signal can affect
formation.

`ACTIVE_REQUIRED` candidates are the currently necessary minimum set, even when
their `satisfaction_status` is `SATISFIED`. Satisfaction is separately exposed
through `satisfied_condition_refs`; it never removes requiredness. Unselected
alternatives remain `DORMANT`, and dormant information is recoverable rather
than deleted.

`GovernedObjectiveConditionRuleV1.alternative_satisfaction_basis_refs` is an
optional, explicit set of governed satisfaction alternatives for one semantic
requirement. When non-empty, any currently present basis satisfies that
requirement. `satisfaction_coverage_refs` on the candidate records only the
actual matched basis, not every declared alternative. Rules without this field
retain the prior exact `satisfaction_coverage_refs` behavior. This is not an
acquisition-path, capability, observation, evidence-fusion, confidence, or
Boolean-expression contract.

## Boundaries

The output is candidate-only, read-only and non-Truth. It does not mutate Goal,
Intent, Concern, Role, Context, Field, Self, Current World, Memory or PCN. It
does not form Information Need, Information Gap, Observation Demand, Capability
Requirement, Decision, Task or Action.

The formation output can be passed as explicit governed condition input to the
existing Minimum Relevant Cognitive View and Information Need APIs. It must be
upstream of Need Formation; no current Information Need is accepted as a
formation input, avoiding a semantic cycle。

`Required Cognitive Condition ≠ Satisfaction Basis ≠ Information Need ≠
Information Gap ≠ Acquisition Path`。
