# Capability Scope Boundary v1

Scope answers only:

> Is this structured requirement inside the governed capability/module domain?

Scope may evaluate problem class, operation, input contract, output contract,
requirement type and required authority. Existing scope results include
`IN_SCOPE`, unsupported problem/operation/input/output and authority-not-allowed
conditions.

Scope must not answer:

- whether a model file is installed;
- whether checksum/integrity matches;
- whether dependencies are healthy;
- whether a device/runtime is available;
- whether Provider execution is authorized now;
- whether A's Need is sufficient.

An out-of-scope result is a logical capability failure, not a Runtime Admission
failure.
