# A Route Active Observation Controlled Integration v1

## Scope

This phase extends the existing `Field Perception Orchestrator` inside its existing integration directory. It does not create `Active Observation Governance`, `Observation Control Governance`, or `Perception Governance` as new owners.

The controlled candidate chain is:

```text
Information Need
 -> Observation Demand
 -> Observation Request
 -> Attention Target
 -> Capability Requirement
 -> Capability / Model Admission
 -> Bounded Provider Session Candidate
 -> Perception Evidence
 -> Observation Gateway
 -> Observation Candidate
 -> Evidence Sufficiency
 -> STOP / CONTINUE / REDIRECT / SWITCH_PROVIDER /
    ADD_CAPABILITY / RECONSIDER / DEFER / FAIL
 -> A Route next-cycle ingress candidate
```

All outputs are synthetic, candidate-only, deterministic, traceable, and non-mutating. No provider, model, camera, OCR, SLAM, runtime, scheduler, database, or device is executed.

## Owner reuse

`Field Perception Orchestrator` owns the new candidate semantics because the existing owner already contains information-gap detection, observation goal, region, capability, budget, stop, and re-observation candidates. Observation Manager remains a reusable request/attention/evidence substrate. Observation Gateway remains the evidence-to-observation admission owner. Model Manager remains the model/provider candidate admission and routing owner. A Route Orchestration remains the lifecycle/handoff owner.

## Frozen distinctions

- Observation Demand != Observation Request.
- Observation Request != Capability Requirement.
- Capability Requirement != Model Selection.
- Model Selection != Provider Invocation.
- Provider Session Candidate != Provider Runtime Execution.
- Observation Gateway Admission != Continue Authorization.
- Evidence Sufficiency != Model Confidence.

## Evidence Sufficiency

Sufficiency is evaluated against information need, task/safety need, expected evidence, source diversity/independence, contradiction, uncertainty, temporal validity, target coverage, semantic coverage, and spatial coverage when required. Model confidence is preserved only as a quality input.

## Provider autonomy

`provider_autonomous_continuous_execution = false`. Frame arrival, prior success, model/provider availability, prior routing, previous OCR/SLAM success, and Observation Gateway admission cannot independently start or extend a provider session. Safety-critical baseline observation is a candidate exception only when explicit policy, scope, capability, budget, temporal validity, revoke condition, and provenance exist.

## A Route boundary

The integration emits candidate references targeting `A Route Orchestration` `INGRESS_READY` and next-cycle ingress. It does not call or mutate A Route Orchestration. `runtime_handoff_ready=false` and `mutation_authority=false` remain frozen.

## Scenario baseline

R01-R12 are preserved as product regression gates. R13-R36 extend idempotency, stale/contradictory evidence, provider failure, budgets, safety revocation, intent/field changes, cross-modal cases, next-cycle linkage, and the synthetic subway-sign product path.

Current status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
