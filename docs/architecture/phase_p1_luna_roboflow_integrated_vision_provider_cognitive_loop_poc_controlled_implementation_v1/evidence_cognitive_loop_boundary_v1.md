# Evidence and Cognitive-Loop Boundary

Detection and OCR remain separate Evidence families.

Detection uses `VisualDetectionEvidenceCandidateV1`. OCR uses the existing
`OCRRawEvidenceV1` plus `OCRStructuredEvidenceEnvelopeV1`. Provider confidence
is retained as metadata and is never used directly as Sufficiency.

`cognitive_loop_adapter_v1.py` forms a candidate Current World from Evidence.
Structural fixtures may supply an A-owned assessment; real mode omits it and
uses the narrow A-side evidence-coverage bridge in the adapter. That bridge
evaluates declared evidence-kind coverage, missing evidence, contradictions,
uncertainty and source diversity. It creates only a generic hypothesis
candidate and an evidence sufficiency candidate; it does not infer an exit,
read OCR as Truth, or use provider confidence as Sufficiency. It then forms
`NextCycleIngressCandidateV1` for targeted re-observation. A Decision
candidate is accepted only when already owned by Decision Governance.

No output declares World Truth, mutates Field, creates Task, executes Action,
or autonomously retries/re-observes.
