# A Route Active Observation Control Gap Audit v1

## Scope and evidence posture

This is a read-only inventory audit and architecture-planning package. It does not implement a runtime capability, modify an owner, activate a provider, or start Emotion/B Route work. The supplied terminal evidence is accepted as an input fact for this audit: A Route Orchestration is 20/20 with 0 blockers, and Observation Gateway is 22/22 with 0 blockers.

The two passed modules solve different problems:

- A Route Orchestration organizes lifecycle and handoff progression.
- Observation Gateway normalizes provider/input evidence, forms candidate observations, admits structurally valid candidates, and targets `INGRESS_READY`.

Neither result proves that Luna has a governed reason to observe, a scoped observation target, a capability/provider selection loop, task-relative evidence sufficiency, or bounded continue/redirect/switch/stop control.

## Inventory conclusion

The repository contains a substantial set of relevant candidate and planning assets. The strongest existing control candidate is `capabilities/midplatform/field_perception_orchestrator/`. Its current path already exposes information-gap detection, observation-goal formation, region planning, capability planning, model requirement formation, resource budgeting, invocation-history suppression, stop conditions, and re-observation policy. `capabilities/midplatform/observation_manager/` adds request classification, attention and region candidates, OCR/vision request candidates, evidence intake, cross-modal association, evidence quality, and an admission handoff candidate.

Model Manager provides candidate capability matching, model admission, resource evaluation, routing, lifecycle and fallback references. Cognitive Attention assets define target/priority/resource candidates. Observation Gateway and A Route Orchestration are both verified controlled modules, but remain candidate/controlled integration boundaries rather than a product runtime loop.

The inventory therefore does not justify a new parallel `Active Observation Governance` owner. The correct decision is option **B**: reuse the existing Field Perception Orchestrator as the narrow Active Observation Control candidate owner and add controlled typed integration around it. This owner may govern demand/request/control candidates; it must not own world truth, provider implementation, model inference, downstream state mutation, or semantic evidence authority.

## Historical root cause

The historical failure mode is not simply “missing YOLO/OCR/SLAM.” The repository had provider/model assets and several observation-oriented designs, but the demand chain was distributed across task contracts, attention planning, field perception, observation manager, model manager, and provider-specific governance. In some older assets, provider availability, frame arrival, or a direct routing decision could be mistaken for permission to invoke. In other assets, an admitted observation candidate could be mistaken for sufficient evidence or continuation authority.

The root architecture gap is the missing governed control chain:

```text
Context / Current World / Intent / Task / Safety Need
  -> Information Need
  -> Observation Demand
  -> Observation Request
  -> Attention Target / Region
  -> Capability Requirement
  -> Capability and Model Admission
  -> Scoped Provider Session Boundary
  -> Perception Evidence
  -> Observation Gateway
  -> Canonical Observation Candidate
  -> Task-relative Evidence Sufficiency
  -> Continue / Redirect / Switch / Stop / Reconsider
  -> Next Cognitive Cycle
```

## Current chain completeness

The chain is **PARTIAL**. Information gap, observation goal, target/region, capability requirement, provider routing candidates, evidence normalization, Observation Gateway admission, and A Route ingress all exist in some form. The missing product closures are:

1. a single route-level demand/request handoff;
2. task/information-need-relative Evidence Sufficiency;
3. a bounded provider session start/stop/revoke boundary;
4. a unified control result for continue, redirect, switch, stop, defer, and reconsider;
5. feedback from observation outcome back to the next observation demand/cognitive cycle.

## Ownership matrix conclusion

The detailed matrix assigns every required decision to a current owner, candidate owner, or explicit gap. The current ownership shape is:

- Field Perception Orchestrator: discovers information gaps and forms observation demand, goals, regions, capability requirements, resource and control candidates.
- Attention Layer / Cognitive State Formation: contributes priority, salience, risk, uncertainty, and attention target candidates; it does not execute providers.
- Capability Registry / Model Manager: matches capabilities and creates model/provider admission, routing, resource, lifecycle, and fallback candidates; it does not originate cognitive need.
- Capability/Model Admission plus Runtime Executor: owns the future permission boundary for provider start; the product handoff is not yet closed.
- Observation Gateway: owns evidence normalization, observation candidate lifecycle, provenance, contradiction/correction preservation, and A Route ingress; it does not authorize continued observation.
- A Route Orchestration / Cognitive Flow: owns lifecycle sequencing, reconsideration, and cycle linkage; it does not own semantic observation authority.
- Safety/Permission/Admission: must own any explicit safety exception policy; baseline safety priority cannot become general provider autonomy.

