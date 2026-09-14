# Cognitive Evidence Adapter Skeleton Model v1

`EvidenceCandidate` is immutable and contains `source_ref`, `timestamp`, `context_ref`, `confidence`, `uncertainty`, `content`, and `trace_ref`.

It can be converted to the shared `Candidate` contract with `truth_confirmed=false`. It intentionally exposes no truth-confirmation method and cannot request Decision, Action, State Mutation, or Memory Mutation.

