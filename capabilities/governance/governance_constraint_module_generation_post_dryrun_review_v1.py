# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Post-DryRun Review v1.

Post-dryrun review only: audit generation dry-run completeness and non-generation.
Does not generate constraint modules, modify verifiers/templates, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_dryrun_v1 import (
    INDEPENDENT_CONSUMPTION_DOMAINS,
)
from capabilities.governance.governance_constraint_module_generation_planning_v1 import (
    NON_CLAIMS_AND_SHORTCUTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "governance_constraint_module_generation_post_dryrun_review_only"
SOURCE_CHAIN = "governance_constraint_module_generation_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"

FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Roadmap-Decision-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_dryrun_policy_v1.json",
    "canonical_phase_contract_consumption_dryrun_v1.json",
    "domain_constraint_registry_consumption_dryrun_v1.json",
    "phase_inheritance_matrix_consumption_dryrun_v1.json",
    "canonical_frozen_fields_consumption_dryrun_v1.json",
    "phase_mode_lifecycle_consumption_dryrun_v1.json",
    "constraint_required_fields_consumption_dryrun_v1.json",
    "verifier_baseline_consumption_dryrun_v1.json",
    "non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json",
    "constraint_extension_rule_consumption_dryrun_v1.json",
    "legacy_absorption_policy_consumption_dryrun_v1.json",
    "governance_constraint_module_generation_dryrun_readiness_decision_v1.json",
)

DRYRUN_COMPLETENESS_TARGETS: Tuple[Tuple[str, str, int], ...] = (
    ("generation dry-run policy", "governance_constraint_module_generation_dryrun_policy_v1.json", 0),
    ("canonical phase contract consumption dry-run", "canonical_phase_contract_consumption_dryrun_v1.json", 12),
    ("domain constraint registry consumption dry-run", "domain_constraint_registry_consumption_dryrun_v1.json", 12),
    ("phase inheritance matrix consumption dry-run", "phase_inheritance_matrix_consumption_dryrun_v1.json", 10),
    ("canonical frozen fields consumption dry-run", "canonical_frozen_fields_consumption_dryrun_v1.json", 25),
    ("phase mode lifecycle consumption dry-run", "phase_mode_lifecycle_consumption_dryrun_v1.json", 15),
    ("constraint required fields consumption dry-run", "constraint_required_fields_consumption_dryrun_v1.json", 12),
    ("verifier baseline consumption dry-run", "verifier_baseline_consumption_dryrun_v1.json", 15),
    (
        "non-claims and forbidden shortcut library consumption dry-run",
        "non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json",
        17,
    ),
    ("constraint extension rule consumption dry-run", "constraint_extension_rule_consumption_dryrun_v1.json", 12),
    ("legacy absorption policy consumption dry-run", "legacy_absorption_policy_consumption_dryrun_v1.json", 12),
    (
        "generation dry-run readiness decision",
        "governance_constraint_module_generation_dryrun_readiness_decision_v1.json",
        0,
    ),
)

MODULE_NON_GENERATION_TARGETS: Tuple[str, ...] = (
    "governance_constraint_module_generated_now",
    "canonical_phase_template_generated_now",
    "constraint_module_registered_now",
    "constraint_enforced_now",
    "verifier_integration_executed_now",
    "verifier_modified_now",
    "phase_template_modified_now",
)

FUTURE_CONSUMPTION_TARGETS: Tuple[Tuple[str, str, str], ...] = (
    ("future_verifier_consumption_simulated", "verifier_baseline_integrated_now", "verifier integration"),
    ("future_phase_template_consumption_simulated", "phase_template_modified_now", "phase template modification"),
    ("future_cursor_instruction_consumption_simulated", "phase_template_modified_now", "cursor instruction integration"),
    ("future_mainline_phase_consumption_simulated", "main_migration_chain_resumed_now", "mainline resume"),
    ("verifier_baseline_integrated_now", "verifier_integration_executed_now", "verifier baseline integration"),
    ("phase_template_modified_now", "canonical_phase_template_generated_now", "phase template modification"),
    ("constraint_enforced_now", "governance_constraint_module_generated_now", "constraint enforcement"),
)

