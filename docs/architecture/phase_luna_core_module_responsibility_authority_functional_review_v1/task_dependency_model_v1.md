# Task Dependency Model v1

Task may own the dependency graph and ordering relation for Task-to-Task,
capability, observation, environment, permission, resource, and external
prerequisite refs. Source owners retain truth about whether each prerequisite
is satisfied.

`resolve_dependencies_v1()` preserves refs and marks unknown/non-ready values
as waiting. This is the correct shape for candidate aggregation, provided the
result is not promoted into Capability admission or global policy.

Task must reject or wait on missing, stale, revoked, or cross-scope refs rather
than invent satisfaction. Dependency failure is not automatically a Need,
Intent, Concern, or Loop decision.
