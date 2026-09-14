# Explicit Dependency Probe Planning v1

## Probe scope
- Define the contract for a future explicit dependency probe stage.
- Scope is limited to planning artifacts only; no real probing is performed in this phase.

## Supported dependency types
- Python package dependency
- Optional runtime adapter dependency
- Model weight dependency when explicitly required by the candidate contract
- License clearance dependency when gating execution admission

## Expected dependency metadata
- dependency_name
- dependency_category
- expected_version
- version_required
- probe_strategy
- probe_result_type
- candidate_only
- not_fact

## Owner approval gate
- Any dependency probe that would change runtime state must be blocked pending explicit owner approval.
- If approval is absent, the planned probe remains non-executing and deferred.

## Abort conditions
- Dependency is unknown or not explicitly documented.
- Version requirement is ambiguous.
- Probe strategy is not allowed by the dry-run boundary.
- Candidate remains candidate-only and not fact.
- Runtime boundary is violated.

## Rollback policy
- If any prerequisite is unresolved, the stage must rollback to a non-executing state.
- No registry mutation, runtime activation, or model execution is allowed during rollback.

## Evidence chain
- Evidence must be traceable to the prior dry-run planning and post-review artifacts.
- The plan must preserve a clear chain from planning to dry-run to post-review without executing real probes.

## Boundary
- No probe execution.
- No import.
- No package inspection.
- No pip execution.
- No subprocess execution.
- No registry modification.
- No runtime activation.
- No image read.
- No segmentation execution.