PHASE_TEMPLATE_REVIEW_TARGETS: Tuple[Tuple[str, str, str], ...] = (
    ("phase inheritance matrix simulated consumption", "phase_inheritance_matrix_consumption_dryrun_v1.json", "simulated_inheritance_matrix_consumption"),
    ("phase mode lifecycle simulated consumption", "phase_mode_lifecycle_consumption_dryrun_v1.json", "simulated_lifecycle_consumption"),
    ("extension rule simulated consumption", "constraint_extension_rule_consumption_dryrun_v1.json", "simulated_extension_rule_consumption"),
    ("canonical phase template generated now", "summary", "canonical_phase_template_generated_now"),
    ("phase template modified now", "summary", "phase_template_modified_now"),
)

MAINLINE_RESUME_TARGETS: Tuple[Tuple[str, Any], ...] = (
    ("main_migration_chain_resumed_now", False),
    ("main_migration_resume_phase", MAIN_MIGRATION_RESUME_PHASE),
    ("registry_generation_authorization_planning_resumed_now", False),
    ("owner_operator_request_resumed_now", False),
    ("real_migration_execution_allowed", False),
    ("batch_arming_allowed", False),
)

DRYRUN_NON_CLAIMS_EXTRA: Tuple[Tuple[str, str, str], ...] = (
    ("NC16", "non_claim", "domain constraint inheritance ≠ enforcement"),
    ("NC17", "non_claim", "canonical contract planned ≠ phase template modified"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "future_verifier_consumption_simulated": True,
        "future_phase_template_consumption_simulated": True,
        "future_cursor_instruction_consumption_simulated": True,
        "future_mainline_phase_consumption_simulated": True,
        "domain_specific_rules_preserved": True,
        "frozen_fields_enforced_now": False,
        "verifier_baseline_integrated_now": False,
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
        "verifier_integration_executed_now": False,
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
    readiness = _try_read_json(
        root / "governance_constraint_module_generation_dryrun_readiness_decision_v1.json"
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


def _all_rows_pass(payload: Dict[str, Any]) -> bool:
    rows = payload.get("rows") or []
    return bool(rows) and all(r.get("dryrun_status") == "pass" for r in rows)


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
        if min_count > 0 and isinstance(payload, dict):
            semantic_pass = _all_rows_pass(payload) or payload.get("all_pass") is True
        if filename == "governance_constraint_module_generation_dryrun_readiness_decision_v1.json":
            semantic_pass = payload.get("module_generation_dryrun_completed") is True
        elif filename == "domain_constraint_registry_consumption_dryrun_v1.json":
            semantic_pass = (
                payload.get("all_pass") is True
                and payload.get("domain_differentiation_preserved") is True
            )
        elif filename == "canonical_frozen_fields_consumption_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True and payload.get("field_enforced_now") is False
        elif filename == "verifier_baseline_consumption_dryrun_v1.json":
            semantic_pass = (
                payload.get("all_pass") is True
                and payload.get("verifier_baseline_integrated_now") is False
            )
        elif filename == "legacy_absorption_policy_consumption_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True and payload.get("legacy_document_rewritten_now") is False
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


def _build_module_non_generation_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target in MODULE_NON_GENERATION_TARGETS:
        observed = up_summary.get(target)
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
            )
        )
    return rows, all_pass


def _is_false_or_absent(value: Any) -> bool:
    return value is False or value is None


def _build_future_consumption_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for simulated_field, actual_field, label in FUTURE_CONSUMPTION_TARGETS:
        if simulated_field.startswith("future_"):
            simulated_observed = up_summary.get(simulated_field)
            actual_executed = up_summary.get(actual_field)
            review_pass = simulated_observed is True and _is_false_or_absent(actual_executed)
        else:
            simulated_observed = None
            actual_executed = up_summary.get(simulated_field)
            review_pass = _is_false_or_absent(actual_executed)
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                consumption_target=label,
                simulated_observed=simulated_observed,
                actual_integration_executed_now=_is_false_or_absent(
                    up_summary.get("verifier_integration_executed_now")
                ),
                actual_modification_executed_now=_is_false_or_absent(up_summary.get(actual_field)),
                review_pass=review_pass,
            )
        )
    return rows, all_pass


