# Implementation Roadmap

## 1. Contract review

Review A ownership, Field Cognition success semantics, node observability,
Dataset-as-world relationship, and attribution boundaries.

## 2. Cognitive trace/profile foundation

Implement the evaluation-only `CognitiveWhiteBoxTraceV1` and
`LunaCognitiveExecutionProfileV1` by composing existing refs. Do not add UI or
runtime imports.

## 3. Small cognitive corpus

Implement the 15 high-explanation case families in the corpus plan with
structural assertions and explicit unresolved outcomes.

## 4. Progressive evidence trials

Add missing/conflicting/false/stale evidence and multi-cycle re-observation;
measure burden and ownership attribution.

## 5. External capability comparison

Only after L0/L1 stability, compare RF-DETR/YOLO/OCR or other external
implementations under fixed cognitive cases.

## 6. Dataset scale and future modules

Then expand Dataset/conditions, followed by Memory, B-Route, Learning,
Emotion, or other downstream phases according to validated A-Route gaps.
