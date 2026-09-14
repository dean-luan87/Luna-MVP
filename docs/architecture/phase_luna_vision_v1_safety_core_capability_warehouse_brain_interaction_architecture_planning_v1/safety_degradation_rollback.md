# Safety degradation and rollback

Safety provider failure, incompatible dependency, or performance below the
minimum supported baseline produces `DEGRADED` plus diagnostics and a
rollback/remediation candidate. Existing System Maintenance diagnostics and
Model Manager asset/provisioning contracts are the reusable surfaces.

Degradation does not silently uninstall or replace the mandatory capability,
and rollback is a governed candidate operation rather than runtime execution
in this phase.
