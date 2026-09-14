# Cognitive Evidence Field Model v1

Evidence Field is a context-bound, time-bound, and source-bound collection of Evidence Candidates that Luna currently holds about Reality.

Example for a possible airport exit:

```text
Camera Candidate: blue sign
OCR Candidate: EXIT
VLM Candidate: possible exit
SLAM Candidate: three metres ahead
```

The field retains their distinct sources, scopes, confidence candidates, uncertainty, relationships, and conflicts. It does not collapse them into an exit fact.

```text
Reality -> Evidence Field -> Representation -> Schema -> Hypothesis -> Simulation -> Prediction
distance:   0          1                 2            3           4             5          6
```

Distance is verification distance, not value or authority rank.
