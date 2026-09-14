# System Diagnostics Ontology v1

- **Probe**: a bounded source mechanism that observes or validates one declared condition.
- **Observation**: the probe/telemetry act or its returned observation, not a policy decision.
- **Diagnostic Evidence**: source-linked raw or structured support for a diagnostic claim.
- **Diagnostic Fact**: an authoritative classification within the probe contract and validity window.
- **Health Status**: a bounded condition such as available, degraded, unavailable, stale, or unknown.
- **Diagnostic Assessment/Finding**: derived classification or mismatch report.
- **Diagnostic Incident**: candidate aggregation of related findings, not remediation authority.
- **Diagnostic Report/Snapshot**: versioned presentation of findings and lineage.
- **Diagnostic Trend**: time-correlated evidence, not a governance policy.
- **Drift**: observed mismatch between governed reference and observed state.
- **Failure**: an event/result; it is not automatically an ongoing health state.
- **Admission Block**: a consumer governance result that may reference diagnostics; Diagnostics does not own it.
- **Remediation Candidate**: a candidate recommendation/handoff, never automatic repair.

Probe is not diagnosis; evidence is not an admission decision; health is not
runtime policy; failure detection is not remediation; drift detection is not
protocol mutation.
