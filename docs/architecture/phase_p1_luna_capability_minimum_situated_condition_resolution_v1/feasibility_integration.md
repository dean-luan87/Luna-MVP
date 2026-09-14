# Feasibility integration

The situated precondition engine now computes:

`minimum_condition_requirement.required_condition_refs - situated_state.satisfied_condition_refs`

It does not use `precondition_definition` as the current requirement. The
definition only supplies supported dimensions and adjustment mappings. The
Feasibility candidate retains `minimum_condition_requirement_ref` so the
resolver-to-Feasibility edge is explicit and auditable.

This preserves the distinction:

`Capability declaration ≠ current cognitive need ≠ current situated assessment`.

Condition gaps and adjustments are generated from the resolved minimum
condition set. Opportunity and eligibility remain downstream candidates; no
execution authority is granted.
