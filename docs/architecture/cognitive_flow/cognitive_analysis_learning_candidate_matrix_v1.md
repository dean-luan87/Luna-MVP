# A3 Cognitive Analysis Learning Candidate Admission Matrix v1

| Source | Required Evidence | Review Requirement | Admission State | Allowed Destination |
| --- | --- | --- | --- | --- |
| Analysis Result Candidate | source analysis reference, all retained evidence references, uncertainty, provenance/trace | `review_required` or another declared review-bound state | `not_submitted`, `review_required`, `admission_candidate_ready`, `admission_deferred`, or `admission_rejected`; never admitted/active | future governed Learning Review / Admission Candidate Queue only |
| Raw model output | not a valid source | unavailable | rejected | none |
| Fact Store / Field State | not a source for learning promotion under this contract | unavailable | rejected | none |
| Direct training request | no candidate evidence route | unavailable | rejected | none |

No row authorizes training, model update, Memory write, Case Library write, Knowledge Base write, or Fact promotion.
