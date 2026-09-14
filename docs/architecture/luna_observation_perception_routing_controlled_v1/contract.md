# Contract

`PerceptionRoutingCandidateV1` represents one explicit pair:

`Observation Demand × active Capability Resolution Candidate`

Formation is deterministic and one-to-one: every valid active resolution
candidate produces one routing candidate. Multiple candidates for the same
demand remain separate; the same capability candidate used by two demands also
produces two separate routes.

The candidate carries the demand target, constraints, expected contribution,
capability class, opaque capability/slot references, and full lineage. The
current resolution contract does not expose a slot reference, so `slot_ref` is
empty in this phase; it is not bound or reserved.

Only resolution candidates with `candidate_only=true`, `read_only=true`,
`truth_declared=false`, `world_truth_declared=false`,
`availability_status=AVAILABLE`, and `admission_status=ADMITTED` are eligible.
The formation function validates coherence but does not rerun capability
matching.

Result statuses are:

- `ROUTING_CANDIDATES_FORMED`
- `NO_ROUTING_CANDIDATE`
- `INVALID_INPUT`
- `UNSUPPORTED_ROUTING_SHAPE`

No resolved candidate, unsupported upstream zero-result, or malformed input
produces a fallback route.
