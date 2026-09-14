# Current Canonical Semantics Analysis

## Required Cognitive Condition

`GovernedObjectiveConditionRuleV1` is the governed input at:

`capabilities/midplatform/core/a_route_orchestration/a_route_required_cognitive_condition_formation_types_v1.py:29-48`

Its semantic fields are `condition_ref`, objective applicability, activation /
suppression refs, `satisfaction_coverage_refs`, `minimum_set_ref`, and
`selection_rank`.

The engine at:

`capabilities/midplatform/core/a_route_orchestration/a_route_required_cognitive_condition_formation_engine_v1.py:48-78`

does exact-reference evaluation:

```text
objective applies
∧ activation conditions hold
∧ no suppression condition
→ ACTIVE_REQUIRED candidate

satisfaction_coverage_refs ⊆ current situation refs
→ candidate satisfaction_status = SATISFIED
```

It then selects the lowest-ranked candidate per `minimum_set_ref` at lines
141-160. This is a governed minimum-set selection mechanism. It is not an
alternative satisfaction-basis mechanism for one shared requirement.

The result correctly separates `active_required_condition_refs` from
`satisfied_condition_refs` at lines 147-150 of the type contract. Satisfaction
does not erase requiredness. However, the identity of the required item is
still the individual `condition_ref`.

## Information Need

`ARouteInformationNeedFormationAdapterV1` at
`capabilities/midplatform/core/a_route_orchestration/a_route_information_need_formation_adapter_v1.py:58-66`
forms:

```text
required = goal success conditions
         + governed objective conditions
         + governed role conditions

necessary_unknowns = required - current_cognitive_coverage_refs
```

It creates one `CognitiveNeedCandidateV1` when the difference is non-empty.
The candidate carries generic `missing_information_class` and
`required_evidence_class` metadata, but not an alternative-basis graph or
acquisition-path semantics.

Therefore Need currently binds primarily to an unsatisfied governed condition
set, not directly to an evidence source or acquisition path.

## Branch

`form_governed_cognitive_branches` forms a branch from explicit basis material.
For this chain, each unresolved `(gap_ref, need_refs)` pair becomes one
`UNRESOLVED_INFORMATION_GAP` branch. The branch identifies the exploration line
for a gap; it does not identify a signage/flow/spatial acquisition strategy.

## Acquisition Strategy

`GovernedAcquisitionBasisV1` and
`InformationAcquisitionStrategyCandidateV1` preserve explicit strategy basis,
branch, Need, Gap, capability-class, opportunity, and contribution refs.
The strategy formation engine projects each valid explicit basis for an
admitted branch. It does not decide whether bases are alternative, redundant,
complementary, or jointly sufficient.

## Current Cognitive Coverage

Coverage is a read-only exact-ref set supplied in
`CurrentCognitiveSituationV1.current_cognitive_coverage_refs` and consumed by
the Required Condition and Need formation boundaries. In the Sandbox fixture,
coverage refs are intentionally identical to condition refs through
`satisfaction_coverage_refs=(condition_ref,)`.

Consequently current coverage can prove that a condition token is covered, but
it cannot currently express that one semantic requirement is covered by one of
several governed basis types. It is closer to condition/evidence coverage than
to a rich satisfaction-basis relation.

## Ownership and authority

| Semantic responsibility | Current owner | Review finding |
| --- | --- | --- |
| Required condition applicability | A-Route Cognitive Responsibility | Keep |
| Condition satisfaction against current coverage | Required Condition formation / A-Route cognitive side | Keep |
| Need formation from required minus coverage | A-Route Information Need Formation | Keep |
| Gap-to-branch candidate formation | Cognitive Flow Branch Formation | Keep |
| Branch admission | Cognitive Flow Branch Governance | Keep |
| Strategy candidate projection | Cognitive Flow Strategy Candidate Formation | Keep |
| Overall continuation / stop sufficiency | Existing Sufficiency / Stop owner | Keep |
| Strategy selection / coordination | Not yet implemented | Must not own semantic sufficiency |

All reviewed assets are candidate/read-only boundaries. The proposed review
does not grant Truth, Field, Current World, Memory, Decision, Task, or Action
authority to any new owner.
