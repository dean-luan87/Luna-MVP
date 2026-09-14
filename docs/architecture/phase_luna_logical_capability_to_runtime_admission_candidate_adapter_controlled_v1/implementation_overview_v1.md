# Implementation Overview

Integration package:

`capabilities/midplatform/core/cognitive_flow/integration/logical_capability_to_runtime_admission_candidate_adapter_controlled/`

The package contains only candidate dataclasses, pure supplied-evidence
assessment, synthetic fixtures, a direct Runner, and a direct Verifier. The
assessment never reads the environment and never invokes an execution path.

Existing `CapabilityResolutionCandidateV1` is reused. The local types are
integration candidates for the frozen contract and are not canonical global
types.

