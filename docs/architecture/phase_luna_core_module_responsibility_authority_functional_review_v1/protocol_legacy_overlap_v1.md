# Protocol Legacy Overlap v1

| Asset family | Disposition |
|---|---|
| Protocol Manager registry/checker | KEEP / NARROW; candidate governance surface. |
| Local module schemas/contracts | NARROW; remain local until cross-module. |
| Duplicate enums/contracts | LEGACY_OVERLAP; later consolidation only. |
| Compatibility adapters | KEEP / NARROW; explicit version translation only. |
| Dynamic Flow/A Route/B1/B2 contracts | COMPATIBILITY_ONLY; no lifecycle authority. |
| Navigation/speech protocols | NARROW; domain owner retains semantic/action authority. |
| Model/Capability/Provider admission protocols | KEEP as protocol contracts; admission owners remain separate. |
| Permission/admission contracts | KEEP as representation contracts; policy/admission owners remain separate. |
| Migration helpers | DEFER / COMPATIBILITY_ONLY; no execution here. |
| Runner/Verifier protocol checks | COMPATIBILITY_ONLY; evidence, not governance mutation. |

No migration or deletion occurs in this phase.
