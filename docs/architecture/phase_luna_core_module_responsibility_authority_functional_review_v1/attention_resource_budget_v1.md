# Attention Resource Budget v1

Candidate resources include compute, latency, sensor time, model invocation
budget, token budget, battery/energy and bandwidth.

Brain/resource governance supplies ceilings, reservations, protected minimums
and revocation/permission constraints. Attention may split or rank a bounded
candidate allocation and report insufficient budget, starvation risk or
degradation.

Attention does not own a global resource ledger, grant unlimited budget, commit
Provider invocations or override safety/resource policy. Actual acquisition
resource consumption remains with Observation/Capability/Provider governance.
