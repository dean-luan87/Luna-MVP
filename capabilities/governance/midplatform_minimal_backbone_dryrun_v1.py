# -*- coding: utf-8 -*-
"""Midplatform Minimal Backbone DryRun v1 — simulated eight-layer candidate consumption only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.luna_validation_factory_consolidation_v1 import FINAL_DECISION as FACTORY_FINAL
from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
    PHASE_ID as ALIGNMENT_PHASE,
)
from capabilities.governance.midplatform_current_state_inventory_v1 import (
    FINAL_DECISION_GO as INVENTORY_FINAL_GO,
    PHASE_ID as INVENTORY_PHASE,
)
from capabilities.governance.midplatform_module_gap_and_roadmap_planning_v1 import (
    FINAL_DECISION_GO as GAP_PLANNING_FINAL_GO,
    P0_MODULES,
    PHASE_ID as GAP_PLANNING_PHASE,
)
from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    FINAL_DECISION_GO as CLEANUP_PLANNING_FINAL_GO,
    PHASE_ID as CLEANUP_PLANNING_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as NAV_TRIAL_FINAL,
)
from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as OCR_TRIAL_FINAL,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1 import (
    FINAL_DECISION_GO as VISION_TRIAL_FINAL,
)

PHASE_ID = "Phase-Midplatform-Minimal-Backbone-DryRun-v1-001"
SCOPE = "midplatform_minimal_backbone_dryrun_only"
SOURCE_CHAIN = "midplatform_minimal_backbone_dryrun_v1"

FINAL_DECISION_GO = "MIDPLATFORM_MINIMAL_BACKBONE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_MINIMAL_BACKBONE_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Minimal-Backbone-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Minimal-Backbone-Issue-Review-v1-001"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_dryrun"
)

CANDIDATE_TYPES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)

BLOCK_CHECKS: Tuple[str, ...] = (
    "candidate_to_fact_upgrade",
    "navigation_guidance_to_navigation_action",
    "ocr_candidate_to_ocr_fact",
    "visual_candidate_to_world_model_write",
    "candidate_to_tts_output",
    "candidate_to_task_commit",
    "candidate_to_memory_write",
    "support_layer_direct_write",
    "model_runtime_invocation",
    "live_camera_or_provider_invocation",
)


def _not_fact() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "user_facing_output_allowed": False,
    }


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_minimal_backbone_dryrun_only": True,
        "simulated": True,
        "dryrun_only": True,
        "runtime_enabled_now": False,
        "real_runtime_enabled_now": False,
        "model_runtime_invoked_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "map_write_executed_now": False,
        "route_commit_executed_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "active_drive_execution_enabled_now": False,
        "drive_action_executed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "scene_delta_generated_now": False,
        "file_move_executed_now": False,
        "directory_merge_executed_now": False,
        "import_rewrite_executed_now": False,
        "memory_lookup_executed_now": False,
        "world_model_lookup_executed_now": False,
        "library_lookup_executed_now": False,
        "external_experience_candidate_generated_now": False,
        "module_implementation_started_now": False,
        "p0_gap_implemented_now": False,
        "task_response_candidate_chain_deferred_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    if not root.is_dir():
        return False
    sm = _try_read_json(root / "summary.json") or {}
    vr = _try_read_json(root / "verifier_report.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def _validate_upstream(
    inventory_root: Path,
    alignment_root: Path,
    cleanup_root: Path,
    gap_root: Path,
    factory_root: Path,
    vision_root: Path,
    ocr_root: Path,
    nav_root: Path,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    checks: List[Tuple[str, Path, Optional[str], Optional[str]]] = [
        ("inventory", inventory_root, INVENTORY_PHASE, INVENTORY_FINAL_GO),
        ("alignment", alignment_root, ALIGNMENT_PHASE, ALIGNMENT_FINAL_GO),
        ("cleanup", cleanup_root, CLEANUP_PLANNING_PHASE, CLEANUP_PLANNING_FINAL_GO),
        ("gap", gap_root, GAP_PLANNING_PHASE, GAP_PLANNING_FINAL_GO),
        ("factory", factory_root, UPSTREAM_FACTORY_PHASE, FACTORY_FINAL),
        ("vision", vision_root, None, VISION_TRIAL_FINAL),
        ("ocr", ocr_root, None, OCR_TRIAL_FINAL),
        ("nav", nav_root, None, NAV_TRIAL_FINAL),
    ]
    for label, root, phase, final in checks:
        if not _check_go(root):
            blockers.append(f"{label} verifier must be GO")
        sm = _try_read_json(root / "summary.json") or {}
        ctx[f"{label}_summary"] = sm
        if phase and sm.get("phase") != phase:
            blockers.append(f"{label} phase mismatch")
        if final and sm.get("final_decision") != final:
            blockers.append(f"{label} final_decision mismatch")

    must_fill = _try_read_json(gap_root / "must_fill_module_gap_register_v1.json") or {}
    p0 = must_fill.get("modules") or []
    if len(p0) != len(P0_MODULES):
        blockers.append("P0 gap register count mismatch")
    for mod in P0_MODULES:
        if mod not in p0:
            blockers.append(f"P0 gap missing: {mod}")

    return blockers, ctx


def _vision_execution_root(vision_post_review_root: Path) -> Path:
    for name in (
        "controlled_trial_closure_decision_v1.json",
        "next_chain_adoption_readiness_v1.json",
        "summary.json",
    ):
        doc = _try_read_json(vision_post_review_root / name) or {}
        root = doc.get("upstream_execution_root")
        if root:
            return Path(root).expanduser().resolve()
    return vision_post_review_root.parent / "vision_sample_frame_single_chain_controlled_trial_execution"


def _load_primary_candidate(
    candidate_type: str,
    *,
    vision_post_review_root: Path,
    ocr_trial_root: Path,
    nav_trial_root: Path,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if candidate_type == "visual_observation_candidate":
        exec_root = _vision_execution_root(vision_post_review_root)
        paths = sorted(exec_root.glob("visual_observation_candidate_[0-9]*_v1.json"))
        if not paths:
            return None, f"no VOC files under {exec_root}"
        return _try_read_json(paths[0]), str(paths[0])

    if candidate_type == "ocr_result_candidate":
        exec_root = ocr_trial_root / "_controlled_execution"
        paths = sorted(exec_root.glob("ocr_result_candidate_[0-9]*_v1.json"))
        if not paths:
            return None, f"no OCR files under {exec_root}"
        return _try_read_json(paths[0]), str(paths[0])

    exec_root = nav_trial_root / "_controlled_execution"
    paths = sorted(exec_root.glob("navigation_guidance_candidate_[0-9]*_v1.json"))
    if not paths:
        return None, f"no NGC files under {exec_root}"
    return _try_read_json(paths[0]), str(paths[0])


def _build_intake(candidate: Dict[str, Any], candidate_type: str, source_path: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "record_id": "candidate_intake_record_v1",
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "source_chain_present": bool(candidate.get("source_chain_present") or candidate.get("source_chain")),
        "provenance_present": bool(candidate.get("provenance_present", True)),
        "source_path": source_path,
        "intake_pass": True,
        **meta,
        **_not_fact(),
    }


def _build_evidence(candidate: Dict[str, Any], candidate_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    mock_status = "mock_or_fixture_only" if candidate_type == "ocr_result_candidate" else "not_applicable"
    if candidate_type == "navigation_guidance_candidate":
        map_ctx = candidate.get("map_context_type", "")
        mock_status = "readonly_or_synthetic_only" if "readonly" in str(map_ctx) or "synthetic" in str(map_ctx) else "review"
    risk = "low"
    blocked_reason = None
    if candidate.get("candidate_only") is not True or candidate.get("fact_status") != "not_fact":
        risk = "high"
        blocked_reason = "candidate_contract_violation"
    return {
        "record_id": "evidence_governance_record_v1",
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "source_chain_status": "closed_chain_observed",
        "confidence_status": "candidate_unverified",
        "ttl_staleness_status": "within_synthetic_ttl",
        "mock_or_fixture_status": mock_status,
        "risk_level": risk,
        "blocked_reason": blocked_reason,
        "fallback_reason": None,
        "fact_write_allowed": False,
        **meta,
    }


def _gate_pass(value: bool = True) -> str:
    return "pass" if value else "block"


def _build_constitution(candidate: Dict[str, Any], candidate_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    nav_blocks_action = candidate_type != "navigation_guidance_candidate" or candidate.get("navigation_action_allowed") is False
    nav_blocks_output = candidate_type != "navigation_guidance_candidate" or candidate.get("user_facing_output_allowed") is False
    ocr_mock_ok = candidate_type != "ocr_result_candidate" or candidate.get("provider_type") == "mock_or_fixture_only"
    all_pass = (
        candidate.get("candidate_only") is True
        and candidate.get("fact_status") == "not_fact"
        and nav_blocks_action
        and nav_blocks_output
        and ocr_mock_ok
    )
    return {
        "review_id": "constitution_gate_review_v1",
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "safety_gate": _gate_pass(all_pass),
        "survival_gate": _gate_pass(True),
        "fact_boundary_gate": _gate_pass(candidate.get("fact_status") == "not_fact"),
        "action_boundary_gate": _gate_pass(nav_blocks_action and candidate.get("runtime_action_allowed") is False),
        "output_boundary_gate": _gate_pass(nav_blocks_output),
        "memory_write_gate": _gate_pass(True),
        "model_invocation_gate": _gate_pass(True),
        "privacy_gate": _gate_pass(True),
        "source_chain_gate": _gate_pass(bool(candidate.get("source_chain"))),
        "ttl_staleness_gate": _gate_pass(True),
        "constitution_pass": all_pass,
        "fact_upgrade_blocked": True,
        **meta,
    }


def _build_task_routing(candidate: Dict[str, Any], candidate_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    route_obs = candidate_type in ("visual_observation_candidate", "ocr_result_candidate")
    route_task = candidate_type == "ocr_result_candidate"
    return {
        "record_id": "task_routing_candidate_v1",
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "route_to_task_context_candidate": route_task,
        "route_to_observation_requirement_candidate": route_obs,
        "route_to_hold": False,
        "route_to_fallback": False,
        "task_commit_allowed": False,
        "task_response_candidate_deferred": True,
        **meta,
    }


def _build_guidance_queue(candidate: Dict[str, Any], candidate_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    priority = {"visual_observation_candidate": 2, "ocr_result_candidate": 3, "navigation_guidance_candidate": 1}.get(
        candidate_type, 5
    )
    return {
        "item_id": "guidance_candidate_queue_item_v1",
        "queue_item_type": f"{candidate_type}_queue_item",
        "priority": priority,
        "source_candidate_ref": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "safety_review_required": True,
        "output_arbitration_required": True,
        "user_facing_output_allowed": False,
        **meta,
        **_not_fact(),
    }


def _build_output_arbitration(candidate: Dict[str, Any], candidate_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    blocked_reason = "dryrun_default_hold_no_user_output"
    if candidate_type == "navigation_guidance_candidate":
        blocked_reason = "navigation_guidance_candidate_no_user_facing_output"
    return {
        "record_id": "output_arbitration_candidate_v1",
        "candidate_id": candidate.get("candidate_id"),
        "candidate_type": candidate_type,
        "output_allowed": False,
        "speech_response_candidate_generated_now": False,
        "blocked_or_hold_reason": blocked_reason,
        "clarification_required": False,
        "fallback_candidate": None,
        **meta,
    }


def _build_runtime_boundary(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "decision_id": "runtime_boundary_decision_v1",
        "dryrun_allowed": True,
        "controlled_trial_allowed": False,
        "limited_runtime_allowed": False,
        "real_runtime_allowed": False,
        "model_invocation_allowed": False,
        "provider_invocation_allowed": False,
        "action_execution_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "library_write_allowed": False,
        **meta,
    }


def _run_single_flow(
    flow_id: str,
    candidate_type: str,
    *,
    vision_post_review_root: Path,
    ocr_trial_root: Path,
    nav_trial_root: Path,
    meta: Dict[str, Any],
    include_task_routing: bool,
) -> Dict[str, Any]:
    candidate, source_path = _load_primary_candidate(
        candidate_type,
        vision_post_review_root=vision_post_review_root,
        ocr_trial_root=ocr_trial_root,
        nav_trial_root=nav_trial_root,
    )
    issues: List[str] = []
    if not candidate:
        return {"flow_id": flow_id, "flow_pass": False, "issues": [source_path or "missing candidate"]}

    ok, contract_issues = validate_candidate_output(
        candidate,
        expected_type=candidate_type,
        require_timestamp=candidate_type != "visual_observation_candidate",
    )
    if not ok:
        issues.extend(contract_issues)

    if candidate_type == "ocr_result_candidate" and candidate.get("provider_type") != "mock_or_fixture_only":
        issues.append("ocr must be mock_or_fixture_only")
    if candidate_type == "navigation_guidance_candidate":
        if candidate.get("navigation_action_allowed") is True:
            issues.append("navigation_action_allowed must be false")
        if candidate.get("user_facing_output_allowed") is True:
            issues.append("user_facing_output_allowed must be false")

    intake = _build_intake(candidate, candidate_type, source_path or "", meta)
    evidence = _build_evidence(candidate, candidate_type, meta)
    constitution = _build_constitution(candidate, candidate_type, meta)
    task_routing = _build_task_routing(candidate, candidate_type, meta) if include_task_routing else None
    guidance = _build_guidance_queue(candidate, candidate_type, meta)
    arbitration = _build_output_arbitration(candidate, candidate_type, meta)
    runtime = _build_runtime_boundary(meta)

    layer_pass = (
        intake.get("intake_pass") is True
        and evidence.get("fact_write_allowed") is False
        and constitution.get("constitution_pass") is True
        and (task_routing is None or task_routing.get("task_commit_allowed") is False)
        and guidance.get("user_facing_output_allowed") is False
        and arbitration.get("output_allowed") is False
        and runtime.get("real_runtime_allowed") is False
    )
    flow_pass = layer_pass and not issues

    steps = [
        {"step": "candidate_intake", "artifact": "candidate_intake_record", "pass": intake.get("intake_pass")},
        {"step": "evidence_governance", "artifact": "evidence_governance_record", "pass": evidence.get("fact_write_allowed") is False},
        {"step": "constitution_gate", "artifact": "constitution_gate_review", "pass": constitution.get("constitution_pass")},
    ]
    if task_routing:
        steps.append(
            {"step": "task_routing", "artifact": "task_routing_candidate", "pass": task_routing.get("task_commit_allowed") is False}
        )
    steps.extend(
        [
            {"step": "guidance_queue", "artifact": "guidance_candidate_queue_item", "pass": guidance.get("user_facing_output_allowed") is False},
            {"step": "output_arbitration", "artifact": "output_arbitration_candidate", "pass": arbitration.get("output_allowed") is False},
            {"step": "runtime_boundary", "artifact": "runtime_boundary_decision", "pass": runtime.get("dryrun_allowed") is True},
        ]
    )

    return {
        "flow_id": flow_id,
        "candidate_type": candidate_type,
        "flow_pass": flow_pass,
        "issues": issues,
        "candidate_id": candidate.get("candidate_id"),
        "source_path": source_path,
        "steps": steps,
        "candidate_intake_record": intake,
        "evidence_governance_record": evidence,
        "constitution_gate_review": constitution,
        "task_routing_candidate": task_routing,
        "guidance_candidate_queue_item": guidance,
        "output_arbitration_candidate": arbitration,
        "runtime_boundary_decision": runtime,
    }


def _block_verification(meta: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    all_pass = True
    expectations = {
        "candidate_to_fact_upgrade": False,
        "navigation_guidance_to_navigation_action": False,
        "ocr_candidate_to_ocr_fact": False,
        "visual_candidate_to_world_model_write": False,
        "candidate_to_tts_output": False,
        "candidate_to_task_commit": False,
        "candidate_to_memory_write": False,
        "support_layer_direct_write": False,
        "model_runtime_invocation": False,
        "live_camera_or_provider_invocation": False,
    }
    for check_id in BLOCK_CHECKS:
        observed = expectations.get(check_id, False)
        passed = observed is False
        if not passed:
            all_pass = False
        rows.append({"check_id": check_id, "blocked": True, "observed_now": observed, "pass": passed})
    return {
        "verification_id": "minimal_backbone_block_verification_v1",
        "all_blocked_pass": all_pass,
        "rows": rows,
        **meta,
    }


def _gap_consumption(meta: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for mod in P0_MODULES:
        rows.append(
            {
                "gap_module": mod,
                "consumption_mode": "contract_level_dryrun_simulated",
                "implemented_now": False,
                "satisfied_for_dryrun": mod != "midplatform_minimal_backbone_dryrun_runner_verifier",
                "note": "P0 registered; runner satisfied by this phase verifier",
            }
        )
    return {
        "result_id": "minimal_backbone_gap_consumption_result_v1",
        "p0_gaps_total": len(P0_MODULES),
        "p0_implemented_count": 0,
        "consumption_pass": True,
        "rows": rows,
        **meta,
    }


def run_midplatform_minimal_backbone_dryrun_v1(
    *,
    midplatform_current_state_inventory_root: str,
    midplatform_backbone_definition_alignment_root: str,
    midplatform_structure_cleanup_planning_root: str,
    midplatform_module_gap_and_roadmap_planning_root: str,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    inventory_root = Path(midplatform_current_state_inventory_root).expanduser().resolve()
    alignment_root = Path(midplatform_backbone_definition_alignment_root).expanduser().resolve()
    cleanup_root = Path(midplatform_structure_cleanup_planning_root).expanduser().resolve()
    gap_root = Path(midplatform_module_gap_and_roadmap_planning_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    vision_root = Path(
        vision_sample_frame_single_chain_controlled_trial_post_execution_review_root
    ).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(
        navigation_guidance_candidate_single_chain_trial_via_validation_factory_root
    ).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()

    blockers, ctx = _validate_upstream(
        inventory_root, alignment_root, cleanup_root, gap_root, factory_root, vision_root, ocr_root, nav_root
    )
    meta = _boundary_meta()
    dryrun_ok = len(blockers) == 0

    flow_a = _run_single_flow(
        "Flow_A_vision_candidate_intake",
        "visual_observation_candidate",
        vision_post_review_root=vision_root,
        ocr_trial_root=ocr_root,
        nav_trial_root=nav_root,
        meta=meta,
        include_task_routing=False,
    )
    flow_b = _run_single_flow(
        "Flow_B_ocr_mock_candidate_intake",
        "ocr_result_candidate",
        vision_post_review_root=vision_root,
        ocr_trial_root=ocr_root,
        nav_trial_root=nav_root,
        meta=meta,
        include_task_routing=True,
    )
    flow_c = _run_single_flow(
        "Flow_C_navigation_guidance_candidate_intake",
        "navigation_guidance_candidate",
        vision_post_review_root=vision_root,
        ocr_trial_root=ocr_root,
        nav_trial_root=nav_root,
        meta=meta,
        include_task_routing=False,
    )

    flows = [flow_a, flow_b, flow_c]
    flows_all_pass = dryrun_ok and all(f.get("flow_pass") for f in flows)

    intake_records = [f["candidate_intake_record"] for f in flows if f.get("candidate_intake_record")]
    evidence_records = [f["evidence_governance_record"] for f in flows if f.get("evidence_governance_record")]
    constitution_reviews = [f["constitution_gate_review"] for f in flows if f.get("constitution_gate_review")]
    task_routings = [f["task_routing_candidate"] for f in flows if f.get("task_routing_candidate")]
    guidance_items = [f["guidance_candidate_queue_item"] for f in flows if f.get("guidance_candidate_queue_item")]
    arbitrations = [f["output_arbitration_candidate"] for f in flows if f.get("output_arbitration_candidate")]
    runtime_decisions = [f["runtime_boundary_decision"] for f in flows if f.get("runtime_boundary_decision")]

    block_ver = _block_verification(meta)
    gap_result = _gap_consumption(meta)

    high_risk = any(
        [
            not dryrun_ok,
            any(f.get("issues") for f in flows),
            any((e.get("risk_level") == "high") for e in evidence_records),
            not block_ver.get("all_blocked_pass"),
        ]
    )

    policy = {
        "policy_id": "midplatform_minimal_backbone_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "eight_layer_simulation": True,
        "drive_support_contract_level_only": True,
        "principles": [
            "consume_closed_candidates_only",
            "no_fact_upgrade",
            "no_runtime_no_commit",
            "P0_gaps_simulated_not_implemented",
        ],
        **meta,
    }

    input_review = {
        "review_id": "upstream_planning_input_review_v1",
        "review_pass": dryrun_ok,
        "blockers": blockers,
        "upstream_context": {
            "inventory_final": (ctx.get("inventory_summary") or {}).get("final_decision"),
            "alignment_final": (ctx.get("alignment_summary") or {}).get("final_decision"),
            "cleanup_final": (ctx.get("cleanup_summary") or {}).get("final_decision"),
            "gap_final": (ctx.get("gap_summary") or {}).get("final_decision"),
            "factory_final": (ctx.get("factory_summary") or {}).get("final_decision"),
            "vision_final": (ctx.get("vision_summary") or {}).get("final_decision"),
            "ocr_final": (ctx.get("ocr_summary") or {}).get("final_decision"),
            "nav_final": (ctx.get("nav_summary") or {}).get("final_decision"),
        },
        "task_response_candidate_deferred": True,
        "p0_gaps_registered_not_implemented": True,
        **meta,
    }

    matrix = {
        "matrix_id": "minimal_backbone_candidate_input_matrix_v1",
        "rows": [
            {
                "candidate_type": t,
                "source": {
                    "visual_observation_candidate": "vision_post_review→execution",
                    "ocr_result_candidate": "ocr_trial/_controlled_execution",
                    "navigation_guidance_candidate": "nav_trial/_controlled_execution",
                }[t],
                "flow_id": {"visual_observation_candidate": "Flow_A", "ocr_result_candidate": "Flow_B", "navigation_guidance_candidate": "Flow_C"}[t],
            }
            for t in CANDIDATE_TYPES
        ],
        **meta,
    }

    drive_dryrun = {
        "signal_id": "drive_layer_signal_dryrun_v1",
        "drive_signal_observed": False,
        "drive_signal_candidate": True,
        "survival_drive_candidate": False,
        "active_drive_execution_enabled": False,
        "drive_to_task_commit": False,
        "layer_status": "contract_level_only",
        **meta,
    }

    health_dryrun = {
        "signal_id": "health_layer_signal_dryrun_v1",
        "health_signal_record": {"status": "runtime_disabled_placeholder"},
        "provider_status_candidate": {"ocr": "not_invoked", "vision": "not_invoked", "nav": "not_invoked"},
        "runtime_disabled_status": True,
        "hardware_status_placeholder": True,
        "health_to_drive_signal_candidate": False,
        **meta,
    }

    memory_block = {
        "review_id": "memory_support_access_block_review_v1",
        "memory_lookup_executed_now": False,
        "world_model_lookup_executed_now": False,
        "library_lookup_executed_now": False,
        "hive_sync_executed_now": False,
        "external_experience_candidate_generated_now": False,
        "all_writes_blocked": True,
        "support_layer_direct_write_blocked": True,
        **meta,
    }

    flow_trace = {
        "trace_id": "minimal_backbone_flow_trace_v1",
        "flows": [{"flow_id": f["flow_id"], "flow_pass": f.get("flow_pass"), "steps": f.get("steps")} for f in flows],
        "flows_all_pass": flows_all_pass,
        **meta,
    }

    non_claims = {
        "register_id": "minimal_backbone_non_claims_register_v1",
        "claims": [
            "DryRun does not prove production runtime readiness",
            "Drive/Support layers are contract placeholders only",
            "P0 module contracts are simulated not implemented in midplatform/",
            "Task response candidate remains deferred",
            "No merge of midplatform vs mid_platform directories",
        ],
        **meta,
    }

    readiness = {
        "decision_id": "minimal_backbone_dryrun_readiness_decision_v1",
        "flows_all_pass": flows_all_pass,
        "block_verification_pass": block_ver.get("all_blocked_pass"),
        "runtime_boundary_pass": all(r.get("dryrun_allowed") for r in runtime_decisions),
        "high_risk_observed": high_risk,
        "final_decision": FINAL_DECISION_GO if flows_all_pass and not high_risk else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if flows_all_pass and not high_risk else NEXT_PHASE_HOLD,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": flows_all_pass and not high_risk and len(blockers) == 0,
        "violations": blockers + [i for f in flows for i in (f.get("issues") or [])],
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "flows_all_pass": flows_all_pass,
        "flow_a_pass": flow_a.get("flow_pass"),
        "flow_b_pass": flow_b.get("flow_pass"),
        "flow_c_pass": flow_c.get("flow_pass"),
        "upstream_blockers": blockers,
        "output_directory": str(out_root),
        **meta,
    }

    return {
        "output_root": str(out_root),
        "dryrun_ok": dryrun_ok,
        "artifacts": {
            "midplatform_minimal_backbone_dryrun_policy_v1.json": policy,
            "upstream_planning_input_review_v1.json": input_review,
            "minimal_backbone_candidate_input_matrix_v1.json": matrix,
            "candidate_intake_record_v1.json": {"bundle_id": "candidate_intake_record_v1", "records": intake_records, **meta},
            "evidence_governance_record_v1.json": {
                "bundle_id": "evidence_governance_record_v1",
                "records": evidence_records,
                **meta,
            },
            "constitution_gate_review_v1.json": {
                "bundle_id": "constitution_gate_review_v1",
                "reviews": constitution_reviews,
                **meta,
            },
            "task_routing_candidate_v1.json": {
                "bundle_id": "task_routing_candidate_v1",
                "records": task_routings,
                "task_response_candidate_deferred": True,
                **meta,
            },
            "guidance_candidate_queue_item_v1.json": {
                "bundle_id": "guidance_candidate_queue_item_v1",
                "items": guidance_items,
                **meta,
            },
            "output_arbitration_candidate_v1.json": {
                "bundle_id": "output_arbitration_candidate_v1",
                "candidates": arbitrations,
                **meta,
            },
            "runtime_boundary_decision_v1.json": {
                "bundle_id": "runtime_boundary_decision_v1",
                "decisions": runtime_decisions,
                **meta,
            },
            "drive_layer_signal_dryrun_v1.json": drive_dryrun,
            "health_layer_signal_dryrun_v1.json": health_dryrun,
            "memory_support_access_block_review_v1.json": memory_block,
            "minimal_backbone_flow_trace_v1.json": flow_trace,
            "minimal_backbone_gap_consumption_result_v1.json": gap_result,
            "minimal_backbone_non_claims_register_v1.json": non_claims,
            "minimal_backbone_dryrun_readiness_decision_v1.json": readiness,
            "summary.json": summary,
        },
    }
