# Implementation Overview

## Reused canonical assets

- `VisionProviderAdmissionCandidateV1`
- `VisualDetectionEvidenceCandidateV1`
- `ObservationGatewayEvidenceHandoffCandidateV1`
- `OCRRawEvidenceV1` and `OCRStructuredEvidenceEnvelopeV1`
- `CurrentWorldCandidateV1`
- `CognitiveHypothesisCandidateV1`
- `EvidenceSufficiencyCandidateV1`
- `NextCycleIngressCandidateV1`
- existing FPO information-gap and re-observation builders

## New local integration assets

- `RoboflowProviderRequestV1`: explicit governed refs and real-mode flag.
- `RoboflowNativeResultV1`: adapter-private native payload container.
- `RoboflowNormalizedProviderResultV1`: Luna-owned normalized result with no
  raw payload field.
- `RoboflowCognitiveLoopResultV1`: integration result composed from existing
  canonical candidates.

Real mode uses request-carried `goal_ref` and `concern_ref`; it does not
accept a user-supplied Hypothesis/Sufficiency/Information Gap assessment.
The local adapter is only a controlled A-side formation bridge for structural
evidence coverage. It stops at a Next Observation candidate or a Decision
Governance handoff and never executes either path.

These are integration records, not new authority domains or replacements for
canonical types.
