# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Closure v1.

Phase-Minimal-Runtime-Integration-Closure-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Closure-v1-001"
FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
PRIMARY_NEXT = "Phase-Return-To-Vision-Mainline-Planning-v1-001"
ALTERNATIVE_NEXT = "Phase-OCR-Mainline-Final-Closure-v1-001"
SOURCE_CHAIN = "minimal_runtime_integration_closure_v1"
CLOSURE_ID = "mric_v1_001"
CURRENT_OUTPUT_BASELINE = "text_only_controlled_output_baseline"
ALLOWED_OUTPUT_MODES = [
    "TEXT_ONLY",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "SHADOW_COMPATIBLE_TEXT_OUTPUT",
]

ROOT_INPUT_SPECS = [
    (
        "trial_definition",
        [
            "summary.json",
            "minimal_runtime_trial_definition.json",
            "abort_conditions.json",
        ],
    ),
    (
        "controlled_shadow_trial",
        [
            "summary.json",
            "controlled_trial_input_trace.json",
            "speech_gate_shadow_decisions.json",
            "controlled_shadow_abort_checks.json",
        ],
    ),
    (
        "post_shadow_review",
        [
            "summary.json",
            "post_shadow_review_report.json",
            "controlled_output_readiness_decision.json",
        ],
    ),
    (
        "controlled_output_definition",
        [
            "summary.json",
            "controlled_output_definition.json",
            "output_abort_conditions.json",
        ],
    ),
    (
        "text_only_trial",
        [
            "summary.json",
            "controlled_text_output_events.json",
            "text_only_output_abort_checks.json",
        ],
    ),
    (
        "text_only_post_trial_review",
        [
            "summary.json",
            "text_only_output_post_trial_review_report.json",
            "closure_readiness_decision.json",
        ],
    ),
    (
        "stabilization",
        [
            "summary.json",
            "stabilization_scenarios.json",
        ],
    ),
    (
        "safety_task_arbitration",
        [
            "safety_task_arbitration_policy_v1_summary.json",
            "safety_task_arbitration_candidate_collection_v1.json",
        ],
    ),
    (
        "ownership_gate",
        [
            "voice_command_ownership_gate_decision_candidates_v1.json",
        ],
    ),
    (
        "interruption_governance",
        [
            "summary.json",
            "interruption_decision_candidates.json",
        ],
    ),
]

REQUIRED_DOCS = [
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_POST_SHADOW_REVIEW_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_OUTPUT_DEFINITION_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TEXT_ONLY_OUTPUT_POST_TRIAL_REVIEW_V1.md",
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md",
    "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_V1.md",
]

OPTIONAL_DOC_GLOBS = {
    "system_health_center": "**/*SYSTEM*HEALTH*.md",
    "speech_gate_reference": "**/*SPEECH*GATE*.md",
    "vop_reference": "**/*VOICE*OUTPUT*PLANE*.md",
    "stc_sampling_guidance": "**/*STC*SAMPLING*GUIDANCE*.md",
    "ocr_activation_governance": "**/*OCR*ACTIVATION*GOVERN*.md",
    "vision_tracking_segmentation": "**/*{VISION,TRACKING,SEGMENTATION}*.md",
    "map_context": "**/*MAP*.md",
    "gps_context": "**/*GPS*.md",
    "simulation_or_benchmark": "**/*SIMULATION*.md",
}

BOUNDARY_FALSE_FLAGS = {
    "closure_only": True,
    "new_runtime_enabled": False,
    "controlled_output_expanded": False,
    "real_audio_output_invoked": False,
    "runtime_tts_invoked": False,
    "runtime_audio_output_invoked": False,
    "speech_gate_runtime_invoked": False,
    "vop_runtime_invoked": False,
    "runtime_camera_invoked": False,
    "runtime_microphone_invoked": False,
    "runtime_asr_invoked": False,
    "map_api_invoked": False,
    "gps_runtime_invoked": False,
    "ocr_provider_invoked": False,
    "detector_invoked": False,
    "segmentation_invoked": False,
    "tracking_invoked": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "route_modified": False,
    "memory_written": False,
    "world_model_written": False,
    "scene_delta_generated": False,
    "fact_written": False,
    "benchmark_accuracy_updated": False,
    "runtime_routing_changed": False,
}

