# B Contingency Request and Result Contracts

## BContingencyRequestCandidateV1

Candidate-only schema:

| Field | Contract meaning |
|---|---|
| request_ref | B request identity |
| source_a_work_ref | originating A working envelope |
| concern_ref | Brain-admitted concern ref |
| source_state_version_ref | A state version at request time |
| uncertainty_ref | uncertainty identity |
| uncertainty_description_ref | bounded uncertainty description |
| assumptions | assumptions B may explore |
| trigger_conditions | conditions that activate scenario |
| reasoning_scope_refs | A-provided reasoning scope |
| depth_limit | bounded reasoning depth |
| resource_limit_ref | resource envelope reference |
| stop_condition_refs | bounded stopping conditions |
| inherited_evidence_refs | read-only evidence refs |
| inherited_hypothesis_refs | read-only hypothesis refs |
| reality_constraints_refs | current-reality constraints |
| validity_boundary_refs | validity limits |
| trace_ref | trace reference |
| provenance_refs | provenance references |
| candidate_only | must be true |

Only A is the normal initiator. Brain may govern whether A is authorized to
request the contingency path.

## BContingencyResultCandidateV1

Candidate-only schema:

| Field | Contract meaning |
|---|---|
| result_ref | result identity |
| source_request_ref | originating B request |
| concern_ref | inherited concern ref |
| source_state_version_ref | A state version used by B |
| assumptions | assumptions used |
| trigger_conditions | scenario triggers |
| expected_state_refs | expected states |
| response_candidate_refs | conditional responses |
| confidence_refs | confidence candidates |
| uncertainty_refs | uncertainty candidates |
| validity_boundary_refs | validity constraints |
| invalidation_condition_refs | stale/invalidation conditions |
| evidence_basis_refs | read-only evidence basis |
| trace_ref | trace |
| provenance_refs | provenance |
| candidate_only | must be true |
| binding | must be false |

B result must not declare truth, mutate A or Loop, create Decision or Action,
create a new Concern, select Provider identity or become a binding plan.

## Result adoption

A compares B result with current reality and may issue a candidate disposition:

- KEEP;
- USE;
- PARTIAL_USE;
- SUPERSEDE;
- DISCARD;
- REQUEST_UPDATED_B.

Reality update can invalidate B without treating B as a failed capability.
