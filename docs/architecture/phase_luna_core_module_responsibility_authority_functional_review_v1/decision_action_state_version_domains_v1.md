# Decision / Action State-Version Domains v1

Keep domains distinct:

- Decision version: option/commitment lineage and revocation.
- Task version: dependency/readiness/completion organization.
- Action contract/execution version: concrete operation, target and
  idempotency lineage.
- Capability/Runtime Admission version: logical and executable availability.
- Field/Context/Current World version: source/precondition freshness.
- Loop version: mechanical persistence lineage.

Action admission must bind to valid source versions; no global state version is
introduced.
