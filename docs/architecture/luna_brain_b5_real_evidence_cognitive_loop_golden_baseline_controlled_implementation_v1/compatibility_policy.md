# Compatibility policy

Supported classifications are `BACKWARD_COMPATIBLE`,
`REQUIRES_TARGETED_REGRESSION`, `REQUIRES_FULL_REGRESSION`,
`BREAKING_CHANGE`, and `BLOCKED_CHANGE`.

Compatibility is based on explicit declared change metadata, never filenames.
Guard or trace semantic changes require full review; semantic changes cannot
be declared backward compatible.
