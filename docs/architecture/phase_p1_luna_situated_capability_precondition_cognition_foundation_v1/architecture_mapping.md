# Architecture mapping and audit

## Existing assets

- `Self State Awareness` defines dynamic, candidate-only Self State and keeps
  the reducer as the sole mutation authority.
- `Field State Reducer / Field State Read Model` provides the Field-owned
  read-side boundary; this phase only carries `field_state_refs`.
- `Field Perception Orchestrator / Active Observation Control` owns existing
  Observation Demand and Request candidates.
- The Active Observation Preconditions implementation supplies the first
  concrete necessity, requirement-condition, feasibility, window, and
  eligibility semantics.
- Capability Registry owns capability identity and metadata. Capability
  Governance / Capability Admission owns capability binding/admission
  authority. The Universal Capability Slot planning candidate already exposes
  availability, health, resources, and governance references.
- `MinimumSituatedConditionRequirementV1` is resolved from the current
  Information Need and Goal against the capability's supported condition
  dimensions.

The resolver is implemented at
`capabilities/midplatform/core/situated_capability_preconditions/minimum_situated_condition_resolution_v1.py`.

The Slot asset does not currently declare or assess situated Self/Field/Target
preconditions. No Slot schema was modified; the generic layer uses an additive
`CapabilityPreconditionDefinitionV1` declaration plus a
`MinimumSituatedConditionRequirementV1` resolver instead of creating a new
Slot architecture.

## Generic versus specialization

Generic: need, precondition definition, situated state references, feasibility,
condition candidates, condition gap, adjustment need, opportunity, eligibility,
trace, provenance, candidate-only and execution prohibitions.

Active Observation-specific: visibility, completeness, scale, orientation,
occlusion, stability, sensor conditions, and the existing Observation Window
vocabulary. These are mapped, not copied into a second generic implementation.

No new Brain owner, Self owner, Field owner, Provider Runtime, or Action owner
is introduced.
