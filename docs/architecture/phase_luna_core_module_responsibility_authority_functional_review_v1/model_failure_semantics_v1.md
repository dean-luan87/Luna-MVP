# Model Failure Semantics v1

| Case | Primary owner |
|---|---|
| MODEL_NOT_REGISTERED / invalid identity | Model Governance |
| MODEL_ASSET_MISSING / observed path absent | Diagnostics evidence; Runtime Admission consequence |
| MODEL_VERSION_MISMATCH | Model Governance declaration or Runtime Admission comparison |
| MODEL_CHECKSUM_MISSING/MISMATCH | Model declaration/integrity evidence; Runtime Admission blocks |
| MODEL_DEPENDENCY_UNSATISFIED | Diagnostics observation; Runtime Admission blocks |
| MODEL_LOADER_INCOMPATIBLE | Model/Loader contract; Runtime Admission consequence |
| MODEL_PROVIDER_INCOMPATIBLE | Mapping contract / Provider admission |
| MODEL_CAPABILITY_MAPPING_INVALID | Split mapping responsibility; Capability side or Model side |
| MODEL_DEPRECATED / RETIRED | Model Governance lifecycle |
| MODEL_HEALTH_DEGRADED / RUNTIME_UNAVAILABLE | Diagnostics; Runtime/Provider admission |

These are documentation classifications, not new enums.
