# Negative Guards v1

Every synthetic output preserves these guards:

- no Capability mutation by Model;
- no Model mutation by Capability or Provider;
- no Provider mutation by Model;
- no Runtime Admission or Provider Admission;
- no model loading, checksum/dependency/runtime-health probe;
- no Provider invocation;
- no Brain/A/Task selection of physical Model or Provider;
- no Scheduler, Planner or source mutation.

The candidate records remain candidate-only and compatibility-only.

