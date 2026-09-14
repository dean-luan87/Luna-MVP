# Compatibility candidate contract

Canonical implementation:
`capabilities/midplatform/field_perception_orchestrator/integration/perception_routing_admission_compatibility_v1.py`

Owner: `Field Perception Orchestrator / Active Observation Control`.

`PerceptionRoutingAdmissionCompatibilityCandidateV1` is an immutable
projection of exactly one `PerceptionRoutingCandidateV1`. It preserves:

- source routing candidate, Observation Demand, Capability Requirement, and
  Capability Resolution refs;
- capability/class and slot handoff refs;
- observation class, targets, constraints, and expected contribution refs;
- Need/Gap, Strategy/Branch, parent problem, state, context, lineage,
  provenance, and trace refs.

The candidate explicitly remains:

```text
candidate_only = true
read_only = true
truth_declared = false
world_truth_declared = false
runtime_admission_requested = false
runtime_admission_executed = false
```

The result uses the minimal statuses:

- `ADMISSION_COMPATIBILITY_CANDIDATE_FORMED`
- `NO_ADMISSION_COMPATIBILITY_CANDIDATE`
- `ADMISSION_COMPATIBILITY_GAP`
- `INVALID_INPUT`

Formation is one-to-one: every valid input routing candidate produces one
compatibility candidate. Multiple routes remain multiple candidates; same
class is not deduplicated, and the same capability supporting multiple
demands is not merged.

Formation fails closed for malformed collections, duplicate route refs,
missing targets, unsupported observation class, invalid candidate flags, stale
or incoherent lineage, and runtime-implying source flags. It does not rerun
Capability Resolution.
