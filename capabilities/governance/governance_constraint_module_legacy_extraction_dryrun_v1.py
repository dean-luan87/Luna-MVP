# -*- coding: utf-8 -*-
"""Governance Constraint Module Legacy Extraction DryRun v1.

Legacy extraction dry-run only: simulate consumption of planning artifacts.
Does not generate constraint modules, modify legacy phases, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    CONSTRAINT_DOMAINS,
    PLANNED_MODULE_ARTIFACTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"
DRYRUN_SCOPE = "governance_constraint_module_legacy_extraction_dryrun_only"
SOURCE_CHAIN = "governance_constraint_module_legacy_extraction_dryrun_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN"

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "legacy_extraction_planning_policy_v1.json",
    "legacy_governance_chain_inventory_v1.json",
    "legacy_phase_to_constraint_source_matrix_v1.json",
    "canonical_frozen_field_extraction_plan_v1.json",
    "phase_mode_lifecycle_contract_extraction_plan_v1.json",
    "domain_constraint_extraction_plan_v1.json",
    "governance_constraint_inheritance_policy_plan_v1.json",
    "legacy_absorption_policy_plan_v1.json",
    "governance_constraint_module_output_plan_v1.json",
    "legacy_extraction_planning_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "legacy_extraction_dryrun_only": True,
        "simulated": True,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
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
    readiness = _try_read_json(root / "legacy_extraction_planning_readiness_decision_v1.json") if root else None
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


def _simulate_inventory_consumption(inventory: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in inventory.get("rows") or []:
        review_pass = (
            r.get("legacy_validated_governance_chain") is True
            and r.get("source_for_constraint_extraction") is True
            and r.get("rewrite_required") is False
            and r.get("deprecated") is not True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                legacy_chain_id=r.get("legacy_chain_id"),
                legacy_chain_name=r.get("legacy_chain_name"),
                phase_count=r.get("phase_count"),
                latest_known_verdict=r.get("latest_known_verdict"),
                boundary_ok_observed=r.get("boundary_ok_observed"),
                legacy_validated_governance_chain=r.get("legacy_validated_governance_chain"),
                source_for_constraint_extraction=r.get("source_for_constraint_extraction"),
                rewrite_required=False,
                deprecated_now=False,
                simulated_inventory_consumption=True,
                legacy_as_template_source=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_mapping_dryrun(matrix: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in matrix.get("rows") or []:
        domain = r.get("contributes_to_constraint") or r.get("legacy_phase_or_chain")
        review_pass = r.get("rewrite_legacy_phase") is False and bool(r.get("source_chains"))
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                constraint_domain=domain,
                source_legacy_chains=r.get("source_chains"),
                reusable_rules=r.get("reusable_rules"),
                domain_specific_rules=r.get("domain_specific_rules"),
                simulated_mapping=True,
                constraint_generated_now=False,
                constraint_registered_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _simulate_frozen_field_dryrun(frozen: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in frozen.get("rows") or []:
        review_pass = (
            r.get("should_be_in_canonical_contract") is True
            and r.get("domain_override_allowed") is False
            and r.get("canonical_default_value") == "false"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                canonical_field_pattern=r.get("canonical_field_pattern"),
                canonical_default_value=r.get("canonical_default_value"),
                applies_to_phase_modes=r.get("applies_to_phase_modes"),
                source_chains=r.get("source_chains"),
                should_be_in_canonical_contract=r.get("should_be_in_canonical_contract"),
                domain_override_allowed=False,
                simulated_extraction=True,
                canonical_contract_generated_now=False,
                field_enforced_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 25


def _simulate_lifecycle_dryrun(lifecycle: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in lifecycle.get("rows") or []:
        review_pass = r.get("should_be_in_canonical_contract") is True and bool(r.get("forbidden_actions"))
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
                required_verifier_baseline=r.get("required_verifier_baseline"),
                simulated_lifecycle_consumption=True,
                lifecycle_contract_generated_now=False,
                phase_template_modified_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 15


def _simulate_domain_dryrun(domain: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    differentiated = {"Evidence Chain", "Owner/Operator Approval", "Boundary Object Registry", "Registry Generation"}
    for r in domain.get("rows") or []:
        name = r.get("domain_constraint_name")
        has_domain_rules = bool(r.get("domain_specific_forbidden_shortcuts")) and bool(
            r.get("domain_specific_non_claims")
        )
        review_pass = r.get("inherits_canonical_contract") is True and has_domain_rules
        if name in differentiated and not has_domain_rules:
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                domain_constraint_name=name,
                domain_scope=r.get("domain_scope"),
                source_chains=r.get("source_chains"),
                domain_specific_forbidden_shortcuts=r.get("domain_specific_forbidden_shortcuts"),
                domain_specific_required_fields=r.get("domain_specific_required_fields"),
                domain_specific_no_go_conditions=r.get("domain_specific_no_go_conditions"),
                domain_specific_non_claims=r.get("domain_specific_non_claims"),
                inherits_canonical_contract=True,
                simulated_domain_extraction=True,
                domain_constraint_generated_now=False,
                domain_constraint_registered_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_inheritance_dryrun(inheritance: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    review_pass = (
        inheritance.get("inheritance_model") == "canonical_contract_plus_domain_constraints"
        and inheritance.get("new_phase_must_declare_inherits") is True
        and inheritance.get("copying_full_canonical_freeze_fields_forbidden_later") is True
        and inheritance.get("verifier_must_load_constraint_manifest_later") is True
    )
    return _dryrun_row(
        inheritance_model=inheritance.get("inheritance_model"),
        new_phase_must_declare_inherits=inheritance.get("new_phase_must_declare_inherits"),
        new_phase_must_declare_phase_mode=inheritance.get("new_phase_must_declare_phase_mode"),
        new_phase_must_declare_domain_constraints=inheritance.get("new_phase_must_declare_domain_constraints"),
        new_phase_must_declare_specific_objects=inheritance.get("new_phase_must_declare_specific_objects"),
        new_phase_must_declare_specific_no_go=inheritance.get("new_phase_must_declare_specific_no_go"),
        copying_full_canonical_freeze_fields_forbidden_later=inheritance.get(
            "copying_full_canonical_freeze_fields_forbidden_later"
        ),
        domain_specific_extension_allowed=inheritance.get("domain_specific_extension_allowed"),
        canonical_override_requires_explicit_approval=inheritance.get("canonical_override_requires_explicit_approval"),
        verifier_must_load_constraint_manifest_later=inheritance.get("verifier_must_load_constraint_manifest_later"),
        phase_template_must_reference_constraint_module_later=inheritance.get(
            "phase_template_must_reference_constraint_module_later"
        ),
        simulated_inheritance_policy_consumption=True,
        inheritance_policy_enforced_now=False,
        phase_template_modified_now=False,
        dryrun_status="pass" if review_pass else "fail",
    ), review_pass


def _simulate_absorption_dryrun(absorption: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    review_pass = (
        absorption.get("legacy_as_source_evidence") is True
        and absorption.get("legacy_as_template_source") is False
        and absorption.get("rewrite_policy") == "do_not_rewrite_except_factual_correction"
        and absorption.get("old_chain_modification_allowed_now") is False
    )
    return _dryrun_row(
        legacy_phase_status=absorption.get("legacy_phase_status"),
        rewrite_policy=absorption.get("rewrite_policy"),
        absorption_note_required_later=absorption.get("absorption_note_required_later"),
        legacy_as_source_evidence=True,
        legacy_as_template_source=False,
        old_chain_archival_required_now=absorption.get("old_chain_archival_required_now"),
        old_chain_modification_allowed_now=False,
        legacy_phases_preserved=absorption.get("legacy_phases_preserved"),
        legacy_eval_out_preserved=absorption.get("legacy_eval_out_preserved"),
        legacy_verifier_reports_preserved=absorption.get("legacy_verifier_reports_preserved"),
        factual_correction_record_allowed=absorption.get("factual_correction_record_allowed"),
        simulated_absorption_policy_consumption=True,
        legacy_document_rewritten_now=False,
        legacy_eval_out_modified_now=False,
        dryrun_status="pass" if review_pass else "fail",
    ), review_pass


def _simulate_output_plan_dryrun(output_plan: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in output_plan.get("rows") or []:
        review_pass = r.get("not_generated_now") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                planned_artifact=r.get("planned_artifact"),
                purpose=r.get("purpose"),
                source_plans=r.get("source_plans"),
                used_by_future_verifier=r.get("used_by_future_verifier"),
                used_by_future_phase_template=r.get("used_by_future_phase_template"),
                used_by_future_cursor_instructions=r.get("used_by_future_cursor_instructions"),
                simulated_output_plan_consumption=True,
                not_generated_now=True,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_governance_constraint_module_legacy_extraction_dryrun_v1(
    *,
    governance_constraint_module_legacy_extraction_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_legacy_extraction_planning_root)
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
    if up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_dryrun") is not True:
        blockers.append("upstream not ready_for_governance_constraint_module_legacy_extraction_dryrun")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("legacy_extraction_planning_only") is not True:
        blockers.append("upstream legacy_extraction_planning_only must be true")
    if up_summary.get("main_migration_chain_paused") is not True:
        blockers.append("upstream main_migration_chain_paused must be true")
    if up_summary.get("main_migration_resume_phase") != MAIN_MIGRATION_RESUME_PHASE:
        blockers.append("upstream main_migration_resume_phase mismatch")
    if up_summary.get("inheritance_model") != "canonical_contract_plus_domain_constraints":
        blockers.append("upstream inheritance_model mismatch")
    absorption_up = up_art.get("legacy_absorption_policy_plan_v1.json", {})
    if absorption_up.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if absorption_up.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")

    for flag in (
        "legacy_phase_modified_now",
        "legacy_document_rewritten_now",
        "legacy_eval_out_modified_now",
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_enforced_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "automation_implemented_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")

    for flag in (
        "ready_for_governance_constraint_module_generation",
        "ready_for_canonical_phase_template_generation",
        "ready_for_verifier_integration",
        "ready_for_phase_template_modification",
        "ready_for_automation_implementation",
        "ready_for_legacy_document_rewrite",
        "ready_to_resume_main_migration_chain",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")

    inventory_rows, inventory_pass = _simulate_inventory_consumption(
        up_art.get("legacy_governance_chain_inventory_v1.json", {})
    )
    mapping_rows, mapping_pass = _simulate_mapping_dryrun(
        up_art.get("legacy_phase_to_constraint_source_matrix_v1.json", {})
    )
    frozen_rows, frozen_pass = _simulate_frozen_field_dryrun(
        up_art.get("canonical_frozen_field_extraction_plan_v1.json", {})
    )
    lifecycle_rows, lifecycle_pass = _simulate_lifecycle_dryrun(
        up_art.get("phase_mode_lifecycle_contract_extraction_plan_v1.json", {})
    )
    domain_rows, domain_pass = _simulate_domain_dryrun(
        up_art.get("domain_constraint_extraction_plan_v1.json", {})
    )
    inheritance_dryrun, inheritance_pass = _simulate_inheritance_dryrun(
        up_art.get("governance_constraint_inheritance_policy_plan_v1.json", {})
    )
    absorption_dryrun, absorption_pass = _simulate_absorption_dryrun(
        up_art.get("legacy_absorption_policy_plan_v1.json", {})
    )
    output_rows, output_pass = _simulate_output_plan_dryrun(
        up_art.get("governance_constraint_module_output_plan_v1.json", {})
    )

    sim_pass = all(
        (
            inventory_pass,
            mapping_pass,
            frozen_pass,
            lifecycle_pass,
            domain_pass,
            inheritance_pass,
            absorption_pass,
            output_pass,
        )
    )
    if not sim_pass:
        blockers.append("one or more dry-run simulations failed")

    if any(r.get("deprecated_now") for r in inventory_rows):
        blockers.append("legacy chains must not be marked deprecated")
    if any(r.get("rewrite_required") for r in inventory_rows):
        blockers.append("legacy chains must not require rewrite")
    if any(r.get("legacy_as_template_source") for r in inventory_rows):
        blockers.append("legacy chains must not be template source")

    dryrun_ready = sim_pass and not blockers
    boundary_ok = dryrun_ready

    legacy_extraction_dryrun_policy = _dryrun_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    legacy_chain_inventory_consumption_dryrun = {
        "rows": inventory_rows,
        "row_count": len(inventory_rows),
        "all_pass": inventory_pass,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        **_dryrun_meta(),
    }
    phase_to_constraint_mapping_dryrun = {
        "rows": mapping_rows,
        "row_count": len(mapping_rows),
        "constraint_domain_count": len(CONSTRAINT_DOMAINS),
        "all_pass": mapping_pass,
        **_dryrun_meta(),
    }
    canonical_frozen_field_extraction_dryrun = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "all_pass": frozen_pass,
        "canonical_contract_generated_now": False,
        **_dryrun_meta(),
    }
    phase_mode_lifecycle_contract_dryrun = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_pass": lifecycle_pass,
        "lifecycle_contract_generated_now": False,
        **_dryrun_meta(),
    }
    domain_constraint_extraction_dryrun = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "domain_differentiation_preserved": domain_pass,
        **_dryrun_meta(),
    }
    constraint_inheritance_policy_dryrun = inheritance_dryrun
    legacy_absorption_policy_dryrun = absorption_dryrun
    constraint_module_output_plan_dryrun = {
        "rows": output_rows,
        "row_count": len(output_rows),
        "all_pass": output_pass,
        "all_not_generated_now": all(r.get("not_generated_now") for r in output_rows),
        **_dryrun_meta(),
    }

    legacy_extraction_dryrun_readiness_decision = {
        "ready_for_governance_constraint_module_legacy_extraction_post_dryrun_review": boundary_ok,
        "ready_for_governance_constraint_module_generation": False,
        "ready_for_canonical_phase_template_generation": False,
        "ready_for_verifier_integration": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_legacy_document_rewrite": False,
        "ready_to_resume_main_migration_chain": False,
        "legacy_extraction_dryrun_completed": boundary_ok,
        "legacy_chain_inventory_consumption_dryrun_pass": inventory_pass,
        "phase_to_constraint_mapping_dryrun_pass": mapping_pass,
        "canonical_frozen_field_extraction_dryrun_pass": frozen_pass,
        "phase_mode_lifecycle_contract_dryrun_pass": lifecycle_pass,
        "domain_constraint_extraction_dryrun_pass": domain_pass,
        "inheritance_policy_dryrun_pass": inheritance_pass,
        "legacy_absorption_policy_dryrun_pass": absorption_pass,
        "output_plan_dryrun_pass": output_pass,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_legacy_extraction_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "legacy_chain_count": len(inventory_rows),
        "constraint_domain_count": len(mapping_rows),
        "frozen_field_pattern_count": len(frozen_rows),
        "phase_mode_count": len(lifecycle_rows),
        "domain_constraint_count": len(domain_rows),
        "planned_artifact_count": len(output_rows),
        "inheritance_model": inheritance_dryrun.get("inheritance_model"),
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "all_dryrun_pass": sim_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "legacy_extraction_dryrun_policy": legacy_extraction_dryrun_policy,
        "legacy_chain_inventory_consumption_dryrun": legacy_chain_inventory_consumption_dryrun,
        "phase_to_constraint_mapping_dryrun": phase_to_constraint_mapping_dryrun,
        "canonical_frozen_field_extraction_dryrun": canonical_frozen_field_extraction_dryrun,
        "phase_mode_lifecycle_contract_dryrun": phase_mode_lifecycle_contract_dryrun,
        "domain_constraint_extraction_dryrun": domain_constraint_extraction_dryrun,
        "constraint_inheritance_policy_dryrun": constraint_inheritance_policy_dryrun,
        "legacy_absorption_policy_dryrun": legacy_absorption_policy_dryrun,
        "constraint_module_output_plan_dryrun": constraint_module_output_plan_dryrun,
        "legacy_extraction_dryrun_readiness_decision": legacy_extraction_dryrun_readiness_decision,
    }
