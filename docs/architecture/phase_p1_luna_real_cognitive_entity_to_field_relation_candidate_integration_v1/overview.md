# Phase-P1 Luna Real Cognitive Entity To Field Relation Candidate Integration v1

## Status

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

This phase is a controlled integration with one real YOLO provider execution.
The Agent performs static implementation only; the user terminal owns Runtime
and verifier execution.

## Scope

The phase establishes the first relation-level projection from the already
available L1 `EntityCandidateV1` and visual subject-binding candidate to the
existing candidate-only `RelationCandidateV1`:

```text
Real YOLO
→ Runtime Observation
→ Visual Evidence Candidate
→ EntityCandidateV1
→ L1 Subject Binding Candidate
→ RelationCandidateV1
→ Field Semantic Event / Cognitive Trace
```

The relation predicate is `OBSERVED_IN_FIELD`. It means only that an
observation-linked entity candidate was observed in the current Field context.
It is not a claim of Field membership, persistent presence, ownership,
function, social role, task meaning, Field Truth, or World Truth.

The canonical `RelationCandidateV1` from the Cognitive Primitive Layer is
reused directly. No second Relation contract or new owner is introduced.

## Runtime boundary

The real visual source remains the previously validated local YOLO path. The
Field reference is `field:visual-frame:v1` with
`CONTROLLED_CONTEXT_CANDIDATE` semantics. Detection, bbox, frame dimensions,
confidence, evidence references, runtime observation references, and
trace/provenance remain source-linked. No OCR, SLAM, camera, tracking, action,
Field mutation, or truth promotion is part of this phase.

## Explicit non-goals

- L2 canonical physical subject resolution.
- L3 persistent or Memory identity.
- Target Binding.
- Field-conditioned meaning, ownership, function, or role.
- Field Reducer policy repair or Evidence Sufficiency changes.
- Cross-Field resolver, Memory, PCN, or Rumination.

See [relation_contract.md](./relation_contract.md),
[verification.md](./verification.md), and the canonical
[Field-Conditioned Entity Semantics & Cross-Field Information Reuse Principle](../field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md).

## Runtime verification repair status

The first user-terminal Runtime verification reached the real YOLO,
EntityCandidate, Subject Binding, and RelationCandidate path. It produced 12
detections, 12 Evidence candidates, 12 EntityCandidates, and 12 relation
projections. All relation semantics and negative guards passed; the sole
failure was `relation_traceable`.

The failure is classified as `RELATION_TRACEABILITY_INTEGRATION_GAP`: the
Relation Trace projected a capability/model binding provenance reference as a
detection reference. The repair reads `detection_ref` from the canonical
`VisualDetectionEvidenceCandidateV1` selected by the EntityCandidate's
evidence reference. It does not alter relation semantics, identity semantics,
or any canonical Runtime owner.

Current status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.

## Second Runtime verification repair

The second user-terminal Runtime confirmed that
`RelationTrace.source_detection_refs` now contains the real canonical
detection reference:
`yolo_vision-unit:real-provider-frame:provider-runtime:real-visual-field-projection:v1_000`.
The complete Detection → Evidence → EntityCandidate → Subject Binding →
RelationCandidate → Relation Trace lineage therefore remains intact.

The verifier still reported the sole failure `relation_traceable`. Static
inspection showed that the positive semantic trace stores
`relation_candidate_ref` inside its canonical `payload`, while the verifier
read it from the event top level. This is classified as
`VERIFIER_TRACE_PROJECTION_GAP`. The repair reads the existing payload field;
it does not weaken the positive trace check and does not require semantic
traces for guard-only negative cases.

Current status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
