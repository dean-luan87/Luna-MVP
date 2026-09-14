# Asset inventory

| Asset / responsibility | Classification | Current evidence and boundary |
|---|---|---|
| Intent Governance | A — canonical independent owner | `capabilities/midplatform/core/intent_governance`; owns Intent candidates and Intent mutation guards |
| Context Foundation | A — canonical independent owner | `context_foundation`; owns context assembly/projections and source-owner preservation |
| Role / interaction identity | H — unresolved | No single canonical Role runtime owner was found in the inspected core assets; preserve role refs without assigning Brain ownership |
| Field Event Admission / Field State Reducer | A — canonical independent owners | Admission and reduction remain outside Brain; Brain may reference resulting Field state |
| Field Perception Orchestrator | A — canonical independent owner | Owns observation/re-observation control and acquisition handoff |
| Observation Gateway | A — canonical independent owner | Owns evidence admission; Brain must not bypass it |
| A-Route Orchestration | A — canonical independent owner | Owns route mechanics; has no semantic authority over cognition |
| Cognitive State Formation Governance | A — canonical independent owner | Owns canonical Attention, Hypothesis, Current World, Sufficiency, Gap, Revision, and Stop production |
| Cognitive Flow Governance | A — canonical independent owner | Owns mechanical Cognitive Flow lifecycle and transition storage |
| Dynamic Cognitive Regulation Governance | A — canonical independent owner | Produces bounded regulation candidates; does not become Brain state authority |
| Goal / Concern / Information Need | B/H — split and partially unresolved | Goal/Concern have architectural Brain relationships; active cognitive need is formed/consumed by canonical cognition; no concrete Brain acceptance owner is established |
| Decision Governance | A — canonical independent owner | Owns Decision formation and handoff; Brain does not execute decisions |
| Task Manager | A — canonical independent owner | Owns Task lifecycle/readiness/recovery; Brain does not execute tasks |
| Memory / Experience Governance | A — canonical independent owner | Owns admission and mutation; Brain may receive candidate refs only |
| Cognitive Learning Governance | A — canonical independent owner | Owns learning candidate/admission behavior; Brain cannot promote learning directly |
| Self Governance | A — canonical independent owner | Owns self continuity/stability candidates; Brain references, does not mutate |
| Emotion subsystem / integration governance | B/H — external service | Emotion assets exist and Dynamic Regulation names an external integration boundary; no Brain mutation authority is established |
| Closure / Assimilation candidates | B — canonical candidate contracts | Existing candidate-only lifecycle, outcome, closure, and assimilation types are reusable; acceptance authority at Brain boundary remains unresolved |
| Capability / Model governance | A — canonical independent owner | Capability Registry, Capability Governance, Model Manager, and Provider Governance retain selection/admission/execution authority |
| System Protocols | A — canonical external boundary | Protocol Manager and module protocols constrain Brain; Brain cannot override them |
| Brain runtime owner | H — unresolved | Architecture documents describe Brain-level responsibility, but no concrete canonical runtime owner/API was found |

## Inventory conclusion

Existing owners are sufficiently present to support a Brain protocol boundary,
but not a new canonical Brain runtime implementation. The main missing assets
are a Brain request authority, Brain-local state contract, closure acceptance
authority, and assimilation consumer/owner.
