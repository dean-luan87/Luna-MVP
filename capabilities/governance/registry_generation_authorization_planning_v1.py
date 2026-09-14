# -*- coding: utf-8 -*-
"""Registry Generation Authorization Planning v1.

Registry generation authorization planning only: plan authorization mechanisms for
Boundary Object Registry Generation. Does not send authorization requests, grant
authorization, generate registry, or register objects.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.boundary_object_registry_generation_roadmap_decision_v1 import (
    COMPLETED_CHAIN as REGISTRY_GENERATION_CHAIN,
    FINAL_DECISION as REGISTRY_ROADMAP_FINAL,
    SELECTED_ROUTE as REGISTRY_ROADMAP_SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Registry-Generation-Authorization-Planning-v1-001"
PLANNING_SCOPE = "registry_generation_authorization_planning_only"
SOURCE_CHAIN = "registry_generation_authorization_planning_v1"

RETURN_SOURCE_PHASE = "Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001"
RETURN_REQUIRED_FINAL = "RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_READY"
RETURN_REQUIRED_NEXT = "Phase-Registry-Generation-Authorization-Planning-v1-001"

REGISTRY_ROADMAP_PHASE = "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001"

FINAL_DECISION = "REGISTRY_GENERATION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Registry-Generation-Authorization-DryRun-v1-001"

RETURN_UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "return_to_registry_generation_authorization_planning_policy_v1.json",
    "branch_closure_input_review_v1.json",
    "deferred_governance_constraint_module_source_pack_reference_v1.json",
    "mainline_resume_target_binding_v1.json",
    "registry_generation_authorization_planning_reentry_scope_v1.json",
    "return_to_mainline_non_claims_register_v1.json",
    "return_to_registry_generation_authorization_planning_readiness_decision_v1.json",
)

REQUEST_SCHEMA_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("request identity", "unique registry generation authorization request identifier"),
    ("requested registry generation scope", "explicit boundary object registry generation scope"),
    ("registry source set", "inventory of sources bound to this request"),
    ("source final approval requirement", "source set must be final approved before grant"),
    ("contamination final check requirement", "contamination final check must pass before grant"),
    ("entry generation boundary", "entry generation allowed only within declared boundary"),
    ("protected object exclusion", "protected assets excluded from registry generation scope"),
    ("file operation exclusion", "file operations excluded from request scope"),
    ("owner/operator dependency", "owner approval and operator acknowledgement required"),
    ("execution window exclusion", "execution window not opened by request planning"),
    ("non-generation statement", "request planned does not mean registry generated"),
    ("non-registration statement", "registry generated later does not mean object registered"),
    ("requester role", "role that may submit registry authorization request later"),
    ("approver role", "role that may grant registry generation authorization later"),
    ("abort / revoke / rollback authority", "abort, revoke, rollback authorities must be declared"),
)

GRANT_SCHEMA_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("grant identity", "unique registry generation authorization grant identifier"),
    ("granted scope", "explicit registry outputs authorized for generation"),
    ("excluded scope", "registration/file operation/mainline execution excluded"),
    ("source set final approval status", "must reference final approved source set"),
    ("contamination final check status", "must reference passed contamination final check"),
    ("registry generation permission boundary", "generation allowed only within boundary"),
    ("entry generation permission boundary", "entry generation/commit separate authorization"),
    ("post-generation review requirement", "review required before registration"),
    ("registration exclusion", "boundary object registration not included in grant"),
    ("file operation exclusion", "file operations not included in grant"),
    ("expiration / TTL", "grant must have expiration semantics"),
    ("revocation rule", "grant may be revoked under declared conditions"),
)

SOURCE_APPROVAL_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("source inventory", "boundary object registry generation source inventory"),
    ("source whitelist", "approved source types from generation planning"),
    ("source misuse cases", "misuse cases from generation dry-run and review"),
    ("protected object list", "protected assets that must never enter registry"),
    ("policy object list", "policy objects with entry boundary rules"),
    ("category object list", "boundary categories from registry planning"),
    ("owner/operator dependency references", "owner/operator protocol chain references"),
    ("post-dryrun review references", "boundary object registry generation post-dryrun review"),
    ("non-claims references", "non-claims from generation and authorization planning"),
    ("forbidden shortcut references", "forbidden shortcuts from governance constraints"),
    ("branch closure reference", "governance constraint module branch closure eval_out"),
    ("return-to-mainline wrapper reference", "return_to_registry_generation_authorization_planning eval_out"),
)

CONTAMINATION_RISKS: Tuple[Tuple[str, str], ...] = (
    ("summary misuse risk", "summary.json used as registry entry without validation"),
    ("verifier_report misuse risk", "verifier_report.json promoted to registry fact"),
    ("non-claims-as-entry risk", "non-claims text inserted as registry entries"),
    ("protected object contamination risk", "protected assets leak into registry source set"),
    ("deprecated source risk", "deprecated legacy sources used without review"),
    ("stale source risk", "stale eval_out used after branch closure"),
    ("legacy-as-template risk", "legacy chain treated as template source"),
    ("GC deferred capability misuse risk", "deferred GC capability treated as enforced constraint"),
    ("source pack overreach risk", "GC source pack grants generation permission"),
    ("file operation accidental release risk", "file operation implied by registry planning GO"),
    ("authorization request overread risk", "authorization planning GO read as request sent"),
    ("success claim leakage risk", "verifier GO interpreted as success claim or execution allowed"),
)

REGISTRY_GENERATION_AUTHORITIES: Tuple[Tuple[str, str], ...] = (
    ("boundary object registry manifest generation", "boundary_object_registry_manifest_v1.json"),
    ("registry entry schema generation", "registry_entry_schema_v1.json"),
    ("registry source binding generation", "registry_source_binding_v1.json"),
    ("registry category index generation", "registry_category_index_v1.json"),
    ("registry protected object exclusion list generation", "registry_protected_object_exclusion_v1.json"),
    ("registry policy entry boundary generation", "registry_policy_entry_boundary_v1.json"),
    ("registry contamination guard generation", "registry_contamination_guard_v1.json"),
    ("registry generation readiness decision generation", "registry_generation_readiness_decision_v1.json"),
    ("registry non-claims library generation", "registry_non_claims_library_v1.json"),
    ("registry forbidden shortcut library generation", "registry_forbidden_shortcut_library_v1.json"),
    ("registry owner operator dependency generation", "registry_owner_operator_dependency_v1.json"),
    ("registry post-generation review artifact generation", "registry_post_generation_review_v1.json"),
)

ENTRY_GENERATION_BOUNDARIES: Tuple[Tuple[str, str], ...] = (
    ("entry type whitelist", "only declared entry types may be generated"),
    ("source binding required", "every entry must bind to approved source"),
    ("protected object exclusion", "protected objects never become entries"),
    ("policy entry boundary", "policy entries require separate boundary check"),
    ("category entry boundary", "category entries require category validation"),
    ("summary forbidden as entry", "summary fields forbidden as direct entries"),
    ("verifier_report forbidden as entry", "verifier_report forbidden as direct entries"),
    ("non-claims forbidden as entry", "non-claims text forbidden as entries"),
    ("GC source pack reference only", "GC outputs reference-only; not entry source"),
    ("commit separate authorization", "entry commit requires separate grant"),
    ("registration separate authorization", "object registration requires separate grant"),
    ("file operation blocked", "file operation never implied by entry boundary"),
)

OWNER_OPERATOR_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("owner approval request", "owner approval request required before grant"),
    ("owner approval grant", "owner approval must be explicit grant not planning"),
    ("operator acknowledgement", "operator acknowledgement required before execution window"),
    ("execution window closed", "execution window remains closed during planning"),
    ("abort on missing owner", "abort if owner approval missing at request time"),
    ("abort on missing operator", "abort if operator acknowledgement missing"),
    ("revoke on owner withdrawal", "revoke grant if owner withdraws approval"),
    ("revoke on operator withdrawal", "revoke grant if operator withdraws acknowledgement"),
    ("rollback on unauthorized entry", "rollback entries generated without grant"),
    ("rollback on contamination failure", "rollback if contamination check fails post-generation"),
)

FILE_OPERATION_BLOCKS: Tuple[Tuple[str, str], ...] = (
    ("no file read", "file read not authorized by planning phase"),
    ("no file write", "file write not authorized by planning phase"),
    ("no file delete", "file delete not authorized by planning phase"),
    ("no protected asset write", "protected asset write blocked"),
    ("no hr queue write", "human review queue write blocked"),
    ("no dnae write", "DnAE/permanent block write blocked"),
    ("no migration file touch", "migration-related file operations blocked"),
    ("no eval_out mutation", "eval_out mutation blocked except planning artifacts"),
    ("no legacy rewrite", "legacy document rewrite blocked"),
    ("no batch arming file prep", "batch arming file preparation blocked"),
)

VERIFIER_USAGE_CHECKS: Tuple[Tuple[str, str, str], ...] = (
    ("RV01", "registry authorization planning only", "registry_generation_authorization_planning_only != true"),
    ("RV02", "request not sent", "registry_generation_authorization_request_sent_now != false"),
    ("RV03", "not authorized", "registry_generation_authorized_now != false"),
    ("RV04", "registry not generated", "boundary_object_registry_generated_now != false"),
    ("RV05", "object not registered", "boundary_object_registered_now != false"),
    ("RV06", "source not final approved", "registry_source_final_approved_now != false"),
    ("RV07", "contamination not final checked", "registry_contamination_final_checked_now != false"),
    ("RV08", "entry not generated", "registry_entry_generated_now != false"),
    ("RV09", "entry not committed", "registry_entry_committed_now != false"),
    ("RV10", "GC not enforced", "governance_constraint_module_enforced_now != false"),
    ("RV11", "file operation not executed", "file_operation_executed_now != false"),
    ("RV12", "mainline not resumed execution", "main_migration_chain_resumed_now != false"),
)

NON_CLAIMS_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("Registry request not sent", "Registry Generation Authorization Planning GO does not mean registry generation request is sent."),
    ("Registry not authorized", "Authorization Planning GO does not mean registry generation is authorized."),
    ("Source not final approved", "Source final approval planned does not mean source set is final approved."),
    ("Contamination not executed", "Contamination check planned does not mean contamination final check executed."),
    ("Entry not generated", "Entry generation boundary planned does not mean entry is generated."),
    ("Registry not generated", "Registry generation authorization planned does not mean boundary object registry is generated."),
    ("Registration not implied", "Registry generated in future does not mean boundary object registered."),
    ("GC source pack not enforced", "Governance Constraint Module source pack does not mean enforced module."),
    ("Return does not release migration", "Return to mainline does not release real migration / rollback / batch arming."),
    ("Verifier GO not success claim", "Verifier GO does not mean success claim."),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "registry_generation_authorization_planning_only": True,
        "registry_generation_authorization_request_sent_now": False,
        "registry_generation_authorized_now": False,
        "registry_source_final_approved_now": False,
        "registry_contamination_final_checked_now": False,
        "registry_generation_authority_released_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "governance_constraint_module_generated_now": False,
        "governance_constraint_module_enforced_now": False,
        "artifact_generation_planning_continued_now": False,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "authorization_granted_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_integration_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "governance_constraint_module_branch_closed": True,
        "governance_constraint_module_as_deferred_capability": True,
        "legacy_extraction_as_source_pack": True,
        "frozen_fields_enforced_now": False,
        "verifier_baseline_integrated_now": False,
        "file_operation_executed_now": False,
        "owner_approval_request_sent_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "batch_arming_allowed": False,
        "main_migration_chain_resumed_now": False,
        "main_migration_chain_paused": True,
        "main_migration_resume_phase": RETURN_REQUIRED_NEXT,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
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


def _eval_out_root() -> Path:
    return Path(__file__).resolve().parents[2] / "_eval_out"


def _load_return_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(
        root / "return_to_registry_generation_authorization_planning_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in RETURN_UPSTREAM_ARTIFACTS:
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


def _load_registry_chain_phase(eval_out_name: str) -> Dict[str, Any]:
    root = _eval_out_root() / eval_out_name
    return {
        "summary": _try_read_json(root / "summary.json") or {},
        "verifier": _try_read_json(root / "verifier_report.json") or {},
    }


def _load_registry_roadmap(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else _eval_out_root() / "boundary_object_registry_generation_roadmap_decision_v1_smoke_v0"
    return {
        "root": root,
        "summary": _try_read_json(root / "summary.json") or {},
        "verifier": _try_read_json(root / "verifier_report.json") or {},
        "readiness": _try_read_json(root / "registry_generation_roadmap_readiness_decision_v1.json") or {},
    }


def run_registry_generation_authorization_planning_v1(
    *,
    return_to_registry_generation_authorization_planning_root: str,
    boundary_object_registry_generation_roadmap_decision_root: Optional[str] = None,
) -> Dict[str, Any]:
    ret = _load_return_upstream(return_to_registry_generation_authorization_planning_root)
    reg_roadmap = _load_registry_roadmap(boundary_object_registry_generation_roadmap_decision_root)
    ret_summary = ret["summary"]
    ret_verifier = ret["verifier"]
    ret_readiness = ret["readiness"]
    reg_summary = reg_roadmap["summary"]
    reg_verifier = reg_roadmap["verifier"]
    reg_readiness = reg_roadmap["readiness"]

    blockers: List[str] = []
    if not ret["loaded"]:
        blockers.append(f"missing return upstream artifacts: {ret['missing']}")
    if ret_verifier.get("verifier") != "GO" or ret_verifier.get("passed") is not True:
        blockers.append("return wrapper verifier is not GO")
    if ret_summary.get("boundary_ok") is not True:
        blockers.append("return wrapper boundary_ok is not true")
    if ret_summary.get("final_decision") != RETURN_REQUIRED_FINAL:
        blockers.append(f"return final_decision must be {RETURN_REQUIRED_FINAL}")
    if ret_summary.get("recommended_next_phase") != RETURN_REQUIRED_NEXT:
        blockers.append(f"return recommended_next_phase must be {RETURN_REQUIRED_NEXT}")
    if ret_summary.get("return_to_mainline_wrapper_only") is not True:
        blockers.append("return_to_mainline_wrapper_only must be true")
    if ret_readiness.get("return_to_mainline_completed") is not True:
        blockers.append("return wrapper not completed")

    for flag, expected in (
        ("registry_generation_authorization_planning_executed_now", False),
        ("governance_constraint_module_branch_closed", True),
        ("governance_constraint_module_as_deferred_capability", True),
        ("legacy_extraction_as_source_pack", True),
        ("artifact_generation_planning_continued_now", False),
    ):
        if ret_summary.get(flag) is not expected:
            blockers.append(f"return {flag} must be {expected}")

    reentry = ret["artifacts"].get("registry_generation_authorization_planning_reentry_scope_v1.json", {})
    if reentry.get("artifact_generation_planning_recursion_blocked") is not True:
        blockers.append("return reentry must block artifact planning recursion")

    if reg_verifier.get("verifier") != "GO" or reg_verifier.get("passed") is not True:
        blockers.append("registry generation roadmap verifier is not GO")
    if reg_summary.get("boundary_ok") is not True:
        blockers.append("registry generation roadmap boundary_ok is not true")
    if reg_summary.get("final_decision") != REGISTRY_ROADMAP_FINAL:
        blockers.append(f"registry roadmap final_decision must be {REGISTRY_ROADMAP_FINAL}")
    if reg_summary.get("selected_route") != REGISTRY_ROADMAP_SELECTED_ROUTE:
        blockers.append(f"registry roadmap selected_route must be {REGISTRY_ROADMAP_SELECTED_ROUTE}")
    if reg_readiness.get("ready_for_registry_generation_authorization_planning") is not True:
        blockers.append("registry roadmap not ready_for_authorization_planning")

    chain_rows: List[Dict[str, Any]] = []
    chain_pass = True
    for phase_name, eval_out in REGISTRY_GENERATION_CHAIN:
        data = _load_registry_chain_phase(eval_out)
        sm = data["summary"]
        vr = data["verifier"]
        go = vr.get("verifier") == "GO" and vr.get("passed") is True
        boundary = sm.get("boundary_ok") is True
        review_pass = go and boundary
        if not review_pass:
            chain_pass = False
        chain_rows.append(
            _planning_row(
                phase_name=phase_name,
                eval_out_dir=eval_out,
                verifier_status=vr.get("verifier", "UNKNOWN"),
                boundary_ok=boundary,
                registry_generated_observed=sm.get("boundary_object_registry_generated_now") is True,
                object_registered_observed=sm.get("boundary_object_registered_now") is True,
                entry_generated_observed=sm.get("registry_entry_generated_now") is True,
                entry_committed_observed=sm.get("registry_entry_committed_now") is True,
                source_final_validated_observed=sm.get("registry_source_final_validated_now") is True
                or sm.get("registry_generation_source_validated_now") is True,
                contamination_final_observed=sm.get("registry_contamination_check_final_executed_now") is True
                or sm.get("registry_generation_contamination_checked_now") is True,
                file_operation_observed=sm.get("file_operation_executed_now") is True,
                owner_approval_observed=sm.get("owner_approval_granted_now") is True,
                review_pass=review_pass,
            )
        )

    if not chain_pass:
        blockers.append("registry generation chain phases must all be GO with boundary_ok")

    if reg_summary.get("boundary_object_registry_generated_now") is not False:
        blockers.append("registry must not be generated")
    if reg_summary.get("boundary_object_registered_now") is not False:
        blockers.append("objects must not be registered")
    if reg_summary.get("registry_entry_generated_now") is not False:
        blockers.append("registry entry must not be generated")
    if reg_summary.get("registry_entry_committed_now") is not False:
        blockers.append("registry entry must not be committed")
    if reg_summary.get("file_operation_executed_now") is not False:
        blockers.append("file operation must not be executed")
    if reg_summary.get("owner_approval_granted_now") is not False:
        blockers.append("owner approval must not be granted")

    input_review_rows = [
        _planning_row(
            check_id=cid,
            check_name=name,
            expected=expected,
            observed=observed,
            review_pass=observed == expected,
        )
        for cid, name, expected, observed in (
            ("MR01", "return_verifier_go", True, ret_verifier.get("verifier") == "GO" and ret_verifier.get("passed") is True),
            ("MR02", "return_final_decision", RETURN_REQUIRED_FINAL, ret_summary.get("final_decision")),
            ("MR03", "return_main_target", RETURN_REQUIRED_NEXT, ret_summary.get("mainline_resume_target")),
            ("MR04", "return_branch_closed", True, ret_summary.get("governance_constraint_module_branch_closed")),
            ("MR05", "return_gc_deferred", True, ret_summary.get("governance_constraint_module_as_deferred_capability")),
            ("MR06", "return_artifact_not_continued", False, ret_summary.get("artifact_generation_planning_continued_now")),
            ("MR07", "registry_roadmap_go", True, reg_verifier.get("verifier") == "GO"),
            ("MR08", "registry_roadmap_route", REGISTRY_ROADMAP_SELECTED_ROUTE, reg_summary.get("selected_route")),
            ("MR09", "registry_chain_pass", True, chain_pass),
            ("MR10", "registry_not_generated", False, reg_summary.get("boundary_object_registry_generated_now")),
        )
    ]
    input_review_pass = all(r.get("review_pass") for r in input_review_rows) and not blockers

    request_rows = [
        _planning_row(schema_field=f, why_required=w, request_sent_now=False)
        for f, w in REQUEST_SCHEMA_FIELDS
    ]
    grant_rows = [
        _planning_row(schema_field=f, why_required=w, grant_issued_now=False, registry_generation_authorized_now=False)
        for f, w in GRANT_SCHEMA_FIELDS
    ]
    source_rows = [
        _planning_row(component=c, planning_role=r, final_approved_now=False, gc_reference_only=("branch closure" in r or "return-to-mainline" in r))
        for c, r in SOURCE_APPROVAL_COMPONENTS
    ]
    contamination_rows = [
        _planning_row(risk_id=f"CR{i+1:02d}", risk_name=n, mitigation_required=True, final_checked_now=False)
        for i, (n, _) in enumerate(CONTAMINATION_RISKS)
    ]
    authority_rows = [
        _planning_row(authority_name=n, artifact_scope=a, requires_grant=True, authorized_now=False, generated_now=False)
        for n, a in REGISTRY_GENERATION_AUTHORITIES
    ]
    entry_rows = [
        _planning_row(boundary_rule=n, boundary_statement=s, entry_generated_now=False, entry_committed_now=False)
        for n, s in ENTRY_GENERATION_BOUNDARIES
    ]
    owner_rows = [
        _planning_row(dependency=n, requirement=s, satisfied_now=False)
        for n, s in OWNER_OPERATOR_DEPENDENCIES
    ]
    file_block_rows = [
        _planning_row(block_rule=n, block_statement=s, file_operation_executed_now=False)
        for n, s in FILE_OPERATION_BLOCKS
    ]
    verifier_rows = [
        _planning_row(verifier_check_id=cid, check_name=cn, failure_condition=fc, planned_now=True)
        for cid, cn, fc in VERIFIER_USAGE_CHECKS
    ]
    non_claims_rows = [
        _planning_row(scenario=s, required_non_claim=nc, planned_now=True, generated_now=False)
        for s, nc in NON_CLAIMS_SCENARIOS
    ]

    all_rows = (
        request_rows,
        grant_rows,
        source_rows,
        contamination_rows,
        authority_rows,
        entry_rows,
        owner_rows,
        file_block_rows,
        verifier_rows,
        non_claims_rows,
    )
    if any(not all(r.get("not_generated_now") for r in rows) for rows in all_rows):
        blockers.append("all planned outputs must have not_generated_now=true")

    counts_ok = (
        len(request_rows) >= 15
        and len(grant_rows) >= 12
        and len(source_rows) >= 12
        and len(contamination_rows) >= 12
        and len(authority_rows) >= 12
        and len(entry_rows) >= 12
        and len(owner_rows) >= 10
        and len(file_block_rows) >= 10
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 10
    )
    if not counts_ok:
        blockers.append("registry authorization planning coverage requirements not met")

    planning_ready = input_review_pass and counts_ok and not blockers
    boundary_ok = planning_ready

    registry_generation_authorization_planning_policy = _planning_row(
        phase_name=PHASE_ID,
        return_source_phase=RETURN_SOURCE_PHASE,
        registry_roadmap_source_phase=REGISTRY_ROADMAP_PHASE,
        registry_roadmap_selected_route=reg_summary.get("selected_route"),
        governance_constraints_ref=CONSTRAINT_DOC_ID,
        governance_constraint_module_reference_only=True,
    )

    mainline_return_input_review = {
        "rows": input_review_rows,
        "registry_generation_chain_rows": chain_rows,
        "row_count": len(input_review_rows),
        "chain_row_count": len(chain_rows),
        "all_pass": input_review_pass,
        "registry_generation_chain_all_pass": chain_pass,
        **_planning_meta(),
    }

    def _artifact(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "rows": rows,
            "row_count": len(rows),
            "all_not_generated_now": all(r.get("not_generated_now") for r in rows),
            **_planning_meta(),
        }

    registry_generation_authorization_planning_readiness_decision = {
        "ready_for_registry_generation_authorization_dryrun": boundary_ok,
        "ready_for_registry_generation_authorization_request": False,
        "ready_for_registry_generation_authorization_grant": False,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_registry_entry_generation": False,
        "ready_for_registry_entry_commit": False,
        "ready_for_file_operation": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_to_resume_main_migration_chain": False,
        "authorization_planning_completed": boundary_ok,
        "request_schema_planned": len(request_rows) >= 15,
        "grant_schema_planned": len(grant_rows) >= 12,
        "source_final_approval_authority_planned": len(source_rows) >= 12,
        "contamination_final_check_authority_planned": len(contamination_rows) >= 12,
        "registry_generation_authority_planned": len(authority_rows) >= 12,
        "entry_generation_boundary_planned": len(entry_rows) >= 12,
        "owner_operator_dependency_planned": len(owner_rows) >= 10,
        "file_operation_block_planned": len(file_block_rows) >= 10,
        "verifier_usage_planned": len(verifier_rows) >= 12,
        "non_claims_planned": len(non_claims_rows) >= 10,
        "governance_constraint_module_enforced_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "REGISTRY_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "return_to_registry_input_loaded": ret["loaded"],
        "registry_generation_roadmap_input_loaded": reg_summary.get("phase") == REGISTRY_ROADMAP_PHASE,
        "source_selected_route_observed": reg_summary.get("selected_route"),
        "request_schema_field_count": len(request_rows),
        "grant_schema_field_count": len(grant_rows),
        "source_approval_component_count": len(source_rows),
        "contamination_risk_count": len(contamination_rows),
        "registry_generation_authority_count": len(authority_rows),
        "entry_boundary_count": len(entry_rows),
        "owner_operator_dependency_count": len(owner_rows),
        "file_operation_block_count": len(file_block_rows),
        "verifier_usage_check_count": len(verifier_rows),
        "non_claims_scenario_count": len(non_claims_rows),
        "all_authorization_planning_complete": counts_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "REGISTRY_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "registry_generation_authorization_planning_policy": registry_generation_authorization_planning_policy,
        "mainline_return_input_review": mainline_return_input_review,
        "registry_generation_authorization_request_schema_planning": _artifact(request_rows),
        "registry_generation_authorization_grant_schema_planning": _artifact(grant_rows),
        "registry_source_final_approval_authority_planning": _artifact(source_rows),
        "registry_contamination_final_check_authority_planning": _artifact(contamination_rows),
        "registry_generation_authority_planning_matrix": _artifact(authority_rows),
        "registry_entry_generation_boundary_planning": _artifact(entry_rows),
        "registry_owner_operator_dependency_planning": _artifact(owner_rows),
        "registry_file_operation_block_planning": _artifact(file_block_rows),
        "registry_generation_authorization_verifier_usage_planning": _artifact(verifier_rows),
        "registry_generation_authorization_non_claims_planning": _artifact(non_claims_rows),
        "registry_generation_authorization_planning_readiness_decision": registry_generation_authorization_planning_readiness_decision,
    }
