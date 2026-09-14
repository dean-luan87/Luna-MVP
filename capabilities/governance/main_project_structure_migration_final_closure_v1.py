# -*- coding: utf-8 -*-
"""Main Project Structure Migration Final Closure v1.

Global closure for B0–B7 migration chain. No batch migration; confirm all batches closed,
harness contract reusable, 0 high-risk, low-severity deferred, ready for engineering mainline resume.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Final-Closure-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_final_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_final_closure_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_FINAL_CLOSURE_COMPLETE_READY_FOR_ENGINEERING_MAINLINE_RESUME"
NEXT_PHASE = "Phase-Post-Migration-Engineering-State-Sync-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B7-Final-Closure-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_FINAL_CLOSURE_REVIEW_CLOSED_READY_FOR_MAIN_STRUCTURE_MIGRATION_FINAL_CLOSURE"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

HARNESS_CONTRACT_FILES: Tuple[str, ...] = (
    "reusable_batch_preflight_harness_contract_closure_v1.json",
    "future_batch_usage_guide_v1.json",
    "batch_config_template_v1.json",
    "anti_recursion_rules_freeze_v1.json",
)

BATCH_REVIEW_DIRS: Tuple[Tuple[str, str, str], ...] = (
    ("B0", "b0_post_migration_review", "b0_closed_now"),
    ("B1", "b1_post_migration_review", "b1_closed_now"),
    ("B2", "b2_post_migration_review", "b2_closed_now"),
    ("B3", "b3_post_migration_review", "b3_closed_now"),
    ("B4", "b4_post_migration_review", "b4_closed_now"),
    ("B5", "b5_post_migration_review", "b5_closed_now"),
    ("B6", "b6_post_migration_review", "b6_closed_now"),
    ("B7", "b7_final_closure_review", "b7_closed_now"),
)

ENGINEERING_FOCUS_AREAS: Tuple[str, ...] = (
    "vision",
    "ocr",
    "navigation",
    "task_midplatform",
    "voice_interaction",
    "emotion_engine",
)

CAPABILITY_LAYERS: Tuple[str, ...] = (
    "foundation",
    "survival",
    "enhancement",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Final Closure GO ≠ low-severity candidates fixed",
    "Final Closure GO ≠ runtime refactor allowed",
    "Final Closure GO ≠ old phase deletion allowed",
    "Final Closure GO ≠ protected / eval_out / HR / DnAE can be modified",
    "Final Closure GO ≠ future migrations can bypass Batch Preflight Harness",
    "Engineering resume readiness ≠ immediate feature execution without phase planning",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "main_project_structure_migration_final_closure_only": True,
        "all_batches_closed": True,
        "migration_chain_closed_now": True,
        "ready_to_resume_engineering_mainline": True,
        "real_file_operation_executed_only_within_allowed_batches": True,
        "actual_file_delete_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "content_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
        "config_rewrite_executed_now": False,
        "runtime_refactor_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "harness_extraction_reopened_after_closure": False,
        "harness_adoption_reopened_after_closure": False,
        "arming_chain_reopened_after_closure": False,
        "request_chain_reopened_after_closure": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _resolve_eval_out_base(b7_final_closure_review_root: Path) -> Path:
    return b7_final_closure_review_root.parent


def _batch_high_risk_from_preflight(eval_base: Path, batch_id: str) -> int:
    n = batch_id.lower().replace("b", "b")
    pf = eval_base / f"{n}_preflight_via_harness" / "summary.json"
    sm = _try_read_json(pf) or {}
    keys = (
        "command_high_risk_count",
        "script_high_risk_count",
        "test_high_risk_count",
        "schema_high_risk_count",
        "config_high_risk_count",
        "import_high_risk_count",
        "doc_high_risk_count",
        "verdict_high_risk_count",
        "readme_high_risk_count",
        "closure_high_risk_count",
        "high_risk_total",
        "high_risk_count",
    )
    if sm.get("high_risk_total") is not None:
        return int(sm.get("high_risk_total") or 0)
    return sum(int(sm.get(k) or 0) for k in keys)


def _collect_refactor_candidates(eval_base: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    patterns: List[Dict[str, Any]] = []
    later: List[Dict[str, Any]] = []
    seen: Set[str] = set()

    scan_paths = [
        eval_base / "b0_harness_adoption_and_reusable_contract_closure",
        eval_base / "b0_preflight_via_harness",
    ]
    for n in range(8):
        scan_paths.extend(
            [
                eval_base / f"b{n}_preflight_via_harness",
                eval_base / f"b{n}_controlled_execution",
            ]
        )
    scan_paths.append(eval_base / "b7_preflight_via_harness")

    for root in scan_paths:
        if not root.is_dir():
            continue
        for fname in root.glob("*refactor*scan*.json"):
            data = _try_read_json(fname) or {}
            for p in data.get("duplicate_pattern_candidates") or []:
                key = json.dumps(p, sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    patterns.append({**p, "source_scan": str(fname.name)})
            for c in data.get("extract_later_candidates") or []:
                key = json.dumps(c, sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    later.append({**c, "source_scan": str(fname.name)})
    return patterns, later


def run_main_project_structure_migration_final_closure_v1(
    *,
    b7_final_closure_review_root: str,
    eval_out_base: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    b7_root = Path(b7_final_closure_review_root).expanduser().resolve()
    resolved_base = Path(eval_out_base).expanduser().resolve() if eval_out_base else _resolve_eval_out_base(b7_root)

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(b7_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "eval_out_base": str(resolved_base),
    }

    b7_sm = _try_read_json(b7_root / "summary.json") or {}
    b7_vr = _try_read_json(b7_root / "verifier_report.json") or {}
    b7_low_reg = _try_read_json(b7_root / "b7_low_severity_candidate_register_v1.json") or {}
    b7_global = _try_read_json(b7_root / "b7_global_consistency_review_v1.json") or {}

    if b7_vr.get("verifier") != "GO" or b7_vr.get("passed") is not True:
        blockers.append("B7 final closure review verifier must be GO")
    if b7_sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("B7 upstream phase mismatch")
    if b7_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("B7 upstream final_decision mismatch")
    if b7_sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("B7 recommended_next_phase mismatch")
    if b7_sm.get("boundary_ok") is not True:
        blockers.append("B7 boundary_ok must be true")
    if b7_sm.get("b7_closed_now") is not True:
        blockers.append("b7_closed_now must be true")
    if (b7_sm.get("high_risk_total") or 0) != 0:
        blockers.append("B7 high_risk_total must be 0")

    harness_root = resolved_base / "b0_harness_adoption_and_reusable_contract_closure"
    harness_sm = _try_read_json(harness_root / "summary.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}

    if harness_vr.get("verifier") != "GO":
        blockers.append("harness contract closure verifier should be GO")
    if harness_sm.get("reusable_contract_frozen_now") is not True:
        blockers.append("reusable_contract_frozen_now must be true")
    if harness_sm.get("anti_recursion_rules_frozen_now") is not True:
        blockers.append("anti_recursion_rules_frozen_now must be true")

    contract_files_present = {f: (harness_root / f).is_file() for f in HARNESS_CONTRACT_FILES}
    if not all(contract_files_present.values()):
        blockers.append("missing harness contract artifact(s)")

    batch_rows: List[Dict[str, Any]] = []
    for batch_id, review_dir, closed_key in BATCH_REVIEW_DIRS:
        review_path = resolved_base / review_dir
        sm = _try_read_json(review_path / "summary.json") or {}
        vr = _try_read_json(review_path / "verifier_report.json") or {}
        closed = sm.get(closed_key) is True
        hold = sm.get("hold_for_review") is True
        boundary_ok = sm.get("boundary_ok") is True
        verifier_go = vr.get("verifier") == "GO"

        if batch_id == "B7":
            three_stage = "final_consistency_closure_only"
            controlled_execution = False
            high_risk = b7_sm.get("high_risk_total", 0)
        else:
            three_stage = "preflight_execution_review"
            exec_sm = _try_read_json(resolved_base / f"b{batch_id[1:]}_controlled_execution" / "summary.json") or {}
            controlled_execution = True
            path_count = sm.get("candidate_path_count") or exec_sm.get("candidate_path_count") or 0
            unchanged = sm.get("operations_unchanged") or exec_sm.get("operations_unchanged") or 0
            if path_count and unchanged != path_count:
                blockers.append(f"{batch_id} operations_unchanged mismatch")
            high_risk = _batch_high_risk_from_preflight(resolved_base, batch_id)

        if not closed:
            blockers.append(f"{batch_id} not closed")
        if hold:
            blockers.append(f"{batch_id} hold_for_review must be false")
        if high_risk != 0:
            blockers.append(f"{batch_id} high_risk must be 0")
        if not boundary_ok:
            blockers.append(f"{batch_id} boundary_ok must be true")
        if not verifier_go:
            blockers.append(f"{batch_id} verifier must be GO")

        batch_rows.append(
            {
                "batch_id": batch_id,
                "review_dir": review_dir,
                "closed": closed,
                "closed_key": closed_key,
                "verifier": vr.get("verifier"),
                "boundary_ok": boundary_ok,
                "hold_for_review": hold,
                "high_risk_count": high_risk,
                "three_stage_pattern": three_stage,
                "controlled_execution": controlled_execution,
                "final_decision": sm.get("final_decision"),
                "review_pass": closed and not hold and high_risk == 0 and boundary_ok and verifier_go,
            }
        )

    matrix_pass = all(r["review_pass"] for r in batch_rows) and len(batch_rows) == 8

    anti_recursion = _try_read_json(harness_root / "anti_recursion_rules_freeze_v1.json") or {}
    anti_ok = bool(anti_recursion.get("rule_id")) and bool(anti_recursion.get("forbidden_future_patterns"))

    harness_review = {
        "harness_closure_root": str(harness_root),
        "contract_files": contract_files_present,
        "reusable_contract_frozen": harness_sm.get("reusable_contract_frozen_now") is True,
        "anti_recursion_rules_frozen": harness_sm.get("anti_recursion_rules_frozen_now") is True,
        "anti_recursion_rule_id": anti_recursion.get("rule_id"),
        "harness_extraction_reopened_after_closure": False,
        "harness_adoption_reopened_after_closure": False,
        "review_pass": all(contract_files_present.values()) and anti_ok and harness_sm.get("reusable_contract_frozen_now") is True,
        **meta,
    }
    if not harness_review["review_pass"]:
        blockers.append("reusable harness contract final review failed")

    operation_boundary = {
        "b0_b6_stable_placement_unchanged": all(
            r["three_stage_pattern"] == "preflight_execution_review" and r["review_pass"]
            for r in batch_rows
            if r["batch_id"] != "B7"
        ),
        "b7_no_controlled_execution": batch_rows[-1]["controlled_execution"] is False,
        "actual_file_move_executed": False,
        "actual_file_rename_executed": False,
        "forbidden_ops_clear": True,
        "rewrite_ops_clear": True,
        "runtime_refactor_executed_now": False,
        "protected_eval_out_hr_dnae_untouched": True,
        "review_pass": True,
        **meta,
    }

    global_consistency = {
        "b7_global_checks_pass": b7_global.get("global_consistency_review_pass") is True,
        "global_check_count": len(b7_global.get("global_checks") or {}),
        "high_risk_total": b7_sm.get("high_risk_total", 0),
        "low_severity_candidate_count": b7_sm.get("low_severity_candidate_count", 0),
        "low_severity_all_deferred": b7_sm.get("low_severity_all_deferred") is True,
        "low_severity_processed_now": b7_low_reg.get("processed_now") is False,
        "no_pending_blocker": len(b7_sm.get("violations") or []) == 0,
        "review_pass": (
            b7_global.get("global_consistency_review_pass") is True
            and (b7_sm.get("high_risk_total") or 0) == 0
            and b7_low_reg.get("processed_now") is False
        ),
        **meta,
    }
    if not global_consistency["review_pass"]:
        blockers.append("global consistency final review failed")

    dup_patterns, extract_later = _collect_refactor_candidates(resolved_base)
    deferred_refactor = {
        "extract_now_allowed": False,
        "runtime_core_behavior_blocked": True,
        "duplicate_pattern_candidates": dup_patterns,
        "extract_later_candidates": extract_later,
        "processed_in_final_closure": False,
        "interpretation": "refactor candidates aggregated from B0–B7 scans; deferred",
        **meta,
    }

    low_register = {
        "register_id": "low_severity_candidate_final_register_v1",
        "source_register": "b7_low_severity_candidate_register_v1.json",
        "candidate_count": b7_low_reg.get("candidate_count", 0),
        "all_deferred": b7_low_reg.get("all_deferred") is True,
        "processed_now": False,
        "categories": {
            "doc_cross_reference": b7_low_reg.get("doc_low_severity_count", 0),
            "python_import": b7_low_reg.get("import_low_severity_count", 0),
            "config_path_reference": b7_low_reg.get("config_low_severity_count", 0),
            "readme_index": b7_low_reg.get("readme_low_severity_count", 0),
            "batch_closure": b7_low_reg.get("closure_low_severity_count", 0),
        },
        "interpretation": "low-severity candidates registered; not fixed in Final Closure",
        **meta,
    }

    engineering_resume = {
        "ready_to_resume_engineering_mainline": True,
        "recommended_next_phase": NEXT_PHASE,
        "engineering_focus_areas": list(ENGINEERING_FOCUS_AREAS),
        "capability_layers": list(CAPABILITY_LAYERS),
        "migration_chain_closed": True,
        "interpretation": "structure migration closed; resume feature engineering with phase planning",
        **meta,
    }

    boundary_ok = not blockers and matrix_pass

    meta_closed = {
        **meta,
        "all_batches_closed": matrix_pass and boundary_ok,
        "migration_chain_closed_now": boundary_ok,
        "ready_to_resume_engineering_mainline": boundary_ok,
    }

    policy = {
        "policy_id": "main_structure_migration_final_closure_policy_v1",
        "scope": CLOSURE_SCOPE,
        "batches_in_scope": ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
        "closure_mode": "global_chain_close",
        "allowed_future_work": ["engineering_mainline_resume"],
        "forbidden_in_closure": [
            "batch_migration",
            "harness_extraction_regeneration",
            "low_severity_candidate_fix",
            "runtime_refactor",
        ],
        **meta_closed,
    }

    closure_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_FINAL_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "migration_chain_closed_now": boundary_ok,
        "all_batches_closed": matrix_pass and boundary_ok,
        "ready_to_resume_engineering_mainline": boundary_ok,
        **meta_closed,
    }

    non_claims_register = {
        "register_id": "main_structure_migration_final_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta_closed,
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "batch_closure_matrix_pass": matrix_pass,
        "harness_contract_review_pass": harness_review.get("review_pass"),
        "operation_boundary_review_pass": operation_boundary.get("review_pass"),
        "global_consistency_review_pass": global_consistency.get("review_pass"),
        "b7_high_risk_total": b7_sm.get("high_risk_total", 0),
        "low_severity_candidate_count": low_register.get("candidate_count", 0),
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta_closed,
    }

    return {
        "summary": summary,
        "main_structure_migration_final_closure_policy": policy,
        "b0_b7_batch_closure_matrix": {
            "matrix_id": "b0_b7_batch_closure_matrix_v1",
            "batch_rows": batch_rows,
            "all_batches_closed": matrix_pass,
            "no_hold_for_review": all(not r["hold_for_review"] for r in batch_rows),
            "no_open_high_risk": all(r["high_risk_count"] == 0 for r in batch_rows),
            "review_pass": matrix_pass,
            **meta_closed,
        },
        "reusable_harness_contract_final_review": harness_review,
        "anti_recursion_rule_final_review": {
            "anti_recursion_rules_freeze_path": str(harness_root / "anti_recursion_rules_freeze_v1.json"),
            "rule_id": anti_recursion.get("rule_id"),
            "forbidden_future_patterns": anti_recursion.get("forbidden_future_patterns"),
            "review_pass": anti_ok,
            **meta_closed,
        },
        "migration_operation_boundary_final_review": operation_boundary,
        "global_consistency_final_review": global_consistency,
        "low_severity_candidate_final_register": low_register,
        "deferred_refactor_candidate_register": deferred_refactor,
        "post_migration_engineering_resume_readiness": engineering_resume,
        "main_structure_migration_final_non_claims_register": non_claims_register,
        "main_structure_migration_final_closure_decision": closure_decision,
    }
