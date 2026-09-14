# Module Responsibility Documentation Alignment

## 1. Purpose

This M0 document gives existing engineering and architecture assets one consistent responsibility vocabulary. It does not modify their contracts, schemas, code, Runtime behavior, or canonical owners.

## 2. Field State System

**Owner:** Field System, with the reducer retaining mutation authority and the read model remaining read-only.

**Responsible for:** admitted real-world and Field state candidates, deterministic reduction, state transition traceability, replay, and current Field projections.

**Not responsible for:** user psychological understanding, Memory, Intent generation, causal judgment, Decision selection, or Action execution.

**Status:** `ENGINEERING_BASELINE_ACTIVE`.

Field State answers what governed evidence says about the current world slice. Psychological or social interpretation belongs to later cognitive objects and cannot be folded into the reducer.

## 3. Observation Manager

**Owner:** Observation Manager / Reality Evidence Pipeline.

**Responsible for:** observation request coordination, observation-resource coordination, cross-modal evidence candidates, evidence quality, provenance, temporal context, trace, and replay.

**Not responsible for:** final cognition, final fact declaration, Cognitive Attention ownership, Understanding, Decision, or Action.

**Status:** `ENGINEERING_BASELINE_ACTIVE`.

Observation Manager may coordinate perceptual attention as an engineering observation concern. This must not be confused with Cognitive Attention, which allocates cognitive resources after Field and context inputs exist.

## 4. Task Manager

**Owner:** Task Manager.

**Responsible for:** approved task lifecycle, dependencies, interruption, aggregation, and governed capability routing.

**Not responsible for:** Intent generation, Goal ownership, causal judgment, final Decision selection, Runtime dispatch authority, or Action execution.

**Status:** `ENGINEERING_BASELINE_ACTIVE`.

Intent explains a candidate direction. Task Manager manages an admitted task after upstream governance. A task name or lifecycle state must never be treated as evidence that Task Manager created Luna's intent.

## 5. Model Manager

**Owner:** Capability Governance / Model Manager.

**Responsible for:** model identity, asset admission, matching, routing candidates, lifecycle, fallback, diagnostics, trace, and replay.

**Not responsible for:** the cognitive subject, Reality, final cognition, Goal, Intent, Decision, or Action.

**Status:** `ENGINEERING_BASELINE_ACTIVE`.

Model outputs remain capability results or evidence candidates. They require admission and cognitive processing; Model Manager cannot become Luna's meaning, belief, or decision owner.

## 6. Memory System

**Owner:** Memory System.

**Responsible for:** historical information and experience persistence, candidate admission, consolidation, activation, retrieval, and context-bound historical influence.

**Not responsible for:** full cognition, Reality override, direct Cognitive Core mutation, Self or Identity mutation, Personal Cognitive Network ownership, or Decision selection.

**Status:** `ARCHITECTURE_AND_CONTROLLED_SKELETON`.

Memory provides past influence to the present Field and Understanding. It does not declare the current world, automatically become Self, or serve as the entire cognitive network.

## 7. Personal Cognitive Network

**Owner:** Personal Cognitive Network Governance.

**Responsible for:** governed cross-object connections, context-bound activation, and read-only cognitive projection.

**Not responsible for:** Self, Role, Relationship, Memory, Emotion, Value, Belief, Schema, source persistence, or source mutation.

**Status:** `FUTURE_CORE_CAPABILITY`.

PCN connects references; it does not absorb the referenced objects. It must not become a universal memory warehouse or a hidden cognitive owner.

## 8. Supporting engineering organs

### Protocol Manager

Protocol Manager remains an active engineering module under Cognitive OS governance. It supports compatible protocol boundaries but does not judge Reality, make decisions, or execute actions.

### OCR and Vision

OCR and Vision remain active perception capabilities. They produce traceable evidence candidates; they do not declare facts, write Memory, select Decisions, or execute Actions.

### Root A3 Runtime

The root A3 Runtime retains its existing owner and authorized scope. Its presence does not establish Dynamic Cognitive Architecture v2 Runtime support. Its M0 status is `LEGACY_RUNTIME_UNALIGNED`.

## 9. Cognitive architecture objects

- **Self:** owns identity continuity, capability reality, resources, boundaries, and regulated growth review.
- **Role:** owns Field-bound participation identity and Role lifecycle.
- **Relationship:** owns social relationship state and context candidates.
- **Emotion:** remains a future integration and adaptive-signal boundary; it does not own Value or Decision.
- **Value Utility:** evaluates value, utility, cost, and risk candidates; it does not choose Action.
- **Intent:** governs Intent Candidates; it does not replace Goal, Task Manager, Decision, or Action.
- **Causal Reasoning:** remains planning-only typed causal candidate reasoning.
- **Experience Compression:** remains planning-only and candidate-based; it cannot write Memory or Schema directly.
- **A/B Route:** preserves current Reality versus future simulation; B Route remains unimplemented.
- **Decision Arbitration:** selects a governed Decision Candidate; it does not orchestrate tasks or execute actions.
- **Action Governance:** defines the future governed execution path; M0 does not activate it.

## 10. Owner invariants

Every object has one final responsibility Owner. Integration does not transfer ownership. Projection does not imply mutation. Architectural validation does not imply Runtime activation. Existing module baselines remain authoritative for engineering behavior.
