# Protocol Governance Existence Test v1

| Alternative | Finding |
|---|---|
| Every module owns its protocol | Rejected: cross-module contracts lose one lifecycle/version authority. |
| Schema/file is authority | Rejected: artifacts implement contracts but do not govern change. |
| Diagnostics owns protocols | Rejected: Diagnostics detects drift; it does not change contracts. |
| Generic Change Control owns protocols | Too broad; change control is a function inside protocol governance. |
| Independent Protocol Governance | **KEEP / NARROW**: preserves identity, compatibility, lifecycle, and auditability. |

The boundary is justified for cross-module protocol source-of-truth, version,
compatibility, change control, drift response, and migration declaration.
