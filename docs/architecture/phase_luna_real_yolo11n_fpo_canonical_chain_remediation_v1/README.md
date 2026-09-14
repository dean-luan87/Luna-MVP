# Luna Real YOLO11n / FPO Canonical-Chain Remediation v1

This package records the targeted remediation of F-001/P1 and the related
F-004/P2 real-path version/invalidation gap.

Disposition: `MINIMAL_ROUTE_B_COMPATIBILITY_SEAM`.

The existing FPO executor remains in place. A new FPO-side adapter consumes
references from Capability Governance, Runtime Admission, and Provider
Governance. It does not create or mutate their lifecycle records. Real
Provider invocation fails closed when the canonical chain is absent, stale,
or inconsistent.

The A-Route S3 caller now has an explicit upstream-records input and invokes
the fail-closed context builder before passing the resulting context to the
FPO seam. No current repository caller was found that produces all five
required governed records, so this phase does not manufacture them.

No model, Provider, camera, Observation, or runtime was executed in this
phase. Terminal verification remains required.
