# Need / Can / How / When

`CapabilityNeedCandidateV1` expresses the current Goal/Intent/Concern-bound
capability need. `CapabilityNecessityCandidateV1` distinguishes:

- `REQUIRED`: the capability need is active and current continuation is not
  sufficient;
- `NOT_REQUIRED`: the capability may be available, but current cognition can
  continue without it;
- `DEFERRED`: required candidate inputs are unavailable.

The minimum condition resolver answers which subset of a capability's
supported dimensions is required for this Information Need. It is not driven
by the case name. `CapabilityFeasibilityCandidateV1` answers Can by comparing
that resolved requirement with the situated state. `CapabilityConditionGapV1` answers what
condition is missing. `CapabilityConditionAdjustmentNeedV1` gives only an
abstract condition improvement such as `NEED_BETTER_VISIBILITY` or
`NEED_STABLE_RELATION`.

`CapabilityOpportunityCandidateV1` answers When using `OPEN`, `CLOSED`, or
`UNSTABLE`. None of these candidates prescribes motion, creates an Action, or
invokes a Provider.
