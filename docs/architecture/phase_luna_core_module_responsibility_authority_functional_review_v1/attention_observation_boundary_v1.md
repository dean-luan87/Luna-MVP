# Attention / Observation Boundary v1

## Attention owns candidate allocation

- priority and urgency candidate;
- object, region or spatial focus candidate;
- modality preference candidate;
- persistence/decay candidate;
- bounded budget candidate;
- acquisition constraints and source versions.

## Observation/FPO owns execution

- acquisition request admission;
- sensor/provider execution;
- evidence creation and return;
- acquisition status and failure;
- gateway/evidence provenance.

Attention must not open a camera, invoke OCR/YOLO/SLAM/provider, declare
evidence, or immediately execute a follow-up route. Existing Observation
Attention schemas explicitly enforce candidate-only, not-fact and
not-runtime-output flags.

Observation may return focus-satisfied, target-unavailable, evidence-returned,
acquisition-failed or stale-focus refs. Attention records candidate state; A
decides semantic sufficiency.
