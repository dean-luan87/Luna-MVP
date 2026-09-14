# User control, degradation, and upgrade boundary

Optional user uninstall may be represented as a candidate. Mandatory Safety
uninstall or disable-below-baseline is rejected. User presentation and
notification settings are outside this module and cannot disable the
underlying safety capability.

Provider failure or below-baseline status produces `DEGRADED` or
`SAFETY_BASELINE_BLOCKED` candidates with escalation and rollback references.
Approved replacement is eligibility only; no automatic upgrade or rollback
is performed.
