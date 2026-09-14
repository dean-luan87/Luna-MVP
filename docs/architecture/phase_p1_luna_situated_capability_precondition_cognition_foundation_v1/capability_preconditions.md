# Capability preconditions

`CapabilityPreconditionDefinitionV1` is the declaration surface for a
Capability Requirement. It contains supported condition dimensions and
abstract adjustment mappings; it does not declare the current requirement's
minimum conditions and does not perform cognition.

`MinimumSituatedConditionRequirementV1` is resolved from the current
Information Need and Goal. For the controlled OCR vocabulary, text presence
requires target visibility, while primary sign reading additionally requires
completeness, adequate scale, and stable relation. The resolver fails closed
when a need has no canonical policy or the capability does not support a
selected dimension.

`SituatedCapabilityStateV1` is the current contextual assessment input.  Its
optional `condition_state_candidates` field can carry condition assessments
derived from Self/Field/Target/Relation observations.  When present, the
generic evaluator uses those candidate statuses; it does not treat
`UNKNOWN` as satisfied.

The generic evaluator compares the two:

`minimum_condition_requirement.required_condition_refs - situated_state.satisfied_condition_refs`

An empty difference can produce `FEASIBLE` (or `FEASIBLE_UNSTABLE` when the
relation stability candidate is unstable).  A non-empty unsatisfied or
unknown set produces `NOT_FEASIBLE`; unknown refs are retained separately as
`unknown_condition_refs`.  Provider/model availability is intentionally not
part of this feasibility predicate.
