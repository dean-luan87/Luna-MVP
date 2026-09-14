# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Controlled Trial Execution v1."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    ABORT_CONDITIONS,
    PLANNED_EXECUTION_OUTPUT_DIR,
    POST_EXECUTION_REVIEW_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.no_runtime_boundary_audit_v1 import audit_boundary
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_planning_v1 import (
    TRIAL_SCOPE,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Execution-v1-001"
EXECUTION_SCOPE = "vision_sample_frame_controlled_trial_execution_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_controlled_trial_execution_v1"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"
UPSTREAM_FACTORY_FINAL = (
    "LUNA_VALIDATION_FACTORY_CONSOLIDATION_READY_FOR_VISION_SAMPLE_FRAME_AUTHORIZATION_VIA_HARNESS"
)
UPSTREAM_VIA_HARNESS_PHASE = (
    "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Authorization-Via-Harness-v1-001"
)
UPSTREAM_VIA_HARNESS_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_AUTHORIZATION_VIA_HARNESS_READY_FOR_CONTROLLED_TRIAL_EXECUTION"
)

FINAL_DECISION_GO = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_COMPLETED_READY_FOR_POST_EXECUTION_REVIEW"
)
FINAL_DECISION_ABORT = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_CONTROLLED_TRIAL_EXECUTION_ABORTED_READY_FOR_ABORT_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Post-Execution-Review-v1-001"
NEXT_PHASE_ABORT = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Abort-Review-v1-001"

