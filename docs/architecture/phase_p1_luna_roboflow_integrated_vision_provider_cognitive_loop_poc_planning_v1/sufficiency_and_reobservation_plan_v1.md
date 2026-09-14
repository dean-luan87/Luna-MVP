# Sufficiency and Re-observation Plan

## Reused mechanisms

The repository already provides `EvidenceSufficiencyCandidateV1` with
expected/received evidence kinds, source diversity, contradiction and
uncertainty refs, temporal validity, target/semantic/spatial coverage and a
candidate status. The active observation engine distinguishes `SUFFICIENT`,
`INSUFFICIENT`, `CONTESTED`, `STALE`, `NEEDS_CONFIRMATION`,
`NEEDS_ADDITIONAL_MODALITY`, `NEEDS_REDIRECT` and `NEEDS_PROVIDER_SWITCH`.

`field_perception_information_gap_detector_v1.py` aggregates missing, stale,
uncertain and conflicting information. `field_perception_reobservation_policy_v1.py`
enables another bounded observation on stale/conflicted evidence. The
observation engine can produce `NextCycleIngressCandidateV1` with feedback and
correction refs.

## Ownership

- A owns local relevance, hypothesis interpretation, sufficiency consequence,
  reconsideration and next-step recommendation.
- FPO/Attention/Observation translates a recommendation into a bounded
  acquisition candidate and manages correlation/deduplication.
- Capability/Runtime/Provider Governance owns the corresponding admission
  boundaries.
- Brain is involved only when the consequence changes Goal/Concern/Grant or
  global constraints.

## Targeted second observation

For the exit scenario, insufficient detection can request an ROI-focused OCR
or a new visual observation. A should provide the information gap/target;
Attention/Observation forms the request. The provider cannot autonomously
start a second request. No retry engine is introduced.

## Missing seam

The existing mechanisms are mostly controlled/candidate-oriented and use
generic mappings. A future PoC implementation still needs a caller-aware
translation from Roboflow text/detection output into the chosen canonical
evidence family, plus a real evidence-to-A reassessment input. This is an
implementation seam, not a new semantic owner.

