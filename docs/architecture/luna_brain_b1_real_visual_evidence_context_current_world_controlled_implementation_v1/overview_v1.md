# B1 Real Visual Evidence → Context / Current World

This package implements the first downstream controlled integration for an
already-produced YOLO11n `VisualDetectionEvidenceCandidateV1`.

The route is:

`YOLO11n evidence reference → Observation Gateway integration adapter → Observation Context handoff → Context Foundation candidate → CurrentWorldCandidateV1`

The adapter is an integration surface of the existing Observation Gateway;
it is not a new semantic owner. The existing Context World State Controlled
Integration engine remains the Context/Field/Current World candidate adapter.

No provider is invoked by B1. The real case consumes a previously validated
structured evidence reference so this phase isolates Evidence → Brain
integration from YOLO execution.

Evidence admission is structural/procedural only. It does not declare truth,
admit facts, mutate Field State, mutate Current World, create Intent/Decision/
Task, or generate natural-language conclusions. Field Event creation requires
an explicit field-relevance signal; Field State Reducer eligibility is not
execution.
