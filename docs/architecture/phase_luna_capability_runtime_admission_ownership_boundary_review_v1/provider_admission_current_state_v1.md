# Provider Admission — Current State

## Current controlled path

The Real Capability Single Invocation Trial assembles:

1. `CapabilityRequirementV1` from a governed Need.
2. Scope and logical Resolution through Universal Capability Slot Governance.
3. Model contract resolution through `resolve_model_contract_v1()`.
4. Technical model admission from the supplied physical asset, checksum and
   dependency inputs.
5. `VisionProviderAdmissionCandidateV1` through
   `build_vision_provider_admission_candidate_v1()`.
6. Provider invocation through `run_authorized_vision_provider_v1()` only when
   the admission candidate is authorized.

## Provider admission rules observed

Provider authorization requires a bounded observation/provider session,
non-empty requirement/model/admission/trace refs, expected evidence kind,
`provider_admitted=True`, and no autonomous Provider execution. Missing model
admission produces `PROVIDER_NOT_ADMITTED`; missing model path in a real call
produces `MODEL_NOT_AVAILABLE`; invocation failure is represented as
`PROVIDER_INVOCATION_FAILED`.

## Classification

The trial is `CONTROLLED_TRIAL_ADMISSION` with reuse of canonical model,
capability and Provider admission assets. It is not yet a complete
`CANONICAL_RUNTIME_CONTRACT`, because its five readiness inputs are terminal
arguments and the assembled admission is not the mandatory output of a
general logical-resolution bridge.

## Authority

Provider does not self-admit. Capability Admission coordinates qualification;
Model Manager supplies model evidence/admission; Provider Governance/FPO
supplies Provider-specific admission; the Provider adapter executes only after
the explicit candidate is authorized.

