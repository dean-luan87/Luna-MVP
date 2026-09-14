# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Planning v1.

Module generation planning only: plan output shapes for formal Governance Constraint Module v1.
Does not generate constraint modules, modify verifiers, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    DOMAIN_CONSTRAINTS,
    FROZEN_FIELD_PATTERNS,
    PHASE_MODES,
)
from capabilities.governance.governance_constraint_module_legacy_extraction_roadmap_decision_v1 import (
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Planning-v1-001"
PLANNING_SCOPE = "governance_constraint_module_generation_planning_only"
SOURCE_CHAIN = "governance_constraint_module_generation_planning_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "legacy_extraction_roadmap_decision_policy_v1.json",
    "completed_legacy_extraction_chain_review_v1.json",
    "legacy_extraction_roadmap_route_candidate_matrix_v1.json",
    "constraint_module_generation_dependency_matrix_v1.json",
    "constraint_module_generation_planning_scope_v1.json",
    "legacy_extraction_roadmap_non_release_matrix_v1.json",
    "constraint_module_generation_entry_readiness_risk_matrix_v1.json",
    "legacy_extraction_roadmap_decision_non_claims_register_v1.json",
    "legacy_extraction_roadmap_readiness_decision_v1.json",
)

CANONICAL_CONTRACT_SECTIONS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
    ("canonical phase lifecycle", "define Planning→DryRun→Review→Roadmap lifecycle", ("Legacy Extraction chain", "Migration Governance Constraints")),
    ("phase mode semantics", "define canonical meaning per phase mode", ("Legacy Extraction Planning",)),
    ("common frozen fields", "define canonical *_now=false patterns", ("Legacy Extraction Planning",)),
    ("common forbidden actions", "define actions forbidden in all non-execution phases", ("Migration Governance Constraints",)),
    ("common readiness fields", "define ready_for_* semantics", ("Permission Semantics Canonicalization",)),
    ("common non-claims", "define canonical non-claims library entries", ("Evidence Chain Governance",)),
    ("common verifier baseline", "define MIN_CHECKS and boundary_ok requirements", ("Governance Debt Register",)),
    ("success claim default block", "success_claim_allowed=false by default", ("Success Claim Gate Canonicalization",)),
    ("authorization default block", "authorization_granted_now=false by default", ("Owner/Operator Approval Protocol",)),
    ("file operation default block", "file_operation_executed_now=false by default", ("File Operation domain",)),
    ("protected asset default block", "protected/HR/DnAE modification blocked", ("Protected Asset chain",)),
    ("mainline resume default block", "main_migration_chain_resumed_now=false by default", ("Legacy Extraction Roadmap Decision",)),
)

INHERITANCE_MATRIX_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("phase name", "identify phase identity for inheritance lookup"),
    ("phase mode", "declare Planning/DryRun/Review/Roadmap mode"),
    ("inherited canonical contract", "reference governance_canonical_phase_contract_v1"),
    ("domain constraints", "list applicable domain constraint modules"),
    ("specific objects", "declare phase-specific core objects"),
    ("specific no-go conditions", "declare phase-specific NO-GO triggers"),
    ("output artifacts", "declare expected eval_out artifacts"),
    ("verifier baseline", "reference governance_constraint_verifier_baseline_v1"),
    ("non-claims source", "reference governance_constraint_non_claims_library_v1"),
    ("roadmap return target", "declare recommended_next_phase field semantics"),
)

REQUIRED_FIELD_GROUPS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("phase identity fields", ("phase", "phase_name", "planning_scope", "decision_scope", "review_scope")),
    ("source dependency fields", ("source_phase", "source_verifier_go_observed", "source_boundary_ok_observed", "governance_constraints_ref")),
    ("boundary fields", ("boundary_ok", "violations", "fact_status", "write_allowed")),
    ("frozen permission fields", ("authorization_granted_now", "file_operation_executed_now", "success_claim_allowed")),
    ("readiness fields", ("ready_for_*", "final_decision", "recommended_next_phase")),
    ("final decision fields", ("final_decision", "recommended_next_phase")),
    ("recommended next phase fields", ("recommended_next_phase",)),
    ("non-claims fields", ("legacy_as_source_evidence", "legacy_as_template_source")),
    ("verifier status fields", ("verifier", "passed", "check_count", "min_checks")),
    ("governance constraints reference fields", ("governance_constraints_ref",)),
    ("mainline resume fields", ("main_migration_chain_paused", "main_migration_chain_resumed_now", "main_migration_resume_phase")),
    ("legacy absorption fields", ("legacy_phase_modified_now", "legacy_document_rewritten_now", "legacy_eval_out_modified_now")),
)

