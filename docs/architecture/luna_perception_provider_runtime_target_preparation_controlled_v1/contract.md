# Contract

Canonical module: `capabilities/midplatform/provider_runtime_governance/provider_runtime_target_preparation_v1.py`.

The input has a tuple of FPO compatibility candidates and a tuple of `GovernedProviderRuntimeTargetMappingV1` entries. Each mapping explicitly names:

- source compatibility candidate;
- capability class;
- provider candidate and provider class;
- mapping, admission and availability refs;
- controlled availability/admission status and eligibility;
- optional opaque `source_model_ref`.

Formation is exact and explicit:

`one valid compatibility candidate × each matching AVAILABLE + ADMITTED + eligible mapping → one target candidate`

All valid mappings are retained. Same provider class does not deduplicate candidates; the same provider across different demands creates separate lineage-preserving targets. A target is not a binding and has no selected/bound/winner provider field, execution identity, session, or runtime request.

The result uses minimal fail-closed statuses: `PROVIDER_TARGET_CANDIDATES_FORMED`, `NO_PROVIDER_TARGET_CANDIDATE`, `NO_PROVIDER_MAPPING`, `NO_MATCHING_PROVIDER`, `PROVIDER_UNAVAILABLE`, `PROVIDER_NOT_ADMITTED`, and `INVALID_INPUT`.

`source_model_ref` is optional and only carried from an explicit mapping. No model is inferred from provider class, capability class, target, or scenario text.
