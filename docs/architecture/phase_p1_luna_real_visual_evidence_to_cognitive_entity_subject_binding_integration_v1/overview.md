# Phase-P1 Luna Real Visual Evidence to Cognitive Entity Subject Binding Integration v1

## Status

`GO — VERIFIED — PHASE CLOSED`

This phase is a static implementation plus user-terminal verification phase.
The Agent does not execute YOLO, Provider Runtime, Python, or the Runner.

The first user-terminal Runtime attempt successfully reached real YOLO and the
full subject-binding path, but verification was blocked by a summary contract
projection defect. The phase remains open pending terminal re-verification.

## Scope

The phase implements the selected Route B from the Canonical Subject Reference
Reuse Audit:

```text
Real Visual Evidence
  -> EntityCandidateV1
  -> VisualEvidenceSubjectBindingCandidateV1
  -> Field Semantic Event.subject_ref_candidate
```

The binding stops at `L1 — Cognitive Candidate Reference`. It does not resolve
physical identity, persistent identity, Target Binding, Field Truth, or World
Truth.

## Reused Runtime Path

The evaluation integration reuses the previous real visual projection and
canonical semantic-event path:

```text
Real YOLO
  -> Runtime Observation
  -> Visual Evidence Candidate
  -> EntityCandidateV1
  -> Subject Binding Candidate
  -> field_definition_observed Candidate
  -> Field Event Admission
  -> Field State Reducer
```

No Provider Runtime, Field Admission, Reducer, Evidence Sufficiency, or
canonical Cognitive Primitive contract is modified.

## Intended Outcome

`subject_ref_candidate` is populated with an observation/evidence-linked
`EntityCandidateV1.entity_id`, while all of the following remain true:

- `identity_resolution_status=UNRESOLVED`;
- `semantic_state_resolution_status=UNRESOLVED`;
- `semantic_value_candidate=null`;
- `semantic_target_resolved=false`;
- the one-event/one-source sufficiency contract remains fail-closed.

The repair also preserves real frame dimensions through the existing Provider
detection record; dimensions are not hardcoded or inferred from the bbox.

## Closure

The final user-terminal verification passed with:

```text
all_checks_passed=true
failed_checks=[]
cognitive_logic_result=PASS
operational_result=PASS
final_decision=GO
validation_errors_empty=true
```

The verified Runtime used `LIVE_RUNTIME` real YOLO execution. This phase is
closed for the declared L1 candidate-binding scope.
