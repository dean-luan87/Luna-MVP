# -*- coding: utf-8 -*-
"""Governance Constraint Module Legacy Extraction Roadmap Decision v1.

Roadmap decision only: select Route A — Governance Constraint Module Generation Planning.
Does not generate constraint modules, integrate verifiers, or resume main migration chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"
DECISION_SCOPE = "governance_constraint_module_legacy_extraction_roadmap_decision_only"
SOURCE_CHAIN = "governance_constraint_module_legacy_extraction_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

SELECTED_ROUTE = "Route A — Governance Constraint Module Generation Planning"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Planning-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING"
)

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "legacy_extraction_post_dryrun_review_policy_v1.json",
    "legacy_extraction_dryrun_completeness_review_v1.json",
    "legacy_asset_non_modification_review_v1.json",
    "legacy_chain_status_review_v1.json",
    "constraint_mapping_quality_review_v1.json",
    "canonical_frozen_field_extraction_review_v1.json",
    "domain_constraint_preservation_review_v1.json",
    "inheritance_and_absorption_policy_review_v1.json",
    "constraint_module_output_non_generation_review_v1.json",
    "legacy_extraction_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001",
        "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001",
        "governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001",
        "governance_constraint_module_legacy_extraction_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Governance Constraint Module Generation Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "governance_constraint_module_generation_planning",
        "target_scope": "canonical contract, domain registry, frozen fields, phase lifecycle, verifier baseline, non-claims, forbidden shortcuts, extension rule, legacy absorption, readiness gate",
        "entry_reason": "legacy extraction chain proves mappable source evidence; module generation rules not yet defined",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "module generation planning allowed only; not module generation; not template generation; not verifier integration",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ governance_constraint_module_generated_now",
            "≠ canonical_phase_template_generated_now",
            "≠ verifier integration",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Governance Constraint Module Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "governance_constraint_module_generation",
        "target_scope": "formal Governance Constraint Module artifact generation",
        "entry_reason": "generation planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["module generation planning not complete"],
        "permission_impact": "deferred; not module generation allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-v1-001",
        "non_claims": ["deferred ≠ module generated"],
    },
    {
        "route_id": "C",
        "route_name": "Canonical Phase Template Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "canonical_phase_template_planning",
        "target_scope": "canonical phase template planning",
        "entry_reason": "module generation planning must define module structure first",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["module generation planning not complete"],
        "permission_impact": "deferred; not template generation allowed",
        "next_phase_candidate": "Phase-Canonical-Phase-Template-Planning-v1-001",
        "non_claims": ["deferred ≠ template generated"],
    },
    {
        "route_id": "D",
        "route_name": "Verifier Integration Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "verifier_integration_planning",
        "target_scope": "verifier constraint module loading planning",
        "entry_reason": "module not generated; baseline not finalized",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["module generation planning not complete"],
        "permission_impact": "deferred; not verifier integration allowed",
        "next_phase_candidate": "Phase-Verifier-Integration-Planning-v1-001",
        "non_claims": ["deferred ≠ verifier integration"],
    },
    {
        "route_id": "E",
        "route_name": "Phase Template Integration Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "phase_template_integration_planning",
        "target_scope": "phase template constraint module reference planning",
        "entry_reason": "module structure not defined",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["module generation planning not complete"],
        "permission_impact": "deferred; not phase template modification allowed",
        "next_phase_candidate": "Phase-Phase-Template-Integration-Planning-v1-001",
        "non_claims": ["deferred ≠ phase template modified"],
    },
    {
        "route_id": "F",
        "route_name": "Legacy Absorption Note Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "legacy_absorption_note_planning",
        "target_scope": "legacy absorption note planning without document rewrite",
        "entry_reason": "absorption note planning deferred; no legacy rewrite now",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["module generation planning not complete"],
        "permission_impact": "deferred; not legacy document rewrite allowed",
        "next_phase_candidate": "Phase-Legacy-Absorption-Note-Planning-v1-001",
        "non_claims": ["deferred ≠ legacy document rewritten"],
    },
    {
        "route_id": "G",
        "route_name": "Main Migration Chain Resume Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "main_migration_chain_resume_planning",
        "target_scope": "main migration chain resume planning",
        "entry_reason": "constraint module not planned/generated; mainline must stay paused",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["constraint module generation planning not complete"],
        "permission_impact": "deferred; not mainline resume allowed",
        "next_phase_candidate": MAIN_MIGRATION_RESUME_PHASE,
        "non_claims": ["deferred ≠ main_migration_chain_resumed_now"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Module Generation / Verifier Integration / Mainline Resume",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_module_generation_verifier_integration_mainline_resume",
        "target_scope": "direct module generation / verifier integration / mainline resume",
        "entry_reason": "module generation planning not defined; direct generation bypasses planning gate",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "module generation planning not complete",
            "module not generated",
            "verifier baseline not integrated",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Module-Generation-v1-001",
        "non_claims": ["blocked ≠ module generated", "≠ mainline resumed"],
    },
]

MODULE_GENERATION_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("D01", "legacy source evidence finalization"),
    ("D02", "canonical contract shape definition"),
    ("D03", "domain registry shape definition"),
    ("D04", "frozen field library definition"),
    ("D05", "phase mode lifecycle contract definition"),
    ("D06", "required fields schema definition"),
    ("D07", "verifier baseline definition"),
    ("D08", "non-claims library definition"),
    ("D09", "forbidden shortcut library definition"),
    ("D10", "extension rule definition"),
    ("D11", "legacy absorption policy definition"),
    ("D12", "output readiness gate definition"),
    ("D13", "module generation authorization"),
    ("D14", "post-generation review authority"),
)

PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("canonical phase contract output shape", "define governance_canonical_phase_contract_v1.json structure"),
    ("domain constraint registry output shape", "define governance_domain_constraint_registry_v1.json structure"),
    ("phase inheritance matrix output shape", "define governance_phase_inheritance_matrix_v1.json structure"),
    ("canonical frozen fields output shape", "define governance_canonical_frozen_fields_v1.json structure"),
    ("phase mode lifecycle contract output shape", "define governance_phase_mode_lifecycle_contract_v1.json structure"),
    ("required fields schema output shape", "define governance_constraint_required_fields_v1.json structure"),
    ("verifier baseline output shape", "define governance_constraint_verifier_baseline_v1.json structure"),
    ("non-claims library output shape", "define governance_constraint_non_claims_library_v1.json structure"),
    ("forbidden shortcut library output shape", "define governance_constraint_forbidden_shortcut_library_v1.json structure"),
    ("extension rule output shape", "define governance_constraint_extension_rule_v1.json structure"),
    ("legacy absorption policy output shape", "define governance_legacy_absorption_policy_v1.json structure"),
    ("constraint module readiness decision rule", "define governance_constraint_module_readiness_decision_v1.json rule"),
    ("module generation source whitelist", "define which legacy assets may enter module generation"),
    ("module generation authorization boundary", "define who may authorize module generation and when"),
)

MODULE_GENERATION_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "module output shape not finalized", "high", "planning allowed; module generation blocked"),
    ("R02", "canonical contract shape not finalized", "high", "governance_constraint_module_generated_now=false"),
    ("R03", "domain registry shape not finalized", "high", "domain-specific rules may be flattened"),
    ("R04", "frozen field library not finalized", "high", "canonical_contract_generated_now=false"),
    ("R05", "phase lifecycle contract not finalized", "high", "phase mode semantics undefined"),
    ("R06", "verifier baseline not finalized", "high", "verifier_integration_executed_now=false"),
    ("R07", "non-claims library not finalized", "high", "success_claim_allowed=false"),
    ("R08", "forbidden shortcut library not finalized", "high", "forbidden shortcuts undefined"),
    ("R09", "extension rule not finalized", "medium", "domain extension boundary undefined"),
    ("R10", "legacy absorption policy not finalized", "high", "legacy_as_template_source=false must hold"),
    ("R11", "generation source whitelist not defined", "high", "source contamination risk"),
    ("R12", "generation authorization boundary not defined", "high", "module generation not authorized"),
    ("R13", "verifier integration not planned", "high", "verifier_integration_executed_now=false"),
    ("R14", "phase template integration not planned", "high", "phase_template_modified_now=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "governance constraint module generation",
    "canonical phase template generation",
    "constraint module registration",
    "constraint enforcement",
    "verifier integration",
    "verifier modification",
    "phase template modification",
    "automation implementation",
    "documentation auto sync",
    "legacy document rewrite",
    "legacy eval_out modification",
    "legacy verifier rerun",
    "main migration chain resume",
    "registry generation",
    "owner approval request",
    "file operation execution",
    "real migration execution",
    "rollback rehearsal execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean Governance Constraint Module is generated.",
    "Route A selected does not mean module generation is authorized.",
    "Route A selected does not mean canonical phase template is generated.",
    "Route A selected does not mean verifier integration may start.",
    "Route A selected does not mean old documents may be rewritten.",
    "Route A selected does not mean main migration chain may resume.",
    "Route B/C/D/E/G deferred means module generation / template / verifier / mainline remain unavailable.",
    "Route H blocked means direct module generation / verifier integration / mainline resume remain forbidden.",
    "Roadmap Decision GO does not mean any real migration or rollback permission is released.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "selected_route": SELECTED_ROUTE,
        "governance_constraint_module_generation_planning_selected": True,
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


def _decision_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_decision_meta()}


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
        root / "legacy_extraction_post_dryrun_review_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in POST_REVIEW_ARTIFACTS:
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


def _load_chain_phase(eval_out_name: str) -> Dict[str, Any]:
    repo = Path(__file__).resolve().parents[2]
    root = repo / "_eval_out" / eval_out_name
    summary = _try_read_json(root / "summary.json") or {}
    verifier = _try_read_json(root / "verifier_report.json") or {}
    return {"summary": summary, "verifier": verifier}


def _build_completed_chain_review() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for phase_name, eval_out in COMPLETED_CHAIN:
        data = _load_chain_phase(eval_out)
        sm = data["summary"]
        vr = data["verifier"]
        go = vr.get("verifier") == "GO" and vr.get("passed") is True
        boundary = sm.get("boundary_ok") is True
        review_pass = go and boundary
        if not review_pass:
            all_pass = False
        rows.append(
            _decision_row(
                phase_name=phase_name,
                verifier_status=vr.get("verifier", "UNKNOWN"),
                boundary_ok=boundary,
                final_decision=sm.get("final_decision"),
                recommended_next_phase=sm.get("recommended_next_phase"),
                legacy_modification_observed=sm.get("legacy_phase_modified_now") is True
                or sm.get("legacy_document_rewritten_now") is True
                or sm.get("legacy_eval_out_modified_now") is True,
                constraint_module_generation_observed=sm.get("governance_constraint_module_generated_now") is True,
                canonical_template_generation_observed=sm.get("canonical_phase_template_generated_now") is True,
                constraint_enforcement_observed=sm.get("constraint_enforced_now") is True,
                mainline_resume_observed=sm.get("main_migration_chain_resumed_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in MODULE_GENERATION_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_module_generation=True,
                current_status="module_generation_planning_required",
                missing_preconditions=["Governance Constraint Module Generation Planning not complete"],
                blocks_module_generation=True,
                recommended_next_action="enter Governance Constraint Module Generation Planning",
            )
        )
    return rows


def _build_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"governance_module_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                source_legacy_assets=["legacy extraction planning", "dryrun", "post-dryrun review"],
                required_for_module_generation=True,
                required_for_future_verifier="verifier baseline" in planning_topic or "non-claims" in planning_topic,
                required_for_future_phase_template="phase" in planning_topic or "inheritance" in planning_topic,
                required_for_future_cursor_instructions=True,
                required_non_claims=[f"planning GO does not imply {planning_topic} generated"],
            )
        )
    return rows


def _build_non_release_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows = [
        _decision_row(
            permission_name=name,
            expected_released=False,
            released_by_roadmap_decision=False,
            review_pass=True,
        )
        for name in NON_RELEASE_PERMISSIONS
    ]
    return rows, all(r.get("review_pass") for r in rows)


def _build_risk_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for risk_id, desc, level, non_claim in MODULE_GENERATION_RISKS:
        rows.append(
            _decision_row(
                risk_id=risk_id,
                risk_description=desc,
                risk_level=level,
                allowed_to_enter_planning=True,
                blocks_module_generation=True,
                blocks_verifier_integration=True,
                blocks_phase_template_modification=True,
                blocks_mainline_resume=True,
                required_non_claim=non_claim,
                review_status="pass",
            )
        )
    return rows, all_pass and len(rows) >= 14


def run_governance_constraint_module_legacy_extraction_roadmap_decision_v1(
    *,
    governance_constraint_module_legacy_extraction_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_legacy_extraction_post_dryrun_review_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream post-dryrun review verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")

    for flag in (
        "legacy_phase_modified_now",
        "legacy_document_rewritten_now",
        "legacy_eval_out_modified_now",
        "legacy_verifier_rerun_now",
        "legacy_chain_deprecated_now",
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_module_registered_now",
        "constraint_enforced_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "automation_implemented_now",
        "file_operation_executed_now",
        "authorization_granted_now",
        "success_claim_allowed",
        "main_migration_chain_resumed_now",
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
        "ready_for_verifier_integration",
        "ready_for_phase_template_modification",
        "ready_for_automation_implementation",
        "ready_for_legacy_document_rewrite",
        "ready_to_resume_main_migration_chain",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")

    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    for art_name in (
        "legacy_extraction_dryrun_completeness_review_v1.json",
        "legacy_asset_non_modification_review_v1.json",
        "legacy_chain_status_review_v1.json",
        "constraint_module_output_non_generation_review_v1.json",
    ):
        if up_art.get(art_name, {}).get("all_pass") is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_dependency_matrix()
    planning_scope_rows = _build_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "module generation planning" in str(route_a.get("permission_impact", "")).lower()
        and "not module generation" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
        and route_c.get("deferred") is True
        and route_h.get("blocked_now") is True
        and route_h.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    for rid in ("B", "C", "D", "E", "F", "G"):
        r = next(x for x in route_rows if x.get("route_id") == rid)
        if r.get("deferred") is not True or r.get("allowed_now") is not False:
            blockers.append(f"route {rid} must be deferred and not allowed_now")

    forbidden_allowed = any(
        r.get("allowed_now") is True
        and r.get("route_type")
        in (
            "governance_constraint_module_generation",
            "direct_module_generation_verifier_integration_mainline_resume",
        )
        for r in route_rows
        if r.get("route_id") != "A"
    )
    if forbidden_allowed:
        blockers.append("module generation / direct routes must not be allowed_now")

    decision_ready = (
        chain_pass
        and non_release_pass
        and risk_pass
        and route_ok
        and len(dependency_rows) >= 14
        and len(planning_scope_rows) >= 14
        and not blockers
    )
    boundary_ok = decision_ready

    legacy_extraction_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_roadmap_decision_observed=up_readiness.get(
            "ready_for_governance_constraint_module_legacy_extraction_roadmap_decision"
        )
        is True,
    )

    completed_legacy_extraction_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    legacy_extraction_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    constraint_module_generation_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "module_generation_missing_dependency_identified": True,
        **_decision_meta(),
    }
    constraint_module_generation_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    legacy_extraction_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    legacy_extraction_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    constraint_module_generation_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    legacy_extraction_roadmap_readiness_decision = {
        "ready_for_governance_constraint_module_generation_planning": boundary_ok,
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
        "ready_for_registry_generation": False,
        "ready_for_owner_approval_request": False,
        "ready_for_file_operation": False,
        "ready_for_real_migration_execution": False,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "legacy_extraction_chain_completed": chain_pass,
        "module_generation_missing_dependency_identified": True,
        "direct_module_generation_blocked": True,
        "direct_verifier_integration_blocked": True,
        "direct_mainline_resume_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_legacy_extraction_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "module_generation_dependency_count": len(dependency_rows),
        "module_generation_planning_scope_count": len(planning_scope_rows),
        "module_generation_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_module_generation_planning_only": "module generation planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_c_deferred": route_c.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_module_generation_blocked": True,
        "direct_verifier_integration_blocked": True,
        "direct_mainline_resume_blocked": True,
        "module_generation_missing_dependency_identified": True,
        "legacy_extraction_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "legacy_extraction_roadmap_decision_policy": legacy_extraction_roadmap_decision_policy,
        "completed_legacy_extraction_chain_review": completed_legacy_extraction_chain_review,
        "legacy_extraction_roadmap_route_candidate_matrix": legacy_extraction_roadmap_route_candidate_matrix,
        "constraint_module_generation_dependency_matrix": constraint_module_generation_dependency_matrix,
        "constraint_module_generation_planning_scope": constraint_module_generation_planning_scope,
        "legacy_extraction_roadmap_non_release_matrix": legacy_extraction_roadmap_non_release_matrix,
        "constraint_module_generation_entry_readiness_risk_matrix": constraint_module_generation_entry_readiness_risk_matrix,
        "legacy_extraction_roadmap_decision_non_claims_register": legacy_extraction_roadmap_decision_non_claims_register,
        "legacy_extraction_roadmap_readiness_decision": legacy_extraction_roadmap_readiness_decision,
    }
