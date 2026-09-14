# -*- coding: utf-8 -*-
"""Permission Semantics Canonicalization Planning v1.

Planning only: define canonical permission/state semantics and development norms blueprint.
Does not execute canonicalization, modify verifiers/templates, or release authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    CANONICAL_NON_CLAIM_SNIPPET,
)

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"
PLANNING_SCOPE = "permission_semantics_canonicalization_planning_only"
PLANNING_ID = "permission_semantics_canonicalization_planning_v1_001"
SOURCE_CHAIN = "permission_semantics_canonicalization_planning_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING"
)
SELECTED_ROUTE = "Route A — Permission Semantics Canonicalization Planning"
BOUND_B = "Route B — Terminology Canonical Table Planning"
BOUND_C = "Route C — Success Claim Gate Canonicalization Planning"

FINAL_DECISION = "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001"


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "canonicalization_planning_only": True,
        "canonicalization_executed_now": False,
        "debt_fix_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "not_enforced_now": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str], artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and not missing
    return {"root": root, "loaded": loaded, "summary": summary or {}, "artifacts": art, "missing": missing}


def _sem_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta()}


def _build_phase_type_table() -> List[Dict[str, Any]]:
    specs = [
        ("planning", "structured design without side effects", "design matrices/policies", "execute/commit/write", "planning_only=true", "does not imply execution"),
        ("dry-run", "simulated evaluation without real actions", "simulate chains", "runtime/subprocess/file ops", "dryrun_only=true", "does not imply real action"),
        ("review", "read-only audit of upstream artifacts", "read/compare matrices", "authorize/write/fix", "review_only=true", "does not imply authorization"),
        ("post-review", "read-only audit after prior phase", "validate completeness", "fix/automation", "post_register_review_only=true", "does not imply debt fixed"),
        ("roadmap decision", "select next governance route only", "route matrices/decisions", "release permissions", "roadmap_decision_only=true", "does not imply permission release"),
        ("register", "structured registration without remediation", "debt/register matrices", "fix debt", "register_only=true", "does not imply fix"),
        ("post-register review", "audit register reliability", "review registers", "fix/register as complete", "post_register_review_only=true", "register GO ≠ fixed"),
        ("authorization planning", "plan authorization chain", "plan matrices", "grant authorization", "authorization_granted_now=false", "planned ≠ granted"),
        ("authorization dry-run", "simulate authorization chain", "simulated auth steps", "real approval", "authorization_granted_now=false", "simulated ≠ granted"),
        ("authorization review", "audit authorization planning/dry-run", "review auth artifacts", "open execution window", "review_only=true", "review ≠ granted"),
        ("execution planning", "plan execution prerequisites", "execution plans", "commit execution", "execution_committed=false", "planning ≠ committed"),
        ("execution dry-run", "simulate execution without commit", "simulated execution", "runtime/subprocess", "execution_committed=false", "dry-run ≠ executed"),
        ("execution review", "audit execution planning/dry-run", "review execution artifacts", "declare success", "review_only=true", "review ≠ success"),
        ("real execution", "authorized real side effects", "commit with evidence", "skip authorization chain", "authorization_granted_now=true required", "requires independent authorization chain"),
    ]
    rows = []
    for pt, meaning, allowed, forbidden, flags, not_impl in specs:
        rows.append(
            _sem_row(
                phase_type=pt,
                canonical_meaning=meaning,
                allowed_actions=allowed,
                forbidden_actions=forbidden,
                required_flags=flags,
                must_not_imply=not_impl,
                required_non_claims=f"{pt} GO does not mean execution or authorization granted",
                verifier_required_checks=["phase_type_flag_check", "forbidden_state_combination_check"],
            )
        )
    return rows


def _build_permission_state_table() -> List[Dict[str, Any]]:
    specs = [
        ("allowed", "permitted within declared scope", "planning/dry-run/register", "used as granted", "*_allowed fields", "allowed ≠ committed"),
        ("not_allowed", "explicitly forbidden in scope", "blocked routes", "ignored", "allowed_now=false", "not_allowed ≠ blocked with reason"),
        ("blocked", "hard stop with documented reason", "route/debt blockers", "soft deferral", "blocked_now=true", "blocked ≠ deferred"),
        ("deferred", "postponed; not selected now", "roadmap routes", "forbidden forever", "deferred=true", "deferred ≠ allowed"),
        ("released", "permission explicitly released in scope", "authorized execution", "without release source", "permission_release=true", "released requires source"),
        ("not_released", "permission explicitly not released", "all non-exec phases", "inferred from GO", "*_release=false", "default for governance phases"),
        ("permitted", "synonym guard for allowed in context", "scope docs", "global permission", "context-bound fields", "permitted ≠ granted"),
        ("denied", "explicit denial recorded", "authorization chain", "silent false", "authorization_denied=true", "denied ≠ not_requested"),
        ("gated", "conditional on gate pass", "success claim/evidence", "automatic pass", "gate_pass required", "gated ≠ passed"),
        ("frozen", "must remain false/until gate", "non-execution phases", "thaw on GO", "mandatory freeze fields", "frozen ≠ optional"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, valid_contexts=vc, invalid_contexts=ic, required_boolean_fields=f, must_not_imply=ni, required_verifier_check="permission_state_semantics_check")
        for t, m, vc, ic, f, ni in specs
    ]


def _build_authorization_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("authorization_planned", "auth chain designed", "plan artifacts", "owner", "none", "authorization_requested", "planned ≠ requested"),
        ("authorization_requested", "formal request issued", "request record", "operator", "authorization_planned", "authorization_granted/denied", "requested ≠ granted"),
        ("authorization_granted", "explicit grant recorded now", "grant record", "owner", "authorization_requested", "execution_window", "granted ≠ committed"),
        ("authorization_denied", "explicit denial", "denial record", "owner", "authorization_requested", "retry", "denied ≠ pending"),
        ("owner_approval_required", "owner must approve", "policy matrix", "owner", "planning", "owner_approval_granted", "required ≠ granted"),
        ("owner_approval_granted", "owner explicit approval", "approval evidence", "owner", "owner_approval_required", "operator_ack", "owner ≠ operator"),
        ("operator_acknowledgement_required", "operator must ack", "ack matrix", "operator", "owner_approval_granted", "operator_acknowledgement_granted", "ack required ≠ granted"),
        ("operator_acknowledgement_granted", "operator ack recorded", "ack evidence", "operator", "operator_acknowledgement_required", "execution_window", "ack ≠ execution"),
        ("execution_window_required", "window must be opened", "window policy", "owner/operator", "authorization_granted", "execution_window_opened", "required ≠ opened"),
        ("execution_window_opened", "time-bounded window open", "window record", "operator", "execution_window_required", "execution_committed", "opened ≠ committed"),
        ("abort_authority_required", "abort path must exist", "abort policy", "owner/operator", "execution_window_opened", "abort_authority_confirmed", "required ≠ confirmed"),
        ("abort_authority_confirmed", "abort authority acknowledged", "abort ack", "owner/operator", "abort_authority_required", "execution_aborted", "confirmed ≠ aborted"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, required_evidence=e, required_actor=a, valid_transition_from=vf, valid_transition_to=vt, forbidden_shortcuts="skip owner/operator", must_not_imply=ni, required_verifier_check="authorization_state_check")
        for t, m, e, a, vf, vt, ni in terms
    ]


def _build_execution_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("execution_planned", "execution steps designed", "auth + boundary gates", "plan doc", "authorization", "planned ≠ allowed"),
        ("execution_allowed", "scope permits execution attempt", "window open + auth", "allow record", "authorization_granted", "allowed ≠ committed"),
        ("execution_committed", "real side effect committed", "evidence + audit", "commit record", "execution_allowed", "committed requires evidence"),
        ("execution_started", "execution begun", "start timestamp", "start event", "execution_allowed", "started ≠ completed"),
        ("execution_completed", "execution finished successfully", "completion evidence", "complete record", "execution_started", "completed ≠ succeeded claim"),
        ("execution_aborted", "execution stopped by authority", "abort record", "abort event", "execution_started", "aborted ≠ failed"),
        ("execution_failed", "execution failed", "failure evidence", "fail record", "execution_started", "failed ≠ rollback success"),
        ("execution_rolled_back", "rollback applied", "rollback evidence", "rollback record", "execution_committed", "rollback success without gate"),
        ("runtime_invoked", "runtime engine invoked", "runtime log", "runtime flag", "execution_allowed", "runtime requires auth"),
        ("subprocess_invoked", "subprocess executed", "subprocess log", "subprocess flag", "execution_allowed", "subprocess tracked separately"),
        ("file_operation_executed", "file move/delete/rename/merge", "file op audit", "file op flag", "boundary authorization", "file ops require boundary gate"),
        ("write_committed", "persistent write committed", "write audit", "write flag", "write authorization", "write not implied by summary text"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, required_preconditions=rp, required_evidence=re, invalid_without=iw, must_not_imply=ni, required_verifier_check="execution_state_check")
        for t, m, rp, re, iw, ni in terms
    ]


def _build_artifact_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("planned_artifact", "named future output in plan", "planning phases", "executable without gen", False, False, "plan entry", "artifact_planned_check"),
        ("candidate_artifact", "placeholder/simulated artifact", "dry-run", "runtime evidence", False, False, "candidate marker", "candidate_not_executable"),
        ("generated_artifact", "artifact physically written in scope", "authorized phases", "from candidate only", True, False, "generation auth", "artifact_generated_check"),
        ("executable_artifact", "artifact that may trigger execution", "authorized execution", "from candidate", True, False, "exec authorization", "executable_artifact_check"),
        ("runtime_evidence", "evidence from runtime execution", "real execution", "dry-run matrix", True, True, "runtime exec + evidence auth", "runtime_evidence_check"),
        ("audit_evidence", "audit trail evidence", "review/execution", "verifier report alone", True, False, "audit chain", "audit_evidence_check"),
        ("success_claim_evidence", "evidence supporting success claim", "success gate", "summary/GO", True, True, "success gate + runtime evidence", "success_evidence_check"),
        ("verifier_report", "verifier check results", "all phases", "runtime evidence", False, False, "verifier run", "verifier_report_not_runtime_evidence"),
        ("summary", "phase summary JSON", "all phases", "success evidence", False, False, "phase completion", "summary_not_success_evidence"),
        ("readiness_decision", "readiness for next phase type", "all phases", "authorization granted", False, False, "readiness fields", "readiness_implication_check"),
        ("non_claims_register", "explicit non-claims list", "governance phases", "optional", False, False, "non-claims rules", "non_claims_presence_check"),
        ("boundary_matrix", "boundary freeze/object matrix", "migration/governance", "authorization substitute", False, False, "boundary review", "boundary_object_check"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, allowed_usage=au, forbidden_usage=fu, can_support_execution=cse, can_support_success_claim=csc, required_evidence=re, required_verifier_check=rv)
        for t, m, au, fu, cse, csc, re, rv in terms
    ]


def _build_readiness_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("ready_for_planning", "preconditions for planning phase", "upstream GO", "planning", "does not imply dry-run executed"),
        ("ready_for_dryrun", "preconditions for dry-run", "planning GO", "dry-run", "does not imply real action"),
        ("ready_for_review", "preconditions for review", "dry-run GO", "review", "does not imply authorization"),
        ("ready_for_post_review", "preconditions for post-review", "primary review GO", "post-review", "does not imply fix"),
        ("ready_for_roadmap_decision", "preconditions for roadmap", "review/post-review GO", "roadmap", "does not imply ready_for_execution"),
        ("ready_for_register", "preconditions for register", "roadmap Route D etc.", "register", "does not imply fix"),
        ("ready_for_post_register_review", "preconditions for post-register review", "register GO", "post-register review", "register GO ≠ fixed"),
        ("ready_for_authorization_planning", "preconditions for auth planning", "semantics/canonical planning", "authorization planning", "does not imply granted"),
        ("ready_for_authorization_request", "preconditions to request auth", "auth planning GO", "auth request", "does not imply authorization_granted"),
        ("ready_for_execution_planning", "preconditions for execution planning", "authorization path clear", "execution planning", "does not imply execution allowed"),
        ("ready_for_real_execution", "high bar for real execution", "full auth chain + window", "real execution", "separate high-threshold gate"),
        ("not_ready", "explicit not ready", "blockers present", "none until fixed", "must list violations"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, required_preconditions=rp, allowed_next_phase_types=an, must_not_imply=ni, required_non_claims=f"{t} does not imply authorization or execution", required_verifier_check="readiness_implication_check")
        for t, m, rp, an, ni in terms
    ]


def _build_result_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("GO", "phase-scoped verifier checks passed", "phase boundary only", "execution/success/auth", "verifier_report", "go_not_success_claim"),
        ("NO_GO", "phase checks failed", "phase boundary", "silent pass", "verifier_report", "no_go_blocks_advancement"),
        ("pass", "individual check passed", "check item", "phase GO", "check record", "pass ≠ GO alone"),
        ("fail", "individual check failed", "check item", "ignored", "check record", "fail → NO_GO"),
        ("completed", "phase workflow completed", "phase scope", "succeeded", "summary", "completed ≠ succeeded"),
        ("reviewed", "review performed", "review scope", "accepted", "review matrix", "reviewed ≠ accepted"),
        ("accepted", "review acceptance recorded", "review gate", "authorization", "acceptance record", "accepted ≠ granted"),
        ("rejected", "review rejection", "review gate", "ignored", "rejection record", "rejected blocks"),
        ("succeeded", "real-world success", "execution scope", "phase GO", "success evidence", "succeeded requires gate"),
        ("success_claim_allowed", "success claim gate open", "success gate only", "from GO", "success gate matrix", "independent gate"),
        ("success_claim_blocked", "success claim forbidden", "default governance", "from GO", "success gate", "default true until gate"),
        ("boundary_ok", "phase boundary checks ok", "phase scope", "execution safe", "boundary matrix", "boundary_ok ≠ execution safe"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, scope_limit=sl, must_not_imply=ni, required_supporting_artifacts=rsa, required_verifier_check=rv)
        for t, m, sl, ni, rsa, rv in terms
    ]


def _build_route_state_table() -> List[Dict[str, Any]]:
    terms = [
        ("selected_route", "chosen next governance route", "roadmap decision", "permission release", "permission_release must be false"),
        ("blocked_route", "route forbidden now", "roadmap matrix", "skippable by final decision", "blocked_now=true"),
        ("deferred_route", "route postponed", "roadmap matrix", "forbidden forever", "deferred=true"),
        ("dependency_route", "required companion route", "Route B/C binding", "dependency satisfied", "required_dependencies listed"),
        ("excluded_route", "explicitly excluded", "selected decision", "executable", "excluded_routes list"),
        ("allowed_route", "route allowed for scoped action", "planning/dry-run/register", "execution without scope", "allowed_now with permission_impact"),
        ("recommended_next_phase", "suggested next phase id", "readiness/summary", "authorization", "recommended_next_phase naming"),
        ("route_priority", "P0/P1/blocked priority", "route matrix", "auto execution", "priority field"),
        ("route_blocker", "reason route blocked", "dependency matrix", "ignored", "blocker fields"),
        ("route_dependency", "dependency between routes", "roadmap", "automatic satisfaction", "required_dependencies"),
    ]
    return [
        _sem_row(term=t, canonical_meaning=m, valid_usage=vu, must_not_imply=ni, permission_impact_rules=pir, required_verifier_check="route_permission_impact_check")
        for t, m, vu, ni, pir in terms
    ]


def _build_forbidden_combinations() -> List[Dict[str, Any]]:
    specs = [
        ("FC01", "planning_only=true", "execution_committed=true", "planning must not commit"),
        ("FC02", "dryrun_only=true", "runtime_invoked=true", "dry-run must not invoke runtime"),
        ("FC03", "review_only=true", "write_allowed=true", "review must not write"),
        ("FC04", "roadmap_decision_only=true", "authorization_granted_now=true", "roadmap must not grant auth"),
        ("FC05", "register_only=true", "fix_executed_now=true", "register must not fix"),
        ("FC06", "canonicalization_planning_only=true", "canonicalization_executed_now=true", "planning must not execute canonicalization"),
        ("FC07", "authorization_granted_now=false", "real_rehearsal_execution_allowed=true", "rehearsal requires auth"),
        ("FC08", "owner_approval_granted_now=false", "execution_window_opened_now=true", "window requires owner approval"),
        ("FC09", "success_claim_allowed=true", "real_execution_observed=false", "success requires execution"),
        ("FC10", "success_claim_allowed=true", "evidence_generated_now=false", "success requires evidence"),
        ("FC11", "selected_route set", "execution_allowed=true without permission_release", "route ≠ execution release"),
        ("FC12", "verifier=GO", "success_claim_allowed=true in non-success phase", "GO ≠ success claim"),
        ("FC13", "ready_for_roadmap_decision=true", "ready_for_execution=true", "roadmap ready ≠ execution ready"),
        ("FC14", "candidate_artifact=true", "executable_artifact=true", "candidate ≠ executable"),
        ("FC15", "verifier_report_generated=true", "runtime_evidence_generated=true", "verifier report ≠ runtime evidence"),
        ("FC16", "summary_generated=true", "success_evidence_generated=true", "summary ≠ success evidence"),
        ("FC17", "documentation_auto_sync_executed_now=false", "documentation_synced=true", "no silent doc sync"),
        ("FC18", "automation_implemented_now=false", "automation_active=true", "automation candidate ≠ active"),
        ("FC19", "debt_fix_executed_now=false", "debt_status=fixed", "register/planning ≠ fixed"),
        ("FC20", "boundary_ok=true", "real_execution_allowed=true without auth", "boundary ok ≠ execution allowed"),
    ]
    return [
        _sem_row(
            forbidden_combination_id=fid,
            state_a=a,
            state_b=b,
            forbidden_reason=reason,
            failure_condition="both conditions true",
            expected_error_level="NO_GO",
            required_verifier_check="forbidden_state_combination_check",
        )
        for fid, a, b, reason in specs
    ]


def _build_development_norms() -> List[Dict[str, Any]]:
    norms = [
        ("N01", "phase type declaration norm", "every phase declares exactly one primary phase type flag", "all governance phases", "planning_only|dryrun_only|review_only|...", "missing phase type flag", "planning_only=true in summary", "execution_committed=true in planning", "phase_type_flag_check"),
        ("N02", "permission field naming norm", "use *_allowed for scope permission; *_granted_now for explicit grant", "all non-execution", "real_*_allowed, authorization_granted_now", "allowed used for granted", "real_rehearsal_execution_allowed=false", "authorization_granted_now=true without chain", "permission_non_release_check"),
        ("N03", "authorization field naming norm", "separate owner/operator/window fields", "authorization chain", "owner_approval_granted_now, operator_acknowledgement_granted_now, execution_window_opened_now", "single auth boolean", "three separate false fields", "owner_approval_granted_now=true alone", "authorization_state_check"),
        ("N04", "execution field naming norm", "execution_allowed vs execution_committed vs runtime_invoked", "execution-adjacent", "execution_committed, runtime_invoked, subprocess_invoked", "allowed implies committed", "execution_committed=false", "execution_allowed=true with committed=true without auth", "execution_non_commit_check"),
        ("N05", "artifact state field naming norm", "candidate vs generated vs executable suffixes", "dry-run/review/execution", "evidence_candidate_only, evidence_generated_now", "candidate without _only", "evidence_candidate_only=true", "candidate marked generated", "artifact_candidate_check"),
        ("N06", "readiness decision norm", "ready_for_* must name target phase type", "all with readiness", "ready_for_* disambiguated", "ready_for_execution without auth", "ready_for_dryrun=true", "ready_for_execution=true in planning", "readiness_implication_check"),
        ("N07", "final decision naming norm", "final_decision encodes phase outcome not execution", "all phases", "final_decision, recommended_next_phase", "SUCCESS in final_decision", "PLANNING_READY_FOR_DRYRUN", "EXECUTION_SUCCEEDED", "final_decision_implication_check"),
        ("N08", "non-claims generation norm", "every phase lists what GO does not mean", "all governance", "non_claims register", "missing non-claims", "9+ non-claims listed", "GO only summary", "non_claims_presence_check"),
        ("N09", "forbidden state combination norm", "verifier rejects illegal flag pairs", "all phases", "forbidden_state_combination_matrix", "conflicting flags true", "matrix referenced", "planning_only + execution_committed", "forbidden_combination_check"),
        ("N10", "verifier mandatory check norm", "verify_* includes governance_constraints_ref", "all verify scripts", "governance_constraints_ref", "missing ref", "ref in verifier_report", "no ref", "governance_constraints_ref_check"),
        ("N11", "documentation sync reference norm", "doc sync declared not executed in planning", "phases with handoff", "documentation_auto_sync_executed_now=false", "silent sync", "false in summary", "documentation_synced=true without flag", "documentation_sync_status_check"),
        ("N12", "governance constraints ref norm", "link to migration_governance_development_constraints_v1", "all migration governance", "governance_constraints_ref", "missing ref", CONSTRAINT_DOC_ID, "ad-hoc rules only", "governance_constraints_ref_check"),
    ]
    return [
        _sem_row(norm_id=nid, norm_name=nn, canonical_rule=cr, target_phase_types=tpt, required_fields=rf, forbidden_patterns=fp, example_good=eg, example_bad=eb, required_verifier_check=rvc, effective_stage="planning_defined_not_enforced")
        for nid, nn, cr, tpt, rf, fp, eg, eb, rvc in norms
    ]


def _build_verifier_checklist() -> List[Dict[str, Any]]:
    checks = [
        ("VS01", "phase type flag check", "all", "phase type flags", "flag missing or mismatch", "NO_GO"),
        ("VS02", "permission non-release check", "non-execution", "authorization_granted_now=false", "granted true", "NO_GO"),
        ("VS03", "authorization non-release check", "non-auth phases", "owner/operator/window false", "any granted without chain", "NO_GO"),
        ("VS04", "execution non-commit check", "non-execution", "execution_committed=false", "committed true", "NO_GO"),
        ("VS05", "runtime/subprocess/file operation check", "non-execution", "runtime/subprocess/file false", "any true", "NO_GO"),
        ("VS06", "artifact candidate vs executable check", "dry-run/planning", "candidate not executable", "candidate=executable", "NO_GO"),
        ("VS07", "evidence usability check", "review/execution", "evidence layer correct", "candidate for success", "NO_GO"),
        ("VS08", "success claim gate check", "all high-risk", "success_claim_blocked default", "success_claim_allowed without gate", "NO_GO"),
        ("VS09", "route permission impact check", "roadmap", "permission_release=false", "release true", "NO_GO"),
        ("VS10", "readiness implication check", "all", "ready_for_* disambiguated", "roadmap ready implies execution", "NO_GO"),
        ("VS11", "final decision implication check", "all", "final_decision scope", "execution in final_decision", "NO_GO"),
        ("VS12", "forbidden state combination check", "all", "forbidden matrix", "illegal pair true", "NO_GO"),
        ("VS13", "non-claims presence check", "governance", "non_claims present", "missing", "NO_GO"),
        ("VS14", "boundary object check", "migration", "boundary matrix when required", "missing matrix", "NO_GO"),
        ("VS15", "documentation sync status check", "all with handoff", "auto_sync false unless declared", "silent sync", "NO_GO/WARN"),
        ("VS16", "governance constraints ref check", "all migration governance", "governance_constraints_ref set", "missing", "NO_GO"),
        ("VS17", "owner/operator state check", "authorization", "separate fields", "conflated", "NO_GO"),
        ("VS18", "execution window state check", "authorization/execution", "window opened only with approval", "window without owner", "NO_GO"),
        ("VS19", "automation state check", "all", "automation_implemented_now=false default", "automation_active true", "NO_GO"),
        ("VS20", "debt fix state check", "register/planning", "fix_executed_now=false", "debt_status=fixed", "NO_GO"),
    ]
    return [
        _sem_row(check_id=cid, check_name=cn, target_phase_types=tpt, required_fields=rf, failure_condition=fc, expected_behavior=eb, severity="P0", not_enforced_now=True)
        for cid, cn, tpt, rf, fc, eb in checks
    ]


def _build_non_claims_rules() -> List[Dict[str, Any]]:
    scenarios = [
        ("planning GO", "Planning GO does not mean execution is authorized or committed."),
        ("dry-run GO", "Dry-run GO does not mean real actions occurred or succeeded."),
        ("review GO", "Review GO does not mean authorization was granted."),
        ("roadmap decision GO", "Roadmap GO does not mean permissions were released."),
        ("register GO", "Register GO does not mean governance debt was fixed."),
        ("post-register review GO", "Post-register review GO does not mean debt was remediated."),
        ("canonicalization planning GO", "Canonicalization planning GO does not mean semantics are enforced or canonicalized."),
        ("authorization planning GO", "Authorization planning GO does not mean owner/operator approval was granted."),
        ("authorization dry-run GO", "Authorization dry-run GO does not mean real approval occurred."),
        ("execution planning GO", "Execution planning GO does not mean execution is allowed or committed."),
        ("verifier GO", CANONICAL_NON_CLAIM_SNIPPET),
        ("boundary_ok", "boundary_ok does not mean real execution is safe or authorized."),
        ("selected route", "Selected route does not mean permission release or execution allowed."),
        ("ready_for_next_phase", "ready_for_* names next phase type only; not execution readiness unless explicitly stated."),
        ("candidate artifact generated", "Candidate artifact does not mean executable or runtime evidence."),
        ("evidence candidate generated", "Evidence candidate does not support success claim."),
        ("success claim blocked", "success_claim_blocked=true remains default until explicit success gate passes."),
        ("automation candidate registered", "Automation candidate registration does not mean automation is implemented."),
        ("documentation sync plan generated", "Documentation sync plan does not mean auto-sync executed."),
        ("future phase mapped", "Future phase mapping does not mean that phase may execute immediately."),
    ]
    return [
        _sem_row(scenario=s, required_non_claim=nc, risk_if_missing="phase GO misread as authorization/execution/success", must_be_in_summary=True, must_be_in_verifier_report=True, used_by_future_phase_template=True)
        for s, nc in scenarios
    ]


def run_permission_semantics_canonicalization_planning_v1(
    *,
    governance_debt_register_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "governance_debt_register_roadmap_decision_policy_v1.json",
        "governance_debt_roadmap_route_candidate_matrix_v1.json",
        "governance_debt_priority_decision_matrix_v1.json",
        "selected_governance_debt_roadmap_route_decision_v1.json",
        "permission_semantics_planning_scope_v1.json",
        "future_development_norms_planning_scope_v1.json",
        "forbidden_state_combination_planning_v1.json",
        "canonical_semantics_output_plan_v1.json",
        "governance_roadmap_decision_non_claims_register_v1.json",
        "governance_debt_register_roadmap_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_upstream(governance_debt_register_roadmap_decision_root, upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]
    up_verifier = up_art.get("verifier_report.json") or {}
    up_readiness = up_art.get("governance_debt_register_roadmap_readiness_decision_v1.json") or {}
    selected = up_art.get("selected_governance_debt_roadmap_route_decision_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_route = up_summary.get("selected_route") == SELECTED_ROUTE
    upstream_constraints = up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID
    upstream_ready = up_readiness.get("ready_for_permission_semantics_canonicalization_planning") is True
    upstream_final_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL
    bound_deps = up_summary.get("bound_dependencies") or []
    bound_ok = BOUND_B in bound_deps and BOUND_C in bound_deps

    upstream_flags_ok = (
        up_summary.get("canonicalization_executed_now") is False
        and up_summary.get("debt_fix_executed_now") is False
        and up_summary.get("verifier_modified_now") is False
        and up_readiness.get("ready_for_debt_fix_execution") is False
        and up_readiness.get("ready_for_canonicalization_execution") is False
        and up_readiness.get("ready_for_real_rollback_rehearsal_execution") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
        and up_summary.get("authorization_granted_now") is False
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_roadmap_decision_missing")
    if not upstream_go:
        blockers.append("upstream_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_boundary_not_ok")
    if not upstream_route:
        blockers.append("upstream_route_a_not_selected")
    if not bound_ok:
        blockers.append("upstream_route_b_c_not_bound")
    if not upstream_constraints:
        blockers.append("upstream_constraints_ref_missing")
    if not upstream_ready:
        blockers.append("upstream_not_ready_for_planning")
    if not upstream_final_ok:
        blockers.append("upstream_final_decision_mismatch")
    if not upstream_flags_ok:
        blockers.append("upstream_flags_not_frozen")

    boundary_ok = not blockers

    permission_semantics_canonicalization_planning_policy = {
        "phase_name": PHASE_ID,
        "planning_id": PLANNING_ID,
        "source_phase": SOURCE_PHASE,
        "source_selected_route_observed": SELECTED_ROUTE if upstream_route else up_summary.get("selected_route"),
        "source_bound_dependencies_observed": bound_deps,
        "source_governance_constraints_ref_observed": CONSTRAINT_DOC_ID if upstream_constraints else None,
        "route_b_binding": BOUND_B,
        "route_c_binding": BOUND_C,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        **_planning_meta(),
    }

    phase_rows = _build_phase_type_table()
    perm_rows = _build_permission_state_table()
    auth_rows = _build_authorization_state_table()
    exec_rows = _build_execution_state_table()
    art_rows = _build_artifact_state_table()
    ready_rows = _build_readiness_state_table()
    result_rows = _build_result_state_table()
    route_rows = _build_route_state_table()
    forbidden_rows = _build_forbidden_combinations()
    norm_rows = _build_development_norms()
    verifier_rows = _build_verifier_checklist()
    non_claim_rows = _build_non_claims_rules()

    phase_type_semantics_table = {"rows": phase_rows, "row_count": len(phase_rows), **_planning_meta()}
    permission_state_semantics_table = {"rows": perm_rows, "row_count": len(perm_rows), **_planning_meta()}
    authorization_state_semantics_table = {"rows": auth_rows, "row_count": len(auth_rows), **_planning_meta()}
    execution_state_semantics_table = {"rows": exec_rows, "row_count": len(exec_rows), **_planning_meta()}
    artifact_state_semantics_table = {"rows": art_rows, "row_count": len(art_rows), **_planning_meta()}
    readiness_state_semantics_table = {"rows": ready_rows, "row_count": len(ready_rows), **_planning_meta()}
    result_state_semantics_table = {"rows": result_rows, "row_count": len(result_rows), **_planning_meta()}
    route_state_semantics_table = {"rows": route_rows, "row_count": len(route_rows), **_planning_meta()}
    forbidden_state_combination_matrix = {"rows": forbidden_rows, "row_count": len(forbidden_rows), **_planning_meta()}
    development_norms_matrix = {"rows": norm_rows, "row_count": len(norm_rows), **_planning_meta()}
    verifier_semantics_checklist = {"rows": verifier_rows, "row_count": len(verifier_rows), **_planning_meta()}
    non_claims_generation_rules = {"rows": non_claim_rows, "row_count": len(non_claim_rows), **_planning_meta()}

    ready = boundary_ok
    permission_semantics_canonicalization_planning_readiness_decision = {
        "ready_for_permission_semantics_canonicalization_dryrun": bool(ready),
        "ready_for_canonicalization_execution": False,
        "ready_for_debt_fix_execution": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "canonicalization_planning_completed": bool(ready),
        "phase_type_semantics_table_generated": True,
        "permission_state_semantics_table_generated": True,
        "authorization_state_semantics_table_generated": True,
        "execution_state_semantics_table_generated": True,
        "artifact_state_semantics_table_generated": True,
        "readiness_state_semantics_table_generated": True,
        "result_state_semantics_table_generated": True,
        "route_state_semantics_table_generated": True,
        "forbidden_state_combination_matrix_generated": True,
        "development_norms_matrix_generated": True,
        "verifier_semantics_checklist_generated": True,
        "non_claims_generation_rules_generated": True,
        "route_b_requirement_acknowledged": True,
        "route_c_requirement_acknowledged": True,
        "final_decision": FINAL_DECISION if ready else "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_debt_register_roadmap_decision_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_selected_route_observed": SELECTED_ROUTE if upstream_route else up_summary.get("selected_route"),
        "source_bound_dependencies_observed": bound_deps,
        "phase_type_count": len(phase_rows),
        "permission_state_count": len(perm_rows),
        "forbidden_combination_count": len(forbidden_rows),
        "development_norm_count": len(norm_rows),
        "verifier_checklist_count": len(verifier_rows),
        "non_claims_rule_count": len(non_claim_rows),
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready else "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_planning_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "governance_debt_register_roadmap_decision",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_planning_meta(),
            }
        ],
        "row_count": 1,
        **_planning_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        "final_decision": FINAL_DECISION if ready else "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "reason": "planning blueprint only; dry-run next; not enforced now",
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "permission_semantics_canonicalization_planning_policy": permission_semantics_canonicalization_planning_policy,
        "phase_type_semantics_table": phase_type_semantics_table,
        "permission_state_semantics_table": permission_state_semantics_table,
        "authorization_state_semantics_table": authorization_state_semantics_table,
        "execution_state_semantics_table": execution_state_semantics_table,
        "artifact_state_semantics_table": artifact_state_semantics_table,
        "readiness_state_semantics_table": readiness_state_semantics_table,
        "result_state_semantics_table": result_state_semantics_table,
        "route_state_semantics_table": route_state_semantics_table,
        "forbidden_state_combination_matrix": forbidden_state_combination_matrix,
        "development_norms_matrix": development_norms_matrix,
        "verifier_semantics_checklist": verifier_semantics_checklist,
        "non_claims_generation_rules": non_claims_generation_rules,
        "permission_semantics_canonicalization_planning_readiness_decision": permission_semantics_canonicalization_planning_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
