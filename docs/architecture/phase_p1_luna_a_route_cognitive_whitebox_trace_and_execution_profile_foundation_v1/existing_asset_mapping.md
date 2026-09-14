# Existing Asset Mapping

| Existing asset | Mapping |
|---|---|
| `ObservationDemandCandidateV1` | `OBSERVATION_DEMAND` source ref |
| `ObservationRequestCandidateV1` | `OBSERVATION_REQUEST` source ref |
| `CapabilityRequirementCandidateV1` | `CAPABILITY_REQUIREMENT` source ref |
| `EvidenceSufficiencyCandidateV1` | `SUFFICIENCY` source ref and transition summary |
| `NextCycleIngressCandidateV1` | `REOBSERVATION` / next-cycle source ref |
| `CurrentWorldCandidateV1` | `CURRENT_WORLD_CANDIDATE` source ref |
| `CognitiveHypothesisCandidateV1` | `HYPOTHESIS` / `HYPOTHESIS_REVISION` source ref |
| Information Gap Detector | `INFORMATION_GAP` source ref |
| Re-observation Policy | `REOBSERVATION` metadata/source ref |
| Model Test Trace | parent evaluation trace/artifact ref |
| Model Test Result Envelope | candidate result artifact ref |
| TestBoard Protocol | protected/non-authoritative artifact ref |
| RF-DETR real smoke | precedent only; not a dependency or corpus source |

No existing candidate type was modified. The new types are observation/profile
contracts in the Evaluation subsystem, not replacements for cognitive owners.
