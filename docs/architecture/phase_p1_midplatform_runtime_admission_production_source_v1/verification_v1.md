# Verification surface

`runner_v1.py` contains one repository-backed positive validation case and
fail-closed cases for missing resolution, stale binding, missing provider
binding, version mismatch, revoked Grant, Permission/Safety/Resource blocks,
Envelope incompatibility, invalidation, and missing provenance.

`verifier_v1.py` checks repository source paths, owner preservation, version
lineage, constraints, executable gating, and all no-execution/no-mutation
guards. It also invokes the previous governed-record producer compatibility
surface so `RUNTIME_ADMISSION_PRODUCTION_SOURCE` is source-detected rather
than hardcoded.

Agent did not run the Runner, Verifier, Python, model, Provider, or runtime.
