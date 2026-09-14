# Model Fit Profile Plan

## Scope

Model Fit is scoped by task and condition. There is no global model score and
no automatic preferred runtime model.

## Proposed fields

- model family, model identity, model version, provider and capability;
- task family, dataset/sample class, environment/data condition;
- strengths, weaknesses, known failure modes;
- evidence quality, evidence stability, uncertainty and conflict rate;
- latency and resource cost with measurement status;
- cognitive burden and observation-cycle impact;
- task-success candidate and decision-handoff suitability;
- best-fit conditions and avoid conditions;
- regression against a named previous version or baseline;
- source metric refs, trace refs, provenance, annotation quality, and review
  status.

## Interpretation

A fit profile is an evaluation knowledge candidate. It may recommend review,
but cannot mutate Capability↔Model binding, Provider binding, Runtime
Admission, or routing policy.

## Ground-truth distinction

Quantitative task metrics require an accepted evaluation GT reference. A real
observation without GT may still yield structural/evidence/cognitive metrics,
but must not be reported as ground-truth accuracy.
