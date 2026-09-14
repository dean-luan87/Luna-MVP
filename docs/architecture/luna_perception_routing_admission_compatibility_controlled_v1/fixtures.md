# Controlled fixture coverage

The evaluation package is:
`capabilities/evaluation/perception_routing_admission_compatibility_controlled/`.

It covers single and multiple routes, same-class non-deduplication, same-
capability/multiple-demand non-merge, zero routes, invalid routes, lineage
mismatch, missing target, historical provider/model field non-fabrication,
capability-admitted-not-runtime-admitted, Scenario 12 signage/flow/both,
deterministic replay, malformed collection shape, and unsupported observation
class.

The central Scenario 12 shape is:

```text
signage route → one FPO compatibility candidate
human-flow route → one FPO compatibility candidate
```

Both remain abstract and independent. No OCR, VLM, detector, SLAM, Provider,
Model, Camera, Gateway, or FPO runtime operation is inferred or invoked.
