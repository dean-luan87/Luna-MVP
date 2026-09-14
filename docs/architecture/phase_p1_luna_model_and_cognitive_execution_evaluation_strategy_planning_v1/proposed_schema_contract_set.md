# Proposed Schema Contract Set

Planning only; no types or schemas are implemented in this phase.

## Reuse directly

- Model Test Case Manifest;
- Model Test Result Envelope;
- Model Test Trace;
- EvaluationReportV0;
- ModelBenchmarkRecordV1;
- TestBoard protected artifact records;
- Human Correction records;
- Observation Demand/Request, Capability Requirement, Evidence Sufficiency,
  Current World, Hypothesis, and NextCycle candidate refs.

## New or revised planning contracts for a later phase

1. `EvaluationExecutionProfileV1`: joins case, dataset/sample, governance,
   observation cycles, evidence, cognition, performance, failures, stop reason,
   and trace refs. It is evaluation-only.
2. `ModelFitProfileV1`: task/condition-scoped model/version/provider fit,
   evidence quality, failure modes, latency/resource, cognitive burden, and
   regression refs.
3. `CognitiveBurdenMetricsV1`: raw and normalized uncertainty/conflict,
   hypothesis revision, information-gap, re-observation, and amplification
   measures.
4. `EvaluationFailureGapRefV1`: taxonomy ID, detector, owner, severity,
   affected refs, provenance, and resolution state.
5. Revision to Model Test Case Manifest: references to dataset/sample versions,
   environment condition, resource constraint, and expected observation
   requirement.
6. Revision to MUEP input vocabulary: explicit object detection task/model
   representation, coordinated with existing `detection_tracking` naming.

## Contract invariants

- no global version;
- every result retains model/provider/capability and dataset/sample lineage;
- evaluation output is candidate/evidence, not World Truth;
- no automatic runtime policy or binding mutation;
- unavailable nodes and metrics are explicit;
- old versions remain immutable and comparable.
