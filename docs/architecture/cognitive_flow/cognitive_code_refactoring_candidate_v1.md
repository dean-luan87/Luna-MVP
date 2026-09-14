# Cognitive Code Refactoring Candidate v1

## Candidate R1 — Authority-shape admission validation

Add a future validator at the Candidate/Signal admission boundary to reject or quarantine action, decision, permission, State-mutation, and reality-authority claims. Keep the immutable generic `Candidate` core; do not turn it into a controller.

## Candidate R2 — Additive trigger expansion

Extend `CognitiveTriggerType` only in an authorized skeleton phase with Evidence, Context, Self State, and Attention Expiration triggers. Preserve current trigger values and deterministic validation assets.

## Candidate R3 — Runtime snapshot references

Introduce additive references for evidence, self state, resource budget, interrupt, and feedback only when a runtime-skeleton phase establishes their contracts. Do not turn `CognitiveSnapshot` into persistent State.

## Candidate R4 — Component-oriented package landing zones

When implementation is authorized, prefer complete components:

```text
cognitive/
  kernel/
  organization/
  attention/
  process/
  capability/
  runtime/
  contracts/
  governance/
  validation/
```

Do not create these directories during baseline review and do not split them into unowned utility/type fragments.

## Candidate R5 — Preserve validation separation

Keep synthetic runners and validators in `cognitive/validation/`; do not promote them into business runtime paths or use them as Final Phase Verifiers.

