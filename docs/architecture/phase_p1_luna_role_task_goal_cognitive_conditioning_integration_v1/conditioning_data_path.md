# Conditioning data path

`ARouteOrchestrationRequestV1` carries `role_refs`, `task_refs`, `goal_refs`,
`concern_refs`, and `information_need_refs`. `ARouteIngressRefsV1` additionally
carries reference-only `relation_refs`. A-Route maps these to
`CognitiveStateFormationInputV1` as read-only `SourceRefV1` values.

The controlled replay request is admitted by the existing Observation Gateway;
the A-Route then passes the admitted evidence and conditioning references to
the existing `CognitiveStateFormationEngineV1`.