VERIFIER_BASELINE_CHECKS: Tuple[Tuple[str, str, str], ...] = (
    ("B01", "source verifier GO check", "upstream verifier != GO"),
    ("B02", "source boundary_ok check", "upstream boundary_ok != true"),
    ("B03", "phase mode check", "phase mode not declared or mismatched"),
    ("B04", "inherited constraint check", "domain constraints not declared"),
    ("B05", "frozen field check", "mandatory freeze field != false"),
    ("B06", "forbidden transition check", "final_decision points to forbidden phase"),
    ("B07", "non-claims check", "required non-claims missing"),
    ("B08", "output artifact check", "required artifacts missing"),
    ("B09", "readiness decision check", "ready_for_* contradicts freeze fields"),
    ("B10", "no file operation check", "file_operation_executed_now != false"),
    ("B11", "no authorization release check", "authorization_granted_now != false"),
    ("B12", "no success claim check", "success_claim_allowed != false"),
    ("B13", "no verifier modification check", "verifier_modified_now != false"),
    ("B14", "no template modification check", "phase_template_modified_now != false"),
    ("B15", "no mainline resume check", "main_migration_chain_resumed_now != false"),
)

NON_CLAIMS_AND_SHORTCUTS: Tuple[Tuple[str, str, str], ...] = (
    ("NC01", "non_claim", "Planning GO ≠ execution"),
    ("NC02", "non_claim", "DryRun GO ≠ success"),
    ("NC03", "non_claim", "Post-Review GO ≠ permission release"),
    ("NC04", "non_claim", "Roadmap selected route ≠ authorization"),
    ("NC05", "non_claim", "verifier=GO ≠ success claim"),
    ("NC06", "non_claim", "summary ≠ evidence"),
    ("NC07", "non_claim", "verifier_report ≠ runtime evidence"),
    ("NC08", "non_claim", "source_chain ≠ success evidence"),
    ("NC09", "non_claim", "owner/operator planning ≠ approval granted"),
    ("NC10", "non_claim", "registry planning ≠ registry generated"),
    ("NC11", "non_claim", "generation planning ≠ generation authorized"),
    ("NC12", "non_claim", "read allowed ≠ write allowed"),
    ("NC13", "non_claim", "source whitelist planned ≠ source final validated"),
    ("NC14", "non_claim", "contamination rule planned ≠ contamination final checked"),
    ("NC15", "non_claim", "legacy extraction GO ≠ module generated"),
    ("FS01", "forbidden_shortcut", "copy full canonical freeze fields manually into new phase"),
    ("FS02", "forbidden_shortcut", "use legacy phase as template source for new phase"),
)

EXTENSION_RULES: Tuple[str, ...] = (
    "new phase must declare inherited canonical contract",
    "new phase must declare phase mode",
    "new phase must declare domain constraints",
    "new phase must declare specific objects",
    "new phase must declare specific no-go",
    "new phase must not copy full canonical frozen fields manually",
    "domain-specific extension allowed",
    "canonical override requires explicit approval",
    "verifier must load constraint manifest later",
    "phase template must reference constraint module later",
    "legacy source evidence allowed",
    "legacy template copying forbidden",
)

LEGACY_ABSORPTION_SECTIONS: Tuple[Tuple[str, str], ...] = (
    ("legacy phase status", "legacy_validated_governance_chain; not deprecated"),
    ("legacy source evidence policy", "legacy_as_source_evidence=true"),
    ("legacy template source block", "legacy_as_template_source=false"),
    ("rewrite policy", "do_not_rewrite_except_factual_correction"),
    ("correction policy", "factual_correction_record_allowed=true"),
    ("absorption note policy", "absorption_note_required_later=true"),
    ("legacy eval_out preservation policy", "legacy_eval_out_preserved=true; no overwrite"),
    ("legacy verifier preservation policy", "legacy_verifier_reports_preserved=true; no rerun"),
    ("legacy deprecation block", "legacy_chain_deprecated_now=false"),
    ("legacy archival policy", "old_chain_archival_required_now=false"),
    ("source evidence citation policy", "cite legacy chain as source evidence only"),
    ("future migration resume reference policy", f"resume at {MAIN_MIGRATION_RESUME_PHASE} after module chain complete"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "governance_constraint_module_generation_planning_only": True,
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


def _planning_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta(), "not_generated_now": True}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "legacy_extraction_roadmap_readiness_decision_v1.json") if root else None
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


