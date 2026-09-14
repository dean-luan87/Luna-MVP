# Current Architecture Inventory

## Evidence basis

Inspected source and contract families:

- capabilities/midplatform/core/a_route_orchestration/
- capabilities/midplatform/core/cognitive_flow/
- capabilities/midplatform/core/cognitive_state_formation/
- B1/B2/B3/B4 controlled integrations;
- capabilities/midplatform/core/task_manager/
- Intent, Decision, Action, Outcome, Observation Gateway and Capability
  Governance owners;
- capabilities/midplatform/core/cognitive_memory_experience/
- current Loop controlled implementation under
  cognitive_loop_governed_continuity_candidate_controlled/
- Brain Golden Baseline planning and integrated closure;
- A Route and B Route architecture documents;
- Role, Attention, Hypothesis and Emotion interface contracts.

## Current implemented paths

### B5 baseline path

S3 real provider
→ B1 evidence / Observation Gateway / Current World candidate
→ B2 Cognitive State / Attention / Hypothesis / Cognitive Flow candidates
→ B3 Intent / Decision / Task candidates
→ B4 controlled Outcome / Reconsideration / Reobserve candidates

This is a candidate-only downstream path except for the previously bounded
real provider boundary. The repository B5 route explicitly keeps provider
output away from World Truth and has no provider-to-Brain shortcut.

### A Route controlled path

The A Route Product Loop engine assembles controlled handoffs across ingress,
observation, Context/Field, Cognitive State/Flow, Intent/Decision, Task,
Action, Runtime boundary, Result and Outcome feedback. Its owner guard states
that orchestration has no semantic authority.

The A Route protocol nevertheless names a broad lifecycle from ingress through
Memory/Experience, Learning, Self continuity and Personality context. Those
stages are handoff labels, not proof that A owns their semantics.

### Dynamic Flow path

DynamicCognitiveFlowEngineV1 currently accepts candidate Goal, provisional Plan,
state version, evidence updates, Need/Requirement/Resolution/Invocation
candidates and Capability outcomes. It emits state versions, current minimum
Need, sufficiency, reconsideration, next-step disposition and stale
Requirement decisions.

The current engine contains semantic decision behavior such as Need selection,
sufficiency, reconsideration and continuation. That is the principal target
for later narrowing into A/B reasoning authority.

### Current Loop path

The current Loop package wraps Dynamic Flow with Loop identity, local state,
continuity, lifecycle, closure, outcome, package and assimilation candidates.
It already marks external owner data as references and guards against provider,
Action, Task, Intent, Memory, Experience and autonomous child-loop behavior.

The current Loop package also exposes fields whose names look cognitive:
current Need, hypothesis lineage, sufficiency, reconsideration, capability
path, closure reason and resume decision. This is recorded as authority leakage
for later migration; no code is changed here.

## Existing B Route meanings

Two non-equivalent meanings exist:

1. Future simulation/counterfactual B Route: future interface only, may return a
   Simulation Candidate to A, cannot override current reality or decision.
2. Model-test dual perception Route B: VLM/scene/attention/route candidates,
   planning-only, no real model execution and no direct navigation decision.

This is a naming and contract conflict, not a resolved owner decision.

## Existing short-path/filter evidence

No single canonical Experience / Short-Path Filter owner was found. Existing
assets provide composable pieces:

- ExperienceCandidate and MemoryCandidate boundaries;
- Attention and known-information references;
- Capability Scope/Resolution/Invocation gates;
- observation admission and B1/B2 evidence boundaries;
- direct candidate-only capability resolution.

The proposed filter should be composed from these assets later, not introduced
as a new Brain or reasoning owner in this phase.

## Current contradictions

1. A Route planning calls A Route the canonical loop caller while Cognitive
   Flow remains the Dynamic Flow owner.
2. A Route protocol stages Dynamic Regulation before Decision, while the
   Product Loop engine stages Intent/Causal/Decision after Cognitive State.
3. B Route has two meanings.
4. Loop local candidates currently express judgments that the target assigns
   to A/B reasoning.
5. Brain governance is described architecturally but no single Brain runtime
   owner/API was found.

## Classification summary

- KEEP: existing semantic owners and negative guards;
- NARROW: A Route orchestration, Loop Engine and Dynamic Flow boundaries;
- REASSIGN: reasoning judgments from Loop/Dynamic Flow into A/B contracts;
- DEFER: Semantic Module and Experience/Short-Path Filter implementation;
- CONTRACT GAP: Brain entry, B Route identity, Goal/Sufficiency authority,
  closure assimilation consumer and Behavior owner.
