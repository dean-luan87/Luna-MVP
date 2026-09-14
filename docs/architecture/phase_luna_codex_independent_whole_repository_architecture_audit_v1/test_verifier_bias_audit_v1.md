# Test / Verifier Bias Audit v1

## F-002 — Hardcoded legacy audit

`canonical_flow_consolidated_regression/cross_module_checks_v1.py:32-44` assigns legacy surfaces fixed classifications, including `SAFE_COMPATIBILITY`, and `:202-204` returns `active_bypass_count: 0` and an empty list without inspecting repository files or callers. The consolidated case `legacy_bypass_scan` has no child requirement (`:168`) and is therefore synthetic bookkeeping, not a scan.

## F-003 — Synthetic self-confirmation

`cross_module_checks_v1.py:108-132` constructs refs, versions, provenance, owner/responsibility chains and negative flags itself. `:173-205` verifies those generated fields and only checks that child case references exist. The verifier (`verifier_v1.py:17-70`) checks the summary and child verifier fields; it does not inspect actual callers.

Child verifiers are therefore `BEHAVIORAL_SYNTHETIC` with `SELF_CONFIRMING_RISK`, not `CALLER_AWARE` or `RUNTIME_AWARE`. This does not make the controlled seams invalid; it limits their evidentiary scope. Severity: P2.

