# Permission / Admission relationship

The existing Permission / Admission Manager is the canonical owner reused by
this phase. Its existing `runtime_access_admission` path is used as a pure
permission assessment input. It does not dispatch runtime work and its policy
metadata explicitly keeps runtime dispatch disabled.

The new `RuntimeExecutionGrantDecisionV1` is the phase's typed authoritative
result. It requires explicit permission, safety, constitutional, provider,
capability, resource-feasibility, freshness, validity, and runtime-boundary
conditions. It is separate from the existing candidate assessment so that an
admission assessment cannot accidentally be mistaken for a grant.

Permission allowed is necessary but not sufficient: provider eligibility,
safety, constitutional constraints, resource satisfiability, request
freshness, and preparation lineage must also hold. Resource satisfiable is not
resource allocated, and an allowed grant is not execution.
