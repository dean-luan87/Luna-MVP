# -*- coding: utf-8 -*-
"""Crossing Decision Closure v1 — status freeze / boundary freeze / non-claims."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Crossing-Decision-Closure-v1-001"
CLOSURE_ID = "cdc_v1_001"
CLOSURE_SCOPE = "crossing_decision_closure_only"
SOURCE_CHAIN = "crossing_decision_closure_v1"
FINAL_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "CROSSING_DECISION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
CROSSING_GOVERNANCE_DECISION = "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
POST_CONTROLLED_FRAME_ROADMAP_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
CONTROLLED_FRAME_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

FORBIDDEN_OUTPUT_MODES = [
    "SAFE_TO_CROSS",
    "CROSS_NOW",
    "GO_AHEAD",
    "PROCEED",
    "FOLLOW_THE_CROWD",
    "GREEN_LIGHT_GO",
    "MAP_SAYS_CROSS",
    "COUNTDOWN_SAYS_GO",
]

COMPLETED_PHASES = [
    (
        "Luna Safety Constitution Policy v1",
        "safety_constitution",
        "_eval_out/luna_safety_constitution_policy_v1_smoke_v0/",
        "GO",
        "global safety constitution and crossing inheritance baseline",
    ),
    (
        "Crossing Decision Safety Governance Policy v1",
        "crossing_safety_governance",
        "_eval_out/crossing_decision_safety_governance_policy_v1_smoke_v0/",
        "GO",
        "crossing evidence schema, permission boundary, forbidden output register",
    ),
    (
        "Crossing Decision DryRun v1",
        "crossing_decision_dryrun",
        "_eval_out/crossing_decision_dryrun_v1_smoke_v0/",
        "GO",
        "16-scenario simulated evidence conservative candidate validation",
    ),
    (
        "Crossing Decision Post-DryRun Review v1",
        "post_dryrun_review",
        "_eval_out/crossing_decision_post_dryrun_review_v1_smoke_v0/",
        "GO",
        "forbidden output absence and closure readiness audit",
    ),
]

VALIDATED_CAPABILITIES = [
    "Safety Constitution inheritance",
    "Crossing evidence candidate schema",
    "Crossing permission boundary",
    "Crossing uncertainty policy",
    "Crossing conflict policy",
    "Crossing output policy",
    "Crossing human assistance candidate policy",
    "Forbidden crossing output register",
    "16 scenario dry-run",
    "forbidden output absence verification",
    "conservative handling review",
    "post-dryrun closure readiness",
]

DISABLED_RUNTIMES = [
    "crossing runtime",
    "live camera runtime",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "GPS runtime",
    "tracking runtime",
    "optical flow runtime",
    "Supervision / ByteTrack / OC-SORT",
    "Speech Gate / VOP / TTS",
    "NavigationAction",
    "TaskState commit",
    "WorldModel write",
    "Memory write",
    "Library write",
    "Fact write",
    "SceneDelta",
]

NON_CLAIMS = [
    "closure 不等于 Luna 会过街",
    "closure 不等于真实过街判断",
    "closure 不等于 live crossing runtime",
    "closure 不等于可以输出“可以过马路”",
    "green light candidate 不等于过街许可",
    "countdown OCR candidate 不等于过街许可",
    "crowd flow candidate 不等于跟随人流",
    "map crossing hint 不等于过街许可",
    "route says cross 不等于过街许可",
    "user says go 不等于过街许可",
    "human assistance candidate 不等于已获得人工协助",
    "dry-run conservative output 不等于生产安全能力",
    "policy closure 不等于 production readiness",
]

DEFERRED_CAPABILITIES = [
    "Crossing Decision Controlled Sample Planning",
    "real visual crossing sample manifest",
    "controlled traffic-light/crosswalk sample review",
    "crossing evidence validation framework",
    "live camera crossing guarded trial",
    "visual model adapter for traffic/crosswalk evidence",
    "OCR countdown gated trial",
    "vehicle flow / pedestrian flow tracking adapter",
    "map crossing hint runtime",
    "GPS / route crossing runtime",
    "Speech Gate crossing output guarded trial",
    "human assistance workflow",
    "NavigationAction guarded crossing runtime",
    "Safety Constitution → Survival Constitution upgrade",
    "Gate Taxonomy / Gate Requirement Framework",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform",
    "WorldModel / Memory / Library governance",
]

DEBT_CARRYOVER_TOPICS = [
    "crossing governance complexity",
    "high-risk domain gate taxonomy missing",
    "forbidden output maintenance",
    "Safety Constitution inheritance tracking",
    "future Survival Constitution upgrade",
    "human assistance governance complexity",
    "multimodal crossing evidence validation debt",
    "controlled sample planning deferred",
    "real crossing runtime deferred",
]

ROOT_SPECS = [
    {
        "id": "post_dryrun_review",
        "arg": "post_dryrun_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_closure_readiness_decision.json",
            "forbidden_crossing_output_review.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "crossing_decision_dryrun",
        "arg": "crossing_decision_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_decision_dryrun_results.json",
            "forbidden_crossing_output_check_results.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "crossing_safety_governance",
        "arg": "crossing_safety_governance_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "forbidden_crossing_output_register.json",
            "crossing_output_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_safety_inheritance_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "post_controlled_frame_roadmap_decision",
        "arg": "post_controlled_frame_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "task_aware_visual_focus_policy",
        "arg": "task_aware_visual_focus_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "selective_tracking_adapter_policy",
        "arg": "selective_tracking_adapter_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback_dryrun",
        "arg": "visual_ocr_map_task_feedback_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_controlled_output_definition",
        "arg": "minimal_runtime_controlled_output_definition_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_text_only_output_post_review",
        "arg": "minimal_runtime_text_only_output_post_review_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "voice_command_ownership_gate_policy",
        "arg": "voice_command_ownership_gate_policy_root",
        "required": False,
        "summary": "voice_command_ownership_gate_policy_v1_summary.json",
        "artifacts": ["voice_command_ownership_gate_policy_v1_summary.json"],
    },
    {
        "id": "voice_interruption_governance_dryrun",
        "arg": "voice_interruption_governance_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _verifier_verdict(root: Optional[Path]) -> str:
    if not root:
        return "MISSING"
    report = _read_json(root / "verifier_report.json")
    if isinstance(report, dict):
        return str(report.get("verifier") or report.get("verdict") or "COMPLETE")
    return "COMPLETE"


def _boundary_payload() -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_runtime_allowed": False,
        "crossing_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_crossing_decision_closure_v1(
    *,
    post_dryrun_review_root: str,
    crossing_decision_dryrun_root: str,
    crossing_safety_governance_root: str,
    safety_constitution_root: str,
    post_controlled_frame_roadmap_decision_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    vision_strengthening_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    task_aware_visual_focus_policy_root: Optional[str] = None,
    selective_tracking_adapter_policy_root: Optional[str] = None,
    visual_ocr_map_task_feedback_dryrun_root: Optional[str] = None,
    minimal_runtime_controlled_output_definition_root: Optional[str] = None,
    minimal_runtime_text_only_output_post_review_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}

    post_dryrun_review_input_loaded = (
        roots["post_dryrun_review"]["loaded"]
        and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
        and summaries["post_dryrun_review"].get("forbidden_crossing_outputs_absent") is True
    )
    dryrun_input_loaded = (
        roots["crossing_decision_dryrun"]["loaded"]
        and summaries["crossing_decision_dryrun"].get("final_decision") == DRYRUN_DECISION
        and summaries["crossing_decision_dryrun"].get("scenario_count", 0) >= 16
    )
    crossing_governance_input_loaded = (
        roots["crossing_safety_governance"]["loaded"]
        and summaries["crossing_safety_governance"].get("final_decision") == CROSSING_GOVERNANCE_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"]
        and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    post_controlled_frame_roadmap_decision_input_loaded = (
        roots["post_controlled_frame_roadmap_decision"]["loaded"]
        and summaries["post_controlled_frame_roadmap_decision"].get("final_decision") == POST_CONTROLLED_FRAME_ROADMAP_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    postreview_root = roots["post_dryrun_review"]["root"]
    dryrun_root = roots["crossing_decision_dryrun"]["root"]
    governance_root = roots["crossing_safety_governance"]["root"]

    postreview_readiness = _read_json(postreview_root / "crossing_closure_readiness_decision.json") if postreview_root else {}
    postreview_forbidden = _read_json(postreview_root / "forbidden_crossing_output_review.json") if postreview_root else {}
    dryrun_forbidden = _read_json(dryrun_root / "forbidden_crossing_output_check_results.json") if dryrun_root else {}
    governance_forbidden_register = _read_json(governance_root / "forbidden_crossing_output_register.json") if governance_root else {}
    postreview_governance_debt = _read_json(postreview_root / "governance_debt_review.json") if postreview_root else {}

    completed_phase_rows = []
    for phase_name, root_id, output_dir, status, role_in_closure in COMPLETED_PHASES:
        root = roots[root_id]["root"]
        phase_summary = summaries[root_id]
        completed_phase_rows.append(
            {
                "phase_id": phase_name,
                "status": status,
                "output_dir": output_dir,
                "verifier_verdict": _verifier_verdict(root),
                "final_decision": phase_summary.get("final_decision", ""),
                "role_in_closure": role_in_closure,
                "runtime_enabled": False,
                "write_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    completed_phase_matrix = {
        "phases": completed_phase_rows,
        "completed_phase_count": len(completed_phase_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    validated_capability_summary = {
        "validated_capabilities": VALIDATED_CAPABILITIES,
        "validation_layers": ["safety_constitution", "governance_policy", "dryrun", "post_dryrun_review"],
        "clarifications": [
            "这些是 policy / schema / dry-run / review validation，不是真实 crossing runtime",
            "不是真实过街判断能力",
            "不是 production readiness",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_runtime_summary = {
        "disabled_runtimes": DISABLED_RUNTIMES,
        "crossing_runtime_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_crossing_runtime": True,
        "no_real_crossing_judgment": True,
        "no_safe_to_cross_claim": True,
        "no_crossing_permission_output": True,
        "no_crossing_action_instruction": True,
        "no_human_assistance_obtained_assumption": True,
        "no_map_authority": True,
        "no_OCR_authority": True,
        "no_visual_authority": True,
        "no_crowd_flow_authority": True,
        "no_user_command_override": True,
        "candidate_not_fact": True,
        "conservative_output_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_rows = []
    for forbidden_output in FORBIDDEN_OUTPUT_MODES:
        forbidden_rows.append(
            {
                "forbidden_output": forbidden_output,
                "reason": "current mainline forbids crossing permission or equivalent action instruction",
                "inherited_from_safety_constitution": True,
                "enforced_by_crossing_governance": forbidden_output in (governance_forbidden_register.get("forbidden_outputs") or []),
                "verified_absent_in_dryrun": dryrun_forbidden.get("forbidden_crossing_outputs_absent") is True,
                "verified_absent_in_review": postreview_forbidden.get("forbidden_outputs_absent") is True,
                "runtime_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    forbidden_crossing_output_freeze = {
        "forbidden_outputs": forbidden_rows,
        "forbidden_count": len(forbidden_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_decision_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "deferred_capabilities": DEFERRED_CAPABILITIES,
        "controlled_sample_planning_started": False,
        "crossing_runtime_trial_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_carryover = {
        "carryover_topics": DEBT_CARRYOVER_TOPICS,
        "inherited_review_topics": postreview_governance_debt.get("carryover_topics", []),
        "future_midplatform_function_governance_required": True,
        "future_gate_taxonomy_required": True,
        "future_survival_constitution_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_absent = (
        summaries["crossing_decision_dryrun"].get("forbidden_crossing_outputs_absent") is True
        and summaries["post_dryrun_review"].get("forbidden_crossing_outputs_absent") is True
        and dryrun_forbidden.get("total_violation_count", 1) == 0
        and postreview_forbidden.get("violation_count", 1) == 0
    )

    blockers: List[str] = []
    for flag_name, loaded in (
        ("post_dryrun_review_input_loaded", post_dryrun_review_input_loaded),
        ("dryrun_input_loaded", dryrun_input_loaded),
        ("crossing_governance_input_loaded", crossing_governance_input_loaded),
        ("safety_constitution_input_loaded", safety_constitution_input_loaded),
        ("post_controlled_frame_roadmap_decision_input_loaded", post_controlled_frame_roadmap_decision_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)
    if postreview_readiness.get("ready_for_closure") is not True:
        blockers.append("postreview_not_ready_for_closure")
    if len(completed_phase_rows) < 4:
        blockers.append("completed_phase_matrix_incomplete")
    if not forbidden_absent:
        blockers.append("forbidden_output_not_absent")

    closure_readiness_gate = {
        "go_conditions": [
            "Safety Constitution input loaded",
            "Crossing Governance input loaded",
            "Crossing DryRun input loaded",
            "Post-DryRun Review input loaded",
            "forbidden outputs absent",
            "crossing permission false all cases",
            "safe-to-cross claim false all cases",
            "conservative handling pass",
            "no runtime",
            "no write",
            "no action",
            "no speech",
            "non-claims generated",
            "deferred capability pool generated",
            "governance debt carryover generated",
            "next phase fixed",
        ],
        "no_go_conditions": [
            "any required root missing",
            "any forbidden output appears",
            "any crossing permission allowed",
            "any safe-to-cross claim allowed",
            "crossing runtime invoked",
            "camera/map/OCR/tracking runtime invoked",
            "Speech Gate / TTS invoked",
            "WorldModel / Memory / Fact write",
            "closure claims Luna can cross safely",
            "next phase unclear",
        ],
        "ready_for_closure": not blockers,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_decision_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "source_phase_chain": [
            "Phase-Luna-Safety-Constitution-Policy-v1-001",
            "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001",
            "Phase-Crossing-Decision-DryRun-v1-001",
            "Phase-Crossing-Decision-Post-DryRun-Review-v1-001",
        ],
        "completed_phase_count": len(completed_phase_rows),
        "completed_phase_matrix_ref": "completed_phase_matrix.json",
        "validated_capability_summary_ref": "validated_capability_summary.json",
        "disabled_runtime_summary_ref": "disabled_runtime_summary.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "forbidden_output_freeze_ref": "forbidden_crossing_output_freeze.json",
        "non_claims_register_ref": "crossing_decision_non_claims_register.json",
        "deferred_capability_pool_ref": "deferred_capability_pool.json",
        "governance_debt_carryover_ref": "governance_debt_carryover.json",
        "next_phase_recommendation": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CROSSING_DECISION_CLOSURE_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "crossing_governance_input_loaded": crossing_governance_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "post_controlled_frame_roadmap_decision_input_loaded": post_controlled_frame_roadmap_decision_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "validated_capability_summary_generated": True,
        "disabled_runtime_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "forbidden_crossing_output_freeze_generated": True,
        "non_claims_register_generated": True,
        "deferred_capability_pool_generated": True,
        "governance_debt_carryover_generated": True,
        "closure_readiness_gate_generated": True,
        "safety_constitution_inheritance_closed": safety_constitution_input_loaded,
        "crossing_governance_policy_closed": crossing_governance_input_loaded,
        "crossing_dryrun_closed": dryrun_input_loaded,
        "crossing_post_review_closed": post_dryrun_review_input_loaded,
        "crossing_decision_closed": not blockers,
        "forbidden_crossing_outputs_absent": forbidden_absent,
        "forbidden_output_violation_count": dryrun_forbidden.get("total_violation_count", 0) if dryrun_forbidden else 0,
        "crossing_permission_allowed_false_all_cases": summaries["post_dryrun_review"].get("crossing_permission_allowed_false_all_cases") is True,
        "crossing_action_instruction_allowed_false_all_cases": summaries["post_dryrun_review"].get("crossing_action_instruction_allowed_false_all_cases") is True,
        "safe_to_cross_claim_allowed_false_all_cases": summaries["post_dryrun_review"].get("safe_to_cross_claim_allowed_false_all_cases") is True,
        "conservative_handling_pass": summaries["post_dryrun_review"].get("conservative_handling_pass") is True,
        "human_assistance_obtained_assumed": False,
        "crossing_runtime_claimed": False,
        "real_crossing_judgment_claimed": False,
        "safe_to_cross_capability_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "gate_taxonomy_required_later": True,
        "survival_constitution_required_later": True,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "CROSSING_DECISION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "crossing_decision_closure_summary": crossing_decision_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "validated_capability_summary": validated_capability_summary,
        "disabled_runtime_summary": disabled_runtime_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "forbidden_crossing_output_freeze": forbidden_crossing_output_freeze,
        "crossing_decision_non_claims_register": crossing_decision_non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "governance_debt_carryover": governance_debt_carryover,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": {
            "recommended_next_phase": summary["recommended_next_phase"],
            "final_decision": summary["final_decision"],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
    }
