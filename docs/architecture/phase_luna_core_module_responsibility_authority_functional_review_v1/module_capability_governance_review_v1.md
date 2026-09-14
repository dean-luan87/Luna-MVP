# M12 Capability Governance / Logical Capability Resolution — Module Review

## Identity and purpose

Canonical name: Capability Governance / Capability Resolution. Evidence: universal capability slot registry, scope/resolution assets, Capability Requirement bridge, `logical_capability_to_runtime_admission_candidate_adapter_controlled/`, and Model Manager/manifest contracts. If removed, Luna loses the governed translation from information requirement to logical capability, scope, resolution, and runtime-admission boundary.

## Functions and authority

`CORE`: Capability Requirement formation support, scope assessment, logical capability resolution, capability-slot/module mapping, provider compatibility candidate formation. Runtime Admission is a separate candidate assessment boundary. `SUPPORTING`: catalog/baseline/calibration refs. `COMPATIBILITY_ONLY`: invocation bridge assets. Capability Governance has technical resolution authority, not cognitive Need, Brain Goal, provider execution, or Loop authority. Model Manager owns model asset metadata; Diagnostics supplies health evidence; Provider Governance owns provider admission/invocation.

Responsibility follows each boundary: Capability Governance owns scope/resolution correctness; Runtime Admission/admission governance owns executable-candidate assessment; Provider Governance owns invocation; A owns information need/requirement.

## Inputs, outputs, state, lifecycle

Inputs: A Cognitive Requirement, capability slot/catalog, module scope, model/provider refs, permission/resource/safety constraints. Outputs: Capability Requirement, scope result, Logical Capability Resolution candidate, Runtime Admission Assessment, Executable Capability candidate, Provider Admission input. Logical resolution is candidate/ref; `READY_CANDIDATE` is not executable readiness. State is governance/catalog plus candidate refs.

## Communication and negative boundaries

Allowed: A→Capability Requirement, Capability→Scope/Resolution, Model Manager/Diagnostics→Runtime Admission evidence, Runtime Admission→Provider Governance, Loop→ref persistence. Forbidden: Capability→Goal/Concern, Capability→A Need, Capability→World Truth, Brain/A→model path/provider choice, Loop→admission. Current implementation is synthetic/candidate-only at Runtime Admission; no runtime probes/load/invocation are performed in this review.

## Walkthroughs

1. Normal: A requirement resolves logical capability; scope passes; Runtime Admission evidence yields executable candidate; Provider Governance may admit.
2. Blocked: out-of-scope, missing model, stale checksum/dependency/resource/permission yields blocked assessment and no executable candidate.
3. Changed state: resolution/model/source version changes; stale candidate is invalidated; A receives evidence/status, not a provider selection.

## Overlap, gaps, evolution, disposition

Overlap: `IMPLEMENTATION_OVERLAP` Task capability router vs Capability Governance; `TERMINOLOGY_OVERLAP` logical vs executable capability. Gap: future runtime admission owner/bridge contract and A→Observation return path, not a new owner mandate here. It may evolve into a clean logical-to-admission governance boundary, never a cognitive Need owner or infrastructure-free bypass. **Disposition: KEEP**.

**Ledger summary:** authority = logical scope/resolution and admission coordination; responsibility = technical candidate validity; receiver = Runtime Admission/Provider Governance/A; confidence = high for frozen candidate seam.
