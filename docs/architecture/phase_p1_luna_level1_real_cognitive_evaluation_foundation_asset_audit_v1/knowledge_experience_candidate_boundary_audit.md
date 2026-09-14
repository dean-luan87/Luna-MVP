# Knowledge and Experience Candidate Boundary Audit

## Findings

Memory, Experience, Learning, and related candidate assets exist elsewhere in the repository, including controlled cognitive memory/learning artifacts. The audit did not find a completed, evaluation-owned extraction contract that converts a durable cognitive evaluation run into a Knowledge Candidate or Experience Candidate while preserving review and trace lineage.

The correct future direction is a reference-only candidate extraction step:

`archived evaluation result + CognitiveWhiteBoxTraceV1 + LunaCognitiveExecutionProfileV1 + failure/gap refs → Knowledge Candidate / Experience Candidate`

The output remains a candidate, not runtime memory, admitted knowledge, admitted experience, World Truth, or a policy update. It requires explicit review/admission by the eventual owning subsystem. Evaluation cannot mutate Memory or Experience.

## Boundary rules

- Evaluation result is not World Truth.
- Human correction is not automatically GT or memory.
- `_eval_out` and RF-DETR smoke artifacts are evidence only.
- No semantic compression or automatic promotion is present or authorized.
- Source sample, case, trace, profile, version, invalidation, and review refs must remain attached.

## Readiness

Candidate boundary: `PLANNED / PARTIAL`.

This is not a blocker for static asset audit, but it is a future P1 integration gap if evaluation history is intended to feed learning or experience analysis.

