# Audit matrix

| Dimension | Source | Current audit treatment | Required result |
|---|---|---|---|
| Operational integrity | Full E2E operational source | Recompute two controlled Action-Candidate cases and no runtime dispatch | PASS |
| Cognitive logic | Shared conformance contract and Full E2E contrast output | Reuse required contrast assertions; no aggregate-only shortcut | PASS |
| Owner integrity | Canonical owner refs in cognition, Task Manager, and Action outputs | Check owner fields and forbidden takeover flags | PASS |
| Traceability | Contrast and downstream traceability payloads | Require non-empty linked refs at each applicable hop | PASS |
| Contract integrity | Static source contract audit plus same-scenario contrast audit | Check conditioning fields, candidate projections, and identifier-only scenario use | PASS |
| Negative guards | Full E2E and downstream forbidden flags | Require every observed forbidden flag to be false | PASS |

The final Runner writes only `_eval_out/luna_controlled_cognitive_runtime_final_closure_audit_v1/audit_report_v1.json`.

