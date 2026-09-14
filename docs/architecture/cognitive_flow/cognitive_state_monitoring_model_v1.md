# Cognitive State Monitoring Model v1

Monitoring Candidate compares Current Cognitive State references with new candidate evidence to determine whether the current cognitive approach may be stale, insufficient, interrupted, or still appropriate. It does not observe the world directly, run a loop, or mutate state.

New information alone is insufficient: a Transition Candidate is relevant only when candidate evidence may change how Luna faces the world. A red car may preserve `Maintain`; an approaching-risk interpretation may justify future transition review.
