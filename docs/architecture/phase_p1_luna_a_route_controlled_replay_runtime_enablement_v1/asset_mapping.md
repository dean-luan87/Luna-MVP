# Asset Mapping

| Concern | Canonical asset | Change |
|---|---|---|
| Mode | `capabilities/midplatform/core/execution_mode_v1.py` | Added explicit modes and replay contracts |
| Replay admission | Observation Gateway | Added typed frozen replay admission |
| Ingress | `ARouteIngressRefsV1` | Reused as the reference carrier; optional typed relation interpretation candidates are additive |
| Orchestration | `ARouteOrchestrationEngineV1` | Added replay branch; synthetic branch preserved |
| Cognition | `CognitiveStateFormationEngineV1` | Added replay execution evidence and transitions |
| Runner/Verifier | Canonical A-Route package | Added one controlled fixture and fail-closed verifier |

The additive typed relation candidate remains read-only and candidate-only.
Field State Reducer remains the Field State authority; A-Route/Cognitive State
Formation consume the projection and do not mutate the source candidate.
