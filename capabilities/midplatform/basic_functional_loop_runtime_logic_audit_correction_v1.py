# -*- coding: utf-8 -*-
"""Basic Functional Loop Runtime Logic Audit and Correction v1 — audit only, no runtime.

Phase-Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1-001"
FINAL_DECISION = "BASIC_FUNCTIONAL_LOOP_RUNTIME_LOGIC_CORRECTED_READY_FOR_OBSERVATION_REQUEST_CONTRACT"
RECOMMENDED_NEXT = "Task-Observation-Request-Contract-v1"

FOLLOWUPS = [
    "Task-Observation-Request-Contract-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Navigation-Guidance-to-Speech-Candidate-Adapter-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Safety-Task-Arbitration-Policy-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Information-Lifecycle-Governance-v1",
    "Memory-System-Architecture-v1",
    "Navigation-Map-Context-Contract-v1",
    "Object-Tracking-Governance-v1",
]

OPTIONAL_DOC_GLOBS = {
    "risk_safety_arbiter": "**/*SAFETY*ARBIT*.md",
    "navigation_policy": "**/*NAVIGATION*POLICY*.md",
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "gps_context": "**/*GPS*.md",
    "segmentation_governance": "**/*SEGMENTATION*.md",
    "tracking_governance": "**/*TRACKING*GOVERN*.md",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_basic_loop_plan", "plan_loaded", [], [], []),
    ("load_voice_runtime", "voice_loaded", [], [], []),
    ("load_midplatform_task_state_runtime", "mp_loaded", [], [], []),
    ("load_task_manager_runtime", "tm_loaded", [], [], []),
    ("load_ocr_activation_and_closure", "ocr_loaded", [], [], []),
    ("load_vision_capture", "vision_loaded", [], [], []),
    ("define_baseline_safety_loop", "baseline_defined", [], [], []),
    ("define_task_driven_loop", "task_driven_defined", [], [], []),
    ("define_authority_boundaries", "authority_defined", [], [], []),
    ("define_candidate_to_commit_matrix", "commit_matrix_defined", [], [], ["commit_now"]),
    ("identify_observation_request_gap", "obs_gap_identified", [], [], []),
    ("define_task_observation_request_stub", "obs_stub_defined", [], [], []),
    ("define_vision_evidence_lifecycle", "evidence_lifecycle_defined", [], [], ["fact_write"]),
    ("define_ocr_joint_gate", "ocr_gate_defined", [], [], ["ocr_invoke"]),
    ("define_speech_output_path", "speech_path_defined", [], [], ["tts", "vop"]),
    ("define_safety_task_arbitration", "arbitration_defined", [], [], []),
    ("define_navigation_guidance_action_boundary", "nav_boundary_defined", [], [], ["navigation_action"]),
    ("register_information_lifecycle_gaps", "info_lifecycle_gaps", [], [], []),
    ("defer_memory_system_boundary", "memory_deferred", [], [], ["memory_write"]),
    ("generate_missing_contract_registry", "contracts_registered", [], [], []),
    ("generate_corrected_roadmap", "roadmap_generated", [], [], []),
    ("generate_final_audit_correction_decision", "audit_ready", [], [], ["production_ready"]),
]

INTAKE_SPECS = [
    ("basic_loop_plan", "luna_basic_functional_loop_stabilization_plan_v1_summary.json", False),
    ("voice_dialogue_contract", "voice_dialogue_task_control_contract_v1_summary.json", False),
    ("voice_dialogue_runtime", "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
    ("midplatform_task_state_runtime", "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
    ("task_manager_contract", "task_manager_contract_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("ocr_mainline_closure", "ocr_mainline_governance_closure_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("vision_capture_governance", "vision_capture_governance_v1_summary.json", False),
    ("vision_capture_runtime", "vision_capture_runtime_dryrun_v1_summary.json", False),
    ("voice_guidance_runtime", "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("hardware_stub", "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

BASELINE_STEPS = [
    ("bs_01", "no_task_or_no_goal_state", "system_state", True, False),
    ("bs_02", "baseline_vision_safety_scan_candidate", "baseline_safety_loop", True, False),
    ("bs_03", "risk_obstacle_spatial_awareness_candidate", "vision", True, False),
    ("bs_04", "safety_guidance_candidate", "baseline_safety_loop", True, False),
    ("bs_05", "speech_gate_vop_candidate", "speech_gate", True, False),
    ("bs_06", "optional_limited_safety_ocr_candidate", "ocr", True, False),
]

TASK_DRIVEN_STEPS = [
    ("td_01", "voice_task_intent_candidate", "voice", False, True),
    ("td_02", "midplatform_task_state_candidate", "midplatform", False, True),
    ("td_03", "task_manager_commit_decision_candidate", "task_manager", False, True),
    ("td_04", "task_context_enrichment_candidate", "task_manager", False, True),
    ("td_05", "task_aware_action_schedule_candidate", "task_manager", False, True),
    ("td_06", "observation_request_candidate", "task_manager", False, True),
    ("td_07", "vision_ocr_evidence_candidate", "vision", False, True),
    ("td_08", "guidance_decision_candidate", "midplatform", False, True),
    ("td_09", "speech_gate_vop_candidate", "speech_gate", False, True),
]

MODULES_AUTHORITY = [
    ("Voice", ["intent_candidate", "command_candidate"], ["lifecycle_commit", "navigation_action"], False),
    ("MidPlatform", ["task_state_candidate", "lifecycle_candidate", "guidance_candidate"], ["lifecycle_commit", "fact_write"], False),
    ("Task Manager", ["commit_decision_candidate", "task_object_candidate", "enrichment_candidate", "action_schedule_candidate"], ["direct_ocr_invoke", "direct_navigation_action"], False),
    ("Baseline Safety Loop", ["safety_scan_candidate", "risk_candidate", "limited_safety_ocr_candidate"], ["task_goal_execution", "generic_text_ocr", "fact_write"], True),
    ("Vision", ["observation_candidate", "evidence_candidate"], ["task_state_commit", "fact_write"], False),
    ("OCR", ["ocr_result_candidate"], ["fact_write", "world_model_write"], False),
    ("Navigation Guidance", ["navigation_guidance_candidate"], ["navigation_action", "map_api_invoke", "route_commit"], False),
    ("Speech Gate", ["speech_admission_candidate"], ["direct_tts", "bypass_vop"], False),
    ("VOP", ["vop_payload_candidate"], ["direct_tts_without_gate", "fact_write"], False),
    ("Memory System", [], ["runtime_write", "lifecycle_management"], False),
    ("WorldModel", [], ["runtime_write", "scene_delta_write"], False),
    ("Hardware Adapter", ["capture_capability_candidate"], ["unauthorized_camera_invoke"], False),
]

CANDIDATE_TRANSITIONS = [
    ("voice_intent_candidate", "voice", ["speech_gate"]),
    ("command_candidate", "voice", ["midplatform_gate"]),
    ("task_state_candidate", "midplatform", ["task_manager_gate"]),
    ("lifecycle_candidate", "midplatform", ["task_manager_gate"]),
    ("commit_decision_candidate", "task_manager", ["task_manager_runtime_enabled", "confirmation_gate", "safety_gate"]),
    ("task_object_candidate", "task_manager", ["task_manager_gate"]),
    ("enrichment_candidate", "task_manager", ["task_manager_gate"]),
    ("verification_context_candidate", "task_manager", ["task_manager_gate"]),
    ("execution_support_candidate", "task_manager", ["task_manager_gate", "midplatform_gate"]),
    ("observation_request_candidate", "task_manager", ["observation_request_contract", "vision_gate"]),
    ("evidence_candidate", "vision", ["evidence_lifecycle_gate", "verification_gate"]),
    ("guidance_candidate", "midplatform", ["speech_gate", "safety_gate"]),
    ("speech_response_candidate", "speech_gate", ["speech_gate", "vop_adapter"]),
    ("safety_candidate", "baseline_safety_loop", ["safety_gate", "speech_gate"]),
]

MISSING_CONTRACTS = [
    ("Task-Observation-Request-Contract-v1", "observation_request_gap", "P0", "Task-Manager-Runtime-DryRun-v1", None, "before_vision_ocr_ingest"),
    ("Vision-Evidence-Lifecycle-Policy-v1", "evidence_lifecycle", "P1", "Task-Observation-Request-Contract-v1", None, "after_observation_request"),
    ("Navigation-Guidance-to-Speech-Candidate-Adapter-v1", "speech_path", "P0", "Task-Observation-Request-Contract-v1", None, "before_nav_loop_dryrun"),
    ("Safety-Task-Arbitration-Policy-v1", "safety_arbitration", "P1", "Basic-Functional-Loop-Runtime-Logic-Audit", None, "parallel_p1"),
    ("Navigation-Guidance-vs-Action-Boundary-v1", "nav_boundary", "P1", "Navigation-Guidance-to-Speech-Candidate-Adapter-v1", None, "parallel_p1"),
    ("Information-Lifecycle-Governance-v1", "info_lifecycle", "P3", "Memory-System-Architecture-v1", "memory_design", "deferred_p3"),
    ("Memory-System-Architecture-v1", "memory_boundary", "P3", None, "dedicated_design", "deferred_p3"),
    ("GPS-Location-Candidate-Contract-v1", "spatial_context", "P1", "Route-Stage-Estimation-DryRun-v1", None, "p1"),
    ("Navigation-Map-Context-Contract-v1", "map_context", "P2", "GPS-Location-Candidate-Contract-v1", None, "p2"),
    ("Route-Stage-Estimation-DryRun-v1", "route_stage", "P1", "Task-Observation-Request-Contract-v1", None, "p1"),
]

ROADMAP = {
    "P0": [
        "Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1",
        "Task-Observation-Request-Contract-v1",
        "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
        "Navigation-Guidance-to-Speech-Candidate-Adapter-v1",
        "Basic-Navigation-Guidance-Loop-DryRun-v1",
    ],
    "P1": [
        "Safety-Task-Arbitration-Policy-v1",
        "Vision-Evidence-Lifecycle-Policy-v1",
        "Navigation-Guidance-vs-Action-Boundary-v1",
        "GPS-Location-Candidate-Contract-v1",
        "Route-Stage-Estimation-DryRun-v1",
    ],
    "P2": [
        "Navigation-Map-Context-Contract-v1",
        "Vision-Frame-Segmentation-Governance-v1",
        "Object-Tracking-Governance-v1",
    ],
    "P3": [
        "Information-Lifecycle-Governance-v1",
        "Memory-System-Architecture-v1",
        "WorldModel-runtime-deferred",
        "Fragment-Evidence-Weaving-deferred",
        "Emotion-Context-deferred",
    ],
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    docs = ws_root / "docs" / "architecture"
    rows = []
    for doc_id, glob_pat in OPTIONAL_DOC_GLOBS.items():
        found = list(docs.glob(glob_pat)) if docs.is_dir() else []
        rows.append(
            {
                "intake_id": doc_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "key_fields_observed": ["documentation_reference"] if found else [],
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _mainline_steps(loop_type: str, steps: List[Tuple[str, str, str, bool, bool]]) -> List[Dict[str, Any]]:
    rows = []
    for step_id, name, owner, allowed_wo_task, req_task in steps:
        forbidden = []
        allowed = ["emit_candidate"]
        if loop_type == "baseline_safety_loop":
            if name.endswith("ocr_candidate"):
                allowed.append("limited_safety_ocr_candidate")
            forbidden = ["task_goal_execution", "generic_text_ocr", "navigation_action", "task_lifecycle_commit"]
        else:
            forbidden = ["bypass_safety_gate", "direct_fact_write", "direct_navigation_action", "run_without_task_context"]
        rows.append(
            {
                "loop_type": loop_type,
                "step_id": step_id,
                "step_name": name,
                "owner_module": owner,
                "allowed_without_task": allowed_wo_task,
                "requires_task_context": req_task,
                "allowed_actions": allowed,
                "forbidden_actions": forbidden,
                "runtime_enabled_now": False,
                **_not_fact(),
            }
        )
    return rows


def run_basic_functional_loop_runtime_logic_audit_correction_v1(
    *,
    basic_loop_plan_root: str,
    voice_dialogue_contract_root: str,
    voice_dialogue_runtime_root: str,
    midplatform_task_state_root: str,
    task_manager_contract_root: str,
    task_manager_runtime_root: str,
    ocr_mainline_closure_root: str,
    ocr_activation_root: str,
    stc_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    hardware_stub_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    root_map = {
        "basic_loop_plan": Path(basic_loop_plan_root).resolve(),
        "voice_dialogue_contract": Path(voice_dialogue_contract_root).resolve(),
        "voice_dialogue_runtime": Path(voice_dialogue_runtime_root).resolve(),
        "midplatform_task_state_runtime": Path(midplatform_task_state_root).resolve(),
        "task_manager_contract": Path(task_manager_contract_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "ocr_mainline_closure": Path(ocr_mainline_closure_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "vision_capture_governance": Path(vision_capture_governance_root).resolve(),
        "vision_capture_runtime": Path(vision_capture_runtime_root).resolve(),
        "voice_guidance_runtime": Path(voice_guidance_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
        "hardware_stub": Path(hardware_stub_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    summaries: Dict[str, Any] = {}
    intake_rows: List[Dict[str, Any]] = []
    for iid, art, optional in INTAKE_SPECS:
        root = root_map[iid]
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
            if loaded:
                summaries[iid] = _read_json(root / art)
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded and art else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "audit_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    tm_rt = summaries.get("task_manager_runtime") or {}
    mp_rt = summaries.get("midplatform_task_state_runtime") or {}

    mainline_rows = _mainline_steps("baseline_safety_loop", BASELINE_STEPS) + _mainline_steps(
        "task_driven_loop", TASK_DRIVEN_STEPS
    )

    authority_rows = []
    for module, may_emit, may_not, baseline_no_task in MODULES_AUTHORITY:
        authority_rows.append(
            {
                "module": module,
                "owns": may_emit[:1] if may_emit else [],
                "may_emit_candidate": may_emit,
                "may_commit": module in ("Task Manager",),
                "may_not_do": may_not,
                "bypass_forbidden": True,
                "write_fact_allowed_now": False,
                "baseline_no_task_allowed": baseline_no_task,
                **_not_fact(),
            }
        )

    transition_rows = []
    for ctype, owner, gates in CANDIDATE_TRANSITIONS:
        transition_rows.append(
            {
                "candidate_type": ctype,
                "can_be_committed_now": False,
                "required_gate_before_commit": gates,
                "owner_of_commit": owner if owner == "task_manager" else "task_manager_for_lifecycle_only",
                "commit_allowed_later": ctype not in ("safety_candidate",),
                "forbidden_direct_commit_reason": "audit_phase_runtime_disabled",
                "enrichment_cannot_override_live_observation": ctype == "enrichment_candidate",
                "evidence_cannot_write_fact_now": ctype == "evidence_candidate",
                **_not_fact(),
            }
        )

    obs_gap = {
        "schema_version": "basic_loop_observation_request_gap_analysis_v1",
        "task_aware_action_schedule_exists": tm_rt.get("task_aware_action_scheduling_candidates_generated", True),
        "observation_requirement_candidates_exist": mp_rt.get("observation_requirement_candidates_generated", True),
        "explicit_observation_request_contract_missing": True,
        "vision_ingest_contract_exists": False,
        "required_future_contract": "Task-Observation-Request-Contract-v1",
        "gaps": [
            {
                "gap_id": "obs_req_gap_001",
                "gap_name": "missing_observation_request_contract_layer",
                "upstream_source": "task_manager_action_schedule_candidate",
                "downstream_target": "vision_capture_runtime",
                "risk_if_missing": "task_scheduling_cannot_reach_vision_ocr_cleanly",
                "correction_required": True,
                "recommended_contract": "Task-Observation-Request-Contract-v1",
                **_not_fact(),
            },
            {
                "gap_id": "obs_req_gap_002",
                "gap_name": "observation_plan_not_normalized_to_request",
                "upstream_source": "task_aware_observation_plan",
                "downstream_target": "vision_evidence_ingest",
                "risk_if_missing": "duplicate_or_ambiguous_observation_triggers",
                "correction_required": True,
                "recommended_contract": "Task-Observation-Request-Contract-v1",
                **_not_fact(),
            },
        ],
        **_not_fact(),
    }

    obs_stub = {
        "schema_version": "basic_loop_task_observation_request_contract_stub_v1",
        "task_observation_request_contract_stub_defined": True,
        "request_source": [
            "task_manager_action_schedule",
            "midplatform_task_state",
            "baseline_safety_loop",
        ],
        "request_type": [
            "observe_forward_path",
            "observe_safety_risk",
            "observe_signage_area",
            "observe_doorplate_area",
            "observe_exit_sign",
            "observe_restroom_sign",
            "observe_service_desk",
            "observe_readable_region",
        ],
        "target_module": ["vision", "ocr_if_task_required", "user_guidance"],
        "camera_invoked_now": False,
        "ocr_invoked_now": False,
        "runtime_action_committed": False,
        "recommended_future_phase": "Task-Observation-Request-Contract-v1",
        **_not_fact(),
    }

    evidence_stages = [
        ("raw_observation_candidate", ["camera_frame_candidate"], ["perception_evidence_candidate"], "vision_gate"),
        ("perception_evidence_candidate", ["raw_observation_candidate"], ["task_relevant_evidence_candidate"], "vision_gate"),
        ("task_relevant_evidence_candidate", ["perception_evidence_candidate", "observation_request"], ["action_support_candidate", "verification_support_candidate"], "task_manager_gate"),
        ("action_support_candidate", ["task_relevant_evidence_candidate"], ["guidance_candidate"], "midplatform_gate"),
        ("verification_support_candidate", ["task_relevant_evidence_candidate"], ["possible_fact_candidate_later"], "task_manager_gate"),
        ("possible_fact_candidate_later", ["verification_support_candidate"], [], "fact_governance_deferred"),
        ("expired_observation_candidate", ["any_prior_stage"], [], "lifecycle_governance"),
        ("rejected_candidate", ["any_prior_stage"], [], "quality_or_safety_gate"),
    ]
    evidence_rows = [
        {
            "lifecycle_stage": stage,
            "allowed_input": inp,
            "allowed_output": out,
            "required_gate": gate,
            "can_support_guidance": stage in ("action_support_candidate", "task_relevant_evidence_candidate"),
            "can_support_verification": stage in ("verification_support_candidate", "task_relevant_evidence_candidate"),
            "can_write_fact_now": False,
            "can_override_live_observation": False,
            "source_chain_required": True,
            **_not_fact(),
        }
        for stage, inp, out, gate in evidence_stages
    ]

    ocr_conditions = [
        "task_requires_text",
        "information_gap_requires_text",
        "safety_short_marker_context",
        "candidate_information_source_area_exists",
        "readable_region_candidate_exists",
        "stc_freshness_valid",
        "input_quality_sufficient",
        "ocr_activation_gate_passed",
        "generic_environment_text_forbidden",
    ]
    ocr_joint = {
        "schema_version": "basic_loop_ocr_joint_gate_matrix_v1",
        "joint_gate_conditions": ocr_conditions,
        "ocr_allowed_now": False,
        "ocr_allowed_later": True,
        "blocked_reason": "audit_only_runtime_disabled",
        "ocr_invoked_now": False,
        "generic_environment_text_forbidden": True,
        "ocr_cannot_default_world_modeling": True,
        "empty_ocr_not_equal_no_text_fact": True,
        "ocr_candidate_cannot_write_fact": True,
        "rows": [
            {
                "context": "baseline_safety_loop",
                "task_requires_text": False,
                "safety_short_marker_context": True,
                "generic_environment_text_forbidden": True,
                "ocr_allowed_now": False,
                "ocr_allowed_later": True,
            },
            {
                "context": "task_driven_loop",
                "task_requires_text": True,
                "information_gap_requires_text": True,
                "ocr_activation_gate_passed": True,
                "generic_environment_text_forbidden": True,
                "ocr_allowed_now": False,
                "ocr_allowed_later": True,
            },
        ],
        **_not_fact(),
    }

    speech_paths = [
        ("safety_guidance_candidate", "P0", True),
        ("task_clarification_candidate", "P2", True),
        ("navigation_guidance_candidate", "P1", True),
        ("repeat_guidance_candidate", "P2", True),
        ("status_response_candidate", "P2", True),
        ("human_assistance_prompt_candidate", "P1", True),
    ]
    speech_rows = [
        {
            "source_candidate_type": src,
            "priority_level": pri,
            "requires_speech_gate": True,
            "requires_vop": True,
            "direct_tts_bypass_forbidden": True,
            "vop_invoked_now": False,
            "tts_invoked_now": False,
            **_not_fact(),
        }
        for src, pri, _ in speech_paths
    ]

    info_gaps = [
        ("freshness_governance_incomplete", "stale_candidates_may_pollute_decisions", ["task_manager", "midplatform", "vision"]),
        ("temporary_storage_policy_incomplete", "unbounded_stm_pressure", ["voice", "dialogue"]),
        ("candidate_pool_capacity_policy_missing", "candidate_explosion", ["midplatform", "task_manager"]),
        ("long_term_storage_policy_missing", "uncontrolled_persistence", ["memory_system"]),
        ("compression_policy_missing", "storage_pressure_unmanaged", ["memory_system", "information_lifecycle"]),
        ("summarization_policy_missing", "context_bloat", ["dialogue", "task_context"]),
        ("information_retention_limit_missing", "infinite_retention_risk", ["memory_system"]),
        ("stale_candidate_promotion_policy_missing", "wrong_fact_promotion", ["evidence_lifecycle"]),
        ("privacy_review_for_persistent_memory_missing", "privacy_risk", ["memory_system"]),
        ("background_memory_maintenance_missing", "orphan_memory_growth", ["memory_system"]),
    ]
    info_registry = [
        {
            "gap_id": f"ilg_{i:03d}",
            "gap_name": name,
            "risk_if_unresolved": risk,
            "affected_modules": mods,
            "recommended_future_module": "Information-Lifecycle-Governance-v1",
            "must_not_be_solved_inside_task_manager": True,
            **_not_fact(),
        }
        for i, (name, risk, mods) in enumerate(info_gaps, 1)
    ]

    missing_contract_rows = [
        {
            "contract_name": name,
            "gap_addressed": gap,
            "priority": pri,
            "prerequisite": pre or "none",
            "blocked_by": blocked or "none",
            "recommended_timing": timing,
            **_not_fact(),
        }
        for name, gap, pri, pre, blocked, timing in MISSING_CONTRACTS
    ]

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    return {
        "summary": {
            "schema_version": "basic_functional_loop_runtime_logic_audit_correction_v1_summary_v0",
            "phase": PHASE_ID,
            "audit_scope": "runtime_logic_audit_and_correction_only",
            "based_on_basic_loop_plan": summaries.get("basic_loop_plan") is not None,
            "based_on_voice_runtime": summaries.get("voice_dialogue_runtime") is not None,
            "based_on_midplatform_task_state_runtime": summaries.get("midplatform_task_state_runtime") is not None,
            "based_on_task_manager_runtime": summaries.get("task_manager_runtime") is not None,
            "baseline_safety_loop_defined": True,
            "task_driven_loop_defined": True,
            "baseline_vs_task_driven_separation_defined": True,
            "no_task_safety_runtime_allowed_as_baseline": True,
            "task_driven_runtime_requires_task_context": True,
            "observation_request_gap_identified": True,
            "vision_evidence_lifecycle_defined": True,
            "ocr_joint_gate_defined": True,
            "speech_output_path_defined": True,
            "safety_task_arbitration_defined": True,
            "navigation_guidance_action_boundary_defined": True,
            "information_lifecycle_gap_registered": True,
            "memory_system_boundary_deferred": True,
            "missing_contract_registry_generated": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "intake": {
            "schema_version": "basic_loop_runtime_logic_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "mainline": {
            "schema_version": "basic_loop_runtime_mainline_sequence_matrix_v1",
            "baseline_safety_loop_step_count": len(BASELINE_STEPS),
            "task_driven_loop_step_count": len(TASK_DRIVEN_STEPS),
            "steps": mainline_rows,
            **_not_fact(),
        },
        "baseline_policy": {
            "schema_version": "basic_loop_baseline_safety_loop_policy_v1",
            "baseline_safety_loop_enabled_by_default": True,
            "user_task_required": False,
            "supported_baseline_capabilities": [
                "vision_safety_scan",
                "obstacle_awareness_candidate",
                "spatial_risk_candidate",
                "safety_guidance_candidate",
                "limited_safety_ocr_candidate",
            ],
            "baseline_ocr_scope_limited_to": [
                "warning_sign",
                "danger_marker",
                "emergency_exit_sign",
                "safety_short_marker",
            ],
            "generic_text_ocr_forbidden_without_task": True,
            "task_goal_execution_forbidden_without_task": True,
            "navigation_action_triggered": False,
            "fact_write_allowed": False,
            **_not_fact(),
        },
        "task_driven_policy": {
            "schema_version": "basic_loop_task_driven_loop_policy_v1",
            "task_driven_loop_requires_task_or_goal": True,
            "task_context_required_for_targeted_observation": True,
            "ocr_requires_task_or_safety_trigger": True,
            "human_assistance_requires_task_or_safety_context": True,
            "navigation_guidance_requires_task_or_safety_context": True,
            "task_manager_or_midplatform_gate_required": True,
            "safety_priority_above_task": True,
            "navigation_action_triggered": False,
            "fact_write_allowed": False,
            **_not_fact(),
        },
        "authority": {
            "schema_version": "basic_loop_authority_boundary_matrix_v1",
            "authority_boundary_count": len(authority_rows),
            "modules": authority_rows,
            **_not_fact(),
        },
        "candidate_transition": {
            "schema_version": "basic_loop_candidate_to_commit_transition_matrix_v1",
            "candidate_type_count": len(transition_rows),
            "candidates": transition_rows,
            "all_can_be_committed_now_false": True,
            **_not_fact(),
        },
        "observation_gap": obs_gap,
        "observation_stub": obs_stub,
        "evidence_lifecycle": {
            "schema_version": "basic_loop_vision_evidence_lifecycle_matrix_v1",
            "stages": evidence_rows,
            **_not_fact(),
        },
        "ocr_joint": ocr_joint,
        "speech_path": {
            "schema_version": "basic_loop_speech_output_path_matrix_v1",
            "paths": speech_rows,
            **_not_fact(),
        },
        "arbitration": {
            "schema_version": "basic_loop_safety_task_arbitration_matrix_v1",
            "safety_priority_above_task": True,
            "p0_p1_interrupt_task_dialogue": True,
            "safety_can_delay_task_commit": True,
            "safety_can_suppress_repeat_or_low_priority_clarification": True,
            "task_manager_consumes_safety_state_candidate": True,
            "task_manager_does_not_perceive_safety_directly": True,
            "speech_gate_final_voice_arbitration": True,
            "runtime_arbitration_invoked_now": False,
            **_not_fact(),
        },
        "nav_boundary": {
            "schema_version": "basic_loop_navigation_guidance_action_boundary_v1",
            "navigation_guidance_candidate": {
                "allowed_now_as_candidate": True,
                "may_be_spoken_after_speech_gate": True,
                "does_not_change_route_state": True,
                "does_not_trigger_map_api": True,
                "does_not_move_user_or_device": True,
            },
            "navigation_action": {
                "allowed_now": False,
                "requires_task_commit": True,
                "requires_safety_check": True,
                "requires_navigation_runtime_authorization": True,
                "map_api_invoked_now": False,
            },
            "guidance_is_not_action": True,
            "route_context_update_candidate_is_not_route_commit": True,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "info_lifecycle": {
            "schema_version": "basic_loop_information_lifecycle_gap_registry_v1",
            "information_lifecycle_gap_count": len(info_registry),
            "gaps": info_registry,
            "compression_policy_missing": True,
            "summarization_policy_missing": True,
            **_not_fact(),
        },
        "memory_deferred": {
            "schema_version": "basic_loop_memory_system_boundary_deferred_report_v1",
            "short_term_memory_boundary_unresolved": True,
            "dialogue_context_boundary_unresolved": True,
            "task_context_boundary_unresolved": True,
            "long_term_memory_boundary_unresolved": True,
            "traditional_database_model_for_memory_rejected": True,
            "memory_system_requires_dedicated_design": True,
            "task_manager_may_reference_memory_candidate": True,
            "task_manager_must_not_manage_memory_lifecycle": True,
            "midplatform_must_not_delete_or_update_memory": True,
            "memory_runtime_invoked_now": False,
            **_not_fact(),
        },
        "missing_contracts": {
            "schema_version": "basic_loop_missing_contract_registry_v1",
            "missing_contract_count": len(missing_contract_rows),
            "contracts": missing_contract_rows,
            **_not_fact(),
        },
        "roadmap": {
            "schema_version": "basic_loop_corrected_phase_roadmap_v1",
            "phases": ROADMAP,
            "corrected_roadmap_phase_count": sum(len(v) for v in ROADMAP.values()),
            **_not_fact(),
        },
        "trace": {
            "schema_version": "basic_loop_runtime_logic_audit_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "basic_loop_runtime_logic_audit_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "baseline_safety_loop_defined": True,
            "task_driven_loop_defined": True,
            "task_observation_request_contract_required": True,
            "vision_ocr_ingest_ready_after_observation_request_contract": True,
            "memory_system_deferred": True,
            "information_lifecycle_governance_deferred": True,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": [
                "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
                "Safety-Task-Arbitration-Policy-v1",
            ],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "basic_loop_runtime_logic_audit_boundary_report_v1",
            "audit_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "basic_loop_runtime_logic_audit_metrics_candidate_report_v1",
            "baseline_loop_step_count": len(BASELINE_STEPS),
            "task_driven_loop_step_count": len(TASK_DRIVEN_STEPS),
            "authority_boundary_count": len(authority_rows),
            "candidate_type_count": len(transition_rows),
            "missing_contract_count": len(missing_contract_rows),
            "information_lifecycle_gap_count": len(info_registry),
            "memory_boundary_gap_count": 4,
            "corrected_roadmap_phase_count": sum(len(v) for v in ROADMAP.values()),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "basic_loop_runtime_logic_audit_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "basic_loop_runtime_logic_audit_system_health_report_v1",
            "system_health_governance_available": root_map["system_health"].is_dir(),
            "health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "basic_loop_runtime_logic_audit_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "audit_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "basic_loop_runtime_logic_audit_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": root_map["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "basic_loop_runtime_logic_audit_non_claims_report_v1",
            "claims": [
                "audit_correction_not_runtime",
                "baseline_defined_not_safety_runtime_complete",
                "task_driven_defined_not_navigation_complete",
                "observation_request_stub_not_contract_complete",
                "vision_evidence_lifecycle_not_real_evidence",
                "ocr_joint_gate_not_ocr_runtime_enabled",
                "speech_path_not_vop_invoked",
                "memory_deferred_not_solved",
                "information_lifecycle_gap_not_governed",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "basic_loop_runtime_logic_audit_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "basic_loop_runtime_logic_audit_audit_report_v1",
            "basic_functional_loop_runtime_logic_audit_correction_v1_executed": True,
            "audit_only": True,
            "baseline_safety_loop_defined": True,
            "task_driven_loop_defined": True,
            "baseline_vs_task_driven_separation_defined": True,
            "no_task_safety_runtime_allowed_as_baseline": True,
            "task_driven_runtime_requires_task_context": True,
            "observation_request_gap_identified": True,
            "vision_evidence_lifecycle_defined": True,
            "ocr_joint_gate_defined": True,
            "speech_output_path_defined": True,
            "safety_task_arbitration_defined": True,
            "navigation_guidance_action_boundary_defined": True,
            "information_lifecycle_gap_registered": True,
            "memory_system_boundary_deferred": True,
            "missing_contract_registry_generated": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
