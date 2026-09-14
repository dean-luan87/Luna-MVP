# Observation / FPO / Provider / Gateway Adjudication Summary v1

| Boundary | Disposition | Canonical residual responsibility |
|---|---|---|
| Observation | NARROW | governed acquisition request/result lifecycle |
| FPO | NARROW | acquisition orchestration, target binding, bounded correlation/deduplication |
| Provider Governance | KEEP | Provider admission, invocation, session, runtime result |
| Observation Gateway | KEEP | ingress/evidence normalization, admission, provenance and routing refs |

Target flow:

`A Cognitive Requirement + Attention → Capability Requirement/Resolution →
Runtime Admission → Observation Request → Provider Admission → Provider
Invocation → Provider Result → Evidence Mapping → Gateway Evidence Admission →
Current World/Field candidates → Cognitive Snapshot/Semantic refs → A`.

Action may share Provider infrastructure but retains a separate Action contract.

Documentation only. Runtime, types, enums, owners, camera, OCR, YOLO, ASR,
TTS, SLAM, Provider, Runner and Verifier were not changed or executed.
