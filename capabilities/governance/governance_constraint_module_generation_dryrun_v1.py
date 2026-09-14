# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation DryRun v1.

Module generation dry-run only: simulate consumption of planning output shapes.
Does not generate constraint modules, modify verifiers/templates, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_planning_v1 import (
    CANONICAL_CONTRACT_SECTIONS,
    EXTENSION_RULES,
    INHERITANCE_MATRIX_FIELDS,
    LEGACY_ABSORPTION_SECTIONS,
    NON_CLAIMS_AND_SHORTCUTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001"
DRYRUN_SCOPE = "governance_constraint_module_generation_dryrun_only"
SOURCE_CHAIN = "governance_constraint_module_generation_dryrun_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_READY_FOR_DRYRUN"

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

INDEPENDENT_CONSUMPTION_DOMAINS: Tuple[str, ...] = (
    "Evidence Chain",
    "Owner/Operator Approval",
    "Boundary Object Registry",
    "Registry Generation",
    "Protected Asset / HR / DnAE",
    "File Operation",
)

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_planning_policy_v1.json",
    "canonical_phase_contract_output_shape_planning_v1.json",
    "domain_constraint_registry_output_shape_planning_v1.json",
    "phase_inheritance_matrix_output_shape_planning_v1.json",
    "canonical_frozen_fields_output_shape_planning_v1.json",
    "phase_mode_lifecycle_output_shape_planning_v1.json",
    "constraint_required_fields_output_shape_planning_v1.json",
    "verifier_baseline_output_shape_planning_v1.json",
    "non_claims_and_forbidden_shortcut_library_planning_v1.json",
    "constraint_extension_rule_planning_v1.json",
    "legacy_absorption_policy_output_shape_planning_v1.json",
    "governance_constraint_module_generation_planning_readiness_decision_v1.json",
)

