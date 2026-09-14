# Decision → Direct Action Boundary v1

Normal path: `approved Decision → Task → Action`. A narrow direct path may
bypass Task organization only for a bounded, single-step, low-complexity
operation with no decomposition/dependency graph, explicit target and
preconditions, valid permission/safety/resource constraints, idempotency and
trace requirements, and no hidden long-lived commitment.

Examples can include a short acknowledgement, one notification, a single
speech emission or a stop-current-operation control where existing contracts
support it. Direct path does not bypass Action Governance, Capability/Runtime
Admission, Provider Governance, Brain constraints or result evaluation.
