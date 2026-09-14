# Legacy Task System Migration Analysis v1

## Finding

The existing `capabilities/midplatform/core/task_manager/` contains lifecycle, task decomposition, dependency resolution, capability routing, interruption/recovery, result aggregation, diagnostics, and execution-request candidate assets. Its input explicitly contains `task_goal`; its result contains `task_plan`, subtasks, and execution-request candidates.

## A-route placement

The legacy Task Manager cannot remain an upstream cognitive organizer. In the A-route it may be adapted only as a **Middleware Execution Organization** asset after CWO issuance.

```mermaid
flowchart LR
    B[Brain Intent] --> N[Neural CWO]
    N --> M[Middleware]
    M --> T[Legacy Task Manager adapter]
    T --> C[Capability Execution Candidates]
    C --> R[Middleware Report]
```

## Migration mapping

| Legacy capability | Future Middleware use | Required boundary |
|---|---|---|
| `task_goal` input | Replaced by immutable CWO reference/purpose. | Task Manager cannot originate or rewrite goal semantics. |
| Task decomposition | Objective decomposition into capability-work candidates. | Preserve CWO scope and completion conditions. |
| Capability router | Capability/Provider candidate organization. | Provider execution stays separately admitted. |
| Dependency resolver | Execution-candidate dependency metadata. | Not a cognitive reasoning graph. |
| Interruption/recovery | Middleware delivery/recovery candidates. | Cannot cancel Brain intent or change Attention. |
| Task lifecycle | Provider Session / execution-work lifecycle mapping. | Do not equate with CWO or Brain state lifecycle. |
| Result aggregator | Middleware Report assembly. | Completed work coverage ≠ cognitive completion. |

## Frozen prohibition

Task Manager must not regain Goal, Intent, Attention, Context, Truth, Decision, or Action authority. Legacy task plans remain execution-side implementation candidates, never Cognitive Work Objectives.
