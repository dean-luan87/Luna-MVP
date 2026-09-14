# Luna Capability Readiness Standard v1

## Scope

This standard defines minimum requirements for lifecycle progression, especially for functional_module_ready.

## Functional Module Ready Minimum Conditions

A capability can be marked functional_module_ready only when all conditions below are satisfied:

1. Responsibility is explicitly defined.
2. Input contract is stable and documented.
3. Output contract is stable and documented.
4. Formal module API exists.
5. Main chain is connected end-to-end.
6. Module-level integration runner exists.
7. Main scenarios pass expected status tagging.
8. Diagnostics support is available.
9. Trace support is available.
10. Replay support is available or explicitly marked not applicable.
11. Authority boundaries are explicit.
12. No unresolved main-chain blocker exists.
13. Known limitations are documented.

## Not Required For Functional Module Ready

The following are explicitly not required for functional_module_ready:

- production enablement
- database integration
- real device integration
- model provider live integration
- full performance stress benchmark

## Evidence Rules

- Ready evidence must be machine-readable and reproducible.
- Evidence references must point to real files.
- Status upgrade cannot skip evidence.
- If integration failures reappear, status must be downgraded according to maintenance policy.
