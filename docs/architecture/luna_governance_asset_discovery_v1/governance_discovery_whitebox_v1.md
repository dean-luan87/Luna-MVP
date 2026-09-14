# Governance Discovery Whitebox v1

| Question | Discovery answer |
|---|---|
| Where is the strongest existing Model Manager surface? | `capabilities/midplatform/model_manager/`. |
| Where is the capability registry plane? | `capabilities/registry/`, with a second registry under Model Manager. |
| Where is Model Admission? | `capabilities/midplatform/model_admission_governance/` and Model Manager governance/lifecycle surfaces. |
| Where is Capability Admission? | Capability registry lifecycle/manifests plus field/provider admission packages. |
| Where is calibration? | Capability registry standards, model benchmark records, evaluation registries, baselines, and drift/readiness documents. |
| Where is Provider boundary? | Model Manager provider adapters, capability runtime contracts, and field/vision/OCR/voice provider packages. |
| Who owns Reality? | Core Architecture Baseline: Reality Workspace / Evidence boundary, not Provider. |
| What is the main risk? | Distributed registries, admissions, lifecycle and calibration assets with possible duplicate ownership. |
| What is allowed now? | Read-only inventory, mapping candidates, and duplicate risk registration. |
| What is forbidden now? | Code changes, moves, deletes, renames, merges, runtime execution, and new governance modules. |

Discovery is evidence for a later governance decision, not an authorization to migrate assets.
