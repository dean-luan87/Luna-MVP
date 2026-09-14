# Model Contract, Loader, and Dependency Boundary v1

The Model Contract may declare identity, versions, asset refs, checksum,
loader, dependencies, capability/evidence declarations, provider compatibility,
hardware/runtime constraints, provenance, and lifecycle.

Loader Contract describes how a compatible runtime may instantiate an asset;
Loader != Provider. Model Governance owns loader/dependency declarations and
compatibility metadata. Diagnostics observes actual dependency/runtime state;
Runtime/Provider loads only after admission. Model Governance does not probe or
install dependencies.