def _build_canonical_contract_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            contract_section=section,
            purpose=purpose,
            source_legacy_chains=list(chains),
            required_fields=[f"{section.replace(' ', '_')}_fields"],
            used_by_future_phase=True,
            used_by_future_verifier=True,
            target_artifact="governance_canonical_phase_contract_v1.json",
        )
        for section, purpose, chains in CANONICAL_CONTRACT_SECTIONS
    ]


def _build_domain_registry_shape() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name, scope, sources, module_output in DOMAIN_CONSTRAINTS:
        rows.append(
            _planning_row(
                domain_constraint_name=name,
                inherits_canonical_contract=True,
                domain_specific_required_fields=[f"{name.lower().replace(' ', '_').replace('/', '_')}_required_fields"],
                domain_specific_forbidden_shortcuts=[f"{name}: planning/dry-run/review ≠ execution"],
                domain_specific_no_go_conditions=[f"{name}: permission release without authorization"],
                domain_specific_non_claims=[f"{name} GO does not mean domain execution authorized"],
                source_legacy_chains=list(sources),
                target_artifact="governance_domain_constraint_registry_v1.json",
                planned_module_output=module_output,
            )
        )
    return rows


def _build_inheritance_matrix_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            matrix_field=field,
            why_required=why,
            required_for_new_phase=True,
            used_by_cursor_instruction=True,
            used_by_verifier=True,
            target_artifact="governance_phase_inheritance_matrix_v1.json",
        )
        for field, why in INHERITANCE_MATRIX_FIELDS
    ]


def _build_frozen_fields_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            canonical_field_pattern=pattern,
            default_value=default,
            applies_to_phase_modes=list(modes),
            applies_to_domain_constraints=["all"],
            override_allowed=False,
            source_legacy_chains=["all validated governance chains"],
            target_artifact="governance_canonical_frozen_fields_v1.json",
        )
        for pattern, default, modes in FROZEN_FIELD_PATTERNS
    ]


def _build_phase_mode_lifecycle_shape() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for mode, meaning, allowed, forbidden in PHASE_MODES:
        rows.append(
            _planning_row(
                phase_mode=mode,
                canonical_meaning=meaning,
                allowed_actions=allowed,
                forbidden_actions=forbidden,
                required_readiness_fields=[f"ready_for_{mode.lower().replace(' ', '_').replace('-', '_')}"],
                required_non_claims=[f"{mode} GO does not mean real execution is authorized"],
                next_allowed_phase_modes=["DryRun", "Post-DryRun Review", "Roadmap Decision"],
                target_artifact="governance_phase_mode_lifecycle_contract_v1.json",
            )
        )
    return rows


def _build_required_fields_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            required_field_group=group,
            required_fields=list(fields),
            applies_to_phase_modes=["Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision"],
            applies_to_domain_constraints=["all"],
            why_required=f"{group} must appear in every governed phase summary",
            target_artifact="governance_constraint_required_fields_v1.json",
        )
        for group, fields in REQUIRED_FIELD_GROUPS
    ]


def _build_verifier_baseline_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            baseline_check_id=check_id,
            check_name=check_name,
            required_for_phase_modes=["Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision"],
            required_for_domain_constraints=["all"],
            failure_condition=failure,
            severity="critical",
            target_artifact="governance_constraint_verifier_baseline_v1.json",
        )
        for check_id, check_name, failure in VERIFIER_BASELINE_CHECKS
    ]


