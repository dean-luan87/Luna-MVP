# Audit Method v1

The audit treated the freeze ledger as falsifiable claims. Evidence priority was:

1. actual implementation and direct callers;
2. entrypoints, imports, registries, and executable adapters;
3. controlled fixtures/runners/verifiers as evidence of declared boundaries only;
4. architecture documents as claims and historical context.

No Python, project Runner, project Verifier, model, Provider, Observation, Action, or runtime was executed. Evidence was collected by static file and symbol inspection. A symbol without a caller was not promoted to an active runtime authority. A runnable entrypoint with a real execution branch was recorded as an execution surface even when no production dispatcher caller was found.

Classification vocabulary:

- `CANONICAL`: implementation matches the frozen boundary.
- `COMPATIBILITY_ONLY`: controlled bridge or historical seam with explicit candidate/deferred limits.
- `DORMANT`: present but no repository caller found.
- `ACTIVE_OVERLAP`: executable path exists and overlaps a frozen boundary.
- `AUTHORITY_BYPASS`: active path skips a required canonical authority.
- `DUAL_AUTHORITY`: two paths can make the same final decision/mutation.
- `UNDECLARED_AUTHORITY`: distinct state/transition authority is not represented by the ledger.

