# Implementation summary

Canonical additions:

- structured Module scope fields;
- Requirement requester/problem/operation/contract/authority references;
- `CapabilityScopeAssessmentV1`;
- `CapabilityGapCandidateV1`;
- scope-aware resolution and invocation helpers;
- Self scope visibility refs;
- 35 controlled scenarios.

The old resolution function remains available for foundation compatibility;
the new scoped path explicitly validates scope before using it.
