# Diagnostics Dependency Health v1

Diagnostics may observe package presence, declared/observed version,
importability, compatibility, dependency-group status, probe freshness, and
provenance. The existing dependency-probe assets are evidence/planning or
controlled-probe artifacts; they do not authorize installation.

Model/Runtime Admission consumes dependency health refs and decides whether a
candidate is blocked, degraded, or executable. Diagnostics reports
`DEPENDENCY_MISSING`, version mismatch, probe failure, stale, or unknown where
supported; it does not install, upgrade, or redefine the capability taxonomy.
