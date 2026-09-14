# Verification

## User-terminal command

```bash
python3 -m capabilities.evaluation.real_visual_cognitive_entity_to_field_relation_candidate_integration.real_visual_cognitive_entity_to_field_relation_candidate_runner_v1
python3 -m capabilities.evaluation.real_visual_cognitive_entity_to_field_relation_candidate_integration.real_visual_cognitive_entity_to_field_relation_candidate_verifier_v1
```

The Agent does not execute these commands.

## Required evidence

The verifier is fail-closed and checks that the real YOLO execution produces
real runtime observation/evidence and that the positive case creates canonical
`RelationCandidateV1` output with:

- `subject_ref` equal to an `EntityCandidateV1.entity_id`;
- predicate `OBSERVED_IN_FIELD`;
- the controlled Field context as `object_ref`;
- evidence, trace, and provenance lineage;
- `candidate_only=true` and `fact_admitted=false`.

The controlled guards cover relation creation, non-belonging semantics,
non-fact/non-persistent semantics, unresolved identity, and independent
relations for two same-class detections. They also check that a relation does
not become a new Evidence source, that the 2-event/2-source sufficiency
contract is unchanged, and that the known policy trace debt remains separate.

## Runtime and governance assertions

The positive case must retain real Provider execution with
`recorded_provider_result_used=false`. The current Field context remains
`CONTROLLED_CONTEXT_CANDIDATE`; no physical Field identity or truth is
declared. Target Binding remains unresolved, and no Memory/PCN mutation occurs.

The forbidden-behavior projection continues to use `false` for a forbidden
provider/model invocation violation even though the allowed real YOLO provider
is invoked.

## Expected fail-closed semantics

The relation candidate is not an additional event or independent source.
Consequently, the existing `minimum_event_count=2` and
`source_diversity_requirement=2` contract remains unchanged. Any resulting
insufficient-evidence/no-state-change outcome is expected and is outside this
phase's relation compatibility scope.

## Status

Current status remains `WAITING_FOR_USER_TERMINAL_VERIFICATION` until the user
terminal runs the two commands above. No GO/PASS conclusion is made by the
Agent.

## Verification history

First user-terminal Runtime verification:

- Real YOLO execution: verified.
- Detections: 12.
- Evidence candidates: 12.
- EntityCandidates: 12.
- Relation candidates: 12.
- All relation semantics and negative guards: passed.
- Sole failed check: `relation_traceable`.
- Result: `all_checks_passed=false`, `cognitive_logic_result=FAIL`,
  `operational_result=FAIL`, `final_decision=NO-GO`.

Classification: `RELATION_TRACEABILITY_INTEGRATION_GAP`.

The original Relation Trace populated `source_detection_refs` by filtering
EntityCandidate provenance strings containing `detection`. That selected the
capability/model binding provenance reference
`capability-governance:object-detection-yolo11n-binding:v1`, rather than a
real detection identity. The verifier's traceability condition was not
relaxed. The repair now obtains `detection_ref` from the canonical visual
Evidence record matched by `EntityCandidateV1.evidence_refs`, and checks
consistency across Runtime Observation, Evidence, Detection, EntityCandidate,
Subject Binding, RelationCandidate, and Field context.

This was a Runtime Trace Mapping Gap, not a Verifier Contract Gap. No
cognitive, relation, identity, sufficiency, Reducer, Provider, or policy
semantics were changed. Re-verification is still pending.

## Second verification history

The second user-terminal Runtime confirmed the prior detection mapping repair:

```text
RelationTrace.source_detection_refs
= yolo_vision-unit:real-provider-frame:provider-runtime:
  real-visual-field-projection:v1_000
```

Same-class chair detections also retained independent detection, Evidence,
EntityCandidate, and RelationCandidate lineage. The only remaining failed
check was `relation_traceable`.

Static decomposition found that the positive semantic event stores
`relation_candidate_ref` at `semantic_trace.payload.relation_candidate_ref`,
but the verifier read `semantic_trace.relation_candidate_ref`. The negative
guard-only cases intentionally have `semantic_trace=null`; they are not in the
positive traceability scope and do not cause this check to fail.

Classification: `VERIFIER_TRACE_PROJECTION_GAP` (a verifier contract
integration gap). The verifier now reads the canonical payload location while
retaining all Runtime Observation, Evidence, Detection, EntityCandidate,
Subject Binding, RelationCandidate, and Field consistency checks. No verifier
strength was reduced. Current status remains
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.
