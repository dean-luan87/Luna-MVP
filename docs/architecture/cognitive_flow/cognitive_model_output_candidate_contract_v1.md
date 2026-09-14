# Cognitive Model Output Candidate Contract v1

Every future capability/model output must be wrapped before it reaches the Cognitive Foundation.

## Required fields

- `evidence_candidate_id`;
- `source_capability` and `source_model_reference`;
- `input_reference` and bounded time/space/context references;
- `output_kind` and candidate payload reference;
- `confidence_candidate`, uncertainty, contradiction, and missing-information fields;
- evidence/provenance/trace references; and
- explicit flags: `candidate_only=true`, `not_fact=true`, `decision_authorized=false`, `action_authorized=false`, `state_mutation_requested=false`.

## Prohibited fields or effects

No Decision command, Action command, Permission, Reality/Field-State handle, Reducer handle, Memory write handle, fact-admission flag, or hidden model invocation may be transferred through this contract.
