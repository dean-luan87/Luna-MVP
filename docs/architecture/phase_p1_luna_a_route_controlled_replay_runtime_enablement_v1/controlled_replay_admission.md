# Controlled Replay Admission

`ControlledReplayInputV1` requires replay identity/version, origin class, source provenance, evidence refs, deterministic ordering refs, admitted status, and a non-live declaration. Model/provider/live-observation claims and World Truth are rejected.

Observation Gateway creates `ControlledReplayAdmissionV1`. A-Route consumes that Gateway-owned admission; it does not accept arbitrary evaluation payloads or manufacture evidence.

