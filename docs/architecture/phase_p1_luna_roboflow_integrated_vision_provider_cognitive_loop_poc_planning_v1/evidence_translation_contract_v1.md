# Evidence Translation Contract

## Provider result layers

```text
Roboflow native result (EXTERNAL RESULT)
  → Provider adapter normalization
  → detection/text evidence candidates
  → Observation Gateway evidence admission/correlation
  → Current World candidate and/or Field Event candidate
```

Provider Result is not Evidence, and Evidence is not World Truth.

## Detection mapping

For each detection retain provider id, class candidate, bounding box, frame
and ROI refs, model/workflow version, provider timestamp, confidence,
uncertainty, contradiction refs, trace and provenance. The existing
`VisualDetectionEvidenceCandidateV1` is a suitable detection shape; its
`candidate_only`, `truth_declared`, `fact_admitted`, `field_mutation` and
`current_world_mutation` flags must remain restrictive.

## OCR mapping

OCR should use the existing Observation OCR contract/adapter family and emit
text-region candidates with source frame/ROI, text candidate, recognition
confidence, reading-order/region provenance where available, uncertainty and
contradiction refs. Do not merge OCR text into a Detection record or treat
recognized text as a fact without the Evidence/Gateway boundary.

## Confidence and conflict

Model confidence is evidence metadata, not sufficiency and not truth. Keep
confidence, uncertainty, source diversity and contradiction as separate
fields. Detection/OCR/VLM disagreement becomes linked competing evidence or
conflict refs; the Provider does not resolve semantic conflict. A/Cognitive
State Formation evaluates hypothesis support/opposition and sufficiency.

## Provenance minimum

Preserve source image/frame ref, ROI/coordinate transform, provider identity,
workspace/project/workflow/model ref, model/workflow version, request and
invocation refs, provider output ref, timestamps, trace parent, source
license/origin where a dataset is used, and adapter contract version. Missing
or contradictory provenance blocks downstream candidate admission.

