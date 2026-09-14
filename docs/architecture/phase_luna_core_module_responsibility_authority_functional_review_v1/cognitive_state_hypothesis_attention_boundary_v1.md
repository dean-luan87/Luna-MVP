# Cognitive State Formation / Hypothesis / Attention Boundary

## Hypothesis classification

- `CognitiveHypothesisCandidateV1`: `SEMANTIC_CANDIDATE` / `DERIVED_CANDIDATE`
- active hypothesis refs carried in state versions: `INPUT_REF`
- `HypothesisCompetitionResultV1`: candidate comparison representation
- causal truth or single-truth collapse: explicitly forbidden
- A active hypothesis: `ACTIVE_HYPOTHESIS`, external to State Formation

State Formation may assemble and preserve these refs, but cannot activate, rank, invalidate or adopt them.

## Attention

State Formation receives and assembles Attention candidates. Attention Governance owns priority/budget candidate formation. A owns semantic evidence need. Observation/FPO owns acquisition. State Formation does not rank priorities or schedule Observation.
