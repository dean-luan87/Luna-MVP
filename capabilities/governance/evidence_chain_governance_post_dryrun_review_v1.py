# -*- coding: utf-8 -*-
"""Evidence Chain Governance Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, evidence non-generation,
success claim blocked, lifecycle/acceptance/source chain boundaries frozen.
Does not generate evidence or allow success claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.evidence_chain_governance_dryrun_v1 import (
    BLOCK_SUCCESS_CLAIM_NOW_TYPES,
    REJECT_ACCEPTANCE_RULES,
)
from capabilities.governance.evidence_chain_governance_planning_v1 import (
    ACCEPTANCE_RULES,
    ELIGIBILITY_CONDITIONS,
    NON_CLAIM_SCENARIOS,
    SOURCE_CHAIN_COMPONENTS,
    UPGRADE_PATHS,
    USAGE_SCOPES,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "evidence_chain_governance_post_dryrun_review_only"
SOURCE_CHAIN = "evidence_chain_governance_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Evidence-Chain-Governance-DryRun-v1-001"
FINAL_DECISION = "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "evidence_chain_governance_dryrun_policy_v1.json", 0),
    ("planning artifact completeness dry-run", "evidence_planning_artifact_completeness_dryrun_v1.json", 12),
    ("lifecycle consumption dry-run", "evidence_lifecycle_consumption_dryrun_v1.json", 14),
    ("source chain consumption dry-run", "evidence_source_chain_consumption_dryrun_v1.json", 14),
    ("usage scope dry-run", "evidence_usage_scope_dryrun_v1.json", 12),
    ("upgrade path dry-run", "evidence_upgrade_path_dryrun_v1.json", 10),
    ("acceptance policy dry-run", "evidence_acceptance_policy_dryrun_v1.json", 12),
    ("non-substitution dry-run", "evidence_non_substitution_dryrun_v1.json", 10),
    ("success claim eligibility dry-run", "evidence_success_claim_eligibility_dryrun_v1.json", 12),
    ("verifier usage dry-run", "evidence_verifier_usage_dryrun_v1.json", 12),
    ("non-claims generation dry-run", "evidence_chain_non_claims_generation_dryrun_v1.json", 12),
    ("dry-run readiness decision", "evidence_chain_dryrun_readiness_decision_v1.json", 0),
)

GENERATION_BLOCK_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("evidence_generated_now", "evidence_generated_now"),
    ("runtime_evidence_generated_now", "runtime_evidence_generated_now"),
    ("success_evidence_generated_now", "success_evidence_generated_now"),
    ("evidence_registry_generated_now", "evidence_registry_generated_now"),
    ("rollback_result_evidence_generated_now", "rollback_result_evidence_generated"),
    ("migration_result_evidence_generated_now", "migration_result_evidence_generated"),
    ("evidence_chain_canonicalization_executed_now", "evidence_chain_canonicalization_executed_now"),
)

SUCCESS_CLAIM_ACCEPTANCE_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("evidence_accepted_for_success_claim_now", "evidence_accepted_for_success_claim_now"),
    ("success_claim_allowed", "success_claim_allowed"),
    ("success_claim_allowed_now", "any_success_claim_allowed_now"),
    ("success_claim_gate_generated_now", "success_claim_gate_generated_now"),
    ("success_claim_gate_enforced_now", "success_claim_gate_enforced_now"),
    ("success_conditions_met", "success_conditions_met"),
    ("success_claim_eligibility_satisfied", "eligibility_satisfied"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_gate_enforced_now": False,
        "success_claim_allowed": False,
        "success_claim_canonicalization_executed_now": False,
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
    readiness = _try_read_json(root / "evidence_chain_dryrun_readiness_decision_v1.json") if root else None
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
        if filename == "evidence_planning_artifact_completeness_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True and count >= 12
        if filename == "evidence_lifecycle_consumption_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
        if filename == "evidence_acceptance_policy_dryrun_v1.json" and isinstance(payload, dict):
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


def _build_generation_block_review(up_summary: Dict[str, Any], artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    lc = artifacts.get("evidence_lifecycle_consumption_dryrun_v1.json") or {}
    lc_rows = lc.get("rows") or []
    rollback_gen = any(
        r.get("evidence_type") == "rollback_result_evidence" and r.get("generation_allowed_now") is True
        for r in lc_rows
    )
    migration_gen = any(
        r.get("evidence_type") == "migration_result_evidence" and r.get("generation_allowed_now") is True
        for r in lc_rows
    )
    observed_flags = {
        "evidence_generated_now": up_summary.get("evidence_generated_now") is True,
        "runtime_evidence_generated_now": up_summary.get("runtime_evidence_generated_now") is True,
        "success_evidence_generated_now": up_summary.get("success_evidence_generated_now") is True,
        "evidence_registry_generated_now": up_summary.get("evidence_registry_generated_now") is True,
        "rollback_result_evidence_generated": rollback_gen,
        "migration_result_evidence_generated": migration_gen,
        "evidence_chain_canonicalization_executed_now": up_summary.get("evidence_chain_canonicalization_executed_now") is True,
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, key in GENERATION_BLOCK_TARGETS:
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
                review_notes="no evidence generation" if review_pass else "evidence generation detected",
            )
        )
    return rows, all_pass


def _build_success_claim_acceptance_block_review(
    up_summary: Dict[str, Any],
    artifacts: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    el = artifacts.get("evidence_success_claim_eligibility_dryrun_v1.json") or {}
    any_allowed = any(r.get("success_claim_allowed_now") is True for r in (el.get("rows") or []))
    any_satisfied = any(r.get("satisfied_now") is True for r in (el.get("rows") or []))
    observed_flags = {
        "evidence_accepted_for_success_claim_now": up_summary.get("evidence_accepted_for_success_claim_now") is True,
        "success_claim_allowed": up_summary.get("success_claim_allowed") is True,
        "any_success_claim_allowed_now": any_allowed,
        "success_claim_gate_generated_now": up_summary.get("success_claim_gate_generated_now") is True,
        "success_claim_gate_enforced_now": up_summary.get("success_claim_gate_enforced_now") is True,
        "success_conditions_met": False,
        "eligibility_satisfied": any_satisfied,
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, key in SUCCESS_CLAIM_ACCEPTANCE_TARGETS:
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
                review_notes="success claim blocked" if review_pass else "success claim boundary release",
            )
        )
    return rows, all_pass


def _build_lifecycle_boundary_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    lc = artifacts.get("evidence_lifecycle_consumption_dryrun_v1.json") or {}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in lc.get("rows") or []:
        etype = row.get("evidence_type")
        can = row.get("can_support_success_claim")
        can_now = row.get("can_support_success_claim_now")
        gen = row.get("generation_allowed_now")
        accepted = row.get("accepted_now")
        if etype in BLOCK_SUCCESS_CLAIM_NOW_TYPES:
            if etype in ("evidence_candidate", "verifier_report", "summary"):
                review_pass = can is False and can_now is False and gen is False and accepted is False
            else:
                review_pass = can_now is False and gen is False and accepted is False
        elif etype in ("success_evidence", "runtime_evidence"):
            review_pass = gen is False and accepted is False
        else:
            review_pass = can_now is False and gen is False and accepted is False
        boundary_release = (
            (etype in BLOCK_SUCCESS_CLAIM_NOW_TYPES and can_now is True)
            or gen is True
            or accepted is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                evidence_type=etype,
                can_support_success_claim=can,
                can_support_success_claim_now=False,
                generation_allowed_now=gen,
                accepted_now=accepted,
                boundary_release_detected=boundary_release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_acceptance_policy_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    ac = artifacts.get("evidence_acceptance_policy_dryrun_v1.json") or {}
    ac_by = {r.get("acceptance_rule"): r for r in (ac.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for rule, target, accepted, rejected in ACCEPTANCE_RULES:
        a = ac_by.get(rule, {})
        accepted_when = str(a.get("accepted_when") or accepted)
        rejected_when = str(a.get("rejected_when") or rejected)
        is_reject = rule in REJECT_ACCEPTANCE_RULES
        reviewed_using_accepted_when = (
            is_reject and "never" in accepted_when.lower()
        ) or not is_reject
        review_pass = (
            a.get("accepted_now") is False
            and reviewed_using_accepted_when
            and a.get("simulated_acceptance_check") is True
        )
        if is_reject and "never" not in accepted_when.lower():
            review_pass = False
        if rule == "reject_summary_as_success_evidence" and "success" in accepted_when.lower():
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                acceptance_rule=rule,
                target_evidence_type=a.get("target_evidence_type") or target,
                accepted_when=accepted_when,
                rejected_when=rejected_when,
                accepted_now=False,
                reviewed_reject_rule_using_accepted_when_contains_never=reviewed_using_accepted_when if is_reject else True,
                review_pass=review_pass,
                review_notes="reject uses accepted_when contains never" if is_reject else "acceptance frozen",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_source_chain_standalone_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    sc = artifacts.get("evidence_source_chain_consumption_dryrun_v1.json") or {}
    sc_by = {r.get("source_chain_component"): r for r in (sc.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in SOURCE_CHAIN_COMPONENTS:
        s = sc_by.get(comp, {})
        review_pass = (
            s.get("can_stand_alone_for_success_claim") is False
            and s.get("generated_now") is False
            and s.get("accepted_as_success_evidence_now", False) is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                source_chain_component=comp,
                required_for_success_claim=s.get("required_for_success_claim") is True,
                can_stand_alone_for_success_claim=False,
                generated_now=False,
                accepted_as_success_evidence_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_usage_and_upgrade_block_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    us = artifacts.get("evidence_usage_scope_dryrun_v1.json") or {}
    up = artifacts.get("evidence_upgrade_path_dryrun_v1.json") or {}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in us.get("rows") or []:
        scope = row.get("usage_scope")
        review_pass = row.get("allowed_now") is False and row.get("simulated_usage_check") is True
        if scope == "success_claim_support" and row.get("allowed_now") is True:
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                item_type="usage_scope",
                item_name=scope,
                allowed_now=False,
                required_preconditions_present=bool(row.get("required_preconditions")),
                forbidden_shortcut_present=bool(row.get("forbidden_evidence_types")),
                review_pass=review_pass,
            )
        )
    for row in up.get("rows") or []:
        path = row.get("upgrade_path")
        review_pass = row.get("allowed_now") is False and row.get("simulated_upgrade_check") is True
        if path in (
            "runtime_evidence_to_success_evidence",
            "source_chain_to_evidence_component_only",
        ) and row.get("allowed_now") is True:
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                item_type="upgrade_path",
                item_name=path,
                allowed_now=False,
                required_preconditions_present=bool(row.get("required_preconditions")),
                forbidden_shortcut_present=bool(row.get("forbidden_shortcut")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 22


def _build_eligibility_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    el = artifacts.get("evidence_success_claim_eligibility_dryrun_v1.json") or {}
    el_by = {r.get("eligibility_condition"): r for r in (el.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cond, types, auth in ELIGIBILITY_CONDITIONS:
        e = el_by.get(cond, {})
        review_pass = (
            e.get("required_for_success_claim") is True
            and e.get("satisfied_now") is False
            and e.get("success_claim_allowed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                eligibility_condition=cond,
                required_for_success_claim=True,
                satisfied_now=False,
                success_claim_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu = artifacts.get("evidence_verifier_usage_dryrun_v1.json") or {}
    vu_by = {r.get("verifier_check_id"): r for r in (vu.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS:
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
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc = artifacts.get("evidence_chain_non_claims_generation_dryrun_v1.json") or {}
    nc_by = {r.get("scenario"): r for r in (nc.get("rows") or [])}
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
    return rows, all_pass and len(rows) >= 12


def run_evidence_chain_governance_post_dryrun_review_v1(
    *,
    evidence_chain_governance_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(evidence_chain_governance_dryrun_root)
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
    if up_readiness.get("ready_for_evidence_chain_governance_post_dryrun_review") is not True:
        blockers.append("not ready_for_evidence_chain_governance_post_dryrun_review")
    if up_summary.get("evidence_chain_dryrun_only") is not True:
        blockers.append("upstream evidence_chain_dryrun_only not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated not true")
    if up_summary.get("evidence_generated_now") is not False:
        blockers.append("evidence_generated_now must be false")
    if up_summary.get("runtime_evidence_generated_now") is not False:
        blockers.append("runtime_evidence_generated_now must be false")
    if up_summary.get("success_evidence_generated_now") is not False:
        blockers.append("success_evidence_generated_now must be false")
    if up_summary.get("evidence_accepted_for_success_claim_now") is not False:
        blockers.append("evidence_accepted_for_success_claim_now must be false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    for flag in (
        "ready_for_evidence_chain_canonicalization_execution",
        "ready_for_evidence_registry_generation",
        "ready_for_evidence_generation",
        "ready_for_runtime_evidence_generation",
        "ready_for_success_evidence_generation",
        "ready_for_success_claim_allowance",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    comp_rows, comp_pass = _build_completeness_review(artifacts)
    gen_rows, gen_pass = _build_generation_block_review(up_summary, artifacts)
    sc_rows, sc_pass = _build_success_claim_acceptance_block_review(up_summary, artifacts)
    lc_rows, lc_pass = _build_lifecycle_boundary_review(artifacts)
    ac_rows, ac_pass = _build_acceptance_policy_review(artifacts)
    src_rows, src_pass = _build_source_chain_standalone_review(artifacts)
    uu_rows, uu_pass = _build_usage_and_upgrade_block_review(artifacts)
    el_rows, el_pass = _build_eligibility_review(artifacts)
    vu_rows, vu_pass = _build_verifier_review(artifacts)
    nc_rows, nc_pass = _build_non_claims_review(artifacts)

    review_pass = (
        comp_pass
        and gen_pass
        and sc_pass
        and lc_pass
        and ac_pass
        and src_pass
        and uu_pass
        and el_pass
        and vu_pass
        and nc_pass
        and not blockers
    )
    boundary_ok = review_pass

    evidence_chain_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_evidence_chain_governance_post_dryrun_review_observed=up_readiness.get(
            "ready_for_evidence_chain_governance_post_dryrun_review"
        )
        is True,
    )

    evidence_dryrun_completeness_review = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_review_meta(),
    }
    evidence_generation_block_review = {
        "rows": gen_rows,
        "row_count": len(gen_rows),
        "all_pass": gen_pass,
        **_review_meta(),
    }
    evidence_success_claim_acceptance_block_review = {
        "rows": sc_rows,
        "row_count": len(sc_rows),
        "all_pass": sc_pass,
        **_review_meta(),
    }
    evidence_lifecycle_boundary_review = {
        "rows": lc_rows,
        "row_count": len(lc_rows),
        "all_pass": lc_pass,
        **_review_meta(),
    }
    evidence_acceptance_policy_review = {
        "rows": ac_rows,
        "row_count": len(ac_rows),
        "all_pass": ac_pass,
        **_review_meta(),
    }
    evidence_source_chain_standalone_review = {
        "rows": src_rows,
        "row_count": len(src_rows),
        "all_pass": src_pass,
        **_review_meta(),
    }
    evidence_usage_and_upgrade_block_review = {
        "rows": uu_rows,
        "row_count": len(uu_rows),
        "all_pass": uu_pass,
        **_review_meta(),
    }
    evidence_eligibility_review = {
        "rows": el_rows,
        "row_count": len(el_rows),
        "all_pass": el_pass,
        **_review_meta(),
    }
    evidence_verifier_non_modification_review = {
        "rows": vu_rows,
        "row_count": len(vu_rows),
        "all_pass": vu_pass,
        **_review_meta(),
    }
    evidence_non_claims_non_write_review = {
        "rows": nc_rows,
        "row_count": len(nc_rows),
        "all_pass": nc_pass,
        **_review_meta(),
    }

    evidence_chain_post_dryrun_review_readiness_decision = {
        "ready_for_evidence_chain_governance_roadmap_decision": boundary_ok,
        "ready_for_evidence_chain_canonicalization_execution": False,
        "ready_for_evidence_registry_generation": False,
        "ready_for_evidence_generation": False,
        "ready_for_runtime_evidence_generation": False,
        "ready_for_success_evidence_generation": False,
        "ready_for_evidence_acceptance_for_success_claim": False,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": comp_pass,
        "evidence_generation_block_review_pass": gen_pass,
        "success_claim_acceptance_block_review_pass": sc_pass,
        "lifecycle_boundary_review_pass": lc_pass,
        "acceptance_policy_review_pass": ac_pass,
        "source_chain_standalone_review_pass": src_pass,
        "usage_and_upgrade_block_review_pass": uu_pass,
        "eligibility_review_pass": el_pass,
        "verifier_non_modification_review_pass": vu_pass,
        "non_claims_non_write_review_pass": nc_pass,
        "evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "evidence_chain_governance_dryrun_input_loaded": upstream["loaded"],
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "evidence_chain_governance_dryrun",
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
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review pass; no evidence generated; success claim blocked; roadmap decision next",
        **_review_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "evidence_chain_post_dryrun_review_policy": evidence_chain_post_dryrun_review_policy,
        "evidence_dryrun_completeness_review": evidence_dryrun_completeness_review,
        "evidence_generation_block_review": evidence_generation_block_review,
        "evidence_success_claim_acceptance_block_review": evidence_success_claim_acceptance_block_review,
        "evidence_lifecycle_boundary_review": evidence_lifecycle_boundary_review,
        "evidence_acceptance_policy_review": evidence_acceptance_policy_review,
        "evidence_source_chain_standalone_review": evidence_source_chain_standalone_review,
        "evidence_usage_and_upgrade_block_review": evidence_usage_and_upgrade_block_review,
        "evidence_eligibility_review": evidence_eligibility_review,
        "evidence_verifier_non_modification_review": evidence_verifier_non_modification_review,
        "evidence_non_claims_non_write_review": evidence_non_claims_non_write_review,
        "evidence_chain_post_dryrun_review_readiness_decision": evidence_chain_post_dryrun_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
