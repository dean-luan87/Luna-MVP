# Canonical Flow Contract Closure Summary v1

## Overall adjudication

**FLOW_CONTRACT_SURFACE_COHERENT_WITH_ADAPTER_GAPS.** The canonical flow now has a minimal contract surface for binding, source-state handoff, Outcome→Brain adjudication, version/invalidation and edge observability. Existing authority remains unchanged.

## Contract surface

- Capability↔Model: Capability-owned binding lifecycle; Model-owned declarations.
- Model↔Provider: Provider-owned binding lifecycle; Model-owned declarations.
- Result→Source State: candidate-only handoff; Field/Current World retain mutation/formation authority.
- Outcome→Brain: separate candidate input and Brain adjudication output.
- Version/Invalidation: per-domain refs, no global version.
- Edge Observability: common semantic record, local adapters permitted.

## Online-doc-ready sections

### 03.10.1 | Canonical Flow Contract Surface

The frozen flow is covered by minimal reference-oriented contracts. Existing canonical families are reused; new surfaces are cross-boundary profiles, not new Managers or universal runtime objects.

### 03.10.2 | Capability ↔ Model Binding

Capability Governance owns the binding lifecycle. Model Governance owns model declarations. Binding does not imply runtime readiness or Provider invocation.

### 03.10.3 | Model ↔ Provider Binding

Provider Governance owns the provider-facing binding lifecycle. Model Governance owns model identity, loader and dependency declarations. Compatibility does not imply health or invocation.

### 03.10.4 | Evidence / Result → Source-State

Provider/Action results become candidate evidence and then separately governed Current World and/or Field candidates. Direct source mutation and World Truth declaration are forbidden.

### 03.10.5 | Outcome → Brain Adjudication

Outcome Evaluation supplies a versioned candidate; Brain performs final adjudication and Assimilation in a separate record.

### 03.10.6 | Version / Invalidation Contract

Each domain retains its version. Invalidation carries cause, old/new refs, authority, consequence owner and re-admission/refresh requirements.

### 03.10.7 | Canonical Edge Observability

Every edge exposes producer, consumer, authority, responsibility, class, refs, versions, constraints, status, provenance, failure, next target and execution/mutation flags.

### 03.10.8 | Legacy Bypass Replacement Map

Legacy direct routing, Gateway mutation, Loop closure inference, and model/provider embedding are mapped to canonical contracts but not repaired.

### 03.10.9 | Implementation Readiness

Edge observability is contract-ready. Binding and handoff surfaces need schema/adapter work. Runtime remains deferred.

### 03.10.10 | Remaining Contract Gaps

P1 gaps remain in binding schemas, source-state handoff, Outcome→Brain extension, invalidation propagation, adapters and legacy migration.

## Status

Documentation and schema-level contract closure complete. No runtime, canonical type, protocol, owner, source state, model, Provider, test or UI was changed or executed.

