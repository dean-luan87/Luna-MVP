# Complete Cognitive Flow Trace Model v1

## Purpose

Define one traceable, candidate-only record for an A-route cognitive cycle.

## Required trace envelope

Every trace entry carries:

- `trace_id` and `step_id`;
- `input_reference` and `output_candidate_reference`;
- `source` and `provenance`;
- `context_reference` and applicable time, space, goal, resource, and risk boundaries;
- `evidence_reference`;
- `confidence_candidate` and `unknowns`;
- `boundary_statement`; and
- `validation_status_candidate`.

## Ordered trace steps

| Step | Input | Candidate output | Required boundary |
| --- | --- | --- | --- |
| 1 | Input Signal | Perception Candidate | perception is not a fact or action |
| 2 | Perception Candidate | Information Field Candidate | information field is not Reality State |
| 3 | Information Field | Representation Candidate | representation is not Reality |
| 4 | Representation | Schema Match Candidate | schema match is not confirmation |
| 5 | Schema / context | Attention Allocation Candidate | attention is not importance truth |
| 6 | Active candidates | Workspace Formation Candidate | workspace is temporary and not memory |
| 7 | Workspace | Simulation Branch Candidate | simulation is not future truth |
| 8 | Workspace / branch | Operation Result Candidate | operation is not decision |
| 9 | Operation result | Evaluation Candidate | evaluation is not authority |
| 10 | External observation | Outcome Observation Candidate | outcome is not truth about reasoning |
| 11 | Outcome / trace | Feedback Candidate | feedback is not mutation |
| 12 | Feedback | Future Improvement Candidate | improvement is not adoption |
| 13 | Improvement / validation | Evolution Adoption Candidate | adoption candidate is not rewrite |
| 14 | Validated guidance candidate | Future Cognitive Guidance Candidate | guidance is not automatic routing |

The trace must retain unknowns rather than silently converting them into facts.