def _build_non_claims_library_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            rule_id=rule_id,
            rule_type=rule_type,
            canonical_statement=statement,
            applies_to_phase_modes=["Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision"],
            applies_to_domain_constraints=["all"],
            source_legacy_chains=["Legacy Extraction chain", "Migration Governance Constraints"],
            target_artifact=(
                "governance_constraint_non_claims_library_v1.json"
                if rule_type == "non_claim"
                else "governance_constraint_forbidden_shortcut_library_v1.json"
            ),
        )
        for rule_id, rule_type, statement in NON_CLAIMS_AND_SHORTCUTS
    ]


def _build_extension_rule_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            extension_rule=rule,
            why_required=f"enforce inheritance discipline: {rule}",
            failure_condition=f"violation of {rule}",
            used_by_future_cursor_instruction=True,
            used_by_future_verifier=True,
            target_artifact="governance_constraint_extension_rule_v1.json",
        )
        for rule in EXTENSION_RULES
    ]


def _build_legacy_absorption_shape() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            policy_section=section,
            policy_rule=rule,
            why_required=f"preserve legacy assets while enabling constraint module: {section}",
            used_by_future_documentation=True,
            used_by_future_verifier=True,
            target_artifact="governance_legacy_absorption_policy_v1.json",
        )
        for section, rule in LEGACY_ABSORPTION_SECTIONS
    ]


