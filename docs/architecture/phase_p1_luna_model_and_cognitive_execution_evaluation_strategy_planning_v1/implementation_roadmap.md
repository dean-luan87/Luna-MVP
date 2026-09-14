# Implementation Roadmap

## Phase 1 — contract alignment

- review this strategy with Evaluation, Model Test Lens, TestBoard, and
  canonical governance owners;
- resolve object-detection MUEP vocabulary;
- define media/reference normalization and GT review states;
- keep all changes planning-only until accepted.

## Phase 2 — evaluation-only foundation

- implement the four Dataset Registry declarations from the prior phase;
- extend Model Test Case Manifest with dataset/sample/condition refs;
- validate identity, provenance, versions, annotations, and runtime-forbidden
  boundaries;
- add no loader, downloader, model runner, or runtime import.

## Phase 3 — execution profile and failure taxonomy

- implement `EvaluationExecutionProfileV1`, fit profile, burden metrics, and
  failure refs by composing existing envelopes/traces/reports;
- add caller-aware structural validation;
- write protected TestBoard evidence for future runs.

## Phase 4 — controlled cognitive-chain evaluation

- begin with a small RF-DETR/OCR or existing controlled case suite;
- observe Evidence → Current World → Hypothesis → Sufficiency and stop/handoff;
- add no automatic re-observation or Task/Action execution.

## Phase 5 — comparison and scale

- fixed-suite model/version comparisons;
- condition and resource expansions;
- only after P0/P1 stability, consider public benchmark declarations and larger
  curated suites.
