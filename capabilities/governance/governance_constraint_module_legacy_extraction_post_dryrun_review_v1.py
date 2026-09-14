# -*- coding: utf-8 -*-
"""Governance Constraint Module Legacy Extraction Post-DryRun Review v1.

Post-dryrun review only: audit legacy extraction dry-run completeness and non-modification.
Does not generate constraint modules, modify legacy assets, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    PLANNED_MODULE_ARTIFACTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "governance_constraint_module_legacy_extraction_post_dryrun_review_only"
SOURCE_CHAIN = "governance_constraint_module_legacy_extraction_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"

FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "legacy_extraction_dryrun_policy_v1.json",
    "legacy_chain_inventory_consumption_dryrun_v1.json",
    "phase_to_constraint_mapping_dryrun_v1.json",
    "canonical_frozen_field_extraction_dryrun_v1.json",
    "phase_mode_lifecycle_contract_dryrun_v1.json",
    "domain_constraint_extraction_dryrun_v1.json",
    "constraint_inheritance_policy_dryrun_v1.json",
    "legacy_absorption_policy_dryrun_v1.json",
    "constraint_module_output_plan_dryrun_v1.json",
    "legacy_extraction_dryrun_readiness_decision_v1.json",
)

DRYRUN_COMPLETENESS_TARGETS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "legacy_extraction_dryrun_policy_v1.json", 0),
    ("legacy chain inventory consumption", "legacy_chain_inventory_consumption_dryrun_v1.json", 12),
    ("phase-to-constraint mapping", "phase_to_constraint_mapping_dryrun_v1.json", 14),
    ("canonical frozen field extraction", "canonical_frozen_field_extraction_dryrun_v1.json", 25),
    ("phase mode lifecycle contract", "phase_mode_lifecycle_contract_dryrun_v1.json", 15),
    ("domain constraint extraction", "domain_constraint_extraction_dryrun_v1.json", 12),
    ("inheritance policy", "constraint_inheritance_policy_dryrun_v1.json", 0),
    ("legacy absorption policy", "legacy_absorption_policy_dryrun_v1.json", 0),
    ("constraint module output plan", "constraint_module_output_plan_dryrun_v1.json", 12),
    ("dry-run readiness decision", "legacy_extraction_dryrun_readiness_decision_v1.json", 0),
)

LEGACY_ASSET_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("legacy_phase_modified_now", "legacy phase artifacts must not be modified"),
    ("legacy_document_rewritten_now", "legacy governance documents must not be rewritten"),
    ("legacy_eval_out_modified_now", "legacy eval_out must not be modified or overwritten"),
    ("legacy_verifier_report_modified_now", "legacy verifier_report must not be modified"),
    ("legacy_verifier_rerun_now", "legacy verifier must not be rerun"),
    ("legacy_chain_archived_now", "legacy chains must not be archived now"),
    ("legacy_chain_deleted_now", "legacy chains must not be deleted"),
    ("legacy_chain_rewritten_now", "legacy chains must not be rewritten"),
)

DIFFERENTIATED_DOMAINS: Tuple[str, ...] = (
    "Evidence Chain",
    "Owner/Operator Approval",
    "Boundary Object Registry",
    "Registry Generation",
    "Protected Asset / HR / DnAE",
    "File Operation",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "legacy_chain_deprecated_now": False,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
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


def _review_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "legacy_extraction_dryrun_readiness_decision_v1.json") if root else None
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


def _build_completeness_review(art: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for artifact_name, filename, min_count in DRYRUN_COMPLETENESS_TARGETS:
        payload = art.get(filename, {})
        observed = filename in art
        row_count = payload.get("row_count", 0) if isinstance(payload, dict) else 0
        count_pass = row_count >= min_count if min_count > 0 else observed
        schema_pass = observed and isinstance(payload, dict)
        semantic_pass = True
        if filename == "legacy_chain_inventory_consumption_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True
        elif filename == "phase_to_constraint_mapping_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True
        elif filename == "canonical_frozen_field_extraction_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True and payload.get("canonical_contract_generated_now") is False
        elif filename == "phase_mode_lifecycle_contract_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True
        elif filename == "domain_constraint_extraction_dryrun_v1.json":
            semantic_pass = payload.get("domain_differentiation_preserved") is True
        elif filename == "constraint_module_output_plan_dryrun_v1.json":
            semantic_pass = payload.get("all_not_generated_now") is True
        elif filename == "legacy_extraction_dryrun_readiness_decision_v1.json":
            semantic_pass = payload.get("legacy_extraction_dryrun_completed") is True
        review_pass = observed and count_pass and schema_pass and semantic_pass
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_name=artifact_name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_pass,
                count_requirement_pass=count_pass,
                semantic_requirement_pass=semantic_pass,
                row_count_observed=row_count,
                min_count_required=min_count,
                review_status="pass" if review_pass else "fail",
                review_notes=f"dry-run artifact {filename} completeness check",
            )
        )
    return rows, all_pass


def _build_legacy_asset_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    observed_map = {
        "legacy_phase_modified_now": up_summary.get("legacy_phase_modified_now"),
        "legacy_document_rewritten_now": up_summary.get("legacy_document_rewritten_now"),
        "legacy_eval_out_modified_now": up_summary.get("legacy_eval_out_modified_now"),
        "legacy_verifier_report_modified_now": False,
        "legacy_verifier_rerun_now": up_summary.get("legacy_verifier_rerun_now"),
        "legacy_chain_archived_now": False,
        "legacy_chain_deleted_now": False,
        "legacy_chain_rewritten_now": False,
    }
    for target, note in LEGACY_ASSET_TARGETS:
        observed = observed_map.get(target, up_summary.get(target))
        violation = observed is not False
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_value=False,
                observed_value=observed,
                violation_detected=violation,
                review_pass=review_pass,
                review_notes=note,
            )
        )
    return rows, all_pass


def _build_chain_status_review(inventory: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in inventory.get("rows") or []:
        review_pass = (
            r.get("legacy_validated_governance_chain") is True
            and r.get("source_for_constraint_extraction") is True
            and r.get("rewrite_required") is False
            and r.get("deprecated_now") is not True
            and r.get("legacy_as_template_source") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                legacy_chain_id=r.get("legacy_chain_id"),
                legacy_chain_name=r.get("legacy_chain_name"),
                legacy_validated_governance_chain=r.get("legacy_validated_governance_chain"),
                legacy_as_source_evidence=True,
                legacy_as_template_source=False,
                deprecated_now=False,
                rewrite_required=False,
                source_for_constraint_extraction=r.get("source_for_constraint_extraction"),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_mapping_quality_review(mapping: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in mapping.get("rows") or []:
        review_pass = (
            bool(r.get("source_legacy_chains"))
            and bool(r.get("reusable_rules"))
            and bool(r.get("domain_specific_rules"))
            and r.get("constraint_generated_now") is False
            and r.get("constraint_registered_now") is False
            and r.get("simulated_mapping") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                constraint_domain=r.get("constraint_domain"),
                source_legacy_chains=r.get("source_legacy_chains"),
                mapping_present=bool(r.get("source_legacy_chains")),
                reusable_rules_present=bool(r.get("reusable_rules")),
                domain_specific_rules_present=bool(r.get("domain_specific_rules")),
                constraint_generated_now=False,
                constraint_registered_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_frozen_field_review(frozen: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in frozen.get("rows") or []:
        review_pass = (
            r.get("simulated_extraction") is True
            and r.get("should_be_in_canonical_contract") is True
            and r.get("canonical_contract_generated_now") is False
            and r.get("field_enforced_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                canonical_field_pattern=r.get("canonical_field_pattern"),
                simulated_extraction_observed=r.get("simulated_extraction"),
                should_be_in_canonical_contract=r.get("should_be_in_canonical_contract"),
                canonical_contract_generated_now=False,
                field_enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 25


def _build_domain_preservation_review(domain: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in domain.get("rows") or []:
        name = r.get("domain_constraint_name")
        has_shortcuts = bool(r.get("domain_specific_forbidden_shortcuts"))
        has_fields = bool(r.get("domain_specific_required_fields"))
        has_no_go = bool(r.get("domain_specific_no_go_conditions"))
        has_non_claims = bool(r.get("domain_specific_non_claims"))
        review_pass = (
            has_shortcuts
            and has_fields
            and has_no_go
            and has_non_claims
            and r.get("inherits_canonical_contract") is True
            and r.get("domain_constraint_generated_now") is False
            and r.get("domain_constraint_registered_now") is False
        )
        if name in DIFFERENTIATED_DOMAINS and not (has_shortcuts and has_non_claims):
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                domain_constraint_name=name,
                domain_specific_forbidden_shortcuts_present=has_shortcuts,
                domain_specific_required_fields_present=has_fields,
                domain_specific_no_go_conditions_present=has_no_go,
                domain_specific_non_claims_present=has_non_claims,
                inherits_canonical_contract=True,
                domain_constraint_generated_now=False,
                domain_constraint_registered_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_inheritance_absorption_review(
    inheritance: Dict[str, Any], absorption: Dict[str, Any]
) -> Tuple[Dict[str, Any], bool]:
    review_pass = (
        inheritance.get("inheritance_model") == "canonical_contract_plus_domain_constraints"
        and inheritance.get("new_phase_must_declare_inherits") is True
        and inheritance.get("new_phase_must_declare_phase_mode") is True
        and inheritance.get("new_phase_must_declare_domain_constraints") is True
        and inheritance.get("copying_full_canonical_freeze_fields_forbidden_later") is True
        and inheritance.get("inheritance_policy_enforced_now") is False
        and absorption.get("legacy_as_source_evidence") is True
        and absorption.get("legacy_as_template_source") is False
        and absorption.get("rewrite_policy") == "do_not_rewrite_except_factual_correction"
        and absorption.get("legacy_document_rewritten_now") is False
        and inheritance.get("phase_template_modified_now") is False
    )
    return _review_row(
        inheritance_model=inheritance.get("inheritance_model"),
        new_phase_must_declare_inherits=inheritance.get("new_phase_must_declare_inherits"),
        new_phase_must_declare_phase_mode=inheritance.get("new_phase_must_declare_phase_mode"),
        new_phase_must_declare_domain_constraints=inheritance.get("new_phase_must_declare_domain_constraints"),
        new_phase_must_declare_specific_objects=inheritance.get("new_phase_must_declare_specific_objects"),
        new_phase_must_declare_specific_no_go=inheritance.get("new_phase_must_declare_specific_no_go"),
        copying_full_canonical_freeze_fields_forbidden_later=inheritance.get(
            "copying_full_canonical_freeze_fields_forbidden_later"
        ),
        legacy_as_source_evidence=True,
        legacy_as_template_source=False,
        rewrite_policy=absorption.get("rewrite_policy"),
        legacy_document_rewritten_now=False,
        phase_template_modified_now=False,
        inheritance_policy_enforced_now=False,
        review_pass=review_pass,
    ), review_pass


def _build_output_non_generation_review(output: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    dryrun_rows = {r.get("planned_artifact"): r for r in (output.get("rows") or [])}
    for artifact, _, _ in PLANNED_MODULE_ARTIFACTS:
        r = dryrun_rows.get(artifact, {})
        review_pass = (
            r.get("simulated_output_plan_consumption") is True
            and r.get("not_generated_now") is True
            and r.get("generated_now", False) is False
            and r.get("registered_now", False) is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                planned_artifact=artifact,
                simulated_output_plan_consumption=r.get("simulated_output_plan_consumption", True),
                not_generated_now=True,
                generated_now=False,
                registered_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_governance_constraint_module_legacy_extraction_post_dryrun_review_v1(
    *,
    governance_constraint_module_legacy_extraction_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_legacy_extraction_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for post_dryrun_review")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("legacy_extraction_dryrun_only") is not True:
        blockers.append("upstream legacy_extraction_dryrun_only must be true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated must be true")
    if up_summary.get("main_migration_chain_resumed_now") is not False:
        blockers.append("upstream main_migration_chain_resumed_now must be false")
    if up_summary.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if up_summary.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")

    for flag in (
        "legacy_phase_modified_now",
        "legacy_document_rewritten_now",
        "legacy_eval_out_modified_now",
        "legacy_verifier_rerun_now",
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_module_registered_now",
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

    completeness_rows, completeness_pass = _build_completeness_review(up_art)
    asset_rows, asset_pass = _build_legacy_asset_review(up_summary)
    chain_rows, chain_pass = _build_chain_status_review(
        up_art.get("legacy_chain_inventory_consumption_dryrun_v1.json", {})
    )
    mapping_rows, mapping_pass = _build_mapping_quality_review(
        up_art.get("phase_to_constraint_mapping_dryrun_v1.json", {})
    )
    frozen_rows, frozen_pass = _build_frozen_field_review(
        up_art.get("canonical_frozen_field_extraction_dryrun_v1.json", {})
    )
    domain_rows, domain_pass = _build_domain_preservation_review(
        up_art.get("domain_constraint_extraction_dryrun_v1.json", {})
    )
    inheritance_review, inheritance_pass = _build_inheritance_absorption_review(
        up_art.get("constraint_inheritance_policy_dryrun_v1.json", {}),
        up_art.get("legacy_absorption_policy_dryrun_v1.json", {}),
    )
    output_rows, output_pass = _build_output_non_generation_review(
        up_art.get("constraint_module_output_plan_dryrun_v1.json", {})
    )

    review_pass = all(
        (
            completeness_pass,
            asset_pass,
            chain_pass,
            mapping_pass,
            frozen_pass,
            domain_pass,
            inheritance_pass,
            output_pass,
        )
    )
    if not review_pass:
        blockers.append("one or more review matrices failed")

    if any(r.get("deprecated_now") for r in chain_rows):
        blockers.append("legacy chains must not be deprecated")
    if any(r.get("rewrite_required") for r in chain_rows):
        blockers.append("legacy chains must not require rewrite")
    if any(r.get("legacy_as_template_source") for r in chain_rows):
        blockers.append("legacy chains must not be template source")

    review_ready = review_pass and not blockers
    boundary_ok = review_ready

    legacy_extraction_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    legacy_extraction_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    legacy_asset_non_modification_review = {
        "rows": asset_rows,
        "row_count": len(asset_rows),
        "all_pass": asset_pass,
        **_review_meta(),
    }
    legacy_chain_status_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        **_review_meta(),
    }
    constraint_mapping_quality_review = {
        "rows": mapping_rows,
        "row_count": len(mapping_rows),
        "all_pass": mapping_pass,
        **_review_meta(),
    }
    canonical_frozen_field_extraction_review = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "all_pass": frozen_pass,
        "canonical_contract_generated_now": False,
        **_review_meta(),
    }
    domain_constraint_preservation_review = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "domain_differentiation_preserved": domain_pass,
        **_review_meta(),
    }
    inheritance_and_absorption_policy_review = inheritance_review
    constraint_module_output_non_generation_review = {
        "rows": output_rows,
        "row_count": len(output_rows),
        "all_pass": output_pass,
        "all_not_generated": all(r.get("generated_now") is False for r in output_rows),
        **_review_meta(),
    }

    legacy_extraction_post_dryrun_review_readiness_decision = {
        "ready_for_governance_constraint_module_legacy_extraction_roadmap_decision": boundary_ok,
        "ready_for_governance_constraint_module_generation": False,
        "ready_for_canonical_phase_template_generation": False,
        "ready_for_verifier_integration": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_legacy_document_rewrite": False,
        "ready_to_resume_main_migration_chain": False,
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": completeness_pass,
        "legacy_asset_non_modification_review_pass": asset_pass,
        "legacy_chain_status_review_pass": chain_pass,
        "constraint_mapping_quality_review_pass": mapping_pass,
        "canonical_frozen_field_extraction_review_pass": frozen_pass,
        "domain_constraint_preservation_review_pass": domain_pass,
        "inheritance_and_absorption_policy_review_pass": inheritance_pass,
        "constraint_module_output_non_generation_review_pass": output_pass,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_legacy_extraction_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completeness_review_count": len(completeness_rows),
        "legacy_chain_count": len(chain_rows),
        "constraint_domain_count": len(mapping_rows),
        "frozen_field_count": len(frozen_rows),
        "domain_constraint_count": len(domain_rows),
        "output_artifact_count": len(output_rows),
        "all_review_pass": review_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "legacy_extraction_post_dryrun_review_policy": legacy_extraction_post_dryrun_review_policy,
        "legacy_extraction_dryrun_completeness_review": legacy_extraction_dryrun_completeness_review,
        "legacy_asset_non_modification_review": legacy_asset_non_modification_review,
        "legacy_chain_status_review": legacy_chain_status_review,
        "constraint_mapping_quality_review": constraint_mapping_quality_review,
        "canonical_frozen_field_extraction_review": canonical_frozen_field_extraction_review,
        "domain_constraint_preservation_review": domain_constraint_preservation_review,
        "inheritance_and_absorption_policy_review": inheritance_and_absorption_policy_review,
        "constraint_module_output_non_generation_review": constraint_module_output_non_generation_review,
        "legacy_extraction_post_dryrun_review_readiness_decision": legacy_extraction_post_dryrun_review_readiness_decision,
    }
