# Governance Discovery Go / No-Go v1

## V0 readiness

Ready when all discovery outputs exist and parse, scan roots are recorded, key Model/Capability/Admission/Provider/Calibration assets are represented, and no existing asset is changed.

## V2 decision contract

`LUNA_GOVERNANCE_ASSET_DISCOVERY_READY` means the read-only discovery package is complete. It does not authorize consolidation, ownership migration, file movement, deletion, code changes, Runtime, Provider, Model, Hardware, or Action execution.

Failure output must be `LUNA_GOVERNANCE_ASSET_DISCOVERY_REMEDIATION_REQUIRED` or the verifier's blocked contract.

## Interpretation rule

“Duplicate Candidate” and “Missing Ownership” are review findings, not commands. Canonicalization requires a separate approved phase.
