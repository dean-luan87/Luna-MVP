# B-CR Result Contract and Adoption

## Conceptual result

A B result should carry:

- request ref and source state version;
- completion/status such as completed candidates, partial result, bounded uncertainty, stale source, revoked grant, resource/safety limit, or no useful contingency;
- explored branch refs;
- alternative hypothesis and counterfactual candidates;
- contradiction/consequence findings;
- residual uncertainty and missing-evidence candidates;
- branch/depth/resource usage;
- stale/version, safety and permission status;
- trace/provenance;
- explicit `binding = false`, `world_truth_declared = false`, `decision_created = false`, `action_created = false`.

## A adoption

A may `USE`, `PARTIAL_USE`, `KEEP_AVAILABLE`, `SUPERSEDE`, `DISCARD`, or request updated B where existing contract vocabulary permits. No B result has authority before A evaluation.
