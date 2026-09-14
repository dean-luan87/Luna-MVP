# Dynamic Cognitive Flow / Real Capability Single Invocation Trial

The phase adds an integration-only trial under the existing Cognitive Flow owner. Brain-side formation ends at a bounded `OBJECT_DETECTION` requirement. The requirement is scope-validated and resolved through the existing Capability Registry and Model Contract Repository. The resolved mapping is `object_detection` → `model-asset:yolo11n:weights-v1` → `loader:ultralytics:yolo:v1` → `adapter:yolo:visual-evidence:v1` → `capability:object-detection:v1`.

The Runner invokes the existing S3-Y11 provider adapter exactly once. It preserves the single-frame budget and uses the existing Model Manager/Provider Governance admission. No model is downloaded and no continuous camera is started. The returned evidence is passed through the existing Observation Gateway, then the existing B1 Context World integration and B2 Cognitive State/Flow path.

The 22 scenarios after the real call are controlled projections over the returned evidence and existing Dynamic Cognitive Flow engine. They cover insufficient continuation, controlled sufficiency termination, replan, non-binding remaining candidates, and no second provider call. The Runner persists a JSON summary and trial snapshot. The Verifier reads those files only; it does not import or execute the Runner and cannot trigger another provider invocation.

Evidence remains candidate-only. Provider success does not become World Truth or automatic goal sufficiency. Action, Learning, Memory mutation, capability acquisition, and autonomous observation continuation remain outside the phase.
