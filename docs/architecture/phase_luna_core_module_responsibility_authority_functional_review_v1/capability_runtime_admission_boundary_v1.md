# Capability Runtime Admission Boundary v1

Runtime Admission is a function boundary under the existing Capability
Admission Governance responsibility. It is not a new Manager and not a Model
Manager or Provider implementation.

It consumes supplied refs/evidence for model asset/path/version, integrity,
dependencies, device/runtime health, Provider compatibility, permission,
resource, safety, source state and provenance.

It assesses whether a logically resolved capability can become an Executable
Capability Candidate. It does not probe, calculate checksum, load a model,
invoke Provider or create evidence.

The current candidate adapter distinguishes asset, identity, checksum,
dependency, contract, Provider, permission, resource, safety, stale and
degraded outcomes. This preserves the boundary between logical support and
runtime availability.
