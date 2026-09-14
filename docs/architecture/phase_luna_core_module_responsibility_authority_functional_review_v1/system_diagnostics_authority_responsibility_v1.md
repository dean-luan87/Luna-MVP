# System Diagnostics Authority and Responsibility v1

| Diagnostic authority | Paired responsibility |
|---|---|
| Dependency presence/version/importability | Correct bounded dependency observation, compatibility classification, staleness and provenance. |
| Runtime/process/loader health | Correct availability and contract/version observation. |
| Device health | Correct device availability/degradation measurement for declared device scope. |
| Model asset observation | Correct observed presence/loadability/integrity evidence; Model Manager owns identity and declared asset truth. |
| Provider health | Correct instance/adapter/capacity/latency/failure health evidence. |
| Resource facts | Correct measurement/reporting of memory, GPU, CPU, battery, thermal, network, storage, latency, and bandwidth. |
| Protocol/config/manifest drift | Correct comparison and source-linked mismatch reporting; source owners retain change authority. |

Diagnostics owns errors in these observations/classifications, including stale
PASS publication, provenance loss, cross-component contamination, invalid
aggregation, and failure to expose unknown/conflict. It does not own a wrong
Runtime Admission, Capability resolution, Brain policy, Provider invocation, or
A response except where incorrect diagnostic evidence caused the downstream
error.
