from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _base(case_id: str, title: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "title": title,
        "root_cycle_trace_id": f"root-cycle:{case_id}",
        "context_refs": (f"context:{case_id}",),
        "intent_ref": f"intent:{case_id}",
        "task_ref": f"task:{case_id}",
        "safety_ref": "",
        "field_refs": (f"field:{case_id}",),
        "information_need": "observe task target",
        "observation_goal": "observe task target",
        "target_semantic": "task_target",
        "target_region": "scoped_region",
        "spatial_scope": "scoped_region",
        "temporal_scope": "current_cycle",
        "expected_evidence_kinds": ("VISION_DETECTION",),
        "received_evidence_kinds": (),
        "received_evidence_refs": (),
        "source_diversity": 0,
        "source_independence_candidate": True,
        "target_coverage": False,
        "semantic_coverage": False,
        "spatial_required": False,
        "spatial_coverage": True,
        "temporal_validity": {"valid": True, "stale": False},
        "resource_budget": {"frames": 3, "duration_ms": 1500, "memory_mb": 512},
        "provider_admission_candidate": True,
        "selected_model_candidate_ref": f"model-candidate:{case_id}",
        "provider_candidate_ref": f"provider-candidate:{case_id}",
        "switch_allowed": True,
        "redirect_allowed": True,
        "frame_time_budget": {"max_frames": 3, "max_duration_ms": 1500},
        "retry_budget": {"max_retries": 1},
        "model_confidence": 0.5,
        "expected": {},
    }


def _case(case_id: str, title: str, expected: Dict[str, Any], **updates: Any) -> Dict[str, Any]:
    request = _base(case_id, title)
    request.update(updates)
    request["expected"] = expected
    return {"case_id": case_id, "title": title, "request": request, "expected": expected}


