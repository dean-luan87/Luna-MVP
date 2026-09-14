# Model State Ownership v1

| State | Classification | Owner |
|---|---|---|
| Model identity/asset declaration | AUTHORITATIVE | Model Governance |
| Governed path/declared checksum | AUTHORITATIVE | Model Governance |
| Observed path/checksum/dependency health | EXTERNAL / REFERENCE_ONLY | Filesystem/Diagnostics |
| Model/weights/manifest/loader versions | AUTHORITATIVE by domain | Model Governance or respective contract owner |
| Capability mapping | Shared contract | Capability Governance + Model Governance |
| Provider compatibility mapping | REFERENCE_ONLY/shared | Model/Provider contract boundaries |
| Lifecycle | AUTHORITATIVE | Model Governance |
| Provisioning candidate | CANDIDATE | Model Governance review |
| Runtime health | REFERENCE_ONLY | Diagnostics |
| Loaded runtime instance | EXTERNAL | Runtime/Provider |
| Runtime Admission | CANDIDATE/admission owner | Runtime Admission |
| Provider invocation/result | EXTERNAL | Provider Governance |
| Baseline/calibration/evaluation | REFERENCE_ONLY | respective owners |