The only major unassigned semantic decision is task-relative Evidence Sufficiency. That is a genuine capability gap, not a reason to give Attention, Observation Gateway, Model Manager, Task Manager, or A Route Orchestration a new semantic super-owner.

## Provider Autonomy Principle

The principle is **CONTRACT_PARTIAL_RUNTIME_NOT_PROVEN**:

`Perception Provider has no autonomous continuous-execution authority.`

Camera/audio frame arrival, previous success, model availability, provider availability, and Observation Gateway admission are not execution authorization. The required chain is demand → request → scoped attention → capability requirement → admission → bounded provider session. Safety-critical baseline perception is an explicit exception only when its policy, scope, budget, trace, revocation, and resource constraints are present. It is not a general always-on exception.

## Evidence Sufficiency status

Evidence Sufficiency is **PARTIAL / genuine P0 gap**. Existing assets expose an `evidence_sufficient` input, an evidence quality candidate, stop condition candidates, and sufficiency feedback planning. They do not provide one canonical adjudication relative to the current information need, task or safety need, observation scope, expected evidence, temporal validity, contradiction state, uncertainty, and source independence.

`Evidence Sufficiency != Model Confidence`. A high model confidence can describe the wrong object, wrong region, wrong task, stale evidence, or one side of a contradiction. Admitted observation likewise means structurally admissible, not sufficient, true, or authorized to continue.

## R01-R12 regression baseline

R01-R12 are recorded as a product-level acceptance baseline, not merely documentation examples. They cover no-demand YOLO suppression, task-scoped OCR, Vision-to-OCR candidate handoff, sufficiency-to-stop, spatial-only SLAM demand, no stream-driven SLAM, provider non-mutation, Observation Gateway non-authority, bounded contradiction handling, correction lineage, bounded safety exceptions, and explicit terminal/control outcomes.

The baseline must be used by the future Active Observation Control integration and A Route product readiness work. It must not be satisfied by hardcoded case handling or by weakening provider/admission boundaries.

## A/B/C/D decision

- **A:** Field Perception Orchestrator, Observation Manager candidate path, Model Manager candidate routing/admission, Observation Gateway, A Route Orchestration, Cognitive Flow, Field State Reducer, and Attention candidate contracts are directly reusable under their existing boundaries.
- **B:** Task Observation Request, attention requirement planning, OCR admission checklist, SLAM provider management, model/capability admission contracts, and sufficiency/expectation references require typed adapters or controlled integration.
- **C:** Provider-driven continuous execution, direct provider-to-owner mutation, direct routing treated as invocation authority, and legacy environment-specific request defaults are semantic or operational drift and must not be promoted.
- **D:** Emotion Engine, Advanced Emotion Governance, semantic compression, affective memory compression, Personality-memory fusion, B Route, cross-user transfer, real provider execution expansion, and scheduler-driven permanent observation remain deferred/outside A Route in this phase.

## Genuine P0 gaps

The registry identifies three P0 gaps: unified demand/request control handoff, task-relative Evidence Sufficiency, and bounded provider-session start/stop/revoke handoff. They are product capability/integration gaps. They do not authorize implementation in this phase and do not require a parallel owner.

## Recommended next product module

The next module should be a **Controlled Active Observation Control Integration around the existing Field Perception Orchestrator**. It should connect Context/World/Intent/Task/Safety references to a bounded demand/request lifecycle, consume Observation Gateway output, adjudicate task-relative sufficiency, and emit explicit control candidates. Provider execution remains behind existing Capability/Model Admission and Runtime Executor boundaries.

It should not create `capabilities/.../active_observation_control/` until a later implementation phase explicitly authorizes that work. This audit creates documentation only.

## Technical debt

The Observation Gateway verifier debt is registered as `NON_BLOCKING_VERIFIER_TRACEABILITY_DEBT`: user-terminal evidence says 22/22 and 0 blockers, while some check identifiers were serialized as boolean values. This phase only records the issue. It does not modify the verifier or reopen the passed Observation Gateway implementation.

## Deferred boundary

Emotion Engine, Advanced Emotion Governance runtime, semantic compression, affective memory compression, Personality-memory fusion, B Route, cross-user transfer, real camera/provider execution, scheduler-driven permanent observation, and persistence implementation remain deferred. No new capability implementation was created.

## Status

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