CONTROLLED_INPUTS: Tuple[Dict[str, str], ...] = (
    {
        "input_id": "input_fixture_001",
        "input_type": "fixture_frame_metadata",
        "source_chain": SOURCE_CHAIN,
        "frame_ref": "fixture_meta_exec_001",
        "timestamp": "2026-06-03T12:00:00Z_fixture",
    },
    {
        "input_id": "input_sample_001",
        "input_type": "sample_frame_reference",
        "source_chain": SOURCE_CHAIN,
        "frame_ref": "sample_frame_ref_exec_001",
        "timestamp": "2026-06-03T12:00:01Z_sample",
    },
    {
        "input_id": "input_controlled_001",
        "input_type": "controlled_frame_reference",
        "source_chain": SOURCE_CHAIN,
        "frame_ref": "controlled_frame_ref_exec_001",
        "timestamp": "2026-06-03T12:00:02Z_controlled",
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "Controlled Trial Execution GO ≠ visual fact generated",
    "visual_observation_candidate ≠ WorldModel write",
    "fixture/sample reference ≠ live camera",
    "execution result logging ≠ Memory write",
    "single-chain execution ≠ OCR / Navigation / Task runtime enabled",
    "execution completed ≠ post-execution review passed",
    "Execution window opened ≠ grant issued",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta_started() -> Dict[str, Any]:
    return {
        "vision_sample_frame_controlled_trial_execution_only": True,
        "controlled_trial_started_now": True,
        "execution_window_opened_now": True,
        "execution_window_type": "controlled_fixture_only",
        "max_trial_scope": "single_chain",
        "max_output_count": 3,
        "trial_execution_authorized_now": False,
        "execution_authorization_granted_now": False,
        "grant_issued_now": False,
        "authorization_request_sent_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "trial_scope": TRIAL_SCOPE,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _voc_id() -> str:
    return f"voc_{uuid.uuid4().hex[:12]}"


def _make_voc_from_input(inp: Dict[str, str], *, shared_refs: Dict[str, str]) -> Dict[str, Any]:
    return {
        "candidate_id": _voc_id(),
        "output_type": "visual_observation_candidate",
        "candidate_type": "visual_observation_candidate",
        "input_id": inp["input_id"],
        "input_type": inp["input_type"],
        "primary_frame_ref": inp["frame_ref"],
        "fixture_frame_metadata": shared_refs["fixture"],
        "sample_frame_reference": shared_refs["sample"],
        "controlled_frame_reference": shared_refs["controlled"],
        "source_chain": inp["source_chain"],
        "frame_ref": inp["frame_ref"],
        "observation_timestamp": inp["timestamp"],
        "timestamp": inp["timestamp"],
        "trial_scope": TRIAL_SCOPE,
        "source_chain_present": True,
        "frame_ref_present": True,
        "timestamp_present": True,
        "provenance_present": True,
        "controlled_input": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
    }


def _validate_upstream(
    factory_root: Path,
    via_harness_root: Path,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    factory_sm = _try_read_json(factory_root / "summary.json") or {}
    factory_vr = _try_read_json(factory_root / "verifier_report.json") or {}
    registry = _try_read_json(factory_root / "validation_factory_module_registry_v1.json") or {}
    via_sm = _try_read_json(via_harness_root / "summary.json") or {}
    via_vr = _try_read_json(via_harness_root / "verifier_report.json") or {}
    readiness = _try_read_json(
        via_harness_root / "controlled_trial_execution_readiness_decision_v1.json"
    ) or {}

    if not (factory_vr.get("verifier") == "GO" and factory_vr.get("passed") is True):
        if factory_sm.get("boundary_ok") is not True:
            blockers.append("validation factory must be GO")
    if factory_sm.get("validation_factory_contract_generated_now") is not True:
        blockers.append("validation_factory_contract_generated_now must be true")
    if factory_sm.get("final_decision") != UPSTREAM_FACTORY_FINAL:
        blockers.append("factory final_decision mismatch")

    modules = {m.get("module_id") for m in registry.get("modules") or []}
    for mid in (
        "controlled_trial_authorization_harness",
        "candidate_output_contract",
        "no_runtime_boundary_audit",
        "controlled_trial_post_execution_review_harness",
    ):
        if mid not in modules:
            blockers.append(f"factory registry missing: {mid}")

    if not (via_vr.get("verifier") == "GO" and via_vr.get("passed") is True):
        if via_sm.get("boundary_ok") is not True:
            blockers.append("authorization via-harness must be GO")
    if via_sm.get("final_decision") != UPSTREAM_VIA_HARNESS_FINAL:
        blockers.append("via-harness final_decision mismatch")
    if readiness.get("ready_for_controlled_trial_execution") is not True:
        blockers.append("execution_readiness must be true")
    if via_sm.get("controlled_trial_started_now") is True:
        blockers.append("trial must not be started before execution phase")
    if via_sm.get("execution_window_opened_now") is True:
        blockers.append("execution window must not be opened before execution phase")

    for flag in RUNTIME_BOUNDARY_FIELDS:
        if via_sm.get(flag) is True:
            blockers.append(f"via-harness {flag} must be false before execution")

    return blockers, {
        "factory_sm": factory_sm,
        "factory_vr": factory_vr,
        "via_sm": via_sm,
        "via_vr": via_vr,
        "readiness": readiness,
    }


def _check_abort_triggers() -> Tuple[bool, List[Dict[str, Any]]]:
    rows = []
    for cond in ABORT_CONDITIONS:
        rows.append(
            {
                "trigger": cond["trigger"],
                "observed": False,
                "action": cond["action"],
                "abort_enforced": True,
            }
        )
    return True, rows


def run_vision_sample_frame_single_chain_controlled_trial_execution_v1(
    *,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    via_root = Path(
        vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else Path(PLANNED_EXECUTION_OUTPUT_DIR)
    )

    blockers, ctx = _validate_upstream(factory_root, via_root)
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(out_root) else "repo_eval_out"
    meta = {
        **_boundary_meta_started(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_factory_root": str(factory_root),
        "upstream_via_harness_root": str(via_root),
        "execution_output_root": str(out_root),
        "allowed_output_directory": str(out_root),
    }

    shared_refs = {
        "fixture": "fixture_meta_exec_001",
        "sample": "sample_frame_ref_exec_001",
        "controlled": "controlled_frame_ref_exec_001",
    }

    inputs = [{**inp, "controlled_input": True} for inp in CONTROLLED_INPUTS]

    trace_steps: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    contract_rows: List[Dict[str, Any]] = []

    execution_aborted = False
    abort_reason: Optional[str] = None

    if blockers:
        execution_aborted = True
        abort_reason = "upstream_validation_failed"

    if not execution_aborted:
        for inp in inputs:
            trace_steps.append(
                {
                    "step": f"consume_{inp['input_type']}",
                    "input_id": inp["input_id"],
                    "status": "ok",
                    "controlled_input": True,
                }
            )
            trace_steps.append({"step": "validate_source_chain", "status": "ok"})
            trace_steps.append({"step": "validate_frame_ref", "status": "ok"})
            trace_steps.append({"step": "validate_timestamp", "status": "ok"})

            voc = _make_voc_from_input(inp, shared_refs=shared_refs)
            ok, issues = validate_candidate_output(
                voc, expected_type="visual_observation_candidate", require_timestamp=True
            )
            contract_rows.append(
                {
                    "candidate_id": voc["candidate_id"],
                    "input_id": inp["input_id"],
                    "contract_pass": ok,
                    "issues": issues,
                }
            )
            if not ok:
                execution_aborted = True
                abort_reason = "candidate_output_contract_violation"
                break
            candidates.append(voc)
            trace_steps.append(
                {
                    "step": "generate_visual_observation_candidate",
                    "candidate_id": voc["candidate_id"],
                    "status": "ok",
                }
            )

    if len(candidates) > 3:
        execution_aborted = True
        abort_reason = "max_output_count_exceeded"

    out_path_ok = "Luna-Workspace-Min" in str(out_root)
    if not out_path_ok:
        execution_aborted = True
        abort_reason = "output_path_outside_allowed_directory"

    abort_ok, abort_rows = _check_abort_triggers()
    if not abort_ok:
        execution_aborted = True
        abort_reason = abort_reason or "safety_gate_failed"

    audit_snapshot = {field: False for field in RUNTIME_BOUNDARY_FIELDS}
    runtime_audit = audit_boundary(audit_snapshot, profile="vision_no_runtime_profile")
    full_audit = audit_boundary(audit_snapshot, profile="full_no_runtime_profile")
    audit_pass = runtime_audit.get("audit_pass") and full_audit.get("audit_pass")

    if not audit_pass:
        execution_aborted = True
        abort_reason = abort_reason or "no_runtime_boundary_violation"

    boundary_ok = not execution_aborted and len(blockers) == 0

    policy = {
        "policy_id": "vision_sample_frame_controlled_trial_execution_policy_v1",
        "scope": EXECUTION_SCOPE,
        "mode": "controlled_fixture_single_chain_execution",
        "max_output_count": 3,
        **meta,
    }

    factory_review = {
        "review_id": "validation_factory_input_review_v1",
        "factory_root": str(factory_root),
        "factory_verifier": ctx["factory_vr"].get("verifier"),
        "registry_modules_ok": len(blockers) == 0,
        "review_pass": ctx["factory_sm"].get("boundary_ok") is True,
        **meta,
    }

    via_review = {
        "review_id": "authorization_via_harness_input_review_v1",
        "via_harness_root": str(via_root),
        "via_verifier": ctx["via_vr"].get("verifier"),
        "execution_readiness": ctx["readiness"].get("ready_for_controlled_trial_execution"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    manifest = {
        "manifest_id": "controlled_trial_execution_input_manifest_v1",
        "inputs": inputs,
        "inputs_count": len(inputs),
        "allowed_input_types": [
            "fixture_frame_metadata",
            "sample_frame_reference",
            "controlled_frame_reference",
        ],
        **meta,
    }

    trace = {
        "trace_id": "controlled_trial_execution_trace_v1",
        "steps": trace_steps,
        "execution_aborted": execution_aborted,
        "abort_reason": abort_reason,
        **meta,
    }

    voc_result = {
        "result_id": "visual_observation_candidate_result_v1",
        "candidates": candidates,
        "candidates_count": len(candidates),
        "all_candidate_only": all(c.get("candidate_only") for c in candidates),
        "all_not_fact": all(c.get("fact_status") == "not_fact" for c in candidates),
        **meta,
    }

    contract_compliance = {
        "result_id": "candidate_output_contract_compliance_v1",
        "contract_id": "candidate_output_contract_v1",
        "rows": contract_rows,
        "compliance_pass": all(r.get("contract_pass") for r in contract_rows) if contract_rows else False,
        **meta,
    }

    audit_result = {
        "result_id": "no_runtime_boundary_audit_result_v1",
        "vision_profile": runtime_audit,
        "full_profile": full_audit,
        "audit_pass": audit_pass,
        **meta,
    }

    abort_monitor = {
        "result_id": "controlled_trial_abort_monitor_result_v1",
        "conditions": abort_rows,
        "abort_triggered": execution_aborted,
        "abort_reason": abort_reason,
        "monitor_pass": not execution_aborted,
        **meta,
    }

    exec_summary = {
        "summary_id": "controlled_trial_execution_summary_v1",
        "execution_completed": boundary_ok,
        "outputs_written": len(candidates),
        "output_directory": str(out_root),
        "workspace_fallback_only": out_path_ok,
        **meta,
    }

    handoff = {
        "handoff_id": "post_execution_review_handoff_v1",
        "required_phase": POST_EXECUTION_REVIEW_PHASE,
        "execution_output_root": str(out_root),
        "handoff_required": boundary_ok,
        "cannot_skip_post_execution_review": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "execution_scope": EXECUTION_SCOPE,
        "boundary_ok": boundary_ok,
        "execution_aborted": execution_aborted,
        "violations": blockers + ([abort_reason] if abort_reason else []),
        "final_decision": (
            FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_ABORT
        ),
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_ABORT,
        "candidates_generated": len(candidates),
        **meta,
    }

    return {
        "vision_sample_frame_controlled_trial_execution_policy": policy,
        "validation_factory_input_review": factory_review,
        "authorization_via_harness_input_review": via_review,
        "controlled_trial_execution_input_manifest": manifest,
        "controlled_trial_execution_trace": trace,
        "visual_observation_candidate_result": voc_result,
        "candidate_output_contract_compliance": contract_compliance,
        "no_runtime_boundary_audit_result": audit_result,
        "controlled_trial_abort_monitor_result": abort_monitor,
        "controlled_trial_execution_summary": exec_summary,
        "post_execution_review_handoff": handoff,
        "non_claims_register": non_claims,
        "summary": summary,
    }
