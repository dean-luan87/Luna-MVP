# Working Envelope Refresh Resolution v1

## Resolution

Refresh is a new Working Envelope admission, not a separate Refresh authority.

`source change → invalidation record → Envelope Candidate → binding validation → new Envelope version → old version superseded`.

## Ownership

- Working Envelope governance owns Envelope identity/version, source binding, constraint binding, refresh admission, invalidation status and supersession record.
- Brain owns Concern/Grant validity, global policy and whether the work remains admitted.
- Source owners own source correctness, versions and invalidation causes.
- Semantic Module and Cognitive State Formation consume the new Envelope for derived products.
- A decides whether stale/partial/refresh-required input means more evidence, reconsideration, defer or another semantic consequence.

## Failure responsibility

Working Envelope owns stale Envelope presentation, wrong source-version map, invalid Grant binding, invalid refresh admission, provenance loss and incorrect supersession. Brain owns invalid Concern/Grant policy. Source owners own source errors. A owns incorrect semantic interpretation. Loop only records refs.

## Forbidden bypass

No automatic refresh daemon, cross-owner source mutation, direct A replan, direct Concern closure, or refresh-to-execution path is implied.

