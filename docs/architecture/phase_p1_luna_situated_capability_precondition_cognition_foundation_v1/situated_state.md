# Situated Capability State

`SituatedCapabilityStateV1` is a candidate-only projection for one Capability
Need at one temporal point. It references:

- Capability Requirement;
- Self State references;
- Field State references;
- Target and relation references;
- temporal reference;
- condition-state references and satisfied condition references.

It does not become World State and cannot mutate Self, Field, Target, Relation,
or Reality. `t0` and `t1` may retain the same need and capability requirement
while carrying different situated states.

