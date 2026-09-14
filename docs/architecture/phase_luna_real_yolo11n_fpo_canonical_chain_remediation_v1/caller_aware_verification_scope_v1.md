# Caller-Aware Verification Scope v1

`real_yolo11n_caller_aware_verification_v1.py` reads actual source files and
checks that:

- the real entrypoint accepts canonical binding context;
- the A-Route caller invokes the context builder from explicitly supplied
  upstream records;
- the real branch calls the canonical FPO compatibility adapter;
- the Provider adapter contains the canonical-chain fail-closed guard;
- legacy real-capable callers delegate through the shared Provider guard.

This is source-wiring evidence, not runtime proof. It addresses the earlier
F-002/F-003 criticism for this path by inspecting call structure rather than
validating only self-generated owner/ref records.

The inspection must still report whether any repository caller constructs the
required `CanonicalYOLO11nUpstreamRecordsV1`; the A-Route parameter alone is
not evidence that governed records exist.
