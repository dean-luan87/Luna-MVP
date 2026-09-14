# -*- coding: utf-8 -*-
"""Single-Chain Trial Validation Harness Validation Closure v1.

Compresses harness extraction dry-run + post-review into one closure phase.
"""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.single_chain_trial_validation_harness_v1 import (
    ANTI_RECURSION_RULES,
    HARNESS_ID,
    build_vision_sample_frame_chain_config,
    run_single_chain_trial_plan_and_dryrun,
    validate_limited_runtime_post_dryrun_review,
)

PHASE_ID = "Phase-Single-Chain-Trial-Validation-Harness-Extraction-Validation-Closure-v1-001"
CLOSURE_SCOPE = "single_chain_trial_validation_harness_validation_closure_only"
SOURCE_CHAIN = "single_chain_trial_validation_harness_validation_closure_v1"

UPSTREAM_EXTRACTION_PHASE = "Phase-Single-Chain-Trial-Validation-Harness-Extraction-Planning-v1-001"
UPSTREAM_EXTRACTION_FINAL = "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN"

UPSTREAM_VISION_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-PlanAndDryRun-v1-001"
UPSTREAM_VISION_FINAL = (
    "VISION_SAMPLE_FRAME_SINGLE_CHAIN_PLAN_AND_DRYRUN_READY_FOR_CONTROLLED_TRIAL_PLANNING"
)

