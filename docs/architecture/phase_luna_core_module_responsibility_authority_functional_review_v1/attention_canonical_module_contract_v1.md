# Attention Canonical Module Contract v1

## Adjudication

**Disposition: NARROW.** Attention remains an independent narrow governance and
allocation boundary. It does not decide what cognition needs. It allocates
bounded focus candidates after A has issued a Cognitive Need/Requirement and
within Brain policy.

## Canonical purpose

Attention is Luna's policy-constrained focus and resource-allocation boundary:
it ranks candidate information targets, modalities, regions or objects and
proposes bounded focus/budget allocations for acquisition, while preserving
A's Cognitive Need authority, Brain's global governance and Observation/FPO's
execution authority.

## Repository evidence

- `core/cognitive_state_formation/attention_types_v1.py` defines candidate
  focus/priority data and explicitly marks candidates only.
- Cognitive State Formation validators require `candidate_only=True`,
  `decision_priority=False`, `action_priority=False` and candidate heuristic
  score semantics.
- `situation_understanding/attention_allocation/` contains value assessment,
  L0 scan, budget allocation and a candidate-only adapter.
- Observation Attention Layer schemas prohibit fact writes, runtime triggers,
  navigation, speech and immediate follow-up execution.
- Existing review `module_attention_review_v1.md` already identifies the need
  for an A→Attention→Observation bridge.

## Authority

Attention may authoritatively produce an allocation candidate within supplied
Brain constraints, but does not own global priority policy, Safety, Permission,
resource ceilings, Need, Sufficiency or acquisition admission.

Its responsibility is candidate ranking, focus/budget consistency, stale-focus
handling, competition handling and provenance. A owns whether the selected
focus addresses the Need. Brain owns global constraints. Observation/FPO owns
whether/how acquisition proceeds.

## Inputs and outputs

Inputs: A Cognitive Need/Requirement refs, semantic/Perspective relevance,
Field/Context/Current World refs, Task urgency/dependency refs, Role refs,
Brain policy/budget/safety/permission/resource refs, capability availability
refs and source versions.

Outputs: AttentionFocus/Allocation candidates containing target refs,
priority, urgency, modality preference, spatial/temporal focus, budget
candidate, constraints, version and provenance. Observation/FPO receives
candidate refs; A receives allocation status and evidence-return linkage.

## Negative boundary

No Need creation, semantic judgment, Sufficiency, Reconsideration, Goal or
Concern governance, Capability/Provider selection, Runtime Admission,
Observation execution, camera/OCR/YOLO/SLAM invocation, Action, Loop control,
Memory mutation, Learning, Scheduler creation or World Truth.

## Status

`NO_GAP` for the conceptual narrow owner; `CONTRACT_GAP` for the canonical
A→Attention→Observation handoff; `ADAPTER_GAP` for older Task/goal-driven
focus paths; `RUNTIME_GAP` for a unified production Attention boundary.
