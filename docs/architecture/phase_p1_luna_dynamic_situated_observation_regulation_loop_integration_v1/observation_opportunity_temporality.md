# Observation Opportunity Temporality

Opportunity is a candidate assessment of the current Situated State and
temporal context. `OPEN` is not a permanent Provider permission.

The `OPPORTUNITY_CAN_BE_LOST_BEFORE_EXECUTION` case deliberately produces an
open eligible state at `t1` without issuing an execution admission, then
re-evaluates at `t2` after relation stability is lost. The t2 state is closed,
ineligible, and has no Provider invocation.

The existing execution gate is consulted again for an executing state. A stale
Opportunity reference is never reused to authorize a later Provider call.
