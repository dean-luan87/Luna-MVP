# Action Admission Boundary v1

Before execution, Action Governance checks valid Decision/Task source where
required, Action contract, target/preconditions, source freshness, permission,
safety, resource, capability availability, confirmation, revocation, scope,
duplicate/idempotency and trace/provenance.

Admission means “may be handed to an executor”; it does not mean Provider
invoked, Action succeeded, Task completed or Goal achieved. Unknown required
preconditions remain unsatisfied.
