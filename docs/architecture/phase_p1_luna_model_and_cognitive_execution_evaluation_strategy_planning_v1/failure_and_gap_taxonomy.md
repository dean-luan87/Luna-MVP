# Failure and Gap Taxonomy

The taxonomy is for P0 diagnosis and trace routing. It does not create retry
or remediation engines.

| Category | Meaning |
|---|---|
| `dataset_gap` | Missing, inaccessible, unversioned, biased, or unsuitable sample coverage. |
| `annotation_gap` | Missing, malformed, stale, incomplete, or unreviewed GT/annotation. |
| `capability_gap` | Requirement/slot/contract cannot represent the task. |
| `model_gap` | Model lacks required capability, quality, or condition fit. |
| `provider_gap` | Provider unavailable, incompatible, unadmitted, or result failure. |
| `evidence_gap` | No/insufficient/unstable evidence or missing expected evidence kind. |
| `normalization_gap` | Provider result cannot be safely translated to canonical evidence. |
| `observation_gap` | Demand/request/ROI/frame/cycle handoff incomplete. |
| `cognitive_gap` | Hypothesis, revision, context, or semantic consequence path unavailable. |
| `sufficiency_error` | Sufficiency status conflicts with evidence coverage, uncertainty, or conflict. |
| `re_observation_error` | Missing, unjustified, autonomous, or incorrectly targeted next observation. |
| `governance_boundary_error` | Wrong owner, admission bypass, mutation, or Truth declaration. |
| `traceability_gap` | Missing trace, provenance, source version, lineage, or invalidation. |
| `performance_resource_gap` | Latency, memory, compute, network, or energy constraint failure. |
| `regression` | Fixed-suite behavior regressed against a prior version/baseline. |

Each failure should carry detector, responsible owner, affected case/sample,
source versions, evidence refs, severity, and whether it is structural,
semantic-candidate, or evaluation-only.
