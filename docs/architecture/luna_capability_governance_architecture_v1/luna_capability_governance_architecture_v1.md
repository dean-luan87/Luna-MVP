# Luna Capability Governance Architecture v1.0

## Position

Capability Governance is the L1/L4 governance layer between the Cognitive
Core and capability implementations. It defines what Luna can have, how a
capability is admitted, how health is assessed, and which implementation
options may be presented. It does not execute a capability.

```text
L1 Cognitive OS Governance
          ↓
Capability Governance
  Definition / Registry / Lifecycle / Admission / Calibration
          ↓
Model Manager / Provider Management / Capability Runtime
          ↓
Evidence Gateway → Cognitive Core
```

## Canonical ownership

- Capability Registry owns capability identity, schema, contract, dependency,
  and lifecycle.
- Model Manager owns model assets, versions, resources, compatibility, and
  deployment status. It does not decide Luna's capability value.
- Provider owns the capability implementation entry point and adapter contract.
  It has no Decision, State, Reality, Goal, or Identity authority.
- Capability Admission owns admission decisions for capability candidates and
  coordinates Model, Provider, and Runtime qualification.
- Calibration owns capability-level performance evidence and health assessment,
  not a provider's internal training state.
- Capability Runtime executes an already admitted request and returns an
  evidence candidate. Runtime is not implemented by this phase.

## Capability-first rule

Luna requests a capability (for example, `visual_environment_understanding`),
not a named model. Model options are implementation resources exposed after
Capability Governance has established a requirement and admission context.

## Self and Brain boundaries

Self Regulation may report health, request a capability health query, and
propose stability-preserving adjustments. It cannot switch a model, invoke a
Provider, or bypass admission. Brain may issue a capability request, but it
does not select a model implementation directly.

Capability Governance cannot create Goal, modify Value or Identity, generate a
Decision, or execute an Action.

## Existing asset mapping

This design maps existing assets rather than replacing them:

- `docs/architecture/cognitive_model_manager_runtime_boundary_v1/` supplies
  Model Manager contracts;
- `docs/architecture/cognitive_capability_runtime_contract_v1/` supplies
  capability request/admission/result boundaries;
- `docs/architecture/luna_capability_runtime_integration_v1/` supplies Runtime
  boundary contracts;
- `docs/architecture/luna_governance_asset_discovery_v1/` supplies discovery,
  ownership candidates, and duplicate candidates.

## Phase boundary

This is a Planning Only architecture phase. It does not integrate a Provider,
replace a Model, attach Hardware, activate Runtime, schedule execution, or
perform automatic upgrade/recovery.
