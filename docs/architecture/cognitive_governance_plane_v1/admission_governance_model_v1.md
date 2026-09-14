# Admission Governance Model v1

Admission is the controlled entry gate for Protocol, Capability, Model,
Hardware, Field, and Authority objects.

## Admission checks

1. Identity and provenance;
2. Constitution compatibility;
3. Protocol compatibility;
4. Declared capability and limitation;
5. Authority and permission scope;
6. Resource profile and budget;
7. Health and diagnostics baseline;
8. Evidence/output contract;
9. Risk and failure namespace;
10. Rollback, expiry, and deprecation plan.

Admission result is a candidate: Admitted, Deferred, Rejected, Expired, or
Blocked. Admission is not Runtime enablement and not Provider execution.

## Boundary

Admission cannot create a Goal, make a Decision, modify Reality, grant Action
permission beyond Authority Governance, or bypass Protocol Manager. A Provider
cannot admit itself. A Model cannot admit itself. Any failed Constitution check
is a Governance Blocker.

Health is an admission input. Admission cannot make a Decision. Provider
cannot admit itself.

Health is an admission criterion. Provider cannot admit itself.

The admission health signal is explicit.