FINAL_DECISION = (
    "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_VALIDATION_CLOSED_READY_FOR_VISION_SAMPLE_FRAME_CONTROLLED_TRIAL_PLANNING"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Planning-v1-001"

HARNESS_MODULE_PATH = "capabilities/governance/single_chain_trial_validation_harness_v1.py"
REQUIRED_HARNESS_SYMBOLS: Tuple[str, ...] = (
    "run_single_chain_trial_plan_and_dryrun",
    "build_vision_sample_frame_chain_config",
    "validate_limited_runtime_post_dryrun_review",
)

REQUIRED_CONTRACT_FIELDS: Tuple[str, ...] = (
    "chain_id",
    "chain_domain",
    "trial_scope",
    "input_sources_allowed",
    "input_sources_blocked",
    "positive_flows",
    "blocked_flows",
    "required_gates",
    "stop_conditions",
    "output_contract",
    "no_runtime_boundary_fields",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "single_chain_trial_validation_harness_validation_closure_only": True,
        "closure_only": True,
        "review_only": True,
        "harness_contract_validated_now": True,
        "harness_first_consumer_validated_now": True,
        "harness_module_present_now": True,
        "harness_enforced_globally_now": False,
        "chain_trial_started_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        import json

        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _collect_candidates(obj: Any, found: List[Dict[str, Any]]) -> None:
    if isinstance(obj, dict):
        if obj.get("candidate_type") and obj.get("candidate_id"):
            found.append(obj)
        for v in obj.values():
            _collect_candidates(v, found)
    elif isinstance(obj, list):
        for item in obj:
            _collect_candidates(item, found)


def _review_harness_module(repo_root: Path) -> Tuple[bool, Dict[str, Any], List[str]]:
    issues: List[str] = []
    module_path = repo_root / HARNESS_MODULE_PATH
    file_exists = module_path.is_file()
    symbols_ok = False
    symbol_status: Dict[str, bool] = {}

    if file_exists:
        try:
            mod = importlib.import_module(
                "capabilities.governance.single_chain_trial_validation_harness_v1"
            )
            for sym in REQUIRED_HARNESS_SYMBOLS:
                fn = getattr(mod, sym, None)
                symbol_status[sym] = callable(fn)
            symbols_ok = all(symbol_status.values())
            if mod.HARNESS_ID != HARNESS_ID:
                issues.append("HARNESS_ID mismatch")
        except Exception as exc:  # noqa: BLE001 — governance presence check
            issues.append(f"import_failed:{exc}")
    else:
        issues.append("harness_module_file_missing")

    passed = file_exists and symbols_ok and not issues
    return passed, {
        "review_id": "harness_module_presence_review_v1",
        "module_path": str(module_path),
        "file_exists": file_exists,
        "symbols": symbol_status,
        "run_single_chain_trial_plan_and_dryrun_signature": str(
            inspect.signature(run_single_chain_trial_plan_and_dryrun)
        ),
        "issues": issues,
        "review_pass": passed,
    }, issues


def run_single_chain_trial_validation_harness_validation_closure_v1(
    *,
    single_chain_trial_validation_harness_extraction_planning_root: str,
    vision_sample_frame_single_chain_plan_and_dryrun_root: str,
    repo_root: Optional[str] = None,
    closure_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    extraction_root = Path(
        single_chain_trial_validation_harness_extraction_planning_root
    ).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_plan_and_dryrun_root).expanduser().resolve()
    luna_core = Path(repo_root).expanduser().resolve() if repo_root else extraction_root.parent.parent.parent / "Luna-Core"
    if not (luna_core / "capabilities").is_dir():
        luna_core = Path(__file__).resolve().parents[2]

    out_root = (
        Path(closure_output_root).expanduser().resolve()
        if closure_output_root
        else extraction_root.parent / "single_chain_trial_validation_harness_validation_closure"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(extraction_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_extraction_planning_root": str(extraction_root),
        "upstream_vision_plan_and_dryrun_root": str(vision_root),
        "closure_output_root": str(out_root),
        "harness_module_ref": HARNESS_MODULE_PATH,
    }

    ext_sm = _try_read_json(extraction_root / "summary.json") or {}
    ext_vr = _try_read_json(extraction_root / "verifier_report.json") or {}
    contract = _try_read_json(extraction_root / "reusable_single_chain_trial_validation_contract_v1.json") or {}
    anti_rules = _try_read_json(extraction_root / "anti_recursion_rules_for_single_chain_trials_v1.json") or {}
    chain_schema = _try_read_json(extraction_root / "chain_config_schema_planning_v1.json") or {}

    ext_trusted = ext_vr.get("verifier") == "GO" and ext_vr.get("passed") is True
    ext_summary_ok = (
        ext_sm.get("boundary_ok") is True
        and ext_sm.get("phase") == UPSTREAM_EXTRACTION_PHASE
        and ext_sm.get("final_decision") == UPSTREAM_EXTRACTION_FINAL
    )
    if not ext_trusted and not ext_summary_ok:
        blockers.append("harness extraction planning verifier must be GO")
    if ext_sm.get("final_decision") != UPSTREAM_EXTRACTION_FINAL:
        blockers.append("harness extraction final_decision mismatch")

    contract_fields_ok = all(f in (contract.get("required_fields") or []) for f in REQUIRED_CONTRACT_FIELDS)
    if contract.get("harness_id") != HARNESS_ID:
        blockers.append("contract harness_id mismatch")
    if not contract_fields_ok:
        blockers.append("reusable contract missing required fields")

    module_ok, module_review, module_issues = _review_harness_module(luna_core)
    blockers.extend(module_issues)

    vis_sm = _try_read_json(vision_root / "summary.json") or {}
    vis_vr = _try_read_json(vision_root / "verifier_report.json") or {}
    positive = _try_read_json(vision_root / "vision_sample_frame_positive_flow_result_v1.json") or {}
    blocked = _try_read_json(vision_root / "vision_sample_frame_blocked_flow_result_v1.json") or {}
    gates = _try_read_json(vision_root / "vision_sample_frame_gate_result_v1.json") or {}
    stops = _try_read_json(vision_root / "vision_sample_frame_stop_condition_result_v1.json") or {}
    policy = _try_read_json(vision_root / "vision_sample_frame_plan_and_dryrun_policy_v1.json") or {}

    vis_trusted = vis_vr.get("verifier") == "GO" and vis_vr.get("passed") is True
    vis_summary_ok = (
        vis_sm.get("boundary_ok") is True
        and vis_sm.get("phase") == UPSTREAM_VISION_PHASE
        and vis_sm.get("final_decision") == UPSTREAM_VISION_FINAL
    )
    if not vis_trusted and not vis_summary_ok:
        blockers.append("vision plan+dryrun verifier must be GO")
    if (vis_sm.get("high_risk_count") or 0) != 0:
        blockers.append("vision high_risk_count must be 0")
    if positive.get("all_pass") is not True:
        blockers.append("3 positive flows must pass")
    if (positive.get("flows_passed") or 0) < 3:
        blockers.append("positive_flows_passed must be >= 3")
    if blocked.get("all_stop_or_hold") is not True:
        blockers.append("6 blocked flows must stop/hold")
    if (blocked.get("flows_enforced") or 0) < 6:
        blockers.append("blocked_flows_enforced must be >= 6")
    if gates.get("enforcement_pass") is not True:
        blockers.append("14 gates enforcement_pass required")
    if (gates.get("gates_passed") or 0) < 14:
        blockers.append("gates_passed must be >= 14")
    if stops.get("verification_pass") is not True:
        blockers.append("stop conditions verification_pass required")
    if (stops.get("conditions_passed") or 0) < 10:
        blockers.append("stop conditions must be >= 10")

    candidates: List[Dict[str, Any]] = []
    for fname in (
        "vision_sample_frame_positive_flow_result_v1.json",
        "vision_sample_frame_blocked_flow_result_v1.json",
    ):
        data = _try_read_json(vision_root / fname)
        if data:
            _collect_candidates(data, candidates)

    candidate_ok = True
    for c in candidates:
        if c.get("candidate_only") is not True or c.get("fact_status") != "not_fact":
            candidate_ok = False
            blockers.append(f"candidate_invariant_fail:{c.get('candidate_id')}")

    harness_used = policy.get("mode") == "single_chain_plan_and_dryrun_via_harness" or policy.get("chain_config_ref") == "vision_sample_frame"
    if not harness_used:
        blockers.append("vision first consumer must reference harness mode")

    policy_doc = {
        "policy_id": "single_chain_harness_validation_closure_policy_v1",
        "scope": CLOSURE_SCOPE,
        "merges_phases": [
            "Harness-Extraction-DryRun",
            "Harness-Extraction-PostReview",
        ],
        **meta,
    }

    contract_review = {
        "review_id": "harness_contract_consumption_review_v1",
        "contract_id": contract.get("contract_id"),
        "harness_id": contract.get("harness_id"),
        "required_fields_present": contract_fields_ok,
        "entrypoint": contract.get("entrypoint"),
        "extraction_planning_root": str(extraction_root),
        "extraction_verifier": ext_vr.get("verifier"),
        "review_pass": contract_fields_ok and ext_summary_ok,
        **meta,
    }
    module_review_payload = {**module_review, **meta}

    vision_review = {
        "review_id": "vision_first_consumer_review_v1",
        "chain_id": vis_sm.get("chain_id", "vision_sample_frame"),
        "plan_and_dryrun_root": str(vision_root),
        "harness_mode_confirmed": harness_used,
        "positive_flows_passed": positive.get("flows_passed"),
        "blocked_flows_enforced": blocked.get("flows_enforced"),
        "gates_passed": gates.get("gates_passed"),
        "stop_conditions_passed": stops.get("conditions_passed"),
        "all_candidates_candidate_only": candidate_ok,
        "vision_verifier": vis_vr.get("verifier"),
        "review_pass": vis_summary_ok and candidate_ok and harness_used,
        **meta,
    }

    schema_closure = {
        "closure_id": "reusable_chain_config_schema_closure_v1",
        "schema_id": chain_schema.get("schema_id"),
        "example_chain_id": (chain_schema.get("example") or {}).get("chain_id"),
        "frozen": True,
        **meta,
    }

    anti_closure = {
        "closure_id": "anti_recursion_rule_closure_v1",
        "rules": anti_rules.get("rules") or list(ANTI_RECURSION_RULES),
        "no_full_planning_dryrun_review_chain": True,
        "harness_first_required": True,
        **meta,
    }

    usage_guide = {
        "guide_id": "future_single_chain_usage_guide_v1",
        "standard_flow": ["chain_config", "Harness.run_single_chain_trial_plan_and_dryrun", "Controlled Trial Planning"],
        "per_chain_outputs_only": [
            "chain_config",
            "plan_and_dryrun_result",
            "issue_register",
            "readiness_decision",
        ],
        "extra_review_only_when": [
            "opening real runtime",
            "writing fact layer",
            "committing state",
            "triggering user-facing output",
        ],
        "planned_consumers": ["ocr_mock_result", "navigation_guidance", "task_response", "voice_candidate"],
        **meta,
    }

    boundary_ok = len(blockers) == 0 and module_ok and contract_review.get("review_pass") and vision_review.get("review_pass")

    closure_decision = {
        "decision_id": "single_chain_harness_validation_closure_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "SINGLE_CHAIN_TRIAL_VALIDATION_HARNESS_VALIDATION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "harness_validation_closed": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "harness_contract_validated": boundary_ok,
        "harness_first_consumer_validated": vision_review.get("review_pass"),
        **meta,
    }

    return {
        "single_chain_harness_validation_closure_policy": policy_doc,
        "harness_contract_consumption_review": contract_review,
        "harness_module_presence_review": module_review_payload,
        "vision_first_consumer_review": vision_review,
        "reusable_chain_config_schema_closure": schema_closure,
        "anti_recursion_rule_closure": anti_closure,
        "future_single_chain_usage_guide": usage_guide,
        "single_chain_harness_validation_closure_decision": closure_decision,
        "summary": summary,
    }