def build_active_observation_control_cases_v1() -> Tuple[Dict[str, Any], ...]:
    cases: List[Dict[str, Any]] = [
        _case("R01", "No Intent/Task/Safety Need does not start YOLO", {"provider_session_present": False, "control_decision": "STOP", "provider_autonomous_continuous_execution": False}, information_need="", intent_ref="", task_ref="", camera_frame_arrival=True, provider_autonomy_probe=True, expected_evidence_kinds=()),
        _case("R02", "Subway entrance task scopes observation away from default full-frame OCR", {"provider_session_present": True, "ocr_capability_requirement_present": False, "control_decision": "CONTINUE"}, information_need="find subway line 2 entrance", observation_goal="find subway line 2 entrance", target_semantic="subway_2_entrance", expected_evidence_kinds=("VISION_DETECTION",)),
        _case("R03", "Vision signage region proposes OCR requirement without direct invocation", {"ocr_capability_requirement_present": True, "vision_provider_can_invoke_ocr": False, "provider_invocation": False}, information_need="read sign for subway line 2 entrance", observation_goal="inspect detected signage region", target_semantic="subway_sign", expected_evidence_kinds=("OCR_TEXT_EVIDENCE",), received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:vision:signage-region",), signage_region_detected=True, requested_capability_kinds=("OCR_TEXT_EVIDENCE",)),
        _case("R04", "Sufficient OCR signage evidence stops observation", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP"}, information_need="find subway line 2 entrance", expected_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_refs=("evidence:vision:sign", "evidence:ocr:line2-entrance"), target_coverage=True, semantic_coverage=True, source_diversity=2),
        _case("R05", "Spatial structure need creates SLAM requirement only", {"slam_capability_requirement_present": True, "required_capability_kinds": ["SLAM_SPATIAL_EVIDENCE"], "control_decision": "CONTINUE"}, information_need="determine walkable spatial layout", observation_goal="determine walkable spatial layout", expected_evidence_kinds=("SLAM_SPATIAL_EVIDENCE",), requested_capability_kinds=("SLAM_SPATIAL_EVIDENCE",), spatial_required=True, spatial_coverage=False),
        _case("R06", "Camera stream does not renew SLAM without spatial need", {"provider_session_present": False, "slam_capability_requirement_present": False, "control_decision": "STOP"}, information_need="", intent_ref="", task_ref="", camera_frame_arrival=True, previous_successful_slam=True, expected_evidence_kinds=()),
        _case("R07", "Provider candidates cannot mutate canonical owners", {"mutation_authority": False, "downstream_mutation": False, "control_decision": "CONTINUE"}, provider_mutation_probe=True),
        _case("R08", "Gateway admission is not continuation authorization", {"provider_session_present": False, "gateway_admission_is_continuation_authority": False, "control_decision": "DEFER"}, gateway_admitted=True, provider_admission_candidate=False),
        _case("R09", "Contradictory evidence triggers bounded reconsideration", {"sufficiency_status": "CONTESTED", "control_decision": "RECONSIDER"}, contradiction_refs=("contradiction:vision-ocr",), received_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_refs=("evidence:vision:a", "evidence:ocr:b"), target_coverage=True, semantic_coverage=True, source_diversity=2),
        _case("R10", "User correction redirects future demand and preserves lineage", {"control_decision": "REDIRECT", "provenance_preserved": True}, user_correction=True, correction_refs=("correction:user:target-region",), target_semantic="corrected_subway_entrance"),
        _case("R11", "Safety observation exception is bounded and revocable", {"safety_exception_present": True, "safety_exception_valid": True, "safety_exception_bounded": True, "general_provider_autonomy": False}, intent_ref="", task_ref="", safety_ref="safety:baseline", information_need="maintain minimum safety observation", safety_exception={"explicit_policy_ref":"policy:safety-baseline-v1", "reason":"near-field hazard monitoring", "target_scope":"front_corridor", "capability_scope":["VISION_DETECTION"], "bounded_budget":{"frames":2,"duration_ms":800}, "temporal_validity":{"valid":True}, "revoke_condition":"hazard-clear-or-budget-exhausted"}),
        _case("R12", "Terminal outcomes have explicit stop/defer/reconsider paths", {"control_decision": "STOP", "provider_invocation": False}, task_complete=True, received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:completed",), target_coverage=True, semantic_coverage=True),
        _case("R13", "Duplicate demand is guarded", {"control_decision": "DEFER", "request_present": False, "provider_session_present": False}, duplicate_demand=True),
        _case("R14", "Duplicate observation request is guarded", {"control_decision": "DEFER", "request_present": True, "capability_requirement_present": False, "provider_session_present": False}, duplicate_request=True),
        _case("R15", "Duplicate provider session is guarded", {"control_decision": "DEFER", "provider_session_present": False}, duplicate_provider_session=True),
        _case("R16", "Stale evidence redirects observation", {"sufficiency_status": "STALE", "control_decision": "REDIRECT"}, stale_evidence=True, received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:stale",), target_coverage=True, semantic_coverage=True),
        _case("R17", "OCR contradiction remains contested", {"sufficiency_status": "CONTESTED", "control_decision": "RECONSIDER"}, contradiction_refs=("contradiction:ocr-a-ocr-b",), expected_evidence_kinds=("OCR_TEXT_EVIDENCE",), received_evidence_kinds=("OCR_TEXT_EVIDENCE",), received_evidence_refs=("evidence:ocr:a", "evidence:ocr:b"), target_coverage=True, semantic_coverage=True),
        _case("R18", "Lost visual target redirects region", {"control_decision": "REDIRECT", "sufficiency_status": "NEEDS_REDIRECT"}, target_lost=True, redirect_required=True),
        _case("R19", "Provider failure selects admitted fallback candidate", {"control_decision": "SWITCH_PROVIDER", "provider_invocation": False}, provider_failure=True, fallback_available=True),
        _case("R20", "Resource exhaustion defers observation", {"control_decision": "DEFER", "provider_invocation": False}, budget_exhausted=True),
        _case("R21", "Revoked safety exception stops observation", {"control_decision": "STOP", "provider_invocation": False}, safety_exception_revoked=True, safety_ref="safety:baseline", information_need="maintain minimum safety observation"),
        _case("R22", "Repeated provider failure is terminal", {"control_decision": "FAIL", "repeated_failure_signature_guarded": True}, repeated_provider_failure_signature=True, provider_failure=True, fallback_available=False),
        _case("R23", "Insufficient evidence redirects to a new region", {"control_decision": "REDIRECT", "sufficiency_status": "NEEDS_REDIRECT"}, redirect_required=True),
        _case("R24", "Task cancellation stops observation", {"control_decision": "STOP"}, task_cancelled=True),
        _case("R25", "Intent change triggers reconsideration", {"control_decision": "RECONSIDER"}, intent_changed=True),
        _case("R26", "Field change invalidates prior evidence", {"sufficiency_status": "STALE", "control_decision": "REDIRECT"}, field_changed=True, received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:prior-field",), target_coverage=True, semantic_coverage=True),
        _case("R27", "Delayed provider result defers without hidden retry", {"control_decision": "DEFER", "provider_invocation": False}, delayed_result=True),
        _case("R28", "Unnecessary modality is rejected", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP", "rejected_capability_kinds": ["SLAM_SPATIAL_EVIDENCE"]}, expected_evidence_kinds=("VISION_DETECTION",), received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:vision:target",), target_coverage=True, semantic_coverage=True, forbidden_capability_kinds=("SLAM_SPATIAL_EVIDENCE",)),
        _case("R29", "Sufficiency does not require maximum model confidence", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP", "model_confidence_input": 0.42}, expected_evidence_kinds=("VISION_DETECTION",), received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:vision:adequate",), target_coverage=True, semantic_coverage=True, model_confidence=0.42),
        _case("R30", "High confidence but semantic coverage is insufficient", {"sufficiency_status": "NEEDS_ADDITIONAL_MODALITY", "control_decision": "ADD_CAPABILITY"}, expected_evidence_kinds=("OCR_TEXT_EVIDENCE",), received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:vision:high-confidence-region",), target_coverage=True, semantic_coverage=False, model_confidence=0.99),
        _case("R31", "Independent providers agree", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP"}, expected_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_refs=("evidence:yolo:sign", "evidence:ocr:sign"), target_coverage=True, semantic_coverage=True, source_diversity=2, multi_provider_agreement=True),
        _case("R32", "Cross-modal contradiction is bounded", {"sufficiency_status": "CONTESTED", "control_decision": "RECONSIDER"}, cross_modal_contradiction=True, contradiction_refs=("contradiction:vision-ocr",), received_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_refs=("evidence:vision", "evidence:ocr"), target_coverage=True, semantic_coverage=True),
        _case("R33", "Sufficient observation cannot hide a continuation session", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP", "session_continuation_authorized": False}, previous_successful_detection=True, received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:sufficient",), target_coverage=True, semantic_coverage=True),
        _case("R34", "Completed observation is immutable", {"control_decision": "FAIL", "completed_observation_immutable": True}, completed_observation_mutation_probe=True),
        _case("R35", "Next-cycle ingress candidate is generated", {"control_decision": "STOP", "next_cycle_ingress_present": True, "trace_reverse_lookup_complete": True}, next_cycle_requested=True, received_evidence_kinds=("VISION_DETECTION",), received_evidence_refs=("evidence:cycle-result",), target_coverage=True, semantic_coverage=True),
        _case("R36", "Full subway sign synthetic product case", {"sufficiency_status": "SUFFICIENT", "control_decision": "STOP", "ocr_capability_requirement_present": True, "trace_reverse_lookup_complete": True}, information_need="find subway line 2 entrance", observation_goal="find subway line 2 entrance", target_semantic="subway_line_2_entrance", target_region="signage_region", expected_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_kinds=("VISION_DETECTION", "OCR_TEXT_EVIDENCE"), received_evidence_refs=("evidence:yolo:signage", "evidence:ocr:line2-entrance"), target_coverage=True, semantic_coverage=True, source_diversity=2, requested_capability_kinds=("VISION_DETECTION", "REGION_PROPOSAL", "OCR_TEXT_EVIDENCE")),
    ]
    return tuple(cases)
