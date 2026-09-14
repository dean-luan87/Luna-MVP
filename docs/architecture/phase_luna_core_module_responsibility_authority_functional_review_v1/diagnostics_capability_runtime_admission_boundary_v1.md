# Diagnostics Capability and Runtime Admission Boundary v1

Diagnostics evidence is an input to Runtime Admission together with Model
Manager refs, Provider compatibility, Permission, Safety, Resource, integrity,
and source versions. Diagnostics must never construct an Executable Capability
Candidate.

Logical Capability Resolution remains independent from current health:
`object_detection` may be logically supported while its model/runtime is
unhealthy. Runtime Admission may then return blocked/degraded. Diagnostics
does not turn health into capability taxonomy or execution authority.
