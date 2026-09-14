# LogicalCapabilityResolution Boundary

## Meaning

`CapabilityResolutionCandidateV1` answers:

> Which registered logical capability/module/slot can potentially satisfy this
> Capability Requirement under the current scope, lifecycle, permission,
> resource and registry constraints?

It does not answer whether the current physical model/runtime is executable.

## Input references

- Capability Requirement ref
- logical capability ref
- capability slot ref
- requested operation/input/output refs
- scope/permission/resource refs
- source state version
- trace/provenance

## Output boundary

The existing resolution statuses remain:

- `READY_CANDIDATE`
- `UNAVAILABLE_CANDIDATE`
- `DEGRADED_CANDIDATE`

The output may preserve model/provider/implementation refs, but those refs are
options or candidates. `READY_CANDIDATE` must not be interpreted as Runtime
Admission approval.

## Forbidden interpretation

Logical Resolution must not:

- load a model;
- inspect a live dependency environment;
- compute or verify a checksum;
- probe a device/runtime;
- invoke a Provider;
- create an executable capability fact;
- create a Need, Goal, Decision, or Action.