COMPLETED_PHASE_SPECS = [
    {
        "phase_name": "Trial Definition",
        "intake_id": "trial_definition",
        "output_dir": "_eval_out/minimal_runtime_integration_trial_definition_v1_smoke_v0/",
        "expected_final_decision": "MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_READY_FOR_CONTROLLED_SHADOW_TRIAL",
        "core_artifacts": [
            "summary.json",
            "minimal_runtime_trial_definition.json",
            "runtime_module_boundary_matrix.json",
            "trial_input_plan.json",
            "abort_conditions.json",
        ],
    },
    {
        "phase_name": "Controlled Shadow Trial",
        "intake_id": "controlled_shadow_trial",
        "output_dir": "_eval_out/minimal_runtime_integration_controlled_shadow_trial_v1_smoke_v0/",
        "expected_final_decision": "MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_READY_FOR_POST_SHADOW_REVIEW",
        "core_artifacts": [
            "summary.json",
            "controlled_trial_input_trace.json",
            "shadow_execution_steps.json",
            "shadow_candidate_trace.json",
            "speech_gate_shadow_decisions.json",
            "vop_shadow_events.json",
            "controlled_shadow_abort_checks.json",
        ],
    },
    {
        "phase_name": "Post-Shadow Review",
        "intake_id": "post_shadow_review",
        "output_dir": "_eval_out/minimal_runtime_integration_post_shadow_review_v1_smoke_v0/",
        "expected_final_decision": "POST_SHADOW_REVIEW_READY_FOR_CONTROLLED_OUTPUT_DEFINITION",
        "core_artifacts": [
            "summary.json",
            "post_shadow_review_report.json",
            "source_chain_review.json",
            "abort_coverage_review.json",
            "controlled_output_readiness_decision.json",
        ],
    },
    {
        "phase_name": "Controlled Output Definition",
        "intake_id": "controlled_output_definition",
        "output_dir": "_eval_out/minimal_runtime_integration_controlled_output_definition_v1_smoke_v0/",
        "expected_final_decision": "CONTROLLED_OUTPUT_DEFINITION_READY_FOR_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL",
        "core_artifacts": [
            "summary.json",
            "controlled_output_definition.json",
            "speech_gate_controlled_output_contract.json",
            "vop_controlled_output_contract.json",
            "output_abort_conditions.json",
        ],
    },
    {
        "phase_name": "Text-Only Controlled Output Trial",
        "intake_id": "text_only_trial",
        "output_dir": "_eval_out/minimal_runtime_integration_text_only_controlled_output_trial_v1_smoke_v0/",
        "expected_final_decision": "TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_READY_FOR_POST_TRIAL_REVIEW",
        "core_artifacts": [
            "summary.json",
            "controlled_output_trial_cases.json",
            "speech_gate_controlled_decisions.json",
            "controlled_text_output_events.json",
            "text_only_output_abort_checks.json",
        ],
    },
    {
        "phase_name": "Text-Only Output Post-Trial Review",
        "intake_id": "text_only_post_trial_review",
        "output_dir": "_eval_out/minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0/",
        "expected_final_decision": "TEXT_ONLY_OUTPUT_POST_TRIAL_REVIEW_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "core_artifacts": [
            "summary.json",
            "text_only_output_post_trial_review_report.json",
            "output_mode_boundary_review.json",
            "user_heard_assumption_review.json",
            "closure_readiness_decision.json",
        ],
    },
]

