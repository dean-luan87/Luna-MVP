# Temporal Situation Enhancement Model v1

## Role

Temporal understanding improves the meaning of the current Situation without
replacing it. Static reality says what is represented now; temporal enhancement
states whether a relevant condition appears stable, changing, cyclic, abrupt,
or insufficiently observed.

```text
Situation Candidate
        +
Temporal World State Candidate
        +
Temporal–Self Coupling Candidate
        ↓
Temporal Situation Enhancement Candidate
        ↓
Decision Support Candidate
        ↓
Brain Evaluation
```

## Candidate fields

- `change_relevance_candidate`: why an observed change matters to the current
  Situation.
- `stability_candidate`: stable, transitioning, cyclic, abrupt, or unknown.
- `risk_window_candidate`: bounded possibility that change may affect the
  current Goal or resource envelope.
- `observation_need_candidate`: additional observation may be useful.
- `temporal_uncertainty`: missing duration, coverage, cadence, cause, or trend
  confidence.
- `trace_ref`: source links and interpretation path.

## Example and boundary

Static: “the road is congested.” Temporal enhancement: “the road appears to be
rapidly becoming more congested; duration and cause remain uncertain.”

The enhancement does not decide to reroute, increase observation frequency, or
declare danger. Those remain downstream candidate and Brain-governed work.

