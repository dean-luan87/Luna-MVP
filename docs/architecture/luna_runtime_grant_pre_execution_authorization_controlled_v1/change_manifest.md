# Change manifest

## Added

- Permission / Admission Manager `runtime_execution_grant_v1.py` contract and
  deterministic formation function.
- Controlled evaluation package under
  `capabilities/evaluation/runtime_grant_pre_execution_authorization_controlled/`.
- Runtime Grant ownership, contract, failure, fixture, and negative-guard
  documentation.

## Modified

- Governance Backbone profile validation now permits an explicitly
  authoritative, non-runtime, non-truth decision profile while preserving
  candidate-only validation for candidate profiles.
- Governance preflight/postflight reports preserve the profile's candidate
  flag.

## Reused

- Protocol Manager Governance Backbone and core rule registry.
- Permission / Admission Manager runtime-access assessment path.
- Provider Governance binding candidate.
- Runtime Executor allocation and execution-instance preparation candidates.
- Observation Gateway and FPO ownership boundaries.

## Not modified

- Provider binding/runtime preparation business semantics.
- Runtime Executor execution engine.
- Observation Gateway runtime ingress.
- FPO active observation control.
- Provider Manager / Model Manager binding or registries.

## Deferred

- authoritative Provider Binding decision if required by deployment policy;
- resource allocation, slot reservation, capability activation;
- execution instance creation and provider session start;
- Gateway submission and runtime observation;
- Provider/Model binding and invocation;
- camera, OCR, SLAM, VLM, YOLO and evidence ingress;
- retry scheduling, live revoke interruption, Evidence Fusion, Decision, Task,
  Action, Field/World integration, and historical verifier migration.
