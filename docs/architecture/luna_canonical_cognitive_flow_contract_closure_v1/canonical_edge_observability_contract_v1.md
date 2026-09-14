# Canonical Edge Observability Contract v1

## Semantic record

The minimum observable transition record contains:

`transition_id`, `trace_id`, `parent_transition_refs`, `concern_ref`, `reasoning_cycle_ref`, `producer`, `consumer`, `authority_owner`, `responsibility_owner`, `transition_class`, `input_refs`, `input_versions`, `output_refs`, `output_versions`, `admission_or_validation_status`, `constraint_refs`, `reason_ref`, `decision_ref`, `evidence_refs`, `provenance_refs`, `invalidation_refs`, `failure_classification`, `blocker_refs`, `next_target`, `started_at`, `completed_at`, `source_mutation_executed`, `runtime_execution_executed`, and `candidate_only`.

## Required answers

For every canonical edge, future White-box observability must answer: what is happening; Concern; initiator; authority; responsibility; inputs and versions; evidence; constraints; output; admission requirement/status; mutation; runtime execution; block/degradation reason; stale state; next target; and reverse provenance.

## Boundary

This is a semantic contract, not a UI and not a universal Python class. Modules may map local records into this observability profile through adapters. Observability does not create authority or permit mutation.

