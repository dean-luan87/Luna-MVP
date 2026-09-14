# Task Failure Responsibility v1

Task owns:

- malformed dependency graph;
- invalid Task lifecycle transition;
- incorrect readiness aggregation within its contract;
- incorrect completion evaluation against supplied conditions;
- cross-Task contamination;
- invalid handoff or lost Task trace/provenance.

Task does not own wrong Intent, A Need, Capability resolution, Runtime
Admission, Provider execution, Action runtime, Loop persistence, or Brain
governance errors. It should return blocked/waiting/failed candidates with
source refs instead of semantic recovery advice.
