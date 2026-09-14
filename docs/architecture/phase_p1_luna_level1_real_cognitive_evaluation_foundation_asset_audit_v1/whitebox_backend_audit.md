# White-box Backend Audit

Canonical foundation: `capabilities/evaluation/a_route_cognitive_whitebox_foundation/`.

## Contracts

`CognitiveWhiteBoxTraceV1`, `CognitiveWhiteBoxTraceNodeV1`, `LunaCognitiveExecutionProfileV1`, `ProfileValueV1`, and `CognitiveFailureGapRefV1` are reusable V1 contracts. They contain owner/source/parent/predecessor/successor/cycle/sequence/provenance/source-version/invalidation/candidate-boundary fields. Validators reject authoritative nodes, source/owner omissions, raw/secret metadata, truth, mutation, model/provider/Observation/Action execution, and fabricated unavailable profile values.

The V1 node vocabulary includes the requested cognitive chain. Availability states distinguish `currently_observable`, `partially_observable`, `planned`, and `unavailable`. Profile values distinguish `observed`, `planned`, `unavailable`, `not_observed`, and `not_applicable`.

## Observe / collect / archive / extract

| Capability | Status | Evidence |
|---|---|---|
| Observe | `PARTIAL` | Synthetic trace fixtures and narrow RF-DETR real summary can expose candidate nodes; no general runtime collector. |
| Collect | `PARTIAL` | V1 adapters build profiles from supplied traces; no universal event ingress from A-Route runtime. |
| Archive | `ABSENT` as canonical durable archive | Runner outputs `_eval_out`; TestBoard protects references; neither is a durable evaluation archive contract. |
| Extract | `PLANNED` | Gap refs and profile fields support future diagnostic/Knowledge/Experience candidate extraction, but no safe extraction pipeline was found. |

## Model Test Lens relationship

`capabilities/midplatform/model_test_lens/` is a mature static/test surface with result envelope schemas, local runner bridge, visualization panels, human correction, observation/attention planning, TestBoard refs, and multi-model comparison candidates. Its own types declare it planning/static-site/model-testing oriented, not a White-box product or runtime. Architecture docs identify it as the strongest existing visual base for a future read-only cognitive White-box, but the backend projection from `CognitiveWhiteBoxTraceV1` is not implemented.

## TestBoard relationship

TestBoard artifacts enforce protected, non-deletable process/result/conclusion records and artifact refs. They are a protection/evidence surface, not the owner of cognition, dataset source-of-truth, or durable baseline semantics.

