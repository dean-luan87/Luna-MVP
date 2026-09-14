# Metrics and Cognitive Burden Plan

## Metric layers

Reuse MUEP's task, robustness, and structural layers where applicable, while
adding Luna execution metrics as separate dimensions rather than collapsing
them into one score.

## Cognitive burden definition

**Cognitive burden** is the additional work, uncertainty, and risk imposed on
Luna by a model's output before a governed task handoff can be considered.
It is not model latency alone and is not a semantic truth score.

## Candidate measurements

- uncertainty generation rate;
- evidence conflict rate and unresolved-conflict duration;
- hypothesis creation, revision, and supersession counts;
- additional observation requests and actual cycle count;
- information-gap count and persistence;
- cognitive transition count from Evidence to Sufficiency/handoff;
- failure/retry amplification and provider-result rejection rate;
- stale/invalidated evidence exposure;
- human-review burden where available.

## Reporting

Report raw counts, normalized per case, and measurement availability. Keep
task success, provider confidence, evidence quality, and cognitive burden
separate. Provider confidence must not directly set Sufficiency.
