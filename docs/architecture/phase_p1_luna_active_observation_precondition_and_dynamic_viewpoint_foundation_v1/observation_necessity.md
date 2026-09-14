# Observation necessity

`ObservationNecessityCandidateV1` is evaluated by the active observation
precondition engine from the current information need, required and available
information, information-gap references, and a candidate continuation status.

- `REQUIRED`: information is missing and continuation is not currently possible.
- `NOT_REQUIRED`: continuation is possible, even if some information remains unknown, or the information is already available.
- `DEFERRED`: the continuation prerequisite is unavailable as a candidate.

This freezes the rule `unknown ≠ must observe`. An Observation Demand and an
Information Gap do not by themselves invoke a provider.

