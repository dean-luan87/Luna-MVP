# -*- coding: utf-8 -*-
"""Navigation Guidance Candidate Single-Chain Trial Via Validation Factory v1."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    HARNESS_ID as AUTH_HARNESS_ID,
    build_navigation_guidance_authorization_config,
    run_authorization_validate,
)
from capabilities.governance.controlled_trial_post_execution_review_harness_v1 import (
    HARNESS_ID as POST_REVIEW_HARNESS_ID,
    review_controlled_trial_execution,
)
from capabilities.governance.luna_validation_factory_v1 import (
    FACTORY_ID,
    MODULE_REGISTRY,
    STANDARD_FEATURE_FLOW,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.no_runtime_boundary_audit_v1 import audit_boundary
from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as OCR_UPSTREAM_FINAL,
    PHASE_ID as OCR_UPSTREAM_PHASE,
)
from capabilities.governance.single_chain_trial_validation_harness_v1 import (
    HARNESS_ID as SINGLE_CHAIN_HARNESS_ID,
    build_navigation_guidance_candidate_chain_config,
    run_single_chain_trial_plan_and_dryrun,
)

PHASE_ID = "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Via-Validation-Factory-v1-001"
SCOPE = "navigation_guidance_single_chain_trial_via_validation_factory_only"
SOURCE_CHAIN = "navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1"
TRIAL_SCOPE = "navigation_guidance_candidate_single_chain"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"

FINAL_DECISION_GO = (
    "NAVIGATION_GUIDANCE_CANDIDATE_SINGLE_CHAIN_TRIAL_CLOSED_READY_FOR_TASK_RESPONSE_CANDIDATE_SINGLE_CHAIN_TRIAL"
)
FINAL_DECISION_HOLD = "NAVIGATION_GUIDANCE_CANDIDATE_SINGLE_CHAIN_TRIAL_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Task-Response-Candidate-Single-Chain-Trial-Via-Validation-Factory-v1-001"
NEXT_PHASE_HOLD = "Phase-Navigation-Guidance-Candidate-Single-Chain-Trial-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "navigation_guidance_candidate_single_chain_trial_via_validation_factory"
)

NAV_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "visual_fact_generated_now",
    "real_navigation_runtime_enabled_now",
    "navigation_action_triggered_now",
    "map_write_executed_now",
    "gps_strong_anchor_committed_now",
    "route_commit_executed_now",
    "task_state_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "live_camera_enabled_now",
    "ocr_provider_invoked_now",
    "vision_model_invoked_now",
)

CONTROLLED_INPUTS: Tuple[Dict[str, str], ...] = (
    {
        "input_id": "input_synthetic_route_001",
        "input_type": "synthetic_route_context",
        "source_chain": SOURCE_CHAIN,
        "timestamp": "2026-06-03T16:00:00Z_synthetic",
    },
    {
        "input_id": "input_readonly_map_001",
        "input_type": "readonly_map_hint",
        "source_chain": SOURCE_CHAIN,
        "timestamp": "2026-06-03T16:00:01Z_map_hint",
    },
    {
        "input_id": "input_voc_ref_001",
        "input_type": "visual_observation_candidate_reference",
        "source_chain": SOURCE_CHAIN,
        "timestamp": "2026-06-03T16:00:02Z_voc_ref",
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "Navigation guidance trial closure ≠ navigation action executed",
    "navigation_guidance_candidate closure ≠ user-facing TTS/output",
    "readonly/synthetic map context ≠ map write allowed",
    "candidate closure ≠ GPS strong anchor committed",
    "Validation Factory reuse ≠ skip Post-Execution Review",
    "trial closed ≠ task response chain started",
    "guidance candidate ≠ route commit executed",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta(*, trial_started: bool = False, window_opened: bool = False) -> Dict[str, Any]:
    base = {
        "navigation_guidance_single_chain_trial_via_validation_factory_only": True,
        "validation_factory_reused": True,
        "controlled_trial_started_now": trial_started,
        "execution_window_opened_now": window_opened,
        "execution_window_type": "controlled_fixture_only" if window_opened else None,
        "max_trial_scope": "single_chain",
        "max_output_count": 3,
        "grant_issued_now": False,
        "trial_execution_authorized_now": False,
        "runtime_enabled_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "trial_scope": TRIAL_SCOPE,
        "factory_id": FACTORY_ID,
        "standard_feature_flow": list(STANDARD_FEATURE_FLOW),
        **_not_fact(),
    }
    for field in NAV_BOUNDARY_FIELDS:
        base[field] = False
    return base


def _ngc_id() -> str:
    return f"ngc_{uuid.uuid4().hex[:12]}"


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_upstream(ocr_root: Path, factory_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    osm = _try_read_json(ocr_root / "summary.json") or {}
    ovr = _try_read_json(ocr_root / "verifier_report.json") or {}
    fsm = _try_read_json(factory_root / "summary.json") or {}
    fvr = _try_read_json(factory_root / "verifier_report.json") or {}
    registry = _try_read_json(factory_root / "validation_factory_module_registry_v1.json") or {}

    if not (ovr.get("verifier") == "GO" and ovr.get("passed") is True):
        if osm.get("boundary_ok") is not True:
            blockers.append("OCR mock trial verifier must be GO")
    if osm.get("phase") != OCR_UPSTREAM_PHASE:
        blockers.append("upstream must be OCR mock trial phase")
    if osm.get("final_decision") != OCR_UPSTREAM_FINAL:
        blockers.append("OCR mock final_decision mismatch")
    if osm.get("controlled_trial_closed_now") is not True:
        blockers.append("OCR controlled_trial_closed_now must be true")

    if not (fvr.get("verifier") == "GO" and fvr.get("passed") is True):
        if fsm.get("boundary_ok") is not True:
            blockers.append("validation factory verifier must be GO")
    if fsm.get("phase") != UPSTREAM_FACTORY_PHASE:
        blockers.append("validation factory phase mismatch")

    modules = {m.get("module_id") for m in registry.get("modules") or MODULE_REGISTRY}
    for required in (
        "single_chain_trial_validation_harness",
        "controlled_trial_authorization_harness",
        "candidate_output_contract",
        "no_runtime_boundary_audit",
        "controlled_trial_post_execution_review_harness",
    ):
        if required not in modules:
            blockers.append(f"factory module missing: {required}")

    return blockers, {"ocr_sm": osm, "factory_sm": fsm}


def _make_navigation_candidate(inp: Dict[str, str], *, refs: Dict[str, str]) -> Dict[str, Any]:
    return {
        "candidate_id": _ngc_id(),
        "output_type": "navigation_guidance_candidate",
        "candidate_type": "navigation_guidance_candidate",
        "input_id": inp["input_id"],
        "input_type": inp["input_type"],
        "source_chain": inp["source_chain"],
        "timestamp": inp["timestamp"],
        "observation_timestamp": inp["timestamp"],
        "trial_scope": TRIAL_SCOPE,
        "source_chain_present": True,
        "provenance_present": True,
        "map_context_type": "readonly_or_synthetic_only",
        "user_facing_output_allowed": False,
        "navigation_action_allowed": False,
        "synthetic_route_context": refs.get("synthetic_route_context"),
        "readonly_map_hint": refs.get("readonly_map_hint"),
        "visual_observation_candidate_reference": refs.get("visual_observation_candidate_reference"),
        "task_context_fixture": refs.get("task_context_fixture"),
        "controlled_input": True,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "guidance_text": "synthetic_guidance_not_user_facing",
    }


def _validate_navigation_candidate(c: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ok, issues = validate_candidate_output(
        c, expected_type="navigation_guidance_candidate", require_timestamp=True
    )
    extra = all(
        [
            c.get("navigation_action_allowed") is False,
            c.get("user_facing_output_allowed") is False,
            c.get("map_context_type") == "readonly_or_synthetic_only",
            c.get("provenance_present") is True,
        ]
    )
    return ok and extra, issues


def _write_execution_artifacts(
    exec_root: Path,
    *,
    candidates: List[Dict[str, Any]],
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    exec_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "manifest_id": "controlled_trial_execution_input_manifest_v1",
        "inputs": list(CONTROLLED_INPUTS),
        "inputs_count": 3,
        **meta,
    }
    trace = {
        "trace_id": "controlled_trial_execution_trace_v1",
        "steps": [
            {"step": i + 1, "input_id": inp["input_id"], "output": c["candidate_id"]}
            for i, (inp, c) in enumerate(zip(CONTROLLED_INPUTS, candidates))
        ],
        **meta,
    }
    bundle = {
        "result_id": "navigation_guidance_candidate_result_v1",
        "candidates": candidates,
        "candidates_count": len(candidates),
        **meta,
    }
    contract_rows = []
    all_pass = True
    for c in candidates:
        row_ok, issues = _validate_navigation_candidate(c)
        if not row_ok:
            all_pass = False
        contract_rows.append({"candidate_id": c["candidate_id"], "contract_pass": row_ok, "issues": issues})

    audit_snapshot = {f: False for f in NAV_BOUNDARY_FIELDS}
    nav_audit = audit_boundary(audit_snapshot, profile="navigation_no_runtime_profile")
    wm_audit = audit_boundary(audit_snapshot, profile="memory_worldmodel_no_write_profile")

    abort = {
        "monitor_id": "controlled_trial_abort_monitor_result_v1",
        "abort_triggered": False,
        "monitor_pass": True,
        **meta,
    }
    contract_comp = {
        "compliance_id": "candidate_output_contract_compliance_v1",
        "compliance_pass": all_pass,
        "rows": contract_rows,
        **meta,
    }
    exec_summary = {
        "summary_id": "controlled_trial_execution_summary_v1",
        "output_directory": str(exec_root),
        "execution_output_root": str(exec_root),
        "workspace_fallback_only": True,
        "candidates_generated": len(candidates),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "execution_scope": "navigation_guidance_controlled_execution_embedded",
        "boundary_ok": all_pass and nav_audit.get("audit_pass") and wm_audit.get("audit_pass"),
        "execution_aborted": False,
        "candidates_generated": len(candidates),
        "execution_output_root": str(exec_root),
        **meta,
        **audit_snapshot,
    }

    files = {
        "controlled_trial_execution_input_manifest_v1.json": manifest,
        "controlled_trial_execution_trace_v1.json": trace,
        "navigation_guidance_candidate_result_v1.json": bundle,
        "controlled_trial_abort_monitor_result_v1.json": abort,
        "candidate_output_contract_compliance_v1.json": contract_comp,
        "controlled_trial_execution_summary_v1.json": exec_summary,
        "summary.json": summary,
    }
    for fname, payload in files.items():
        (exec_root / fname).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    for i, c in enumerate(candidates, 1):
        (exec_root / f"navigation_guidance_candidate_{i}_v1.json").write_text(
            json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return {
        "execution_root": str(exec_root),
        "candidates": candidates,
        "contract_pass": all_pass,
        "navigation_audit": nav_audit,
        "summary": summary,
        "abort_triggered": False,
    }


def run_navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1(
    *,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    luna_validation_factory_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    exec_root = out_root / "_controlled_execution"

    upstream_blockers, _ctx = _validate_upstream(ocr_root, factory_root)
    meta_review = _boundary_meta()
    chain_config = build_navigation_guidance_candidate_chain_config(source_chain=SOURCE_CHAIN)

    chain_bundle = run_single_chain_trial_plan_and_dryrun(
        chain_config=chain_config,
        boundary_meta=meta_review,
        upstream_blockers=upstream_blockers,
        policy_id="navigation_guidance_chain_validation_policy_v1",
        scope_label=SCOPE,
    )
    chain_pass = chain_bundle["summary"].get("boundary_ok") is True and len(upstream_blockers) == 0

    auth_meta = _boundary_meta()
    auth_config = build_navigation_guidance_authorization_config(
        source_validation_phase=PHASE_ID,
        output_directory=str(exec_root),
    )
    auth_bundle = run_authorization_validate(
        auth_config,
        boundary_meta=auth_meta,
        upstream_blockers=upstream_blockers if not chain_pass else [],
    )
    auth_pass = auth_bundle.get("validation_pass") is True and chain_pass

    exec_meta = _boundary_meta(trial_started=True, window_opened=True)
    exec_meta["harness_ids"] = {
        "single_chain": SINGLE_CHAIN_HARNESS_ID,
        "authorization": AUTH_HARNESS_ID,
        "post_review": POST_REVIEW_HARNESS_ID,
    }
    refs = {
        "synthetic_route_context": "synthetic_route_exec_001",
        "readonly_map_hint": "readonly_map_hint_exec_001",
        "visual_observation_candidate_reference": "voc_ref_nav_exec_001",
        "task_context_fixture": "task_ctx_fixture_exec_001",
    }
    candidates = [_make_navigation_candidate(inp, refs=refs) for inp in CONTROLLED_INPUTS]
    exec_result = _write_execution_artifacts(exec_root, candidates=candidates, meta=exec_meta)
    exec_pass = exec_result["contract_pass"] and exec_result["summary"].get("boundary_ok") is True

    review_bundle = review_controlled_trial_execution(
        exec_root,
        trial_scope=TRIAL_SCOPE,
        expected_candidate_type="navigation_guidance_candidate",
        candidate_file_prefix="navigation_guidance_candidate",
        allowed_logging_root=str(exec_root),
        extra_boundary_fields=NAV_BOUNDARY_FIELDS,
        require_controlled_input=True,
        require_frame_ref=False,
    )
    post_pass = review_bundle["harness_result"].get("review_pass") is True

    boundary_ok = chain_pass and auth_pass and exec_pass and post_pass and len(upstream_blockers) == 0
    blockers = list(upstream_blockers)
    if not chain_pass:
        blockers.append("chain validation failed")
    if not auth_pass:
        blockers.append("authorization validation failed")
    if not exec_pass:
        blockers.append("controlled execution failed")
    if not post_pass:
        blockers.extend(review_bundle["harness_result"].get("blockers", []))

    closure_meta = _boundary_meta()
    closure_meta["controlled_trial_closed_now"] = boundary_ok
    closure_meta["post_execution_review_passed_now"] = post_pass

    return {
        "navigation_guidance_chain_config": {**chain_config, **closure_meta},
        "navigation_guidance_chain_validation_result": {
            "artifact_id": "navigation_guidance_chain_validation_result_v1",
            "harness_id": SINGLE_CHAIN_HARNESS_ID,
            "validation_pass": chain_pass,
            "summary": chain_bundle["summary"],
            "readiness": chain_bundle["readiness"],
            **closure_meta,
        },
        "navigation_guidance_authorization_config": {**auth_config, **closure_meta},
        "navigation_guidance_authorization_validation_result": {
            "artifact_id": "navigation_guidance_authorization_validation_result_v1",
            "harness_id": AUTH_HARNESS_ID,
            "validation_pass": auth_pass,
            **auth_bundle["authorization_validation_result"],
            **closure_meta,
        },
        "navigation_guidance_controlled_trial_execution_result": {
            "artifact_id": "navigation_guidance_controlled_trial_execution_result_v1",
            "execution_root": str(exec_root),
            "execution_pass": exec_pass,
            "output_count": len(candidates),
            "abort_triggered": False,
            **exec_result,
            **closure_meta,
        },
        "navigation_guidance_post_execution_review_result": {
            "artifact_id": "navigation_guidance_post_execution_review_result_v1",
            "harness_id": POST_REVIEW_HARNESS_ID,
            "review_pass": post_pass,
            **review_bundle["harness_result"],
            **closure_meta,
        },
        "navigation_guidance_candidate_output_contract_review": {
            "review_id": "navigation_guidance_candidate_output_contract_review_v1",
            **review_bundle["candidate_contract"],
            **closure_meta,
        },
        "navigation_guidance_no_runtime_boundary_audit": {
            "review_id": "navigation_guidance_no_runtime_boundary_audit_v1",
            "execution_audit": exec_result["navigation_audit"],
            **review_bundle["no_runtime"],
            "boundary_snapshot": {f: False for f in NAV_BOUNDARY_FIELDS},
            **closure_meta,
        },
        "navigation_guidance_trial_closure_decision": {
            "decision_id": "navigation_guidance_trial_closure_decision_v1",
            "trial_id": "navigation_guidance_controlled",
            "chain_id": "navigation_guidance_candidate_single_chain",
            "navigation_guidance_single_chain_trial_closed": boundary_ok,
            "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
            "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
            "boundary_ok": boundary_ok,
            "blockers": blockers,
            **closure_meta,
        },
        "non_claims_register": {
            "register_id": "non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **closure_meta,
        },
        "summary": {
            "phase": PHASE_ID,
            "scope": SCOPE,
            "boundary_ok": boundary_ok,
            "violations": blockers,
            "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
            "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
            "chain_validation_pass": chain_pass,
            "authorization_validation_pass": auth_pass,
            "execution_pass": exec_pass,
            "post_execution_review_pass": post_pass,
            "output_count": len(candidates),
            "upstream_ocr_trial_root": str(ocr_root),
            "upstream_factory_root": str(factory_root),
            **closure_meta,
        },
    }
