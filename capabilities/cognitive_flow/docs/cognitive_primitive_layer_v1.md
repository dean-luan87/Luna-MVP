# Luna Cognitive Primitive Layer v1

## Phase

- Phase: `Phase-A1-Cognitive-Primitive-Layer-Implementation-v1-001`
- Execution Mode: Controlled Skeleton Implementation
- Scope: minimal candidate-object language only
- Agent stop status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

## Module Position

The Cognitive Primitive Layer is the first implementation surface for Perception Admission in Luna Cognitive Flow. It accepts structured candidate observations, preserves their evidence/trace/provenance, and organizes them into candidate objects. It does not establish facts, maintain Field State, reason, decide, or act.

## Six Object Relationships

```text
Observation Event --references--> Evidence Reference
Observation Event --may support--> Entity Candidate
Entity Candidate --may support--> Relation Candidate
Entity / Relation context --may suggest--> Field Reference Candidate
Observation + Evidence --may support--> State Candidate
```

Every arrow is a candidate relationship. A Field Reference Candidate does not create a Field. A State Candidate does not modify Field State. None of the objects are a Hypothesis, Conclusion, Decision, or Action.

## Cross-Field reuse boundary

`EntityCandidateV1` is reusable as an evidence-linked L1 candidate reference,
not as a resolved physical identity or a Field-independent meaning. Reusing an
Entity Candidate or category knowledge across Fields does not reuse the prior
Field relation, ownership, role, use, or task meaning. Field-conditioned
interpretation remains a separate candidate under the current Field and
context. See the canonical [Field-Conditioned Entity Semantics & Cross-Field Information Reuse Principle](../../../docs/architecture/field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md).

## Input and Output

The builder API takes structured mappings with caller-provided IDs, timestamps, trace references, evidence references, and provenance references. It returns frozen dataclass objects with schema version `luna.cognitive_primitive.v1` and `candidate_only=true`.

The builders are:

- `create_observation()`
- `create_evidence()`
- `create_entity_candidate()`
- `create_relation_candidate()`
- `create_field_reference_candidate()`
- `create_state_candidate()`

The simulation adapter converts one of `shopping_mall`, `airport`, or `street` into an Observation Event only. It has no OCR, SLAM, model, network, fact, or Field State behavior.

## Relationship to Field Kernel

This module precedes Field Event Admission and the Field Kernel. A later authorized adapter may translate suitable primitive candidates into Field Event candidates, but that work is not implemented here. The existing Admission module remains the eligibility gate, the Reducer remains the sole Field State mutation authority, and the Read Model remains read-only.

## Relationship to External Models

OCR, SLAM, Vision, Audio, TTS, and ASR are external organs. Their outputs can be represented as observations or evidence with `source_type=model` or `sensor`; they cannot become facts, entities, Field State, conclusions, or action commands merely by entering this module.

## Prohibited Boundaries

- No fact confirmation or conclusion generation.
- No Field State, Reducer, Read Model, Task Manager, Registry, Manifest, Baseline, Lifecycle, or existing protocol modification.
- No hypothesis, inference, decision, action, tool invocation, database, queue, network, model, OCR, or SLAM call.
- No random ID, system-clock timestamp, runtime loop, runner, or verifier.
- Confidence on Evidence Reference is a source-provided reference value, never factual truth confidence.

## Verification Authority

No runner or verifier is created in this phase by instruction. No validation command is run by the Agent. Any future verification design must preserve the governance rule that final phase verification is user-terminal only and never constitutes an Agent final decision.
