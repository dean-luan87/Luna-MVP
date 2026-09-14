# Change Manifest

Created:

- a LIVE_RUNTIME YOLO11n execution adapter and user-terminal Runner under
  `capabilities/midplatform/core/provider_runtime_to_observation_ingress/`;
- a read-only verifier for the real execution output;
- this phase documentation and the architecture index entry.

Modified:

- provider-result status/admission normalization now permits actual provider
  and model invocation only for `LIVE_RUNTIME`, and distinguishes
  `EMPTY_SUCCESS`;
- the real-provider adapter now maps the existing FPO canonical
  `capability-requirement:...` identity into provider admission instead of
  passing the normalized `provider-requirement:...` resolution identity;
- the real-provider ingress now keeps `controlled_integration_only=true` for
  the Gateway boundary and derives raw-frame dimensions from source image
  metadata, preserving original-image YOLO coordinates;
- no cognition, Gateway, Decision, Task, Action, Archive, or Runtime Executor
  semantics were changed.

Defect remediation:

- `PROVIDER_NOT_ADMITTED` was caused by the integration omitting the canonical
  FPO capability-requirement identity required by the existing admission
  predicate. The predicate and Provider Governance rules were preserved.
- `INVALID_INGRESS` was caused by the real path setting
  `controlled_integration_only=false`; the Gateway validation rule was
  preserved. The 5712x4284 versus 640x480 discrepancy was independent metadata
  drift and was corrected at the new integration mapping.

Agent execution status: no provider, model, Python command, Runner, Verifier,
or test command was executed.
