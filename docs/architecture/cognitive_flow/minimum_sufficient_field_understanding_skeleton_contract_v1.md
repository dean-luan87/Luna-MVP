# Minimum Sufficient Field Understanding Skeleton Contract v1

## Input references

The builder accepts only declared references for Field, Field Identity, Field Affordance, Field Representation, Current Field View, Primitive, Concept, Context, Temporal, Spatial, Task, and Provenance. A concrete request supplies `field_reference`, `constraint_reference`, `task_reference`, scope mappings, provenance, and trace.

Raw model output, provider payload, action command, decision output, Fact Store, Memory, Learning, Reducer command, and State mutation inputs are rejected.

## Candidate contract

Required candidate fields are `field_reference`, `identity_status`, `constraint_reference`, `behavior_boundary`, `information_gap`, `uncertainty`, `temporal_scope`, `spatial_scope`, `task_reference`, `provenance`, `trace_ref`, and `candidate_status`.

`identity_status` is exactly one of `known`, `partially_known`, or `unknown`. `behavior_boundary` includes allowed/forbidden behavior candidates plus risk and exploration boundaries. It is descriptive only: neither an Action nor a permission grant.

The fixed flags are `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, and `not_action=true`.

## Serialization

Serialization is deterministic canonical JSON: UTF-8-compatible values, lexicographically sorted keys, and compact separators. It does not write data or invoke another subsystem.
