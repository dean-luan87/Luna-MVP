# Capability / Provider Boundary v1

Provider Governance owns Provider identity, admission, invocation
authorization, execution contract and Provider-specific failure handling.

Handoff:

`Executable Capability Candidate → ProviderAdmissionInputCandidate → Provider
Governance`.

The Provider admission input is still a candidate/ref. Provider Governance
decides whether actual invocation is authorized. Capability Governance never
directly invokes Provider and never creates Observation evidence.

For perceptual capabilities the downstream path is:

`Provider → Observation/FPO → Evidence → Gateway/Current World/A`.

For non-observation capabilities the execution receiver may differ, but the
Capability/Model/Provider separation remains.
