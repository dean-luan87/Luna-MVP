# -*- coding: utf-8 -*-
"""Success Claim Gate Canonicalization Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, gate non-generation,
success claim blocked, evidence boundary frozen, authorization not satisfied.
Does not generate gate, allow success claim, or produce evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.governance.success_claim_gate_canonicalization_planning_v1 import (
    AUTH_DEPS,
    EVIDENCE_BOUNDARY_TYPES,
    FORBIDDEN_INTERPRETATIONS,
    NON_CLAIM_SCENARIOS,
    OUTPUT_PLAN_ARTIFACTS,
    VERIFIER_CHECKS,
)

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "success_claim_gate_canonicalization_post_dryrun_review_only"
SOURCE_CHAIN = "success_claim_gate_canonicalization_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001"
FINAL_DECISION = "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "success_claim_gate_canonicalization_dryrun_policy_v1.json", 0),
    ("planning artifact completeness dry-run", "success_claim_planning_artifact_completeness_dryrun_v1.json", 10),
    ("gate condition dry-run", "success_claim_gate_condition_dryrun_v1.json", 12),
    ("forbidden interpretation dry-run", "success_claim_forbidden_interpretation_dryrun_v1.json", 14),
    ("evidence boundary dry-run", "success_claim_evidence_boundary_dryrun_v1.json", 12),
    ("authorization dependency dry-run", "success_claim_authorization_dependency_dryrun_v1.json", 10),
    ("non-claims generation dry-run", "success_claim_non_claims_generation_dryrun_v1.json", 15),
    ("verifier usage dry-run", "success_claim_verifier_usage_dryrun_v1.json", 14),
    ("gate output artifact dry-run", "success_claim_gate_output_artifact_dryrun_v1.json", 9),
    ("cross-artifact consistency dry-run", "success_claim_cross_artifact_consistency_dryrun_v1.json", 12),
    ("dry-run readiness decision", "success_claim_gate_dryrun_readiness_decision_v1.json", 0),
)

GATE_NON_GENERATION_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("success_claim_gate_generated_now", "success_claim_gate_generated_now"),
    ("all planned gate artifacts not_generated_now", "all_output_not_generated"),
    ("formal success_claim_gate_policy_v1.json not generated", "formal_policy_generated"),
    ("formal success_claim_condition_matrix_v1.json not generated", "formal_condition_generated"),
    ("formal success_claim_gate_readiness_decision_v1.json not generated", "formal_readiness_generated"),
    ("success_claim_gate_enforced_now", "success_claim_gate_enforced_now"),
)

ALLOWANCE_BLOCK_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("success_claim_allowed", "success_claim_allowed"),
    ("success_claim_allowed_now across dry-run", "any_success_claim_allowed_now"),
    ("success_claim_gate_enforced_now", "gate_enforced"),
    ("success_claim_canonicalization_executed_now", "canonicalization_executed"),
    ("success_conditions_met", "success_conditions_met"),
    ("real_execution_observed", "real_execution_observed"),
    ("authorization_granted_now", "authorization_granted_now"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "success_claim_canonicalization_executed_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_gate_enforced_now": False,
        "success_claim_allowed": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "permission_semantics_canonicalization_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "debt_fix_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _review_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _row_count(payload: Dict[str, Any]) -> int:
    if "row_count" in payload:
        return int(payload["row_count"])
    rows = payload.get("rows")
    return len(rows) if isinstance(rows, list) else 0


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "success_claim_gate_dryrun_readiness_decision_v1.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for _, filename, _ in DRYRUN_ARTIFACTS:
            payload = _try_read_json(root / filename)
            if payload is None:
                missing.append(filename)
            else:
                art[filename] = payload
    loaded = summary is not None and verifier is not None and readiness is not None and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary or {},
        "verifier": verifier or {},
        "readiness": readiness or {},
        "artifacts": art,
        "missing": missing,
    }


def _build_completeness_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in DRYRUN_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok and count_ok
        if filename == "success_claim_planning_artifact_completeness_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True and count >= 10
        if filename == "success_claim_evidence_boundary_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
        if filename == "success_claim_cross_artifact_consistency_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
        review_pass = observed and schema_ok and count_ok and semantic_ok
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_name=name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_ok,
                count_requirement_pass=count_ok,
                semantic_requirement_pass=semantic_ok,
                review_status="pass" if review_pass else "fail",
                review_notes=f"count={count} min={min_count}",
            )
        )
    return rows, all_pass


def _build_gate_non_generation_review(
    up_summary: Dict[str, Any],
    artifacts: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    output_rows = (artifacts.get("success_claim_gate_output_artifact_dryrun_v1.json") or {}).get("rows") or []
    all_not_gen = all(r.get("not_generated_now") is True for r in output_rows) if output_rows else False
    def _planned_not_generated(name: str) -> bool:
        row = next((r for r in output_rows if r.get("planned_artifact") == name), None)
        return row is not None and row.get("not_generated_now") is True

    observed_flags = {
        "success_claim_gate_generated_now": up_summary.get("success_claim_gate_generated_now") is True,
        "all_output_not_generated": not all_not_gen,
        "formal_policy_generated": not _planned_not_generated("success_claim_gate_policy_v1.json"),
        "formal_condition_generated": not _planned_not_generated("success_claim_condition_matrix_v1.json"),
        "formal_readiness_generated": not _planned_not_generated("success_claim_gate_readiness_decision_v1.json"),
        "success_claim_gate_enforced_now": up_summary.get("success_claim_gate_enforced_now") is True,
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, key in GATE_NON_GENERATION_TARGETS:
        obs = observed_flags.get(key, False)
        violation = obs is True
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_value=False,
                observed_value=obs,
                violation_detected=violation,
                review_pass=review_pass,
                review_notes="gate not generated" if review_pass else "gate generation signal detected",
            )
        )
    return rows, all_pass


def _build_allowance_block_review(
    up_summary: Dict[str, Any],
    artifacts: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    any_allowed_now = False
    for key, payload in artifacts.items():
        if key.endswith(".json") and isinstance(payload, dict):
            for row in payload.get("rows") or []:
                if row.get("success_claim_allowed_now") is True or row.get("success_claim_allowed") is True:
                    any_allowed_now = True
    observed_flags = {
        "success_claim_allowed": up_summary.get("success_claim_allowed") is True,
        "any_success_claim_allowed_now": any_allowed_now,
        "gate_enforced": up_summary.get("success_claim_gate_enforced_now") is True,
        "canonicalization_executed": up_summary.get("success_claim_canonicalization_executed_now") is True,
        "success_conditions_met": False,
        "real_execution_observed": up_summary.get("execution_committed") is True,
        "authorization_granted_now": up_summary.get("authorization_granted_now") is True,
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, key in ALLOWANCE_BLOCK_TARGETS:
        obs = observed_flags.get(key, False)
        violation = obs is True
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_value=False,
                observed_value=obs,
                violation_detected=violation,
                review_pass=review_pass,
                review_notes="success claim blocked" if review_pass else "success claim allowance detected",
            )
        )
    return rows, all_pass


def _build_evidence_boundary_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    boundary = artifacts.get("success_claim_evidence_boundary_dryrun_v1.json") or {}
    by_type = {r.get("artifact_or_evidence_type"): r for r in (boundary.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for atype, usage, can_support_planned, _reason, _forbidden_sub in EVIDENCE_BOUNDARY_TYPES:
        b = by_type.get(atype, {})
        can = b.get("can_support_success_claim")
        if atype in ("verifier report", "summary", "candidate evidence"):
            expected_now = False
        else:
            expected_now = can if can is not None else can_support_planned
        generated = b.get("success_evidence_generated_now") is True or b.get("runtime_evidence_generated_now") is True
        accepted = b.get("accepted_as_success_evidence_now") is True
        boundary_release = (can is True and expected_now is False) or generated or accepted
        review_pass = (
            b.get("artifact_or_evidence_type") == atype
            and can == expected_now
            and not generated
            and not accepted
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_or_evidence_type=atype,
                can_support_success_claim=can if can is not None else expected_now,
                expected_can_support_now=expected_now,
                generated_now=False,
                accepted_as_success_evidence_now=False,
                boundary_release_detected=boundary_release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_authorization_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    auth_by = {
        r.get("authorization_dependency"): r
        for r in (artifacts.get("success_claim_authorization_dependency_dryrun_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for dep, _actor, _evidence in AUTH_DEPS:
        a = auth_by.get(dep, {})
        review_pass = (
            a.get("required_for_success_claim") is True
            and a.get("satisfied_now") is False
            and a.get("authorization_granted_now") is False
            and a.get("success_claim_allowed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                authorization_dependency=dep,
                required_for_success_claim=True,
                satisfied_now=False,
                authorization_granted_now=False,
                success_claim_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_forbidden_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    fb_by = {
        r.get("forbidden_id"): r
        for r in (artifacts.get("success_claim_forbidden_interpretation_dryrun_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for fid, interp, _reason, _terms, _nc in FORBIDDEN_INTERPRETATIONS:
        f = fb_by.get(fid, {})
        review_pass = (
            f.get("simulated_check") is True
            and f.get("enforced_now") is False
            and f.get("verifier_modified_now") is False
            and f.get("success_claim_allowed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                forbidden_id=fid,
                forbidden_interpretation=f.get("forbidden_interpretation") or interp,
                simulated_check_observed=f.get("simulated_check") is True,
                enforced_now=False,
                verifier_modified_now=False,
                success_claim_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_verifier_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu_by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("success_claim_verifier_usage_dryrun_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, _phases, _fields, _fail, _sev in VERIFIER_CHECKS:
        v = vu_by.get(vid, {})
        review_pass = (
            v.get("simulated_verifier_consumption") is True
            and v.get("verifier_modified_now") is False
            and v.get("enforced_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                verifier_check_id=vid,
                check_name=v.get("check_name") or name,
                simulated_verifier_consumption=v.get("simulated_verifier_consumption") is True,
                verifier_modified_now=False,
                enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_non_claims_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc_by = {r.get("scenario"): r for r in (artifacts.get("success_claim_non_claims_generation_dryrun_v1.json") or {}).get("rows") or []}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        review_pass = (
            bool(n.get("required_non_claim"))
            and n.get("simulated_generation") is True
            and n.get("generated_now") is False
            and n.get("template_modified_now", n.get("phase_template_modified_now")) is False
            and n.get("documentation_auto_sync_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                scenario=scenario,
                required_non_claim=n.get("required_non_claim") or non_claim,
                simulated_generation=n.get("simulated_generation") is True,
                generated_now=False,
                template_modified_now=False,
                documentation_auto_sync_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 15


def _build_cross_artifact_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    cross = artifacts.get("success_claim_cross_artifact_consistency_dryrun_v1.json") or {}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in cross.get("rows") or []:
        review_pass = row.get("consistency_pass") is True and row.get("enforced_now") is False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                consistency_check_id=row.get("consistency_check_id"),
                check_description=row.get("check_description"),
                source_artifacts=row.get("source_artifacts"),
                consistency_pass=row.get("consistency_pass") is True,
                enforced_now=False,
                review_pass=review_pass,
                review_notes=row.get("dryrun_notes", "cross-artifact post-review"),
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_success_claim_gate_canonicalization_post_dryrun_review_v1(
    *,
    success_claim_gate_canonicalization_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(success_claim_gate_canonicalization_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_readiness.get("ready_for_success_claim_gate_canonicalization_post_dryrun_review") is not True:
        blockers.append("not ready_for_success_claim_gate_canonicalization_post_dryrun_review")
    if up_summary.get("success_claim_gate_dryrun_only") is not True:
        blockers.append("upstream success_claim_gate_dryrun_only not true")
    if up_summary.get("success_claim_gate_generated_now") is not False:
        blockers.append("success_claim_gate_generated_now must be false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    if up_readiness.get("ready_for_success_claim_gate_generation") is not False:
        blockers.append("ready_for_success_claim_gate_generation must remain false")
    if up_readiness.get("ready_for_success_claim_allowance") is not False:
        blockers.append("ready_for_success_claim_allowance must remain false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    boundary_dry = artifacts.get("success_claim_evidence_boundary_dryrun_v1.json") or {}
    by_type = {r.get("artifact_or_evidence_type"): r for r in (boundary_dry.get("rows") or [])}
    if by_type.get("verifier report", {}).get("can_support_success_claim") is not False:
        blockers.append("verifier_report can_support_success_claim must be false")
    if by_type.get("summary", {}).get("can_support_success_claim") is not False:
        blockers.append("summary can_support_success_claim must be false")
    if by_type.get("candidate evidence", {}).get("can_support_success_claim") is not False:
        blockers.append("candidate evidence can_support_success_claim must be false")

    comp_rows, comp_pass = _build_completeness_review(artifacts)
    gate_rows, gate_pass = _build_gate_non_generation_review(up_summary, artifacts)
    allow_rows, allow_pass = _build_allowance_block_review(up_summary, artifacts)
    evidence_rows, evidence_pass = _build_evidence_boundary_review(artifacts)
    auth_rows, auth_pass = _build_authorization_review(artifacts)
    forbidden_rows, forbidden_pass = _build_forbidden_review(artifacts)
    verifier_rows, verifier_pass = _build_verifier_review(artifacts)
    nclaims_rows, nclaims_pass = _build_non_claims_review(artifacts)
    cross_rows, cross_pass = _build_cross_artifact_review(artifacts)

    review_pass = (
        comp_pass
        and gate_pass
        and allow_pass
        and evidence_pass
        and auth_pass
        and forbidden_pass
        and verifier_pass
        and nclaims_pass
        and cross_pass
        and not blockers
    )
    boundary_ok = review_pass

    success_claim_gate_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_success_claim_gate_canonicalization_post_dryrun_review_observed=up_readiness.get(
            "ready_for_success_claim_gate_canonicalization_post_dryrun_review"
        )
        is True,
    )

    success_claim_dryrun_completeness_review = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_review_meta(),
    }
    success_claim_gate_non_generation_review = {
        "rows": gate_rows,
        "row_count": len(gate_rows),
        "all_pass": gate_pass,
        **_review_meta(),
    }
    success_claim_allowance_block_review = {
        "rows": allow_rows,
        "row_count": len(allow_rows),
        "all_pass": allow_pass,
        **_review_meta(),
    }
    success_claim_evidence_boundary_review = {
        "rows": evidence_rows,
        "row_count": len(evidence_rows),
        "all_pass": evidence_pass,
        **_review_meta(),
    }
    success_claim_authorization_dependency_review = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        "all_pass": auth_pass,
        **_review_meta(),
    }
    success_claim_forbidden_interpretation_review = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_review_meta(),
    }
    success_claim_verifier_non_modification_review = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_review_meta(),
    }
    success_claim_non_claims_non_write_review = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_review_meta(),
    }
    success_claim_cross_artifact_consistency_review = {
        "rows": cross_rows,
        "row_count": len(cross_rows),
        "all_pass": cross_pass,
        **_review_meta(),
    }

    success_claim_gate_post_dryrun_review_readiness_decision = {
        "ready_for_success_claim_gate_canonicalization_roadmap_decision": boundary_ok,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_gate_execution": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_success_claim_enforcement": False,
        "ready_for_success_evidence_generation": False,
        "ready_for_runtime_evidence_generation": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_debt_fix_execution": False,
        "ready_for_permission_semantics_canonicalization_execution": False,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": comp_pass,
        "gate_non_generation_review_pass": gate_pass,
        "allowance_block_review_pass": allow_pass,
        "evidence_boundary_review_pass": evidence_pass,
        "authorization_dependency_review_pass": auth_pass,
        "forbidden_interpretation_review_pass": forbidden_pass,
        "verifier_non_modification_review_pass": verifier_pass,
        "non_claims_non_write_review_pass": nclaims_pass,
        "cross_artifact_consistency_review_pass": cross_pass,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "success_claim_gate_canonicalization_dryrun_input_loaded": upstream["loaded"],
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "success_claim_gate_canonicalization_dryrun",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_review_meta(),
            }
        ],
        "row_count": 1,
        **_review_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review pass; gate not generated; success claim blocked; roadmap decision next",
        **_review_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "success_claim_gate_post_dryrun_review_policy": success_claim_gate_post_dryrun_review_policy,
        "success_claim_dryrun_completeness_review": success_claim_dryrun_completeness_review,
        "success_claim_gate_non_generation_review": success_claim_gate_non_generation_review,
        "success_claim_allowance_block_review": success_claim_allowance_block_review,
        "success_claim_evidence_boundary_review": success_claim_evidence_boundary_review,
        "success_claim_authorization_dependency_review": success_claim_authorization_dependency_review,
        "success_claim_forbidden_interpretation_review": success_claim_forbidden_interpretation_review,
        "success_claim_verifier_non_modification_review": success_claim_verifier_non_modification_review,
        "success_claim_non_claims_non_write_review": success_claim_non_claims_non_write_review,
        "success_claim_cross_artifact_consistency_review": success_claim_cross_artifact_consistency_review,
        "success_claim_gate_post_dryrun_review_readiness_decision": success_claim_gate_post_dryrun_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
