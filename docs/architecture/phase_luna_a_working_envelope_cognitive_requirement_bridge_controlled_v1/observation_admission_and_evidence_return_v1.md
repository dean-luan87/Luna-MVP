# Observation admission and evidence return

Observation is represented with existing `ObservationCandidateV1`. Admission state is either `ADMITTED_OBSERVATION` or `REJECTED` in the synthetic fixture. No acquisition or execution occurs.

The `AEvidenceReturnCandidateV1` preserves Requirement, Scope, Resolution, Observation and admission references and targets `A_REASONING_ROLE`. A evaluates returned evidence through the existing A semantic decision bridge. Observation does not create Need or judge sufficiency.