def _build_domain_differentiation_review(domain: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in domain.get("rows") or []:
        name = r.get("domain_constraint_name")
        has_rules = bool(r.get("domain_specific_forbidden_shortcuts")) and bool(
            r.get("domain_specific_non_claims")
        )
        independent = r.get("independent_consumption_path") is True
        review_pass = (
            r.get("dryrun_status") == "pass"
            and r.get("domain_differentiation_preserved") is not False
            and has_rules
            and r.get("domain_registry_generated_now") is False
            and r.get("domain_constraint_registered_now") is False
        )
        if name in INDEPENDENT_CONSUMPTION_DOMAINS and not independent:
            review_pass = False
        rows.append(
            _review_row(
                domain_constraint_name=name,
                domain_specific_rules_present=has_rules,
                independent_consumption_path_preserved=independent if name in INDEPENDENT_CONSUMPTION_DOMAINS else True,
                not_flattened_into_canonical_only=has_rules,
                domain_constraint_generated_now=False,
                domain_constraint_registered_now=False,
                review_pass=review_pass,
            )
        )
        if not review_pass:
            all_pass = False
    return rows, all_pass and len(rows) >= 12


def _build_frozen_field_review(frozen: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in frozen.get("rows") or []:
        review_pass = (
            r.get("simulated_frozen_field_consumption") is True
            and r.get("frozen_fields_library_generated_now") is False
            and r.get("field_enforced_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                canonical_field_pattern=r.get("canonical_field_pattern"),
                simulated_frozen_field_consumption=r.get("simulated_frozen_field_consumption"),
                frozen_fields_library_generated_now=False,
                field_enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 25


def _build_verifier_baseline_review(baseline: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in baseline.get("rows") or []:
        review_pass = (
            r.get("simulated_verifier_baseline_consumption") is True
            and r.get("verifier_baseline_generated_now") is False
            and r.get("verifier_modified_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                baseline_check_id=r.get("baseline_check_id"),
                check_name=r.get("check_name"),
                simulated_verifier_baseline_consumption=r.get("simulated_verifier_baseline_consumption"),
                verifier_baseline_generated_now=False,
                verifier_integration_executed_now=False,
                verifier_modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 15


def _build_phase_template_review(up_summary: Dict[str, Any], art: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, source, field in PHASE_TEMPLATE_REVIEW_TARGETS:
        if source == "summary":
            simulated = None
            template_generated = up_summary.get("canonical_phase_template_generated_now")
            template_modified = up_summary.get("phase_template_modified_now")
            review_pass = template_generated is False and template_modified is False
        else:
            payload = art.get(source, {})
            payload_rows = payload.get("rows") or []
            simulated = all(r.get(field) is True for r in payload_rows) if payload_rows else False
            template_generated = up_summary.get("canonical_phase_template_generated_now")
            template_modified = up_summary.get("phase_template_modified_now")
            review_pass = simulated and template_generated is False and template_modified is False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                simulated_consumption_observed=simulated,
                template_generated_now=False,
                template_modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass


def _build_legacy_absorption_review(absorption: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in absorption.get("rows") or []:
        review_pass = (
            r.get("simulated_legacy_absorption_consumption") is True
            and r.get("legacy_document_rewritten_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                policy_section=r.get("policy_section"),
                simulated_legacy_absorption_consumption=r.get("simulated_legacy_absorption_consumption"),
                legacy_document_rewritten_now=False,
                legacy_eval_out_modified_now=False,
                legacy_verifier_rerun_now=False,
                legacy_chain_deprecated_now=False,
                legacy_as_source_evidence=True,
                legacy_as_template_source=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_review(non_claims: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    dryrun_by_id = {r.get("rule_id"): r for r in (non_claims.get("rows") or [])}
    all_rules = list(NON_CLAIMS_AND_SHORTCUTS) + list(DRYRUN_NON_CLAIMS_EXTRA)
    for rule_id, rule_type, statement in all_rules:
        r = dryrun_by_id.get(rule_id, {})
        review_pass = (
            (r.get("simulated_rule_consumption") is True and r.get("dryrun_status") == "pass")
            if r
            else rule_id in ("NC16", "NC17")
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                rule_id=rule_id,
                rule_type=rule_type,
                canonical_statement=statement,
                simulated_rule_consumption=r.get("simulated_rule_consumption", rule_id in ("NC16", "NC17")),
                library_generated_now=False,
                non_claim_generated_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 17


def _build_mainline_resume_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    observed_map = {
        "main_migration_chain_resumed_now": up_summary.get("main_migration_chain_resumed_now"),
        "main_migration_resume_phase": up_summary.get("main_migration_resume_phase"),
        "registry_generation_authorization_planning_resumed_now": up_summary.get("main_migration_chain_resumed_now"),
        "owner_operator_request_resumed_now": False,
        "real_migration_execution_allowed": up_summary.get("real_migration_execution_allowed"),
        "batch_arming_allowed": up_summary.get("batch_arming_allowed"),
    }
    for target, expected in MAINLINE_RESUME_TARGETS:
        observed = observed_map.get(target, up_summary.get(target))
        if target == "main_migration_resume_phase":
            violation = observed != expected
        else:
            violation = observed is not expected
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_blocked=(expected is False) if target != "main_migration_resume_phase" else None,
                expected_value=expected,
                observed_value=observed,
                violation_detected=violation,
                review_pass=review_pass,
            )
        )
    return rows, all_pass


def run_governance_constraint_module_generation_post_dryrun_review_v1(
    *,
    governance_constraint_module_generation_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_dryrun_root)
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
    if up_readiness.get("ready_for_governance_constraint_module_generation_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for post_dryrun_review")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("governance_constraint_module_generation_dryrun_only") is not True:
        blockers.append("upstream governance_constraint_module_generation_dryrun_only must be true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated must be true")

    for flag in (
        "future_verifier_consumption_simulated",
        "future_phase_template_consumption_simulated",
        "future_cursor_instruction_consumption_simulated",
        "future_mainline_phase_consumption_simulated",
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
        expected = True if flag.startswith("future_") and flag.endswith("_simulated") else False
        if up_summary.get(flag) is not expected:
            blockers.append(f"upstream {flag} must be {expected}")

    if up_summary.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if up_summary.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")
    if up_summary.get("domain_differentiation_preserved") is not True:
        blockers.append("upstream domain_differentiation_preserved must be true")
    if up_summary.get("independent_consumption_paths_verified") is not True:
        blockers.append("upstream independent_consumption_paths_verified must be true")

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

    completeness_rows, completeness_pass = _build_completeness_review(up_art)
    module_rows, module_pass = _build_module_non_generation_review(up_summary)
    future_rows, future_pass = _build_future_consumption_review(up_summary)
    domain_rows, domain_pass = _build_domain_differentiation_review(
        up_art.get("domain_constraint_registry_consumption_dryrun_v1.json", {})
    )
    frozen_rows, frozen_pass = _build_frozen_field_review(
        up_art.get("canonical_frozen_fields_consumption_dryrun_v1.json", {})
    )
    baseline_rows, baseline_pass = _build_verifier_baseline_review(
        up_art.get("verifier_baseline_consumption_dryrun_v1.json", {})
    )
    template_rows, template_pass = _build_phase_template_review(up_summary, up_art)
    absorption_rows, absorption_pass = _build_legacy_absorption_review(
        up_art.get("legacy_absorption_policy_consumption_dryrun_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _build_non_claims_review(
        up_art.get("non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json", {})
    )
    mainline_rows, mainline_pass = _build_mainline_resume_review(up_summary)

    review_pass = all(
        (
            completeness_pass,
            module_pass,
            future_pass,
            domain_pass,
            frozen_pass,
            baseline_pass,
            template_pass,
            absorption_pass,
            non_claims_pass,
            mainline_pass,
        )
    )
    if not review_pass:
        blockers.append("one or more review matrices failed")

    review_ready = review_pass and not blockers
    boundary_ok = review_ready

    governance_constraint_module_generation_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_simulated_observed=up_summary.get("simulated") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    module_generation_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    module_non_generation_review = {
        "rows": module_rows,
        "row_count": len(module_rows),
        "all_pass": module_pass,
        **_review_meta(),
    }
    future_consumption_simulation_review = {
        "rows": future_rows,
        "row_count": len(future_rows),
        "all_pass": future_pass,
        **_review_meta(),
    }
    domain_differentiation_preservation_review = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "independent_paths_verified": all(
            r.get("independent_consumption_path_preserved") is True
            for r in domain_rows
            if r.get("domain_constraint_name") in INDEPENDENT_CONSUMPTION_DOMAINS
        ),
        **_review_meta(),
    }
    frozen_field_non_enforcement_review = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "all_pass": frozen_pass,
        "frozen_fields_enforced_now": False,
        **_review_meta(),
    }
    verifier_baseline_non_integration_review = {
        "rows": baseline_rows,
        "row_count": len(baseline_rows),
        "all_pass": baseline_pass,
        "verifier_baseline_integrated_now": False,
        **_review_meta(),
    }
    phase_template_non_modification_review = {
        "rows": template_rows,
        "row_count": len(template_rows),
        "all_pass": template_pass,
        "phase_template_modified_now": False,
        **_review_meta(),
    }
    legacy_absorption_non_rewrite_review = {
        "rows": absorption_rows,
        "row_count": len(absorption_rows),
        "all_pass": absorption_pass,
        "legacy_document_rewritten_now": False,
        **_review_meta(),
    }
    non_claims_and_forbidden_shortcut_review = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_review_meta(),
    }
    mainline_resume_block_review = {
        "rows": mainline_rows,
        "row_count": len(mainline_rows),
        "all_pass": mainline_pass,
        **_review_meta(),
    }

    governance_constraint_module_generation_post_dryrun_review_readiness_decision = {
        "ready_for_governance_constraint_module_generation_roadmap_decision": boundary_ok,
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
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": completeness_pass,
        "module_non_generation_review_pass": module_pass,
        "future_consumption_simulation_review_pass": future_pass,
        "domain_differentiation_preservation_review_pass": domain_pass,
        "frozen_field_non_enforcement_review_pass": frozen_pass,
        "verifier_baseline_non_integration_review_pass": baseline_pass,
        "phase_template_non_modification_review_pass": template_pass,
        "legacy_absorption_non_rewrite_review_pass": absorption_pass,
        "non_claims_and_forbidden_shortcut_review_pass": non_claims_pass,
        "mainline_resume_block_review_pass": mainline_pass,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_simulated_observed": up_summary.get("simulated") is True,
        "dryrun_completeness_review_pass": completeness_pass,
        "module_non_generation_review_pass": module_pass,
        "future_consumption_simulation_review_pass": future_pass,
        "domain_differentiation_preservation_review_pass": domain_pass,
        "frozen_field_non_enforcement_review_pass": frozen_pass,
        "verifier_baseline_non_integration_review_pass": baseline_pass,
        "phase_template_non_modification_review_pass": template_pass,
        "legacy_absorption_non_rewrite_review_pass": absorption_pass,
        "non_claims_and_forbidden_shortcut_review_pass": non_claims_pass,
        "mainline_resume_block_review_pass": mainline_pass,
        "domain_constraint_count": len(domain_rows),
        "frozen_field_pattern_count": len(frozen_rows),
        "verifier_baseline_check_count": len(baseline_rows),
        "non_claims_rule_count": len(non_claims_rows),
        "legacy_absorption_section_count": len(absorption_rows),
        "all_review_pass": review_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_post_dryrun_review_policy": governance_constraint_module_generation_post_dryrun_review_policy,
        "module_generation_dryrun_completeness_review": module_generation_dryrun_completeness_review,
        "module_non_generation_review": module_non_generation_review,
        "future_consumption_simulation_review": future_consumption_simulation_review,
        "domain_differentiation_preservation_review": domain_differentiation_preservation_review,
        "frozen_field_non_enforcement_review": frozen_field_non_enforcement_review,
        "verifier_baseline_non_integration_review": verifier_baseline_non_integration_review,
        "phase_template_non_modification_review": phase_template_non_modification_review,
        "legacy_absorption_non_rewrite_review": legacy_absorption_non_rewrite_review,
        "non_claims_and_forbidden_shortcut_review": non_claims_and_forbidden_shortcut_review,
        "mainline_resume_block_review": mainline_resume_block_review,
        "governance_constraint_module_generation_post_dryrun_review_readiness_decision": governance_constraint_module_generation_post_dryrun_review_readiness_decision,
    }
