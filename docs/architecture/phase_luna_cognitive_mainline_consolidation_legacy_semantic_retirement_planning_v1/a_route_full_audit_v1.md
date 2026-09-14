# A Route full audit

| Current behavior | Current evidence | Target disposition |
|---|---|---|
| Stage/handoff construction and lifecycle coordination | `a_route_orchestration_engine_v1.py`, protocol/core types | KEEP_ORCHESTRATION |
| Context/PCN/Intent/Cognitive State stage chain | `STAGE_PRODUCERS` | MOVE_UPSTREAM_ENVELOPE / COMPATIBILITY_ONLY |
| Observation ingress and re-observation routing | Product Loop integration and Observation handoffs | KEEP_ORCHESTRATION; source owner remains Observation |
| Cognitive Flow handoff | stage `COGNITIVE_STATE` / Dynamic Regulation | COMPATIBILITY_ONLY until Working Envelope/A bridge is caller |
| Decision/Task/Action handoff | Product Loop integration | KEEP_ORCHESTRATION after cognition; not A semantic ownership |
| Product Loop state machine | `a_route_product_loop_integration_engine_v1.py` | COMPATIBILITY_ONLY / DEPRECATE_LATER for cognitive path |
| Product Loop feedback/reconsider/reobserve | same engine | Narrow to routing; semantic decision moves to A/Outcome Governance |
| Runtime admission/execution | same integration | KEEP as downstream execution boundary, outside A reasoning |
| Historical Route B naming | A Route docs and perception assets | COMPATIBILITY_ONLY; disambiguate as B-CR vs perception Route B |

ARouteOrchestrationEngineV1 already describes itself as a lifecycle/handoff coordinator and has mutation guards. The Product Loop integration still contains semantic-looking cognitive/feedback states and must not be treated as the target A authority without a cutover.

