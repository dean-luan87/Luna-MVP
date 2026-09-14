# Source-State Handoff Boundary v1

`SourceStateHandoffCandidateV1` binds result/evidence refs to a target boundary without mutating that boundary.

Required guards are `candidate_only=True`, `source_mutation_authorized=False`, and `world_truth_declared=False`. Field Event output also requires `admitted=False`, `reducer_executed=False`, and `field_mutation=False`. Current World output uses the existing candidate type and requires no authoritative write or truth declaration.

The adapter owns correlation, target routing, version preservation, provenance preservation, invalidation preservation, and candidate construction. Field owns later admission/reduction; Current World/State Formation owns candidate representation lifecycle; A remains the semantic consumer.

