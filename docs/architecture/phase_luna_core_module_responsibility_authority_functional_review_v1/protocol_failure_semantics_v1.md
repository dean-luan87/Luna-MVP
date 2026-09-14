# Protocol Failure Semantics v1

| Case | Responsibility |
|---|---|
| PROTOCOL_NOT_REGISTERED / invalid identity | Protocol Governance |
| PROTOCOL_VERSION_UNSUPPORTED/MISMATCH | Consumer compatibility/admission; Governance owns declaration |
| PROTOCOL_DEPRECATED/RETIRED | Protocol lifecycle owner |
| PROTOCOL_SCHEMA_INVALID | Producer/consumer validator; Governance owns canonical contract |
| PROTOCOL_FINGERPRINT_MISMATCH | Diagnostics comparison; Governance owns drift consequence |
| PROTOCOL_COMPATIBILITY_INVALID | Protocol Governance |
| PROTOCOL_ADAPTER_REQUIRED | Governance declaration; affected owner supplies adapter |
| PROTOCOL_ADAPTER_FAILED | Adapter implementation owner |
| PROTOCOL_DRIFT | Diagnostics detection; Governance lifecycle/change response |
| PROTOCOL_PROVENANCE_INVALID | Producer/adapter/consumer according to broken lineage |

These are documentation classifications, not new enums.
