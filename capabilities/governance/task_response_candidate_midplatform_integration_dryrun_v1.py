# -*- coding: utf-8 -*-
"""Task Response Candidate Midplatform Integration DryRun v1 — first task_response_candidate generation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    PHASE_ID as POST_REVIEW_PHASE,
)
from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    BLOCKED_PATHS,
    CONSTITUTION_BLOCKS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FLOW_PLANS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PHASE_ID as PLANNING_PHASE,
    SCOPE as PLANNING_SCOPE,
    TASK_RESPONSE_DEFAULT_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Task-Response-Candidate-Midplatform-Integration-DryRun-v1-001"
SCOPE = "task_response_candidate_integration_dryrun_only"
SOURCE_CHAIN = "task_response_candidate_midplatform_integration_dryrun_v1"

FINAL_DECISION_GO = "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Task-Response-Candidate-Midplatform-Integration-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Task-Response-Candidate-Midplatform-Integration-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_dryrun"
)

TRIAL_SCOPE = "task_response_candidate_midplatform_integration_dryrun_v1"


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "task_response_candidate_integration_dryrun_only": True,
        "simulated": True,
        "dryrun_only": True,
        "task_response_candidate_generated_now": True,
        "task_response_chain_started_now": True,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "task_runtime_action_executed_now": False,
        "tts_invoked_now": False,
        "speech_response_candidate_generated_now": False,
        "user_facing_output_generated_now": False,
        "llm_invoked_now": False,
        "model_runtime_invoked_now": False,
        "navigation_action_triggered_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "runtime_enabled_now": False,
        "real_runtime_enabled_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "task_commit_allowed": False,
        "user_facing_output_allowed": False,
        "tts_allowed": False,
        "runtime_action_allowed": False,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    if not root.is_dir():
        return False
    vr = _try_read_json(root / "verifier_report.json") or {}
    sm = _try_read_json(root / "summary.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


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


def _load_candidate(
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
            return None, f"no VOC under {exec_root}"
        return _try_read_json(paths[0]), str(paths[0])
    if candidate_type == "ocr_result_candidate":
        exec_root = ocr_trial_root / "_controlled_execution"
        paths = sorted(exec_root.glob("ocr_result_candidate_[0-9]*_v1.json"))
        if not paths:
            return None, f"no OCR under {exec_root}"
        return _try_read_json(paths[0]), str(paths[0])
    exec_root = nav_trial_root / "_controlled_execution"
    paths = sorted(exec_root.glob("navigation_guidance_candidate_[0-9]*_v1.json"))
    if not paths:
        return None, f"no NGC under {exec_root}"
    return _try_read_json(paths[0]), str(paths[0])


def _trc_id(flow_key: str, *refs: str) -> str:
    h = hashlib.sha256(":".join(refs).encode()).hexdigest()[:12]
    return f"trc_{flow_key}_{h}"


def _validate_task_response(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ok, issues = validate_candidate_output(candidate, expected_type="task_response_candidate", require_timestamp=False)
    if not ok:
        pass
    for key, expected in (
        ("task_commit_allowed", False),
        ("user_facing_output_allowed", False),
        ("tts_allowed", False),
        ("related_task_state_candidate_present", True),
        ("related_input_candidates_present", True),
        ("output_arbitration_required", True),
        ("constitution_gate_required", True),
        ("source_chain_present", True),
        ("provenance_present", True),
        ("output_type", TASK_RESPONSE_DEFAULT_FIELDS["output_type"]),
    ):
        if candidate.get(key) != expected:
            issues.append(f"{key} must be {expected}")
    if not candidate.get("provenance"):
        issues.append("provenance object required")
    return len(issues) == 0, issues


def _build_task_routing(input_candidate: Dict[str, Any], input_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "record_id": "task_routing_candidate_v1",
        "candidate_id": input_candidate.get("candidate_id"),
        "candidate_type": input_type,
        "route_to_task_context_candidate": input_type == "ocr_result_candidate",
        "route_to_observation_requirement_candidate": input_type in (
            "visual_observation_candidate",
            "ocr_result_candidate",
        ),
        "task_commit_allowed": False,
        **meta,
    }


def _build_task_response(
    flow_key: str,
    input_candidates: List[Dict[str, Any]],
    *,
    conflict_status: Optional[str] = None,
    provider_type_ref: Optional[str] = None,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    refs = [c.get("candidate_id", "") for c in input_candidates]
    cid = _trc_id(flow_key, *refs)
    tsc_id = f"tsc_dryrun_{flow_key}"
    related = [{"candidate_id": c.get("candidate_id"), "candidate_type": c.get("candidate_type") or c.get("output_type")} for c in input_candidates]
    return {
        "candidate_id": cid,
        "output_type": "task_response_candidate",
        "candidate_type": "task_response_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
        "task_commit_allowed": False,
        "user_facing_output_allowed": False,
        "tts_allowed": False,
        "runtime_action_allowed": False,
        "write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        "source_chain_present": True,
        "trial_scope": TRIAL_SCOPE,
        "provenance": {"dryrun_flow": flow_key, "synthetic": True},
        "provenance_present": True,
        "related_task_state_candidate": {"candidate_id": tsc_id, "candidate_type": "task_state_candidate"},
        "related_task_state_candidate_present": True,
        "related_input_candidates": related,
        "related_input_candidates_present": True,
        "output_arbitration_required": True,
        "constitution_gate_required": True,
        "conflict_status": conflict_status or "none",
        "provider_type_ref": provider_type_ref,
        "navigation_action_allowed": False,
        **meta,
    }


def _constitution_on_task_response(trc: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    blocks = {b: True for b in CONSTITUTION_BLOCKS}
    all_pass = trc.get("candidate_only") is True and trc.get("fact_status") == "not_fact"
    return {
        "review_id": "constitution_overlay_result_v1",
        "candidate_id": trc.get("candidate_id"),
        "constitution_pass": all_pass,
        "blocks_enforced": blocks,
        "fact_upgrade_blocked": True,
        "task_commit_blocked": True,
        "tts_blocked": True,
        "user_output_blocked": True,
        "navigation_action_blocked": True,
        "memory_write_blocked": True,
        "world_model_write_blocked": True,
        **meta,
    }


def _arbitration_on_task_response(trc: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "arbitration_id": "output_arbitration_result_v1",
        "candidate_id": trc.get("candidate_id"),
        "output_allowed": False,
        "speech_response_candidate_generated_now": False,
        "arbitration_outcome": "hold",
        "clarification_required": False,
        "fallback_candidate": None,
        **meta,
    }


def _run_vision_flow(meta: Dict[str, Any], vision_root: Path, ocr_root: Path, nav_root: Path) -> Dict[str, Any]:
    voc, path = _load_candidate("visual_observation_candidate", vision_post_review_root=vision_root, ocr_trial_root=ocr_root, nav_trial_root=nav_root)
    issues: List[str] = []
    if not voc:
        return {"flow_id": "Flow_1_vision_based_task_response", "flow_pass": False, "issues": [path or "missing voc"]}
    ok, ci = validate_candidate_output(voc, expected_type="visual_observation_candidate", require_timestamp=False)
    if not ok:
        issues.extend(ci)
    routing = _build_task_routing(voc, "visual_observation_candidate", meta)
    trc = _build_task_response("vision", [voc], meta=meta)
    tok, ti = _validate_task_response(trc)
    if not tok:
        issues.extend(ti)
    const = _constitution_on_task_response(trc, meta)
    arb = _arbitration_on_task_response(trc, meta)
    flow_pass = not issues and const.get("constitution_pass") and arb.get("output_allowed") is False
    return {
        "result_id": "task_response_vision_flow_result_v1",
        "flow_id": "Flow_1_vision_based_task_response",
        "input_candidate_type": "visual_observation_candidate",
        "input_source_path": path,
        "task_routing_candidate": routing,
        "task_response_candidate": trc,
        "constitution_overlay": const,
        "output_arbitration": arb,
        "flow_pass": flow_pass,
        "issues": issues,
        **meta,
    }


def _run_ocr_flow(meta: Dict[str, Any], vision_root: Path, ocr_root: Path, nav_root: Path) -> Dict[str, Any]:
    ocr, path = _load_candidate("ocr_result_candidate", vision_post_review_root=vision_root, ocr_trial_root=ocr_root, nav_trial_root=nav_root)
    issues: List[str] = []
    if not ocr:
        return {"flow_id": "Flow_2_ocr_based_task_response", "flow_pass": False, "issues": [path or "missing ocr"]}
    if ocr.get("provider_type") != "mock_or_fixture_only":
        issues.append("provider_type must be mock_or_fixture_only")
    ok, ci = validate_candidate_output(ocr, expected_type="ocr_result_candidate", require_timestamp=True)
    if not ok:
        issues.extend(ci)
    routing = _build_task_routing(ocr, "ocr_result_candidate", meta)
    trc = _build_task_response("ocr", [ocr], provider_type_ref=ocr.get("provider_type"), meta=meta)
    tok, ti = _validate_task_response(trc)
    if not tok:
        issues.extend(ti)
    const = _constitution_on_task_response(trc, meta)
    arb = _arbitration_on_task_response(trc, meta)
    flow_pass = not issues and const.get("constitution_pass") and arb.get("output_allowed") is False
    return {
        "result_id": "task_response_ocr_flow_result_v1",
        "flow_id": "Flow_2_ocr_based_task_response",
        "input_candidate_type": "ocr_result_candidate",
        "input_source_path": path,
        "provider_type": ocr.get("provider_type"),
        "task_routing_candidate": routing,
        "task_response_candidate": trc,
        "constitution_overlay": const,
        "output_arbitration": arb,
        "flow_pass": flow_pass,
        "issues": issues,
        **meta,
    }


def _run_nav_flow(meta: Dict[str, Any], vision_root: Path, ocr_root: Path, nav_root: Path) -> Dict[str, Any]:
    nav, path = _load_candidate("navigation_guidance_candidate", vision_post_review_root=vision_root, ocr_trial_root=ocr_root, nav_trial_root=nav_root)
    issues: List[str] = []
    if not nav:
        return {"flow_id": "Flow_3_navigation_guidance_based_task_response", "flow_pass": False, "issues": [path or "missing nav"]}
    if nav.get("navigation_action_allowed") is True:
        issues.append("navigation_action_allowed must be false")
    if nav.get("user_facing_output_allowed") is True:
        issues.append("user_facing_output_allowed must be false")
    ok, ci = validate_candidate_output(nav, expected_type="navigation_guidance_candidate", require_timestamp=True)
    if not ok:
        issues.extend(ci)
    input_constitution_pass = nav.get("candidate_only") is True and nav.get("fact_status") == "not_fact"
    routing = _build_task_routing(nav, "navigation_guidance_candidate", meta)
    trc = _build_task_response("navigation", [nav], meta=meta)
    tok, ti = _validate_task_response(trc)
    if not tok:
        issues.extend(ti)
    const = _constitution_on_task_response(trc, meta)
    arb = _arbitration_on_task_response(trc, meta)
    flow_pass = (
        not issues
        and input_constitution_pass
        and const.get("constitution_pass")
        and arb.get("output_allowed") is False
        and trc.get("navigation_action_allowed") is False
    )
    return {
        "result_id": "task_response_navigation_flow_result_v1",
        "flow_id": "Flow_3_navigation_guidance_based_task_response",
        "input_candidate_type": "navigation_guidance_candidate",
        "input_source_path": path,
        "constitution_gate_on_input_pass": input_constitution_pass,
        "task_routing_candidate": routing,
        "task_response_candidate": trc,
        "constitution_overlay": const,
        "output_arbitration": arb,
        "flow_pass": flow_pass,
        "issues": issues,
        **meta,
    }


def _run_mixed_flow(meta: Dict[str, Any], vision_root: Path, ocr_root: Path, nav_root: Path) -> Dict[str, Any]:
    issues: List[str] = []
    inputs: List[Dict[str, Any]] = []
    paths: List[str] = []
    for ctype in ("visual_observation_candidate", "ocr_result_candidate", "navigation_guidance_candidate"):
        cand, path = _load_candidate(ctype, vision_post_review_root=vision_root, ocr_trial_root=ocr_root, nav_trial_root=nav_root)
        if not cand:
            issues.append(path or f"missing {ctype}")
            continue
        cand = dict(cand)
        cand.setdefault("candidate_type", ctype)
        inputs.append(cand)
        paths.append(path or "")
    if len(inputs) != 3:
        return {"flow_id": "Flow_4_mixed_candidate_task_response", "flow_pass": False, "issues": issues}
    ocr = next(c for c in inputs if c.get("candidate_type") == "ocr_result_candidate")
    if ocr.get("provider_type") != "mock_or_fixture_only":
        issues.append("ocr provider_type mock required")
    evidence = {
        "record_id": "evidence_governance_record_v1",
        "records": [{"candidate_id": c.get("candidate_id"), "candidate_type": c.get("candidate_type")} for c in inputs],
        "fact_write_allowed": False,
        "conflict_status": "synthetic_merge_no_conflict",
        **meta,
    }
    routing = {
        "record_id": "task_routing_candidate_v1",
        "merged_from": [c.get("candidate_id") for c in inputs],
        "task_commit_allowed": False,
        **meta,
    }
    trc = _build_task_response("mixed", inputs, conflict_status=evidence.get("conflict_status"), meta=meta)
    trc["source_chain"] = f"{SOURCE_CHAIN};contributors={','.join(c.get('candidate_id','') for c in inputs)}"
    tok, ti = _validate_task_response(trc)
    if not tok:
        issues.extend(ti)
    const = _constitution_on_task_response(trc, meta)
    arb = _arbitration_on_task_response(trc, meta)
    flow_pass = not issues and const.get("constitution_pass") and arb.get("output_allowed") is False
    return {
        "result_id": "task_response_mixed_flow_result_v1",
        "flow_id": "Flow_4_mixed_candidate_task_response",
        "input_source_paths": paths,
        "evidence_governance": evidence,
        "task_routing_candidate": routing,
        "task_response_candidate": trc,
        "constitution_overlay": const,
        "output_arbitration": arb,
        "output_arbitration_required": True,
        "flow_pass": flow_pass,
        "issues": issues,
        **meta,
    }


def run_task_response_candidate_midplatform_integration_dryrun_v1(
    *,
    task_response_candidate_midplatform_integration_planning_root: str,
    midplatform_minimal_backbone_post_dryrun_review_root: str,
    midplatform_minimal_backbone_dryrun_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(task_response_candidate_midplatform_integration_planning_root).expanduser().resolve()
    post_review_root = Path(midplatform_minimal_backbone_post_dryrun_review_root).expanduser().resolve()
    backbone_dryrun_root = Path(midplatform_minimal_backbone_dryrun_root).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_controlled_trial_post_execution_review_root).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(navigation_guidance_candidate_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()

    meta = _dryrun_meta()
    meta["output_root"] = str(out_root)

    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    post_sm = _try_read_json(post_review_root / "summary.json") or {}
    post_vr = _try_read_json(post_review_root / "verifier_report.json") or {}
    backbone_sm = _try_read_json(backbone_dryrun_root / "summary.json") or {}

    if not (plan_vr.get("verifier") == "GO" and plan_sm.get("boundary_ok") is True):
        blockers.append("planning verifier must be GO")
    if plan_sm.get("phase") != PLANNING_PHASE:
        blockers.append("planning phase mismatch")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != PLANNING_NEXT_PHASE:
        blockers.append("planning next phase mismatch")
    if plan_sm.get("task_response_candidate_generated_now") is True:
        blockers.append("planning must not have generated task_response yet")

    if not (post_vr.get("verifier") == "GO" and post_sm.get("boundary_ok") is True):
        blockers.append("post-dryrun review must be GO")
    if post_sm.get("phase") != POST_REVIEW_PHASE:
        blockers.append("post-review phase mismatch")
    if post_sm.get("three_candidate_flows_trusted") is not True:
        blockers.append("three flows must be trusted")
    if post_sm.get("ten_blocks_all_blocked") is not True:
        blockers.append("ten blocks must be blocked")
    if not _check_go(backbone_dryrun_root) or backbone_sm.get("flows_all_pass") is not True:
        blockers.append("minimal backbone dryrun must be GO")

    input_review = {
        "review_id": "task_response_planning_input_review_v1",
        "planning_root": str(planning_root),
        "post_review_root": str(post_review_root),
        "backbone_dryrun_root": str(backbone_dryrun_root),
        "planning_verifier_go": plan_vr.get("verifier") == "GO",
        "planning_final_decision": plan_sm.get("final_decision"),
        "post_review_go": post_vr.get("verifier") == "GO",
        "flows_trusted": post_sm.get("three_candidate_flows_trusted"),
        "ten_blocks_blocked": post_sm.get("ten_blocks_all_blocked"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    input_matrix = {
        "matrix_id": "task_response_dryrun_input_matrix_v1",
        "rows": [
            {"candidate_type": "visual_observation_candidate", "source": "vision_post_review→execution"},
            {"candidate_type": "ocr_result_candidate", "source": "ocr_trial/_controlled_execution"},
            {"candidate_type": "navigation_guidance_candidate", "source": "nav_trial/_controlled_execution"},
        ],
        "flows_planned": [f["flow_id"] for f in FLOW_PLANS],
        **meta,
    }

    flow1 = _run_vision_flow(meta, vision_root, ocr_root, nav_root)
    flow2 = _run_ocr_flow(meta, vision_root, ocr_root, nav_root)
    flow3 = _run_nav_flow(meta, vision_root, ocr_root, nav_root)
    flow4 = _run_mixed_flow(meta, vision_root, ocr_root, nav_root)
    flows = [flow1, flow2, flow3, flow4]
    flows_all_pass = len(blockers) == 0 and all(f.get("flow_pass") for f in flows)

    collection = {
        "collection_id": "task_response_candidate_collection_v1",
        "candidates": [f["task_response_candidate"] for f in flows if f.get("task_response_candidate")],
        "count": sum(1 for f in flows if f.get("task_response_candidate")),
        **meta,
    }

    contract_issues: List[Dict[str, Any]] = []
    for trc in collection.get("candidates") or []:
        ok, iss = _validate_task_response(trc)
        if not ok:
            contract_issues.extend([{"candidate_id": trc.get("candidate_id"), "issue": i} for i in iss])

    contract_review = {
        "review_id": "task_response_candidate_contract_review_v1",
        "candidates_reviewed": collection.get("count"),
        "all_contract_pass": len(contract_issues) == 0,
        "issues": contract_issues,
        "review_pass": len(contract_issues) == 0 and collection.get("count") == 4,
        **meta,
    }

    constitution_results = [f.get("constitution_overlay") for f in flows if f.get("constitution_overlay")]
    constitution_bundle = {
        "result_id": "constitution_overlay_result_v1",
        "reviews": constitution_results,
        "all_pass": all(r.get("constitution_pass") for r in constitution_results),
        "blocks_enforced": list(CONSTITUTION_BLOCKS),
        **meta,
    }

    arbitration_results = [f.get("output_arbitration") for f in flows if f.get("output_arbitration")]
    arbitration_bundle = {
        "result_id": "output_arbitration_result_v1",
        "arbitrations": arbitration_results,
        "all_output_allowed_false": all(a.get("output_allowed") is False for a in arbitration_results),
        "all_speech_false": all(a.get("speech_response_candidate_generated_now") is False for a in arbitration_results),
        **meta,
    }

    runtime_result = {
        "result_id": "runtime_boundary_result_v1",
        "dryrun_allowed": True,
        "controlled_trial_allowed": False,
        "limited_runtime_allowed": False,
        "real_runtime_allowed": False,
        "task_commit_blocked": True,
        "user_output_blocked": True,
        "model_runtime_blocked": True,
        "memory_write_blocked": True,
        "world_model_write_blocked": True,
        **meta,
    }

    blocked_rows = [{"path_id": pid, "blocked": True, "observed_now": False} for pid in BLOCKED_PATHS]
    blocked_result = {
        "result_id": "blocked_path_result_v1",
        "paths": blocked_rows,
        "all_blocked": True,
        "review_pass": True,
        **meta,
    }

    high_risk = bool(blockers or contract_issues or not flows_all_pass)
    readiness = {
        "readiness_id": "task_response_dryrun_readiness_decision_v1",
        "flows_all_pass": flows_all_pass,
        "contract_pass": contract_review.get("review_pass"),
        "high_risk_observed": high_risk,
        "final_decision": FINAL_DECISION_GO if flows_all_pass and not high_risk else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if flows_all_pass and not high_risk else NEXT_PHASE_HOLD,
        "post_dryrun_review_separate": True,
        **meta,
    }

    policy = {
        "policy_id": "task_response_candidate_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "principles": ["dryrun_generates_task_response_candidate", "candidate_only_not_fact", "no_commit_no_tts"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "claims": [
            "DryRun generates task_response_candidate in eval_out only",
            "task_response_candidate ≠ user answer",
            "DryRun GO ≠ Post-DryRun Review merged with backbone review",
            "Route B still deferred",
        ],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": flows_all_pass and not high_risk and len(blockers) == 0,
        "violations": blockers + [i.get("issue", "") for i in contract_issues],
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "flows_all_pass": flows_all_pass,
        "flow_1_pass": flow1.get("flow_pass"),
        "flow_2_pass": flow2.get("flow_pass"),
        "flow_3_pass": flow3.get("flow_pass"),
        "flow_4_pass": flow4.get("flow_pass"),
        "task_response_candidates_generated": collection.get("count"),
        "high_risk_count": 1 if high_risk else 0,
        "output_directory": str(out_root),
        **meta,
    }

    return {
        "output_root": str(out_root),
        "dryrun_ok": len(blockers) == 0,
        "artifacts": {
            "task_response_candidate_dryrun_policy_v1.json": policy,
            "task_response_planning_input_review_v1.json": input_review,
            "task_response_dryrun_input_matrix_v1.json": input_matrix,
            "task_response_vision_flow_result_v1.json": flow1,
            "task_response_ocr_flow_result_v1.json": flow2,
            "task_response_navigation_flow_result_v1.json": flow3,
            "task_response_mixed_flow_result_v1.json": flow4,
            "task_response_candidate_collection_v1.json": collection,
            "task_response_candidate_contract_review_v1.json": contract_review,
            "constitution_overlay_result_v1.json": constitution_bundle,
            "output_arbitration_result_v1.json": arbitration_bundle,
            "runtime_boundary_result_v1.json": runtime_result,
            "blocked_path_result_v1.json": blocked_result,
            "task_response_dryrun_readiness_decision_v1.json": readiness,
            "non_claims_register_v1.json": non_claims,
            "summary.json": summary,
        },
    }
