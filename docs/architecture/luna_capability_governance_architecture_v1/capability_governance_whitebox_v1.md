# Capability Governance Whitebox v1

## Ownership questions

| Question | Canonical answer |
|---|---|
| What does Luna own? | Capability identity and lifecycle through Capability Registry |
| What does Model Manager own? | Model assets, versions, resources, compatibility, deployment status |
| Who admits a capability? | Capability Admission, after risk and qualification review |
| Who calibrates health? | Capability Calibration at capability level |
| Who exposes implementation? | Provider Adapter under Provider Governance |
| Who executes? | Capability Runtime, only for an admitted Capability Request |
| Who requests a capability? | Brain / Cognitive Core |

## Boundary questions

1. Can a Model define a new Luna Goal? No.
2. Can a Provider write Reality or Brain state? No; it returns an Evidence
   Candidate through the Evidence Gateway.
3. Can Self Regulation switch a Provider by itself? No; it proposes and
   Capability Governance/Brain review the candidate.
4. Does degraded capability equal Self or Identity failure? No; health is
   capability-scoped and local failure is isolated.
5. Is Runtime active in this phase? No; only the boundary is mapped.

## Existing asset treatment

Existing Model Manager, Capability Runtime, Provider, Admission, Calibration,
and discovery assets are mapped through `capability_duplicate_mapping_v1.json`.
No historical asset is deleted, renamed, moved, or overwritten by this phase.