DRYRUN_NON_CLAIMS_EXTRA: Tuple[Tuple[str, str, str], ...] = (
    ("NC16", "non_claim", "domain constraint inheritance ≠ enforcement"),
    ("NC17", "non_claim", "canonical contract planned ≠ phase template modified"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "governance_constraint_module_generation_dryrun_only": True,
        "simulated": True,
        "future_verifier_consumption_simulated": True,
        "future_phase_template_consumption_simulated": True,
        "future_cursor_instruction_consumption_simulated": True,
        "future_mainline_phase_consumption_simulated": True,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_integration_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "legacy_chain_deprecated_now": False,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "file_operation_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "main_migration_chain_resumed_now": False,
        "main_migration_chain_paused": MAIN_MIGRATION_PAUSED,
        "main_migration_resume_phase": MAIN_MIGRATION_RESUME_PHASE,
        "runtime_invoked": False,
        "execution_committed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _dryrun_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_dryrun_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(
        root / "governance_constraint_module_generation_planning_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
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


def _simulate_contract_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("contract_section"): r for r in (planning.get("rows") or [])}
    for section, _, _ in CANONICAL_CONTRACT_SECTIONS:
        pr = planning_rows.get(section, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("used_by_future_phase") is True
            and pr.get("used_by_future_verifier") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                contract_section=section,
                required_fields=pr.get("required_fields") or [f"{section.replace(' ', '_')}_fields"],
                used_by_future_phase=True,
                used_by_future_verifier=True,
                simulated_contract_consumption=True,
                contract_generated_now=False,
                constraint_enforced_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_domain_registry_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        name = r.get("domain_constraint_name")
        has_domain_rules = bool(r.get("domain_specific_forbidden_shortcuts")) and bool(
            r.get("domain_specific_non_claims")
        )
        independent_path = name in INDEPENDENT_CONSUMPTION_DOMAINS
        review_pass = (
            r.get("not_generated_now") is True
            and r.get("inherits_canonical_contract") is True
            and has_domain_rules
        )
        if independent_path and not has_domain_rules:
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                domain_constraint_name=name,
                inherits_canonical_contract=r.get("inherits_canonical_contract"),
                domain_specific_required_fields=r.get("domain_specific_required_fields"),
                domain_specific_forbidden_shortcuts=r.get("domain_specific_forbidden_shortcuts"),
                domain_specific_no_go_conditions=r.get("domain_specific_no_go_conditions"),
                domain_specific_non_claims=r.get("domain_specific_non_claims"),
                independent_consumption_path=independent_path,
                domain_differentiation_preserved=has_domain_rules,
                simulated_domain_registry_consumption=True,
                domain_registry_generated_now=False,
                domain_constraint_registered_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_inheritance_matrix_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("matrix_field"): r for r in (planning.get("rows") or [])}
    for field, _ in INHERITANCE_MATRIX_FIELDS:
        pr = planning_rows.get(field, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("used_by_cursor_instruction") is True
            and pr.get("used_by_verifier") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                matrix_field=field,
                required_for_new_phase=pr.get("required_for_new_phase", True),
                used_by_cursor_instruction=True,
                used_by_verifier=True,
                simulated_inheritance_matrix_consumption=True,
                inheritance_matrix_generated_now=False,
                phase_template_modified_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _is_false_value(value: Any) -> bool:
    return value is False or value == "false"


def _simulate_frozen_fields_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        review_pass = (
            r.get("not_generated_now") is True
            and r.get("override_allowed") is False
            and _is_false_value(r.get("default_value"))
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                canonical_field_pattern=r.get("canonical_field_pattern"),
                default_value=r.get("default_value", False),
                applies_to_phase_modes=r.get("applies_to_phase_modes"),
                applies_to_domain_constraints=r.get("applies_to_domain_constraints"),
                override_allowed=False,
                simulated_frozen_field_consumption=True,
                frozen_fields_library_generated_now=False,
                field_enforced_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 25


def _simulate_lifecycle_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        review_pass = (
            r.get("not_generated_now") is True
            and bool(r.get("forbidden_actions"))
            and bool(r.get("allowed_actions"))
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                phase_mode=r.get("phase_mode"),
                canonical_meaning=r.get("canonical_meaning"),
                allowed_actions=r.get("allowed_actions"),
                forbidden_actions=r.get("forbidden_actions"),
                required_readiness_fields=r.get("required_readiness_fields"),
                required_non_claims=r.get("required_non_claims"),
                next_allowed_phase_modes=r.get("next_allowed_phase_modes"),
                simulated_lifecycle_consumption=True,
                lifecycle_contract_generated_now=False,
                phase_template_modified_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 15


def _simulate_required_fields_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        review_pass = r.get("not_generated_now") is True and bool(r.get("required_fields"))
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                required_field_group=r.get("required_field_group"),
                required_fields=r.get("required_fields"),
                applies_to_phase_modes=r.get("applies_to_phase_modes"),
                applies_to_domain_constraints=r.get("applies_to_domain_constraints"),
                simulated_required_fields_consumption=True,
                required_fields_module_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_verifier_baseline_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        review_pass = (
            r.get("not_generated_now") is True
            and bool(r.get("failure_condition"))
            and r.get("severity") == "critical"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                baseline_check_id=r.get("baseline_check_id"),
                check_name=r.get("check_name"),
                required_for_phase_modes=r.get("required_for_phase_modes"),
                required_for_domain_constraints=r.get("required_for_domain_constraints"),
                failure_condition=r.get("failure_condition"),
                severity=r.get("severity"),
                simulated_verifier_baseline_consumption=True,
                verifier_baseline_generated_now=False,
                verifier_modified_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 15


def _simulate_non_claims_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_by_id = {r.get("rule_id"): r for r in (planning.get("rows") or [])}
    all_rules = list(NON_CLAIMS_AND_SHORTCUTS) + list(DRYRUN_NON_CLAIMS_EXTRA)
    for rule_id, rule_type, statement in all_rules:
        pr = planning_by_id.get(rule_id, {})
        from_planning = bool(pr)
        review_pass = from_planning and pr.get("not_generated_now") is True if from_planning else True
        if rule_id in ("NC16", "NC17"):
            review_pass = True
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                rule_id=rule_id,
                rule_type=rule_type,
                canonical_statement=statement,
                applies_to_phase_modes=pr.get("applies_to_phase_modes")
                or ["Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision"],
                applies_to_domain_constraints=pr.get("applies_to_domain_constraints") or ["all"],
                simulated_rule_consumption=True,
                library_generated_now=False,
                non_claim_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 17


def _simulate_extension_rule_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_by_rule = {r.get("extension_rule"): r for r in (planning.get("rows") or [])}
    for rule in EXTENSION_RULES:
        pr = planning_by_rule.get(rule, {})
        review_pass = pr.get("not_generated_now") is True if pr else False
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                extension_rule=rule,
                failure_condition=pr.get("failure_condition") or f"violation of {rule}",
                used_by_future_cursor_instruction=True,
                used_by_future_verifier=True,
                simulated_extension_rule_consumption=True,
                extension_rule_module_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_legacy_absorption_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("policy_section"): r for r in (planning.get("rows") or [])}
    for section, _ in LEGACY_ABSORPTION_SECTIONS:
        pr = planning_rows.get(section, {})
        review_pass = pr.get("not_generated_now") is True and bool(pr.get("policy_rule"))
        if section == "rewrite policy" and pr:
            review_pass = review_pass and "do_not_rewrite" in str(pr.get("policy_rule", ""))
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                policy_section=section,
                policy_rule=pr.get("policy_rule"),
                used_by_future_documentation=True,
                used_by_future_verifier=True,
                simulated_legacy_absorption_consumption=True,
                legacy_absorption_policy_generated_now=False,
                legacy_document_rewritten_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_governance_constraint_module_generation_dryrun_v1(
    *,
    governance_constraint_module_generation_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_planning_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream planning verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_dryrun") is not True:
        blockers.append("upstream not ready_for_governance_constraint_module_generation_dryrun")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("governance_constraint_module_generation_planning_only") is not True:
        blockers.append("upstream must be planning_only")

    for flag in (
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_module_registered_now",
        "constraint_enforced_now",
        "verifier_integration_executed_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "automation_implemented_now",
        "documentation_auto_sync_executed_now",
        "legacy_phase_modified_now",
        "legacy_document_rewritten_now",
        "legacy_eval_out_modified_now",
        "legacy_verifier_rerun_now",
        "legacy_chain_deprecated_now",
        "main_migration_chain_resumed_now",
        "file_operation_executed_now",
        "authorization_granted_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")

    if up_summary.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if up_summary.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")
    if up_summary.get("all_not_generated_now") is not True:
        blockers.append("upstream all planned outputs must have not_generated_now=true")

    counts_ok_upstream = (
        up_summary.get("canonical_contract_section_count", 0) >= 12
        and up_summary.get("domain_constraint_count", 0) >= 12
        and up_summary.get("frozen_field_pattern_count", 0) >= 25
        and up_summary.get("phase_mode_count", 0) >= 15
        and up_summary.get("verifier_baseline_check_count", 0) >= 15
        and up_summary.get("non_claims_rule_count", 0) >= 15
        and up_summary.get("extension_rule_count", 0) >= 12
        and up_summary.get("legacy_absorption_section_count", 0) >= 12
    )
    if not counts_ok_upstream:
        blockers.append("upstream planning coverage requirements not met")

    for flag in (
        "ready_for_governance_constraint_module_generation",
        "ready_for_canonical_phase_template_generation",
        "ready_for_constraint_module_registration",
        "ready_for_constraint_enforcement",
        "ready_for_verifier_integration",
        "ready_for_phase_template_modification",
        "ready_for_automation_implementation",
        "ready_for_documentation_auto_sync",
        "ready_for_legacy_document_rewrite",
        "ready_to_resume_main_migration_chain",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")

    contract_rows, contract_pass = _simulate_contract_consumption(
        up_art.get("canonical_phase_contract_output_shape_planning_v1.json", {})
    )
    domain_rows, domain_pass = _simulate_domain_registry_consumption(
        up_art.get("domain_constraint_registry_output_shape_planning_v1.json", {})
    )
    inheritance_rows, inheritance_pass = _simulate_inheritance_matrix_consumption(
        up_art.get("phase_inheritance_matrix_output_shape_planning_v1.json", {})
    )
    frozen_rows, frozen_pass = _simulate_frozen_fields_consumption(
        up_art.get("canonical_frozen_fields_output_shape_planning_v1.json", {})
    )
    lifecycle_rows, lifecycle_pass = _simulate_lifecycle_consumption(
        up_art.get("phase_mode_lifecycle_output_shape_planning_v1.json", {})
    )
    required_rows, required_pass = _simulate_required_fields_consumption(
        up_art.get("constraint_required_fields_output_shape_planning_v1.json", {})
    )
    baseline_rows, baseline_pass = _simulate_verifier_baseline_consumption(
        up_art.get("verifier_baseline_output_shape_planning_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _simulate_non_claims_consumption(
        up_art.get("non_claims_and_forbidden_shortcut_library_planning_v1.json", {})
    )
    extension_rows, extension_pass = _simulate_extension_rule_consumption(
        up_art.get("constraint_extension_rule_planning_v1.json", {})
    )
    absorption_rows, absorption_pass = _simulate_legacy_absorption_consumption(
        up_art.get("legacy_absorption_policy_output_shape_planning_v1.json", {})
    )

    sim_pass = all(
        (
            contract_pass,
            domain_pass,
            inheritance_pass,
            frozen_pass,
            lifecycle_pass,
            required_pass,
            baseline_pass,
            non_claims_pass,
            extension_pass,
            absorption_pass,
        )
    )
    if not sim_pass:
        blockers.append("one or more consumption dry-run simulations failed")

    independent_ok = all(
        r.get("independent_consumption_path") is True and r.get("dryrun_status") == "pass"
        for r in domain_rows
        if r.get("domain_constraint_name") in INDEPENDENT_CONSUMPTION_DOMAINS
    )
    if not independent_ok:
        blockers.append("independent domain consumption paths must pass")

    if any(r.get("field_enforced_now") for r in frozen_rows):
        blockers.append("frozen fields must not be enforced")
    if any(r.get("verifier_modified_now") for r in baseline_rows):
        blockers.append("verifier baseline must not be integrated")
    if any(r.get("phase_template_modified_now") for r in lifecycle_rows + inheritance_rows):
        blockers.append("phase template must not be modified")
    if any(r.get("legacy_document_rewritten_now") for r in absorption_rows):
        blockers.append("legacy absorption must not rewrite documents")

    dryrun_ready = sim_pass and independent_ok and not blockers
    boundary_ok = dryrun_ready

    governance_constraint_module_generation_dryrun_policy = _dryrun_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    canonical_phase_contract_consumption_dryrun = {
        "rows": contract_rows,
        "row_count": len(contract_rows),
        "all_pass": contract_pass,
        "future_phase_consumption_simulated": True,
        "future_verifier_consumption_simulated": True,
        **_dryrun_meta(),
    }
    domain_constraint_registry_consumption_dryrun = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        **_dryrun_meta(),
    }
    phase_inheritance_matrix_consumption_dryrun = {
        "rows": inheritance_rows,
        "row_count": len(inheritance_rows),
        "all_pass": inheritance_pass,
        "future_cursor_instruction_consumption_simulated": True,
        **_dryrun_meta(),
    }
    canonical_frozen_fields_consumption_dryrun = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "all_pass": frozen_pass,
        "field_enforced_now": False,
        **_dryrun_meta(),
    }
    phase_mode_lifecycle_consumption_dryrun = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_pass": lifecycle_pass,
        "future_phase_template_consumption_simulated": True,
        "phase_template_modified_now": False,
        **_dryrun_meta(),
    }
    constraint_required_fields_consumption_dryrun = {
        "rows": required_rows,
        "row_count": len(required_rows),
        "all_pass": required_pass,
        **_dryrun_meta(),
    }
    verifier_baseline_consumption_dryrun = {
        "rows": baseline_rows,
        "row_count": len(baseline_rows),
        "all_pass": baseline_pass,
        "verifier_baseline_integrated_now": False,
        "verifier_modified_now": False,
        **_dryrun_meta(),
    }
    non_claims_and_forbidden_shortcut_library_consumption_dryrun = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_dryrun_meta(),
    }
    constraint_extension_rule_consumption_dryrun = {
        "rows": extension_rows,
        "row_count": len(extension_rows),
        "all_pass": extension_pass,
        "future_cursor_instruction_consumption_simulated": True,
        **_dryrun_meta(),
    }
    legacy_absorption_policy_consumption_dryrun = {
        "rows": absorption_rows,
        "row_count": len(absorption_rows),
        "all_pass": absorption_pass,
        "legacy_document_rewritten_now": False,
        **_dryrun_meta(),
    }

    governance_constraint_module_generation_dryrun_readiness_decision = {
        "ready_for_governance_constraint_module_generation_post_dryrun_review": boundary_ok,
        "ready_for_governance_constraint_module_generation": False,
        "ready_for_canonical_phase_template_generation": False,
        "ready_for_constraint_module_registration": False,
        "ready_for_constraint_enforcement": False,
        "ready_for_verifier_integration": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_legacy_document_rewrite": False,
        "ready_to_resume_main_migration_chain": False,
        "module_generation_dryrun_completed": boundary_ok,
        "canonical_phase_contract_consumption_dryrun_pass": contract_pass,
        "domain_constraint_registry_consumption_dryrun_pass": domain_pass,
        "phase_inheritance_matrix_consumption_dryrun_pass": inheritance_pass,
        "canonical_frozen_fields_consumption_dryrun_pass": frozen_pass,
        "phase_mode_lifecycle_consumption_dryrun_pass": lifecycle_pass,
        "required_fields_consumption_dryrun_pass": required_pass,
        "verifier_baseline_consumption_dryrun_pass": baseline_pass,
        "non_claims_and_forbidden_shortcut_library_consumption_dryrun_pass": non_claims_pass,
        "constraint_extension_rule_consumption_dryrun_pass": extension_pass,
        "legacy_absorption_policy_consumption_dryrun_pass": absorption_pass,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "canonical_contract_section_count": len(contract_rows),
        "domain_constraint_count": len(domain_rows),
        "inheritance_matrix_field_count": len(inheritance_rows),
        "frozen_field_pattern_count": len(frozen_rows),
        "phase_mode_count": len(lifecycle_rows),
        "required_field_group_count": len(required_rows),
        "verifier_baseline_check_count": len(baseline_rows),
        "non_claims_rule_count": len(non_claims_rows),
        "extension_rule_count": len(extension_rows),
        "legacy_absorption_section_count": len(absorption_rows),
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        "all_dryrun_pass": sim_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_dryrun_policy": governance_constraint_module_generation_dryrun_policy,
        "canonical_phase_contract_consumption_dryrun": canonical_phase_contract_consumption_dryrun,
        "domain_constraint_registry_consumption_dryrun": domain_constraint_registry_consumption_dryrun,
        "phase_inheritance_matrix_consumption_dryrun": phase_inheritance_matrix_consumption_dryrun,
        "canonical_frozen_fields_consumption_dryrun": canonical_frozen_fields_consumption_dryrun,
        "phase_mode_lifecycle_consumption_dryrun": phase_mode_lifecycle_consumption_dryrun,
        "constraint_required_fields_consumption_dryrun": constraint_required_fields_consumption_dryrun,
        "verifier_baseline_consumption_dryrun": verifier_baseline_consumption_dryrun,
        "non_claims_and_forbidden_shortcut_library_consumption_dryrun": non_claims_and_forbidden_shortcut_library_consumption_dryrun,
        "constraint_extension_rule_consumption_dryrun": constraint_extension_rule_consumption_dryrun,
        "legacy_absorption_policy_consumption_dryrun": legacy_absorption_policy_consumption_dryrun,
        "governance_constraint_module_generation_dryrun_readiness_decision": governance_constraint_module_generation_dryrun_readiness_decision,
    }
