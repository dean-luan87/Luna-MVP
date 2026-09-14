# Phase contract

This checkpoint composes existing Runner/Verifier entrypoints only. It does not implement new cognition, alter authority, or duplicate fixtures.

Default execution group is `synthetic`. The `real-approved` group is opt-in and contains only the already approved Real Input and Real Capability Single Invocation phases. `all` explicitly runs both groups.

The checkpoint classifies failures by layer and preserves the original phase exit codes and JSON summaries.

For `REAL-CAPABILITY`, the checkpoint requires explicit terminal-owned source,
model, dependency-status, declared-checksum, and observed-checksum arguments.
It forwards them unchanged to the existing child Runner; absent values produce
`READINESS_ARGUMENTS_REQUIRED` without launching that child.
