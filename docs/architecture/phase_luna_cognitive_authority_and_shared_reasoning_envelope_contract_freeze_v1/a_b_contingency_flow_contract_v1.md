# A to B to A Contingency Flow Contract

## Frozen flow

A detects material uncertainty
→ A creates B request
→ B receives bounded Working Envelope
→ B reasons within scope/depth/resource limits
→ B returns non-binding result
→ A compares result with current reality
→ A chooses KEEP, USE, PARTIAL_USE, SUPERSEDE, DISCARD or REQUEST_UPDATED_B

## Concurrency

- B can run concurrently with A under shared governance.
- A can pause while B continues.
- B can finish and wait.
- A can continue while B is waiting.
- B result can become stale after a new A state version.
- Reality update invalidates B without being a B capability failure.

## Cross-B transfer

There is no direct B1 → B2 cognitive transfer.

Required reuse path:

B1 result
→ A evaluates and assimilates as a candidate
→ A creates a new bounded B2 request

This preserves source state versions and prevents hidden B-owned concern
continuity.

## Result binding

B output remains non-binding. A owns relevance, adoption, invalidation and
whether the result affects the current Need, Hypothesis, sufficiency or next
step. Brain retains global adjudication.

## Loop relationship

A and B may use the shared Loop Engine for state persistence, but neither
delegates semantic authority to Loop. A/B commands to Loop must use the
mechanical command contract.
