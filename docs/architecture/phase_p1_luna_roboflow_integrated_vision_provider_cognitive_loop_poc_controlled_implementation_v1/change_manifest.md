# Change Manifest

## Created

New integration package:

`capabilities/midplatform/field_perception_orchestrator/integration/roboflow_provider_poc/`

It contains types, Provider client boundary, Evidence translator, cognitive
loop adapter, structural fixtures, scenario manifest, Runner and Verifier.

## Modified

`capabilities/midplatform/model_manager/registry/provider_registry_v1.json`

Added candidate Roboflow Provider declaration under existing Provider
Governance registry conventions.

`capabilities/midplatform/field_perception_orchestrator/integration/roboflow_provider_poc/`

- switched explicit real transport to `InferenceHTTPClient.run_workflow`;
- added governed workflow output mapping and Goal/Concern refs;
- removed the real-mode requirement for user-supplied semantic assessment;
- added a narrow evidence-coverage A-side formation bridge;
- strengthened real-mode metadata and transport verification.

## Not changed

No canonical owner, enum, existing Evidence type, Field/Current World state,
runtime, model, camera, Action, Task, Memory or Learning implementation was
changed. No dependency was installed and no execution was performed by the
agent. The real input no longer contains Hypothesis, Sufficiency or
information-gap answers.