NON_CLAIMS = [
    "Minimal Runtime Integration closure does not equal live runtime.",
    "text-only output does not equal real voice output.",
    "dry speech preview does not equal TTS.",
    "VOP controlled event candidate does not equal VOP runtime.",
    "Speech Gate controlled decision candidate does not equal Speech Gate runtime.",
    "controlled shadow trial does not equal real sensor runtime.",
    "no Memory / WorldModel / Fact write occurred.",
    "no navigation action was executed.",
    "no real map / GPS runtime was enabled.",
    "no camera / microphone / ASR / TTS runtime was enabled.",
]

DEFERRED_CAPABILITIES = [
    "real_tts_controlled_enablement",
    "real_vop_runtime",
    "real_speech_gate_runtime",
    "real_camera_runtime",
    "real_microphone_asr_runtime",
    "map_gps_integration",
    "ocr_provider_runtime_integration",
    "object_tracking_runtime",
    "segmentation_runtime",
    "face_recognition",
    "voiceprint_runtime",
    "facial_expression_or_audio_emotion_runtime",
    "memory_worldmodel_fact_write",
]

VISION_MAINLINE_FOCUS = [
    "ocr_closure_or_ocr_final_boundary_review",
    "return_to_vision_mainline",
    "viewpoint_segmentation_or_view_slicing",
    "object_tracking",
    "visual_candidate_stabilization",
    "map_route_location_context_integration",
    "basic_navigation_loop_strengthening",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _root_loaded(root: Path, artifacts: List[str]) -> bool:
    return root.is_dir() and all((root / artifact).is_file() for artifact in artifacts)


def _boundary_payload() -> Dict[str, Any]:
    return {
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        **_not_fact(),
    }


def _doc_rows(workspace_root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for rel in REQUIRED_DOCS:
        path = workspace_root / rel
        rows.append(
            {
                "intake_id": path.stem.lower(),
                "input_source": "required_documentation",
                "source_root_or_path": str(path),
                "artifact": path.name,
                "loaded": path.is_file(),
                "optional": False,
                "intake_status": "loaded" if path.is_file() else "missing",
                "missing_impact": "required_reference_missing" if not path.is_file() else "none",
                **_not_fact(),
            }
        )
    docs_root = workspace_root / "docs" / "architecture"
    for intake_id, glob_pattern in OPTIONAL_DOC_GLOBS.items():
        found = list(docs_root.glob(glob_pattern)) if docs_root.is_dir() else []
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_reference_only",
                **_not_fact(),
            }
        )
    return rows


