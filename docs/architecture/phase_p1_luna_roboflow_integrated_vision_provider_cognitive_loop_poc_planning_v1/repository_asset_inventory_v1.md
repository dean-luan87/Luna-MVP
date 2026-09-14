# Repository Asset Inventory

Inventory is source-based and limited to the planned PoC boundary. No code
was executed.

| Surface | Repository asset | Disposition | Finding |
|---|---|---|---|
| Observation demand/request | `field_perception_active_observation_control_types_v1.py` | REUSE | `ObservationDemandCandidateV1`, `ObservationRequestCandidateV1`, `CapabilityRequirementCandidateV1` are candidate-only and traceable. |
| Observation handoff | `field_perception_to_observation_request_adapter_v1.py` | ADAPTER/REUSE | Builds an observation candidate and preserves target, expected evidence, budget, versions and trace context. |
| Active observation loop | `field_perception_active_observation_control_engine_v1.py` | REUSE WITH SCOPE CHECK | Owns bounded acquisition control, not semantic Need or provider autonomy. |
| Sufficiency | same active-observation types/engine | REUSE | `EvidenceSufficiencyCandidateV1` supports coverage, contradictions, uncertainty, temporal validity and candidate status. |
| Re-observation | `field_perception_information_gap_detector_v1.py`, `field_perception_reobservation_policy_v1.py`, observation-control engine | REUSE/ADAPTER | Existing gap and re-observation rules can request another bounded observation. |
| Provider admission | `field_perception_real_vision_evidence_types_v1.py` | REUSE | `VisionProviderAdmissionCandidateV1` is the existing FPO/provider boundary. |
| Provider result/evidence | `field_perception_real_vision_provider_adapter_v1.py` | REUSE PATTERN | Separates native result, evidence candidate and gateway handoff; no truth/source mutation flags. |
| Evidence gateway | `ObservationGatewayEvidenceHandoffCandidateV1` | REUSE | Raw output references and evidence refs remain linked and candidate-only. |
| Current World | `core/cognitive_state_formation/current_world_types_v1.py`, B2 controlled integration | REUSE | `CurrentWorldCandidateV1` is candidate-only and explicitly cannot mutate Field or declare truth. |
| Field | `core/field_event_admission_api_v1.py`, `field_event_admission_types_v1.py`, Field State Reducer | EXISTING OWNER | Field Event remains a proposed transition until Field admission/reduction. |
| Hypothesis | `core/cognitive_state_formation/cognitive_hypothesis_types_v1.py` | REUSE | Supporting/opposing/unknown/conflict refs and candidate confidence are available. |
| A/flow | `a_working_envelope_cognitive_requirement_bridge_controlled`, `a_owned_semantic_decision_loop_bridge_controlled`, cognitive-flow contracts | REUSE/CONTRACT | Existing bridges express requirement and local semantic return; they do not make Roboflow authoritative. |
| Decision | `core/decision_governance/decision_handoff_types_v1.py` and Decision Governance | REUSE LATER | Decision candidate is downstream of sufficiency; not required to force an action in the primary PoC. |
| Task/Action | Task Manager and Action Governance packages | DEFERRED FOR PRIMARY CASE | Include only if a later PoC branch needs an actual side-effect commitment. |
| Canonical governance | `capability_model_provider_binding_controlled`, `runtime_admission_production_controlled`, governed record producer | REUSE | Existing repository-backed chain supplies the canonical upstream seam. |
| YOLO reference provider | `field_perception_real_vision_provider_adapter_v1.py`, YOLO single-frame path | COMPATIBILITY REFERENCE | Demonstrates provider admission/evidence separation; it is not a Roboflow adapter. |
| OCR | `observation_manager_ocr_adapter_v1.py`, `ocr_manager`, OCR evidence adapters | ADAPTER CANDIDATES | Existing OCR surfaces are numerous; the PoC must select one path behind the same Observation/Provider/Evidence boundary. |
| Roboflow assets | `rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun`, test-source backup pool | DATASET/DRY-RUN ONLY | These assets validate external dataset metadata and candidate mapping, not live Roboflow Provider execution. |
| Test images | `capabilities/test_assets/model_test_lens/...`, existing real-image registries | REUSE IF LICENSE/PROVENANCE CLEARS | Use a small static image set; do not add camera/video infrastructure. |

## Reuse verdict

The existing Provider admission and evidence contracts are sufficient for a
planning-level PoC boundary. The missing pieces are Roboflow-specific
repository declarations, an external-request adapter, canonical OCR evidence
translation selection, and caller-aware loop integration.

