# Active Caller Map v1

| Surface | Definition/caller evidence | Classification |
|---|---|---|
| `DynamicCognitiveFlowEngineV1` | Imported by `run_dynamic_cognitive_flow_controlled_implementation_v1.py` and controlled real-capability integration adapters. | TEST/CONTROLLED or COMPATIBILITY_CALLER; no production dispatcher caller found. |
| `ARouteOrchestrationEngineV1` | Exported by package and imported by controlled A-Route runners. | COMPATIBILITY_CALLER. |
| `CognitiveExecutionChainEngineV1` | Imported by `run_cognitive_execution_chain_controlled_integration_v1.py`; no non-controlled caller found. | TEST/CONTROLLED. |
| `ObservationGatewayEngineV1` | Imported by controlled integration runner and real visual gateway adapter. | CONTROLLED/ADAPTER; evidence boundary preserved. |
| `run_yolo11n_real_single_frame_provider_execution_v1.py` | Direct entrypoint; imports FPO control, provisioning, and provider adapter; `_execute` can call `run_authorized_vision_provider_v1`. | ACTIVE_EXECUTION_SURFACE; F-001. |
| `run_yolo_real_smoke_v0.py` | Tool entrypoint imports `run_yolo_real_smoke_v0`; no canonical flow caller found. | TOOL/CONTROLLED REAL SURFACE. |
| OCR guarded provider executor | Explicit guarded-trial entrypoint; docs state no MidPlatform/World write. | GUARDED_TRIAL, not current canonical flow. |
| Loop cutover helpers | Called by their own controlled runner only. | FIXTURE_ONLY/CONTROLLED. |

The audit did not find an active product dispatcher that proves the real YOLO path is the production default. That reduces—but does not remove—the finding: a repository executable path is still not safe to treat as canonical merely because the consolidated synthetic regression lists direct routing as `SAFE_COMPATIBILITY`.