def run_governance_constraint_module_generation_planning_v1(
    *,
    governance_constraint_module_legacy_extraction_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_legacy_extraction_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap decision verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_summary.get("selected_route") != UPSTREAM_SELECTED_ROUTE:
        blockers.append(f"upstream selected_route must be {UPSTREAM_SELECTED_ROUTE}")
    if up_readiness.get("ready_for_governance_constraint_module_generation_planning") is not True:
        blockers.append("upstream not ready_for_governance_constraint_module_generation_planning")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("governance_constraint_module_generation_planning_selected") is not True:
        blockers.append("upstream governance_constraint_module_generation_planning_selected must be true")

    for flag in (
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_module_registered_now",
        "constraint_enforced_now",
        "verifier_integration_executed_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "automation_implemented_now",
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

    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    contract_rows = _build_canonical_contract_shape()
    domain_rows = _build_domain_registry_shape()
    inheritance_rows = _build_inheritance_matrix_shape()
    frozen_rows = _build_frozen_fields_shape()
    lifecycle_rows = _build_phase_mode_lifecycle_shape()
    required_rows = _build_required_fields_shape()
    baseline_rows = _build_verifier_baseline_shape()
    non_claims_rows = _build_non_claims_library_shape()
    extension_rows = _build_extension_rule_shape()
    absorption_rows = _build_legacy_absorption_shape()

    all_rows = (
        contract_rows,
        domain_rows,
        inheritance_rows,
        frozen_rows,
        lifecycle_rows,
        required_rows,
        baseline_rows,
        non_claims_rows,
        extension_rows,
        absorption_rows,
    )
    if any(not all(r.get("not_generated_now") for r in rows) for rows in all_rows):
        blockers.append("all planned outputs must have not_generated_now=true")

    counts_ok = (
        len(contract_rows) >= 12
        and len(domain_rows) >= 12
        and len(inheritance_rows) >= 10
        and len(frozen_rows) >= 25
        and len(lifecycle_rows) >= 15
        and len(required_rows) >= 12
        and len(baseline_rows) >= 15
        and len(non_claims_rows) >= 15
        and len(extension_rows) >= 12
        and len(absorption_rows) >= 12
    )
    if not counts_ok:
        blockers.append("output shape coverage requirements not met")

    planning_ready = counts_ok and not blockers
    boundary_ok = planning_ready

    governance_constraint_module_generation_planning_policy = _planning_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    canonical_phase_contract_output_shape_planning = {
        "rows": contract_rows,
        "row_count": len(contract_rows),
        "target_artifact": "governance_canonical_phase_contract_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in contract_rows),
        **_planning_meta(),
    }
    domain_constraint_registry_output_shape_planning = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "target_artifact": "governance_domain_constraint_registry_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in domain_rows),
        **_planning_meta(),
    }
    phase_inheritance_matrix_output_shape_planning = {
        "rows": inheritance_rows,
        "row_count": len(inheritance_rows),
        "target_artifact": "governance_phase_inheritance_matrix_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in inheritance_rows),
        **_planning_meta(),
    }
    canonical_frozen_fields_output_shape_planning = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "target_artifact": "governance_canonical_frozen_fields_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in frozen_rows),
        **_planning_meta(),
    }
    phase_mode_lifecycle_output_shape_planning = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "target_artifact": "governance_phase_mode_lifecycle_contract_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in lifecycle_rows),
        **_planning_meta(),
    }
    constraint_required_fields_output_shape_planning = {
        "rows": required_rows,
        "row_count": len(required_rows),
        "target_artifact": "governance_constraint_required_fields_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in required_rows),
        **_planning_meta(),
    }
    verifier_baseline_output_shape_planning = {
        "rows": baseline_rows,
        "row_count": len(baseline_rows),
        "target_artifact": "governance_constraint_verifier_baseline_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in baseline_rows),
        **_planning_meta(),
    }
    non_claims_and_forbidden_shortcut_library_planning = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "non_claims_count": sum(1 for r in non_claims_rows if r.get("rule_type") == "non_claim"),
        "forbidden_shortcut_count": sum(1 for r in non_claims_rows if r.get("rule_type") == "forbidden_shortcut"),
        "all_not_generated_now": all(r.get("not_generated_now") for r in non_claims_rows),
        **_planning_meta(),
    }
    constraint_extension_rule_planning = {
        "rows": extension_rows,
        "row_count": len(extension_rows),
        "target_artifact": "governance_constraint_extension_rule_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in extension_rows),
        **_planning_meta(),
    }
    legacy_absorption_policy_output_shape_planning = {
        "rows": absorption_rows,
        "row_count": len(absorption_rows),
        "target_artifact": "governance_legacy_absorption_policy_v1.json",
        "all_not_generated_now": all(r.get("not_generated_now") for r in absorption_rows),
        **_planning_meta(),
    }

    governance_constraint_module_generation_planning_readiness_decision = {
        "ready_for_governance_constraint_module_generation_dryrun": boundary_ok,
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
        "module_generation_planning_completed": boundary_ok,
        "canonical_phase_contract_output_shape_planned": len(contract_rows) >= 12,
        "domain_constraint_registry_output_shape_planned": len(domain_rows) >= 12,
        "phase_inheritance_matrix_output_shape_planned": len(inheritance_rows) >= 10,
        "canonical_frozen_fields_output_shape_planned": len(frozen_rows) >= 25,
        "phase_mode_lifecycle_output_shape_planned": len(lifecycle_rows) >= 15,
        "required_fields_output_shape_planned": len(required_rows) >= 12,
        "verifier_baseline_output_shape_planned": len(baseline_rows) >= 15,
        "non_claims_and_forbidden_shortcut_library_planned": len(non_claims_rows) >= 15,
        "extension_rule_planned": len(extension_rows) >= 12,
        "legacy_absorption_policy_output_shape_planned": len(absorption_rows) >= 12,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_legacy_extraction_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
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
        "all_output_shapes_planned": counts_ok,
        "all_not_generated_now": all(
            r.get("not_generated_now")
            for rows in all_rows
            for r in rows
        ),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_planning_policy": governance_constraint_module_generation_planning_policy,
        "canonical_phase_contract_output_shape_planning": canonical_phase_contract_output_shape_planning,
        "domain_constraint_registry_output_shape_planning": domain_constraint_registry_output_shape_planning,
        "phase_inheritance_matrix_output_shape_planning": phase_inheritance_matrix_output_shape_planning,
        "canonical_frozen_fields_output_shape_planning": canonical_frozen_fields_output_shape_planning,
        "phase_mode_lifecycle_output_shape_planning": phase_mode_lifecycle_output_shape_planning,
        "constraint_required_fields_output_shape_planning": constraint_required_fields_output_shape_planning,
        "verifier_baseline_output_shape_planning": verifier_baseline_output_shape_planning,
        "non_claims_and_forbidden_shortcut_library_planning": non_claims_and_forbidden_shortcut_library_planning,
        "constraint_extension_rule_planning": constraint_extension_rule_planning,
        "legacy_absorption_policy_output_shape_planning": legacy_absorption_policy_output_shape_planning,
        "governance_constraint_module_generation_planning_readiness_decision": governance_constraint_module_generation_planning_readiness_decision,
    }
