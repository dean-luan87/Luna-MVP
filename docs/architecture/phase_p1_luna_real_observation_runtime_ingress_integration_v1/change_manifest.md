# Change Manifest

## Additive contract/runtime changes

- Added a Gateway-owned runtime observation envelope and live admission proof.
- Added optional runtime observation and information-need fields to the
  existing Gateway request.
- Allowed `LIVE_RUNTIME` through the existing execution-mode validation.
- Reused the existing conditioned A-Route/Cognitive State Formation body for
  live-mode admitted observations.

## New phase tooling

- `capabilities/midplatform/core/observation_runtime_ingress/`
- phase Runner and read-only Verifier
- phase documentation
- Missing-information verification now uses explicit partial evidence coverage
  and the canonical sufficiency status (`INSUFFICIENT`).

No Decision, Task, Action, Runtime Executor, Archive, Memory, Learning, or
provider implementation was changed.