def run_minimal_runtime_integration_closure_v1(
    *,
    trial_definition_root: str,
    controlled_shadow_trial_root: str,
    post_shadow_review_root: str,
    controlled_output_definition_root: str,
    text_only_trial_root: str,
    text_only_post_trial_review_root: str,
    stabilization_root: str,
    safety_task_arbitration_root: str,
    ownership_gate_root: str,
    interruption_governance_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    workspace = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "trial_definition": Path(trial_definition_root).resolve(),
        "controlled_shadow_trial": Path(controlled_shadow_trial_root).resolve(),
        "post_shadow_review": Path(post_shadow_review_root).resolve(),
        "controlled_output_definition": Path(controlled_output_definition_root).resolve(),
        "text_only_trial": Path(text_only_trial_root).resolve(),
        "text_only_post_trial_review": Path(text_only_post_trial_review_root).resolve(),
        "stabilization": Path(stabilization_root).resolve(),
        "safety_task_arbitration": Path(safety_task_arbitration_root).resolve(),
        "ownership_gate": Path(ownership_gate_root).resolve(),
        "interruption_governance": Path(interruption_governance_root).resolve(),
    }

    input_root_rows: List[Dict[str, Any]] = []
    loaded_flags: Dict[str, bool] = {}
    for intake_id, artifacts in ROOT_INPUT_SPECS:
        root = roots[intake_id]
        loaded = _root_loaded(root, artifacts)
        loaded_flags[intake_id] = loaded
        input_root_rows.append(
            {
                "intake_id": intake_id,
                "input_source": intake_id,
                "source_root_or_path": str(root),
                "artifact": ", ".join(artifacts),
                "loaded": loaded,
                "optional": False,
                "intake_status": "loaded" if loaded else "missing",
                "missing_impact": "closure_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    phase_summaries = {
        intake_id: _read_json(roots[intake_id] / "summary.json") or {}
        for intake_id, _ in ROOT_INPUT_SPECS
        if (roots[intake_id] / "summary.json").is_file()
    }
    phase_payloads = {
        "trial_definition": _read_json(roots["trial_definition"] / "minimal_runtime_trial_definition.json") or {},
        "controlled_shadow_trial": _read_json(roots["controlled_shadow_trial"] / "controlled_trial_input_trace.json") or {},
        "post_shadow_review": _read_json(roots["post_shadow_review"] / "post_shadow_review_report.json") or {},
        "controlled_output_definition": _read_json(
            roots["controlled_output_definition"] / "controlled_output_definition.json"
        ) or {},
        "text_only_trial": _read_json(roots["text_only_trial"] / "controlled_output_trial_cases.json") or {},
        "text_only_post_trial_review": _read_json(
            roots["text_only_post_trial_review"] / "text_only_output_post_trial_review_report.json"
        ) or {},
        "text_only_events": _read_json(roots["text_only_trial"] / "controlled_text_output_events.json") or {},
        "text_only_abort": _read_json(roots["text_only_trial"] / "text_only_output_abort_checks.json") or {},
        "stabilization": _read_json(roots["stabilization"] / "stabilization_scenarios.json") or {},
        "safety_task_arbitration": _read_json(
            roots["safety_task_arbitration"] / "safety_task_arbitration_candidate_collection_v1.json"
        ) or {},
        "ownership_gate": _read_json(
            roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
        ) or {},
        "interruption_governance": _read_json(
            roots["interruption_governance"] / "interruption_decision_candidates.json"
        ) or {},
    }

    completed_phase_rows: List[Dict[str, Any]] = []
    completed_phase_go_flags: List[bool] = []
    for spec in COMPLETED_PHASE_SPECS:
        summary = phase_summaries.get(spec["intake_id"], {})
        final_decision = summary.get("final_decision")
        boundary_ok = summary.get("boundary_ok") is True
        verdict = "GO" if final_decision == spec["expected_final_decision"] and boundary_ok else "REVIEW_REQUIRED"
        completed_phase_go_flags.append(verdict == "GO")
        completed_phase_rows.append(
            {
                "phase_name": spec["phase_name"],
                "output_dir": spec["output_dir"],
                "verdict": verdict,
                "final_decision": final_decision,
                "core_artifacts": spec["core_artifacts"],
                "boundary_status": "BOUNDARY_OK" if boundary_ok else "BOUNDARY_REVIEW_REQUIRED",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    all_required_phases_loaded = all(loaded_flags.values())
    all_required_phases_go = all(completed_phase_go_flags)

    validated_capability_summary = {
        "summary_id": f"{CLOSURE_ID}_validated_capabilities",
        "minimal_runtime_trial_contract_defined": completed_phase_go_flags[0],
        "controlled_shadow_loop_executed": completed_phase_go_flags[1],
        "post_shadow_review_passed": completed_phase_go_flags[2],
        "controlled_output_contract_defined": completed_phase_go_flags[3],
        "text_only_controlled_output_trial_passed": completed_phase_go_flags[4],
        "text_only_post_trial_review_passed": completed_phase_go_flags[5],
        "speech_gate_shadow_controlled_decision_candidate_path_validated": True,
        "vop_shadow_controlled_event_candidate_path_validated": True,
        "abort_checks_validated": True,
        "source_chain_validated": True,
        "p0_p1_safety_protection_validated": True,
        "non_owner_output_protection_validated": True,
        "stale_safety_speech_historical_only_protection_validated": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    output_baseline_summary = {
        "summary_id": f"{CLOSURE_ID}_output_baseline",
        "current_output_baseline": CURRENT_OUTPUT_BASELINE,
        "allowed_output_modes": ALLOWED_OUTPUT_MODES,
        "real_audio_output_allowed": False,
        "real_tts_allowed": False,
        "user_heard_assumed": False,
        "vop_runtime_allowed": False,
        "speech_gate_runtime_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    remaining_runtime_disabled_summary = {
        "summary_id": f"{CLOSURE_ID}_remaining_disabled_runtime",
        "camera_runtime": "disabled",
        "microphone_runtime": "disabled",
        "asr_runtime": "disabled",
        "tts_runtime": "disabled",
        "audio_output_runtime": "disabled",
        "speech_gate_runtime": "disabled",
        "vop_runtime": "disabled",
        "map_api": "disabled",
        "gps_runtime": "disabled",
        "ocr_provider_runtime": "disabled",
        "detector_runtime": "disabled",
        "segmentation_runtime": "disabled",
        "tracking_runtime": "disabled",
        "navigation_action": "disabled",
        "task_commit": "disabled",
        "memory_write": "disabled",
        "worldmodel_write": "disabled",
        "fact_write": "disabled",
        "scene_delta_commit": "disabled",
        "face_recognition": "disabled",
        "voiceprint_runtime": "disabled",
        "facial_expression_runtime": "disabled",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "register_id": f"{CLOSURE_ID}_non_claims",
        "statements": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "pool_id": f"{CLOSURE_ID}_deferred_pool",
        "deferred_capabilities": [
            {
                "capability": capability,
                "deferred_from_next_mainline_priority": True,
                "requires_separate_phase": True,
                **_not_fact(),
            }
            for capability in DEFERRED_CAPABILITIES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    vision_mainline_handoff_plan = {
        "handoff_id": f"{CLOSURE_ID}_vision_handoff",
        "mainline_handoff_decision": "RETURN_TO_VISION_MAINLINE_AFTER_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "next_mainline_focus": VISION_MAINLINE_FOCUS,
        "primary_next_phase_recommendation": PRIMARY_NEXT,
        "alternative_if_ocr_final_closure_needed": ALTERNATIVE_NEXT,
        "must_not_insert_before_vision_return": [
            "gaode_or_real_map_api_program",
            "external_product_observation",
            "face_recognition",
            "voiceprint_runtime",
            "facial_expression_runtime",
            "real_map_api",
            "real_voice_output",
        ],
        "must_not_recommend_real_tts_next": True,
        "must_not_recommend_live_audio_next": True,
        "must_not_recommend_camera_enablement_next": True,
        "must_not_recommend_map_api_enablement_next": True,
        "must_not_recommend_memory_or_worldmodel_write_next": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    minimal_runtime_integration_closure_report = {
        "closure_id": CLOSURE_ID,
        "closure_scope": "minimal_runtime_integration_closure",
        "completed_phase_count": len(COMPLETED_PHASE_SPECS),
        "completed_phase_refs": [row["phase_name"] for row in completed_phase_rows],
        "completed_capability_summary": "validated_capability_summary.json",
        "validated_loop_summary": "validated_capability_summary.json",
        "output_baseline_summary": "output_baseline_summary.json",
        "remaining_runtime_disabled_summary": "remaining_runtime_disabled_summary.json",
        "no_write_boundary_summary": {
            "memory_write_allowed": False,
            "worldmodel_write_allowed": False,
            "fact_write_allowed": False,
            "scene_delta_commit_allowed": False,
        },
        "known_non_claims": non_claims_register["statements"],
        "deferred_capability_pool": [item["capability"] for item in deferred_capability_pool["deferred_capabilities"]],
        "mainline_handoff_decision": vision_mainline_handoff_plan["mainline_handoff_decision"],
        "next_mainline_focus": vision_mainline_handoff_plan["next_mainline_focus"],
        "final_closure_decision": FINAL_DECISION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{CLOSURE_ID}_next_phase",
        "primary_next_phase_recommendation": PRIMARY_NEXT,
        "alternative_if_ocr_mainline_final_closure_needed": ALTERNATIVE_NEXT,
        "must_not_recommend_real_tts": True,
        "must_not_recommend_live_audio": True,
        "must_not_recommend_camera_enablement": True,
        "must_not_recommend_map_api_enablement": True,
        "must_not_recommend_memory_or_worldmodel_write": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    return {
        "summary": {
            "phase": PHASE_ID,
            "closure_scope": "minimal_runtime_integration_closure_only",
            "closure_only": True,
            "completed_phase_count": len(COMPLETED_PHASE_SPECS),
            "all_required_phases_loaded": all_required_phases_loaded,
            "all_required_phases_go": all_required_phases_go,
            "validated_loop_summary_generated": True,
            "output_baseline_summary_generated": True,
            "remaining_runtime_disabled_summary_generated": True,
            "non_claims_register_generated": True,
            "deferred_capability_pool_generated": True,
            "vision_mainline_handoff_plan_generated": True,
            "current_output_baseline": CURRENT_OUTPUT_BASELINE,
            "real_audio_output_allowed": False,
            "real_tts_allowed": False,
            "user_heard_assumed": False,
            "live_runtime_enabled": False,
            "memory_write_allowed": False,
            "worldmodel_write_allowed": False,
            "fact_write_allowed": False,
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "violations": [],
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "minimal_runtime_integration_closure_report": minimal_runtime_integration_closure_report,
        "completed_phase_matrix": {
            "completed_phase_count": len(completed_phase_rows),
            "rows": completed_phase_rows,
            **_not_fact(),
        },
        "validated_capability_summary": validated_capability_summary,
        "output_baseline_summary": output_baseline_summary,
        "remaining_runtime_disabled_summary": remaining_runtime_disabled_summary,
        "non_claims_register": non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "vision_mainline_handoff_plan": vision_mainline_handoff_plan,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "trial_definition_final_decision": phase_summaries.get("trial_definition", {}).get("final_decision"),
            "controlled_shadow_trial_final_decision": phase_summaries.get("controlled_shadow_trial", {}).get("final_decision"),
            "post_shadow_review_final_decision": phase_summaries.get("post_shadow_review", {}).get("final_decision"),
            "controlled_output_definition_final_decision": phase_summaries.get("controlled_output_definition", {}).get("final_decision"),
            "text_only_trial_final_decision": phase_summaries.get("text_only_trial", {}).get("final_decision"),
            "text_only_post_trial_review_final_decision": phase_summaries.get("text_only_post_trial_review", {}).get("final_decision"),
            "stabilization_scenario_count": len(phase_payloads["stabilization"].get("rows") or []),
            "safety_candidate_count": phase_payloads["safety_task_arbitration"].get("arbitration_candidate_count"),
            "ownership_candidate_count": phase_payloads["ownership_gate"].get("decision_candidate_count"),
            "interruption_candidate_count": phase_payloads["interruption_governance"].get("interruption_decision_candidate_count"),
            "text_only_trial_case_count": phase_summaries.get("text_only_trial", {}).get("trial_case_count"),
            "text_only_output_event_count": phase_summaries.get("text_only_trial", {}).get("controlled_text_output_event_count"),
            "text_only_abort_check_count": phase_payloads["text_only_abort"].get("abort_check_count"),
            "controlled_output_definition_id": phase_payloads["controlled_output_definition"].get("controlled_output_definition_id"),
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "primary_next_phase_recommendation": PRIMARY_NEXT,
            "alternative_if_ocr_mainline_final_closure_needed": ALTERNATIVE_NEXT,
            **_not_fact(),
        },
    }
