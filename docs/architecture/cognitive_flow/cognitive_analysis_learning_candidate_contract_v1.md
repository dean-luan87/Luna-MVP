# A3 Cognitive Analysis Learning Candidate Governance Contract v1

## Position

A `Learning Candidate` is a review-bound record derived by reference from an `Analysis Result Candidate`. It preserves candidate status, evidence, uncertainty, provenance, and review/admission state. It is not a learning outcome, a training record, Memory, Case Library entry, Knowledge Base item, Fact, or Field State.

`runtime_authorized=false` remains unchanged.

## Required Fields

| field | meaning | boundary |
| --- | --- | --- |
| `candidate_id` | governed candidate identity | no automatic identity generation |
| `source_analysis_ref` | reference to the source Analysis Result Candidate | no source replacement or asserted conclusion |
| `evidence_refs` | traceable supporting Evidence references | mandatory; no evidence mutation |
| `confidence` | optional candidate attribute | not training weight, Fact authority, or admission authority |
| `uncertainty` | unresolved/conflict/coverage limits | mandatory and retained |
| `provenance` | source and trace lineage | mandatory and retained |
| `review_status` | required review lifecycle signal | review is not a write permission |
| `admission_status` | candidate admission lifecycle signal | never claims actual admission in this contract |

## Forbidden Operations

The following must be explicitly `false`:

- `direct_training`
- `model_update`
- `memory_write`
- `case_library_write`
- `runtime_executed`

An Analysis Result Candidate cannot directly enter Model Training, Memory System, Knowledge Base, Fact Store, or Case Library. Its only permitted destination under this contract is a future governed **Learning Review / Admission Candidate Queue**; that queue is not implemented here.

## Admission Boundary

Allowed review statuses are review-bound states such as `review_required`, `pending_review`, and `under_review`. Allowed admission statuses stop at candidate/review/deferred/rejected states. No `admitted`, `active`, training, memory, or case-write state is permitted.

## L1 Alignment

The candidate preserves L1 Input/Output Candidate Governance and Protocol Traceability, and it references existing Permission/Admission and Model/Skill Admission governance without creating a new admission mechanism.
