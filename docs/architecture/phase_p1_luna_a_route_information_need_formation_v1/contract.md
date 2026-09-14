# Information Need Formation Contract

## Reused canonical assets

- `GoalContextV1.success_condition_refs`：当前目标要求的 governed cognitive
  conditions。
- `CurrentWorldCandidateV1`：只读的当前认知世界 candidate；其 id、trace 和
  candidate-only boundary 作为 Need 的 state version/provenance 来源。
- `CognitiveNeedCandidateV1`：既有 Need candidate envelope，未创建 V2、Need
  ontology 或新的 canonical owner。
- `validate_cognitive_need`：既有 Need contract validator。

新增的 `ARouteInformationNeedFormationRequestV1` 与 result 是 A-Route 局部
integration boundary，不是第二套 Need contract。request 中的
`current_cognitive_coverage_refs` 是 Current World 的 governed coverage
projection，不是 Information Need，也不是 Information Gap。

## Formation rule

```text
required_conditions
  = ordered_unique(
      goal_context.success_condition_refs,
      governed_objective_condition_refs,
      governed_role_condition_refs
    )

necessary_unknowns
  = required_conditions - current_cognitive_coverage_refs
```

差集非空时，复用 `CognitiveNeedCandidateV1`，并将
`state_version_ref` 指向当前 `CurrentWorldCandidateV1.current_world_id`。
差集为空时返回 `NO_ACTIVE_NEED`，不制造无意义的重复 Need。

## Semantic boundaries

- Information Need ≠ Goal。
- Information Need ≠ Observation Request。
- Information Need ≠ Capability Requirement。
- Information Need ≠ Information Gap。
- Information Need ≠ Evidence。
- Current World coverage can suppress a Need, but formation never mutates the
  Current World。
- Intent, Concern and Task refs are retained as governed source context; they do
  not become conditions through string parsing. A task-specific condition may
  participate only when supplied as an explicit governed condition signal。
- Opaque Context refs are preserved only as provenance/source refs; they are not
  interpreted by string matching。
- Role affects formation only when a governed role condition signal is supplied；
  an ungoverned Role ref is not guessed。

The candidate remains `CURRENT_MINIMUM_NECESSARY_NEED` and `candidate_only=true`.
It does not declare truth or execute any observation, capability, task, or action。

## Closure boundary

User-terminal verification closed the declared formation scope. The closure does
not promote this adapter into a Need Admission/Registration owner and does not
claim upstream autonomous formation of the required condition signals。

The later Required Cognitive Condition Formation boundary now supplies a
governed, state-sensitive candidate input when present. That addition does not
change this adapter's subtraction contract or its ownership。

Self-conditioned objective formation, Goal-conditioned Minimum Self/External
View, pre-observation Attention, and Observation Demand Formation remain outside
this closure。
