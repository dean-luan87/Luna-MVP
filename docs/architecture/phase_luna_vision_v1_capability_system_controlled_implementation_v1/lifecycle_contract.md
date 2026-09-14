# Lifecycle contract

The controlled vocabulary is:

`MANDATORY`, `AVAILABLE`, `NOT_INSTALLED`, `INSTALLING`, `INSTALLED`, `ACTIVE`,
`SUSPENDED`, `DEGRADED`, `INCOMPATIBLE`, `RETIRED`.

Optional capabilities may be registered, installed, activated, suspended,
replaced, or uninstalled through future governed transitions. Safety slots
cannot transition to `NOT_INSTALLED` or `RETIRED`, and may not be disabled
below the minimum baseline. No automatic transition is executed here.
