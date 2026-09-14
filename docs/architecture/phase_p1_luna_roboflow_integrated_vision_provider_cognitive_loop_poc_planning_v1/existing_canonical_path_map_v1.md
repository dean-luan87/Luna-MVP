# Existing Canonical Path Map

## Selected path

```text
Brain Goal/Concern/Grant
  → Working Envelope / A cognitive requirement
  → Observation Demand / Observation Request
  → Capability Requirement
  → Capability Resolution
  → Capability↔Model binding
  → Runtime Admission / Executable Capability candidate
  → Observation/FPO Provider Admission candidate
  → Roboflow external adapter
  → Provider Result
  → Evidence/Gateway candidate
  ├→ Current World candidate
  └→ Field Event candidate (only when an operational transition is proposed)
  → Cognitive State Formation / A adoption
  → Hypothesis competition and local sufficiency
  ├→ Decision candidate
  └→ Information gap → targeted next Observation Request
```

The path is a governed loop, not a single answer pipeline. The primary PoC
may stop at a Decision candidate or a Next Observation candidate. It does not
need Task/Action/Outcome/Brain closure to prove external evidence return.

## Existing edge evidence

- The freeze ledger defines `A → Attention`, `Runtime Admission →
  Observation`, `Provider → Provider Result`, `Provider Result → Evidence`,
  `Evidence → Current World/Field candidates`, and candidate return to A.
- `ObservationDemandCandidateV1`, `ObservationRequestCandidateV1` and
  `CapabilityRequirementCandidateV1` preserve target, evidence expectation,
  budget, trace and provenance.
- `EvidenceSufficiencyCandidateV1` and `NextCycleIngressCandidateV1` already
  express the required ambiguity loop.
- B2 consumes `CurrentWorldCandidateV1` read-only and emits a candidate
  observation need; it does not promote World Truth or mutate source state.

## Compatibility seam to avoid

`field_perception_visual_handoff_facade_v1.py` currently calls the older model
requirement/model-candidate adapters and `run_observation_manager_module_v1`.
That path is useful compatibility infrastructure, but its dictionary-shaped
model candidates must not become a second Capability/Model/Runtime authority
for the Roboflow PoC. The future caller should inject the already governed
records/context and use FPO only for acquisition orchestration.

