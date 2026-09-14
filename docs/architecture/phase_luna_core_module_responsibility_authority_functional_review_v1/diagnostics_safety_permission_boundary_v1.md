# Diagnostics Safety and Permission Boundary v1

Diagnostics may report thermal warning, device fault, runtime instability,
dependency corruption, resource exhaustion, permission-interface failure,
credential-source unavailability, or stale access evidence. Safety Governance
owns safety policy/risk consequence. Permission Governance owns grants, scope,
revocation, and allow/deny decisions. Brain owns global policy and override;
Diagnostics supplies evidence only.

Runtime/Provider/Observation/Action admission enforces supplied refs. A may
decide cognitive consequence, but Diagnostics never grants permission, changes
safety policy, or determines semantic escalation.
