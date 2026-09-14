# Diagnostics Remediation Boundary v1

Diagnostics may report finding severity, affected component refs, candidate
remediation category, and owner-to-notify. It must not install, restart,
rewrite, reload, reconfigure, migrate, allocate, invoke Provider, or repair
automatically.

Remediation belongs to Maintenance or the responsible owner under separate
governance. A recovery recommendation remains candidate-only; the existing
health-watchdog skeleton's no-recovery/no-restart/no-process-control guards
are consistent evidence for this boundary.
