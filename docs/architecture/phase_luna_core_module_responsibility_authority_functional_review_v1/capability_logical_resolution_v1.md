# Logical Capability Resolution v1

Logical Resolution means selecting the capability/module/slot that can
logically satisfy a requirement. It does not select a concrete Provider for
execution and does not establish runtime readiness.

`CapabilityResolutionCandidateV1` may contain module, slot, implementation,
model-asset and Provider-contract refs as mapping candidates. Those refs remain
candidate metadata. `READY_CANDIDATE` means logical scope/binding resolution
passed; it does not mean executable readiness.

Required chain:

`Capability Requirement → Scope Assessment → Logical Resolution → Runtime
Admission Assessment → Executable Capability Candidate → Provider Admission`.

Logical Resolution may return unavailable or degraded candidates for missing
registration, missing slot binding, lifecycle limitations or logical scope
gaps. Runtime asset/dependency/checksum/device conditions belong later.
