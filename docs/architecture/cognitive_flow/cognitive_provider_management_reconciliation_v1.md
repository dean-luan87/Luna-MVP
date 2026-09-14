# Provider Management Reconciliation v1

## Current status

The existing Model Manager has not been code-renamed or migrated. Architecture reconciliation has, however, placed its current capabilities under the future Provider Management responsibility inside Cognitive Middleware.

## Reconciled responsibility

| Concern | Legacy Model Manager asset | Provider Management position |
|---|---|---|
| Model/provider identity | Provider registry views and identity adapters. | Provider metadata and eligibility source. |
| Capability matching | Capability matcher and requested-capability input. | Match CWO-derived capability requirements. |
| Admission | Admission processor and permission/admission governance. | Determine eligible Provider candidates. |
| Health/lifecycle | Lifecycle planner and health diagnostics. | Report availability, degradation, suspension, and reliability. |
| Resource/ownership | Resource evaluator and ownership resolver. | Constrain feasible Provider Session candidates. |
| Routing/fallback | Routing candidate and fallback planner. | Return preferred/alternative Provider Candidate Sets. |
| Trace/replay | Model Manager trace/replay utilities. | Attach execution-side provenance to CWO lineage. |

## Boundary correction

The old conceptual chain `Task → Model Selection → Model Result` is not an A-route entry point. The target chain is:

`CWO → Capability Requirement → Provider Candidate → Provider Session Candidate → Evidence Candidate`.

Provider Management does not own task decision, cognitive Goal, Intent, Attention, cognitive completion, truth, or a direct Brain connection. Its architecture status is **MIGRATE by adapter/projection**, not **REPLACE by rebuild**.
