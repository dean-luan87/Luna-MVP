# Diagnostics Maintenance-Plane Boundary v1

System Diagnostics is a reusable evidence and visibility layer for the
maintenance plane. Protocol Manager, Model Manager, Capability Registry/
Manifest, Baseline, Calibration, and owner-specific maintenance retain their
own lifecycle/change authority. Diagnostics consumes their references and
reports observed mismatch or health; it does not absorb those owners.
