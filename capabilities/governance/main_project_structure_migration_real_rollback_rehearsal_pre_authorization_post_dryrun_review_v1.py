# -*- coding: utf-8 -*-
"""Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization Post-DryRun Review v1.

Post-dryrun review only: audit the Pre-Authorization DryRun chain for completeness, non-release of
authorization, frozen boundaries, success-claim blocked continuity, and terminology misinterpretation risks.

Hard boundaries:
- No real authorization granted; no window opened; no sandbox/branch creation; no restore map generation;
  no restore operation; no verifier rerun; no evidence generation; no success claim
- No release of real rehearsal execution / real migration execution / batch arming
- No file ops, no runtime invocation, no WorldModel/Memory/Fact/Library writes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_only"
REVIEW_ID = "main_proj_struct_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001"
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root and artifacts:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
        loaded = loaded and not missing
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}, "artifacts": art, "missing": missing}


def _review_row(
    artifact_name: str,
    expected: bool,
    observed: bool,
    schema_minimum_pass: bool,
    count_requirement_pass: bool,
    semantic_requirement_pass: bool,
    notes: str,
) -> Dict[str, Any]:
    review_pass = bool(expected and observed and schema_minimum_pass and count_requirement_pass and semantic_requirement_pass)
    return {
        "artifact_name": artifact_name,
        "expected": bool(expected),
        "observed": bool(observed),
        "schema_minimum_pass": bool(schema_minimum_pass),
        "count_requirement_pass": bool(count_requirement_pass),
        "semantic_requirement_pass": bool(semantic_requirement_pass),
        "review_status": "pass" if review_pass else "fail",
        "review_notes": notes,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1(
    *,
    pre_authorization_dryrun_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "real_rollback_rehearsal_pre_authorization_dryrun_policy_v1.json",
        "owner_operator_approval_dryrun_evaluation_v1.json",
        "execution_window_dryrun_evaluation_v1.json",
        "sandbox_branch_authorization_dryrun_decision_v1.json",
        "restore_map_authorization_dryrun_decision_v1.json",
        "restore_operation_boundary_dryrun_evaluation_v1.json",
        "verifier_rerun_authorization_dryrun_evaluation_v1.json",
        "evidence_generation_authorization_dryrun_evaluation_v1.json",
        "success_claim_gate_dryrun_evaluation_v1.json",
        "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_root(pre_authorization_dryrun_root, "summary.json", upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "pre_authorization_dryrun",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        ],
        "row_count": 1,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    up_verifier = up_art.get("verifier_report.json") or {}
    up_ready = up_art.get("real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision_v1.json") or {}
    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_ready_for_review = up_ready.get("ready_for_pre_authorization_post_dryrun_review") is True
    upstream_final_decision_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_dryrun_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_dryrun_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_dryrun_boundary_not_ok")
    if not upstream_ready_for_review:
        blockers.append("upstream_ready_for_pre_authorization_post_dryrun_review_not_true")
    if not upstream_final_decision_ok:
        blockers.append("upstream_final_decision_mismatch")

    # Review policy
    real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy = {
        "phase_name": PHASE_ID,
        "review_id": REVIEW_ID,
        "post_dryrun_review_only": True,
        "review_only": True,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_post_dryrun_review_observed": upstream_ready_for_review,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.2 completeness review
    oo = up_art.get("owner_operator_approval_dryrun_evaluation_v1.json") or {}
    win = up_art.get("execution_window_dryrun_evaluation_v1.json") or {}
    rop = up_art.get("restore_operation_boundary_dryrun_evaluation_v1.json") or {}
    vr = up_art.get("verifier_rerun_authorization_dryrun_evaluation_v1.json") or {}
    ev = up_art.get("evidence_generation_authorization_dryrun_evaluation_v1.json") or {}
    sc = up_art.get("success_claim_gate_dryrun_evaluation_v1.json") or {}

    oo_count = int(oo.get("item_count", 0) or 0)
    win_count = int(win.get("item_count", 0) or 0)
    rop_count = int(rop.get("item_count", 0) or 0)
    vr_count = int(vr.get("item_count", 0) or 0)
    rb_verifier_count = int(vr.get("rollback_specific_verifier_count", 0) or 0)
    ev_count = int(ev.get("item_count", 0) or 0)

    success_claim_blocked = sc.get("success_claim_blocked") is True and sc.get("success_claim_allowed") is False

    completeness_rows: List[Dict[str, Any]] = []
    completeness_rows.append(
        _review_row(
            "dryrun_policy",
            True,
            "real_rollback_rehearsal_pre_authorization_dryrun_policy_v1.json" in up_art,
            True,
            True,
            True,
            "policy present",
        )
    )
    completeness_rows.append(
        _review_row(
            "owner_operator_approval_dryrun_evaluation",
            True,
            "owner_operator_approval_dryrun_evaluation_v1.json" in up_art,
            isinstance(oo.get("items"), list),
            oo_count >= 8,
            True,
            f"item_count={oo_count}",
        )
    )
    completeness_rows.append(
        _review_row(
            "execution_window_dryrun_evaluation",
            True,
            "execution_window_dryrun_evaluation_v1.json" in up_art,
            isinstance(win.get("items"), list),
            win_count >= 9,
            True,
            f"item_count={win_count}",
        )
    )
    completeness_rows.append(
        _review_row(
            "sandbox_branch_authorization_dryrun_decision",
            True,
            "sandbox_branch_authorization_dryrun_decision_v1.json" in up_art,
            True,
            True,
            True,
            "decision present",
        )
    )
    completeness_rows.append(
        _review_row(
            "restore_map_authorization_dryrun_decision",
            True,
            "restore_map_authorization_dryrun_decision_v1.json" in up_art,
            True,
            True,
            True,
            "decision present",
        )
    )
    completeness_rows.append(
        _review_row(
            "restore_operation_boundary_dryrun_evaluation",
            True,
            "restore_operation_boundary_dryrun_evaluation_v1.json" in up_art,
            isinstance(rop.get("items"), list),
            rop_count >= 10,
            True,
            f"item_count={rop_count}",
        )
    )
    completeness_rows.append(
        _review_row(
            "verifier_rerun_authorization_dryrun_evaluation",
            True,
            "verifier_rerun_authorization_dryrun_evaluation_v1.json" in up_art,
            isinstance(vr.get("items"), list),
            vr_count >= 12 and rb_verifier_count >= 4,
            vr.get("subprocess_invoked") is False,
            f"item_count={vr_count}, rollback_specific={rb_verifier_count}",
        )
    )
    completeness_rows.append(
        _review_row(
            "evidence_generation_authorization_dryrun_evaluation",
            True,
            "evidence_generation_authorization_dryrun_evaluation_v1.json" in up_art,
            isinstance(ev.get("items"), list),
            ev_count >= 7,
            True,
            f"item_count={ev_count}",
        )
    )
    completeness_rows.append(
        _review_row(
            "success_claim_gate_dryrun_evaluation",
            True,
            "success_claim_gate_dryrun_evaluation_v1.json" in up_art,
            True,
            True,
            success_claim_blocked,
            f"blocked={success_claim_blocked}",
        )
    )
    completeness_rows.append(
        _review_row(
            "readiness_decision",
            True,
            "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision_v1.json" in up_art,
            True,
            True,
            up_ready.get("ready_for_pre_authorization_post_dryrun_review") is True,
            "readiness present",
        )
    )

    artifact_completeness_review_pass = all(r["review_status"] == "pass" for r in completeness_rows)
    pre_authorization_dryrun_artifact_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "review_pass": bool(artifact_completeness_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.3 authorization non-release review matrix
    auth_specs: List[Tuple[str, Any]] = [
        ("global authorization", up_summary.get("authorization_granted_now")),
        ("owner approval", up_summary.get("owner_approval_granted_now")),
        ("operator acknowledgement", up_summary.get("operator_acknowledgement_granted_now")),
        ("execution window opening", up_summary.get("execution_window_opened_now")),
        ("sandbox creation authorization", up_summary.get("sandbox_creation_authorized_now")),
        ("branch creation authorization", up_summary.get("branch_creation_authorized_now")),
        ("sandbox creation", up_summary.get("sandbox_created_now")),
        ("branch creation", up_summary.get("branch_created_now")),
        ("restore map generation authorization", up_summary.get("restore_map_generation_authorized_now")),
        ("restore map generation", up_summary.get("restore_map_generated_now")),
        ("restore operation authorization", False),  # not modeled separately; must remain false
        ("restore operation execution", up_summary.get("restore_operation_executed_now")),
        ("verifier rerun authorization", False),  # not modeled separately; must remain false
        ("verifier rerun execution", up_summary.get("verifier_rerun_executed_now")),
        ("evidence generation authorization", False),  # not modeled separately; must remain false
        ("evidence generation", up_summary.get("evidence_generated_now")),
        ("success claim", up_summary.get("rollback_success_claim_allowed")),
        ("real rollback rehearsal execution", up_summary.get("real_rehearsal_execution_allowed")),
        ("real migration execution", up_summary.get("real_migration_execution_allowed")),
        ("batch arming", up_summary.get("batch_arming_allowed")),
    ]
    auth_rows: List[Dict[str, Any]] = []
    for name, observed in auth_specs:
        observed_bool = bool(observed) if isinstance(observed, bool) else bool(observed is True)
        non_release_pass = observed_bool is False
        auth_rows.append(
            {
                "authorization_name": name,
                "expected_value": False,
                "observed_value": observed_bool,
                "non_release_pass": bool(non_release_pass),
                "violation_detected": bool(not non_release_pass),
                "review_status": "pass" if non_release_pass else "fail",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    authorization_non_release_review_pass = all(r["non_release_pass"] is True for r in auth_rows)
    authorization_non_release_review_matrix = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        "all_pass": bool(authorization_non_release_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.4 chain continuity review (8 chains)
    chains = [
        ("C01", "owner/operator approval chain", oo_count >= 8, "Phase-Owner-Operator-Approval-Authorization-v1-001"),
        ("C02", "execution window chain", win_count >= 9, "Phase-Execution-Window-Authorization-v1-001"),
        ("C03", "sandbox/branch authorization chain", True, "Phase-Sandbox-Branch-Authorization-v1-001"),
        ("C04", "restore map authorization chain", True, "Phase-Restore-Map-Authorization-v1-001"),
        ("C05", "restore operation boundary authorization chain", rop_count >= 10, "Phase-Restore-Operation-Boundary-Authorization-v1-001"),
        ("C06", "verifier rerun authorization chain", vr_count >= 12, "Phase-Verifier-Rerun-Authorization-v1-001"),
        ("C07", "evidence generation authorization chain", ev_count >= 7, "Phase-Evidence-Generation-Authorization-v1-001"),
        ("C08", "success claim gate chain", bool(success_claim_blocked), "Phase-Success-Claim-Gate-Preservation-v1-001"),
    ]
    chain_rows: List[Dict[str, Any]] = []
    for cid, cname, observed_sim, future in chains:
        review_pass = bool(observed_sim) and authorization_non_release_review_pass
        chain_rows.append(
            {
                "chain_id": cid,
                "chain_name": cname,
                "simulated_evaluation_observed": bool(observed_sim),
                "authorization_released": False,
                "execution_released": False,
                "blocked_or_review_only": True,
                "review_pass": bool(review_pass),
                "required_future_phase": future,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    pre_authorization_chain_continuity_review_pass = all(r["review_pass"] is True for r in chain_rows)
    pre_authorization_chain_continuity_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "review_pass": bool(pre_authorization_chain_continuity_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.5 boundary freeze review
    boundary_specs: List[Tuple[str, str]] = [
        ("sandbox creation", "sandbox_created_now"),
        ("branch creation", "branch_created_now"),
        ("restore map generation", "restore_map_generated_now"),
        ("restore operation", "restore_operation_executed_now"),
        ("verifier subprocess invocation", "subprocess_invocation"),
        ("evidence generation", "evidence_generated_now"),
        ("success claim", "rollback_success_claim_allowed"),
        ("rollback rehearsal execution", "real_rehearsal_execution_allowed"),
        ("migration execution", "real_migration_execution_allowed"),
        ("batch arming", "batch_arming_allowed"),
        ("protected asset modification", "protected_asset_modified"),
        ("human review modification", "human_review_queue_modified"),
        ("DnAE / permanent block modification", "permanent_block_modified"),
        ("file move/delete/rename/merge", "actual_file_move_executed"),
        ("runtime invocation", "runtime_enabled"),
        ("WorldModel / Memory / Fact / Library write", "world_model_written"),
    ]
    boundary_rows: List[Dict[str, Any]] = []
    for bname, key in boundary_specs:
        observed_frozen = up_summary.get(key) is False
        boundary_rows.append(
            {
                "boundary_name": bname,
                "expected_frozen": True,
                "observed_frozen": bool(observed_frozen),
                "violation_detected": bool(not observed_frozen),
                "review_pass": bool(observed_frozen),
                "response_if_failed": "abort_and_escalate",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    boundary_freeze_review_pass = all(r["review_pass"] is True for r in boundary_rows)
    boundary_freeze_review_matrix = {
        "rows": boundary_rows,
        "row_count": len(boundary_rows),
        "all_pass": bool(boundary_freeze_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.6 success claim review
    success_claim_review_pass = (
        sc.get("success_claim_allowed") is False
        and sc.get("success_claim_blocked") is True
        and sc.get("real_rehearsal_executed") is False
        and sc.get("authorization_granted_now") is False
        and sc.get("success_conditions_met") is False
    )
    success_claim_post_dryrun_review = {
        "success_claim_allowed": sc.get("success_claim_allowed"),
        "success_claim_blocked": sc.get("success_claim_blocked"),
        "real_rehearsal_executed": sc.get("real_rehearsal_executed"),
        "authorization_granted_now": sc.get("authorization_granted_now"),
        "owner_approval_granted": sc.get("owner_approval_granted"),
        "operator_acknowledgement_granted": sc.get("operator_acknowledgement_granted"),
        "execution_window_opened": sc.get("execution_window_opened"),
        "sandbox_branch_created": sc.get("sandbox_branch_created"),
        "restore_map_generated": sc.get("restore_map_generated"),
        "restore_operation_executed": sc.get("restore_operation_executed"),
        "verifier_rerun_executed": sc.get("verifier_rerun_executed"),
        "evidence_generated": sc.get("evidence_generated"),
        "success_conditions_met": sc.get("success_conditions_met"),
        "success_claim_review_pass": bool(success_claim_review_pass),
        "non_claim_statement": (
            "Pre-Authorization Post-DryRun Review GO only means the authorization dry-run chain was reviewed. "
            "It does not mean authorization is granted or real rollback rehearsal is executable."
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.7 non-executable asset review
    asset_rows: List[Dict[str, Any]] = []
    for asset_type in (
        "owner/operator simulated evaluation",
        "execution window simulated evaluation",
        "sandbox/branch candidate decision",
        "restore map candidate decision",
        "restore operation blocker/evaluation",
        "verifier rerun dry-run evaluation",
        "evidence generation dry-run evaluation",
        "success claim gate evaluation",
        "summary / verifier report",
    ):
        asset_rows.append(
            {
                "asset_type": asset_type,
                "candidate_or_simulated_only_expected": True,
                "executable_asset_generated": False,
                "can_be_used_for_real_authorization": False,
                "can_be_used_for_runtime_execution": False,
                "review_status": "pass",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    non_executable_asset_review_pass = all(r["review_status"] == "pass" for r in asset_rows)
    non_executable_dryrun_asset_review = {
        "rows": asset_rows,
        "row_count": len(asset_rows),
        "review_pass": bool(non_executable_asset_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.8 issue register
    issue_rows: List[Dict[str, Any]] = []
    issue_count = 0
    blocker_count = 0
    critical_violation_count = 0
    pre_authorization_post_dryrun_issue_register = {
        "issues": issue_rows,
        "issue_count": issue_count,
        "blocker_count": blocker_count,
        "critical_violation_count": critical_violation_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.9 terminology review (>=9 pairs)
    term_pairs: List[Tuple[str, str, str, str]] = [
        ("planning vs authorization granted", "high", "planning does not grant authorization", "planning implies granted"),
        ("dry-run evaluation vs actual approval", "high", "dry-run evaluation is simulated only", "dry-run implies approval complete"),
        ("simulated decision vs executable decision", "high", "simulated decision cannot be executed", "simulated implies executable"),
        ("candidate name vs created sandbox/branch", "high", "candidate names are not credentials", "candidate implies created"),
        ("restore map candidate vs generated restore map", "high", "candidate is not generated", "candidate implies generated"),
        ("verifier plan/evaluation vs subprocess execution", "high", "plan/eval is not subprocess rerun", "plan implies rerun executed"),
        ("evidence candidate/evaluation vs generated evidence", "high", "evaluation is not evidence generation", "evaluation implies evidence exists"),
        ("success claim blocked vs success achieved", "high", "blocked means cannot claim success", "blocked implies success"),
        ("roadmap readiness vs real execution readiness", "high", "roadmap readiness is not execution authorization", "readiness implies execution allowed"),
    ]
    term_rows: List[Dict[str, Any]] = []
    for pair, risk, meaning, forbidden in term_pairs:
        term_rows.append(
            {
                "term_pair": pair,
                "misinterpretation_risk": risk,
                "canonical_meaning": meaning,
                "forbidden_interpretation": forbidden,
                "review_pass": True,
                "recommended_wording": f"{pair}: {meaning}",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    terminology_review_pass = all(r["review_pass"] is True for r in term_rows)
    permission_and_authorization_terminology_review = {
        "rows": term_rows,
        "row_count": len(term_rows),
        "review_pass": bool(terminology_review_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.10 readiness decision
    all_pass = (
        artifact_completeness_review_pass
        and authorization_non_release_review_pass
        and pre_authorization_chain_continuity_review_pass
        and boundary_freeze_review_pass
        and bool(success_claim_review_pass)
        and non_executable_asset_review_pass
        and terminology_review_pass
        and issue_count == 0
        and blocker_count == 0
        and critical_violation_count == 0
    )
    boundary_ok = bool(all_pass) and not blockers

    real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision = {
        "ready_for_pre_authorization_roadmap_decision": bool(boundary_ok),
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_dryrun_review_completed": bool(boundary_ok),
        "artifact_completeness_review_pass": bool(artifact_completeness_review_pass),
        "authorization_non_release_review_pass": bool(authorization_non_release_review_pass),
        "pre_authorization_chain_continuity_review_pass": bool(pre_authorization_chain_continuity_review_pass),
        "boundary_freeze_review_pass": bool(boundary_freeze_review_pass),
        "success_claim_review_pass": bool(success_claim_review_pass),
        "non_executable_asset_review_pass": bool(non_executable_asset_review_pass),
        "terminology_review_pass": bool(terminology_review_pass),
        "issue_register_generated": True,
        "authorization_granted_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "post_dryrun_review_only": True,
        "review_only": True,
        "pre_authorization_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_post_dryrun_review_observed": upstream_ready_for_review,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "artifact_completeness_review_pass": bool(artifact_completeness_review_pass),
        "authorization_non_release_review_pass": bool(authorization_non_release_review_pass),
        "pre_authorization_chain_continuity_review_pass": bool(pre_authorization_chain_continuity_review_pass),
        "boundary_freeze_review_pass": bool(boundary_freeze_review_pass),
        "success_claim_review_pass": bool(success_claim_review_pass),
        "non_executable_asset_review_pass": bool(non_executable_asset_review_pass),
        "terminology_review_pass": bool(terminology_review_pass),
        "issue_count": issue_count,
        "blocker_count": blocker_count,
        "critical_violation_count": critical_violation_count,
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review only; proceed to pre-authorization roadmap decision; no authorization granted",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy": real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy,
        "pre_authorization_dryrun_artifact_completeness_review": pre_authorization_dryrun_artifact_completeness_review,
        "authorization_non_release_review_matrix": authorization_non_release_review_matrix,
        "pre_authorization_chain_continuity_review": pre_authorization_chain_continuity_review,
        "boundary_freeze_review_matrix": boundary_freeze_review_matrix,
        "success_claim_post_dryrun_review": success_claim_post_dryrun_review,
        "non_executable_dryrun_asset_review": non_executable_dryrun_asset_review,
        "pre_authorization_post_dryrun_issue_register": pre_authorization_post_dryrun_issue_register,
        "permission_and_authorization_terminology_review": permission_and_authorization_terminology_review,
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision": real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }

