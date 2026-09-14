# Stage 1 White-box Foundation Regression Finding

Finding: `WB-STAGE1-BACKWARD-COMPATIBILITY`

- Severity: `MAJOR`
- Category: `BACKWARD_COMPATIBILITY`
- Component: White-box foundation
- Stage: Stage 1
- Observed: the user-terminal verifier returned `all_checks_passed=false`
  for the six-scenario synthetic foundation.

The trace and profile contract validators passed for every scenario. The
failure was in verifier expectation logic, not in execution-specific Trace or
Profile identity handling:

1. `premature_sufficiency_guard` compared “no `SUFFICIENT` node” directly to
   `expected_process.premature_sufficiency`. Non-sufficient and contested
   guard fixtures therefore failed even though they correctly avoided a
   sufficient result.
2. The intentional `premature_sufficiency_guard` fixture omits a
   `CURRENT_WORLD_CANDIDATE`; the verifier unconditionally required one for
   every scenario, despite this being the deliberate incomplete-evidence
   guard case.

The remediation makes the fixture expectation explicit and makes the
verifier check the canonical expected sufficiency outcome. It does not remove
the premature-sufficiency guard, trace/profile validation, candidate-only
requirement, ownership fields, or mutation guards.

The historical synthetic mode remains scenario-derived (`cognitive-trace` and
`execution-profile:test-case` identities). Controlled replay continues to use
execution-specific identities through `execution_identity_ref` in the runtime
collector. No Trace V2 or Profile V2 was introduced.

This finding remains part of the full-regression record as resolved only after
the user reruns the White-box verifier successfully.
