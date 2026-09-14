# Cognitive Runtime Snapshot Lifecycle v1

## Snapshot Candidate fields

- Current Field Reference
- Situation Candidate
- Context Candidate
- Goal Candidate
- Attention Candidate
- Unknown State Candidate
- Hypothesis Reference
- Future Space Reference
- temporal/spatial/task/risk boundary, provenance, trace

Snapshots are created per Runtime Instance, refreshed by candidate replacement/revision, and released when the process closes. Snapshot != State Mutation, Field State, Reducer State, Memory write, or persistent identity.
