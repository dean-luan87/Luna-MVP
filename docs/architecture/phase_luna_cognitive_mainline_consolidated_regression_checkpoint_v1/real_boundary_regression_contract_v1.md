# Real-approved boundary contract

The Real Input phase remains controlled and provider-free under its existing contract.

The Real Capability phase is opt-in. It preserves YOLO11n single-frame behavior, `real_provider_invocation_count=1`, `max_real_provider_invocation=1`, and `second_real_invocation_allowed=false`. `REQUEST_MORE_EVIDENCE` must not trigger a second call.

The consolidated checkpoint requires explicit terminal-owned source, model,
dependency-status, declared-checksum, and observed-checksum arguments for the
Real Capability child. It forwards these values unchanged and never invents
readiness state. Missing values produce `READINESS_ARGUMENTS_REQUIRED` without
launching the child or attempting Provider invocation. Failed real children
retain their stdout/stderr together with parsed Runner/Verifier summaries for
first-divergence diagnosis.
