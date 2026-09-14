# Cognitive Test Case Composition

## Composition

`World Sample Ref`
`+ Cognitive Task Ref`
`+ Goal/Concern Ref`
`+ Role/Context Ref`
`+ Environment Condition Ref`
`+ Cognitive Difficulty Ref`
`+ Controlled Perturbation Ref`
`+ Available Capability Set`
`+ Expected Observation Requirement Ref`
`→ Cognitive Test Case Ref`.

The case owns expected process constraints and admissible end states. It does
not contain a hardcoded semantic answer or force a model/provider result.

## Reuse

Extend the existing Model Test Case Manifest with dataset/sample/condition and
cognitive refs. Do not equate its `test_case_id` with a dataset sample ID.
