# Diagnostics Legacy Overlap v1

| Asset family | Disposition | Canonical treatment |
|---|---|---|
| Model/Provider health helpers | NARROW | Produce source health refs; Diagnostics aggregates; Model/Provider retain lifecycle/admission. |
| Field/Task/FPO diagnostics | NARROW | Local module diagnostics remain local; cross-domain health is handed off by ref. |
| Maintenance diagnostic aggregator | COMPATIBILITY_ONLY | Candidate aggregation, not global Truth or remediation. |
| Health watchdog skeleton | NARROW / DEFERRED | Health signal and handoff candidates only; no daemon/restart/repair. |
| Protocol/config drift checks | KEEP + REASSIGN lifecycle | Diagnostics reports drift; Protocol/registry owners change sources. |
| Static validators/Test Lens | KEEP as tooling | No runtime diagnostic/admission authority. |
| Runner/Verifier diagnostics | COMPATIBILITY_ONLY | Test/development evidence, not live health. |
| Dynamic Flow/A Route failure helpers | REASSIGN | Consumer-specific handling; Diagnostics refs only. |

No legacy asset is deleted in this phase.
