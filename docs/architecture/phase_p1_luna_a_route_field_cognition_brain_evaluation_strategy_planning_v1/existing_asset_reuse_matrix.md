# Existing Asset Reuse Matrix

| Existing asset | Status | Owner | Use in A-Route evaluation |
|---|---|---|---|
| `ObservationDemandCandidateV1` / `ObservationRequestCandidateV1` | reusable | FPO/Observation | Demand, target, capability and cycle trace. |
| `CapabilityRequirementCandidateV1` | reusable | Capability Governance | Requirement evidence, not model selection. |
| `EvidenceSufficiencyCandidateV1` | reusable | A/FPO candidate boundary | Sufficiency transitions and gaps. |
| `NextCycleIngressCandidateV1` | reusable | A/FPO | Re-observation candidate and feedback refs. |
| `CurrentWorldCandidateV1` | reusable | Cognitive State Formation | Candidate world representation only. |
| `CognitiveHypothesisCandidateV1` | reusable | A | Hypothesis and revision lineage. |
| Attention/cognitive state assets | extend | A/Attention boundaries | Need actual selected/ignored target trace. |
| Information-gap detector/re-observation policy | reusable/extend | FPO | Structural gaps; needs attribution and cycle lineage. |
| RF-DETR Roboflow PoC | external capability evidence | Provider/FPO | First external provider case, not primary test object. |
| Model/Capability/Provider registries | reusable | canonical governance owners | References only. |
| Model Test Case/Result/Trace | reusable/extend | Model Test Lens | Case/result surface; add A-route profile refs. |
| TestBoard | reusable | Test Governance | Durable protected evidence. |
| OCR Dataset Registry | precedent | Evaluation | Domain precedent; no universal promotion. |
| Previous Model Fit/Execution plans | superseded in emphasis | Evaluation | Retain external capability comparison as L3/L4 support. |
| Unified A-route profile | missing | Evaluation/A boundary | Required next contract. |
| Cognitive White-box UI | future-only | future presentation layer | No implementation now. |

Generated `_tmp_eval_out`, `_eval_out`, and Roboflow smoke outputs remain
evidence-only.
