# -*- coding: utf-8 -*-
"""Terminology Canonical Table Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, formal table non-generation,
entry simulation-only, verifier non-modification, forbidden non-enforcement,
registry non-write, success claim dependency frozen.
Does not generate formal table, enforce terminology, or release execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.governance.terminology_canonical_table_planning_v1 import (
    REQUIRED_TERMS,
    SUCCESS_CLAIM_TOPICS,
)

PHASE_ID = "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "terminology_canonical_table_post_dryrun_review_only"
SOURCE_CHAIN = "terminology_canonical_table_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Terminology-Canonical-Table-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"

FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "terminology_canonical_table_dryrun_policy_v1.json", 0),
    ("planning artifact completeness dry-run", "terminology_planning_artifact_completeness_dryrun_v1.json", 10),
    ("terminology entry structure dry-run", "terminology_entry_structure_dryrun_v1.json", 24),
    ("terminology verifier consumption dry-run", "terminology_verifier_consumption_dryrun_v1.json", 24),
    ("terminology forbidden interpretation dry-run", "terminology_forbidden_interpretation_dryrun_v1.json", 24),
    ("terminology required fields dry-run", "terminology_required_fields_dryrun_v1.json", 24),
    ("terminology success claim dependency dry-run", "terminology_success_claim_dependency_dryrun_v1.json", 12),
    ("terminology semantic registry candidate dry-run", "terminology_semantic_registry_candidate_dryrun_v1.json", 6),
    ("terminology cross-artifact consistency dry-run", "terminology_cross_artifact_consistency_dryrun_v1.json", 12),
    ("terminology dry-run non-claims register", "terminology_dryrun_non_claims_register_v1.json", 9),
    ("dry-run readiness decision", "terminology_canonical_table_dryrun_readiness_decision_v1.json", 0),
)

FORMAL_TABLE_REVIEW_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("canonical_table_generated_now", "canonical_table_generated_now"),
    ("terminology_canonicalization_executed_now", "terminology_canonicalization_executed_now"),
    ("terminology_enforced_now", "terminology_enforced_now"),
    ("registry_written_now", "registry_written_now"),
    ("formal terminology_canonical_table_v1.json not declared generated", "formal_table_v1_declared_generated"),
    ("no canonical_entry_generated_now across 24 terms", "any_canonical_entry_generated"),
)

POST_REVIEW_NON_CLAIMS = [
    "Post-DryRun Review GO does not mean terminology canonical table is generated.",
    "Post-DryRun Review GO does not mean terminology is canonicalized.",
    "Post-DryRun Review GO does not mean terminology rules are enforced.",
    "Post-DryRun Review GO does not mean semantic registry has been written.",
    "Post-DryRun Review GO does not mean verifier has been modified.",
    "Post-DryRun Review GO does not mean phase template has been modified.",
    "Post-DryRun Review GO does not mean success claim gate planning may start automatically.",
    "Post-DryRun Review GO does not mean permission semantics canonicalization may execute.",
    "Post-DryRun Review GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "success_claim_canonicalization_executed_now": False,
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
    readiness = _try_read_json(
        root / "terminology_canonical_table_dryrun_readiness_decision_v1.json"
    ) if root else None
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
        if filename == "terminology_planning_artifact_completeness_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True and count >= 10
        if filename == "terminology_entry_structure_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True and count >= 24
        if filename == "terminology_cross_artifact_consistency_dryrun_v1.json" and isinstance(payload, dict):
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


def _build_formal_table_non_generation_review(
    up_summary: Dict[str, Any],
    entry_dryrun: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    entry_rows = entry_dryrun.get("rows") or []
    any_entry_generated = any(r.get("canonical_entry_generated_now") is True for r in entry_rows)
    formal_declared = up_summary.get("canonical_table_generated_now") is True
    observed_flags = {
        "canonical_table_generated_now": up_summary.get("canonical_table_generated_now") is True,
        "terminology_canonicalization_executed_now": up_summary.get("terminology_canonicalization_executed_now") is True,
        "terminology_enforced_now": up_summary.get("terminology_enforced_now") is True,
        "registry_written_now": up_summary.get("registry_written_now") is True,
        "formal_table_v1_declared_generated": formal_declared,
        "any_canonical_entry_generated": any_entry_generated,
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, key in FORMAL_TABLE_REVIEW_TARGETS:
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
                review_notes="no formal table generation" if review_pass else "formal generation signal detected",
            )
        )
    return rows, all_pass


def _build_entry_simulation_review(entry_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_term = {r.get("term"): r for r in (entry_dryrun.get("rows") or []) if r.get("term")}
    for term in REQUIRED_TERMS:
        row = by_term.get(term, {})
        struct_valid = row.get("future_canonical_entry_structurally_valid") is True
        not_generated = row.get("canonical_entry_generated_now") is False
        not_enforced = row.get("terminology_enforced_now") is False
        simulated_only = struct_valid and not_generated and not_enforced
        review_pass = simulated_only
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                term=term,
                future_canonical_entry_structurally_valid=struct_valid,
                canonical_entry_generated_now=False,
                terminology_enforced_now=False,
                simulated_only=simulated_only,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) == 24


def _build_verifier_non_modification_review(verifier_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in verifier_dryrun.get("rows") or []:
        simulated = row.get("simulated_verifier_consumption") is True
        not_modified = row.get("verifier_modified_now") is False
        not_enforced = row.get("not_enforced_now") is True
        review_pass = simulated and not_modified and not_enforced and bool(row.get("failure_condition"))
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                term=row.get("term"),
                simulated_verifier_consumption=simulated,
                verifier_modified_now=False,
                not_enforced_now=True,
                severity_present=bool(row.get("severity")),
                failure_condition_present=bool(row.get("failure_condition")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 24


def _build_forbidden_non_enforcement_review(forbidden_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in forbidden_dryrun.get("rows") or []:
        present = bool(row.get("forbidden_interpretation"))
        simulated = row.get("simulated_check") is True
        not_enforced = row.get("enforced_now") is False
        not_modified = row.get("verifier_modified_now") is False
        review_pass = present and simulated and not_enforced and not_modified
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                term=row.get("term"),
                forbidden_interpretation_present=present,
                simulated_check=simulated,
                enforced_now=False,
                verifier_modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 24


def _build_required_fields_simulation_review(fields_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in fields_dryrun.get("rows") or []:
        struct_ok = row.get("field_set_structurally_valid") is True
        verifier_req = row.get("verifier_required_observed") is True
        not_enforced = row.get("enforced_now") is False
        template_ok = row.get("phase_template_modified_now") is False
        review_pass = struct_ok and verifier_req and not_enforced and template_ok
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                term=row.get("term"),
                field_set_structurally_valid=struct_ok,
                verifier_required_observed=verifier_req,
                enforced_now=False,
                phase_template_modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 24


def _build_registry_write_review(registry_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in registry_dryrun.get("rows") or []:
        written = row.get("registry_written_now") is True
        enforced = row.get("terminology_enforced_now") is True
        review_pass = (
            row.get("indexable_in_dryrun") is True
            and row.get("future_registry_candidate") is True
            and not written
            and not enforced
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                registry_candidate_type=row.get("registry_candidate_type"),
                indexable_in_dryrun=row.get("indexable_in_dryrun") is True,
                future_registry_candidate=row.get("future_registry_candidate") is True,
                registry_written_now=False,
                terminology_enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 6


def _build_success_claim_dependency_review(success_dryrun: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    topics_seen: set = set()
    for row in success_dryrun.get("rows") or []:
        topic = row.get("success_claim_topic")
        topics_seen.add(topic)
        simulated = row.get("simulated_dependency_check") is True
        not_exec = row.get("success_claim_canonicalization_executed_now") is False
        not_ready_planning = row.get("ready_for_success_claim_gate_planning", False) is False
        review_pass = simulated and not_exec and not_ready_planning and bool(row.get("dependent_terms"))
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                success_claim_topic=topic,
                dependent_terms=row.get("dependent_terms"),
                simulated_dependency_check=simulated,
                success_claim_canonicalization_executed_now=False,
                ready_for_success_claim_gate_planning=False,
                review_pass=review_pass,
            )
        )
    for topic, _terms in SUCCESS_CLAIM_TOPICS:
        if topic not in topics_seen:
            all_pass = False
    return rows, all_pass and len(rows) >= 12


def run_terminology_canonical_table_post_dryrun_review_v1(
    *,
    terminology_canonical_table_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(terminology_canonical_table_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream dryrun boundary_ok is not true")
    if up_readiness.get("ready_for_terminology_canonical_table_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for_terminology_canonical_table_post_dryrun_review")
    if up_summary.get("terminology_dryrun_only") is not True:
        blockers.append("upstream terminology_dryrun_only is not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated is not true")
    if up_summary.get("canonical_table_generated_now") is not False:
        blockers.append("upstream canonical_table_generated_now is not false")
    if up_summary.get("terminology_enforced_now") is not False:
        blockers.append("upstream terminology_enforced_now is not false")
    if up_summary.get("registry_written_now") is not False:
        blockers.append("upstream registry_written_now is not false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")
    if up_readiness.get("ready_for_success_claim_gate_planning") is not False:
        blockers.append("upstream ready_for_success_claim_gate_planning must remain false")
    if up_readiness.get("ready_for_terminology_canonicalization_execution") is not False:
        blockers.append("upstream ready_for_terminology_canonicalization_execution must remain false")

    completeness_rows, completeness_pass = _build_completeness_review(artifacts)
    entry_dryrun = artifacts.get("terminology_entry_structure_dryrun_v1.json") or {}
    formal_rows, formal_pass = _build_formal_table_non_generation_review(up_summary, entry_dryrun)
    entry_rows, entry_pass = _build_entry_simulation_review(entry_dryrun)
    verifier_rows, verifier_pass = _build_verifier_non_modification_review(
        artifacts.get("terminology_verifier_consumption_dryrun_v1.json") or {}
    )
    forbidden_rows, forbidden_pass = _build_forbidden_non_enforcement_review(
        artifacts.get("terminology_forbidden_interpretation_dryrun_v1.json") or {}
    )
    fields_rows, fields_pass = _build_required_fields_simulation_review(
        artifacts.get("terminology_required_fields_dryrun_v1.json") or {}
    )
    registry_rows, registry_pass = _build_registry_write_review(
        artifacts.get("terminology_semantic_registry_candidate_dryrun_v1.json") or {}
    )
    success_rows, success_pass = _build_success_claim_dependency_review(
        artifacts.get("terminology_success_claim_dependency_dryrun_v1.json") or {}
    )

    post_non_claims_rows = [
        _review_row(
            non_claim=nc,
            required=True,
            present=True,
            risk_if_missing="post-dryrun review GO misread",
            review_pass=True,
        )
        for nc in POST_REVIEW_NON_CLAIMS
    ]

    review_pass = (
        completeness_pass
        and formal_pass
        and entry_pass
        and verifier_pass
        and forbidden_pass
        and fields_pass
        and registry_pass
        and success_pass
        and not blockers
    )
    boundary_ok = review_pass

    terminology_canonical_table_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_terminology_canonical_table_post_dryrun_review_observed=up_readiness.get(
            "ready_for_terminology_canonical_table_post_dryrun_review"
        )
        is True,
    )

    terminology_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    terminology_formal_table_non_generation_review = {
        "rows": formal_rows,
        "row_count": len(formal_rows),
        "all_pass": formal_pass,
        **_review_meta(),
    }
    terminology_entry_simulation_review = {
        "rows": entry_rows,
        "row_count": len(entry_rows),
        "all_pass": entry_pass,
        **_review_meta(),
    }
    terminology_verifier_non_modification_review = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_review_meta(),
    }
    terminology_forbidden_interpretation_non_enforcement_review = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_review_meta(),
    }
    terminology_required_fields_simulation_review = {
        "rows": fields_rows,
        "row_count": len(fields_rows),
        "all_pass": fields_pass,
        **_review_meta(),
    }
    terminology_registry_write_review = {
        "rows": registry_rows,
        "row_count": len(registry_rows),
        "all_pass": registry_pass,
        **_review_meta(),
    }
    terminology_success_claim_dependency_review = {
        "rows": success_rows,
        "row_count": len(success_rows),
        "all_pass": success_pass,
        **_review_meta(),
    }
    terminology_post_dryrun_review_non_claims_register = {
        "rows": post_non_claims_rows,
        "row_count": len(post_non_claims_rows),
        "all_present": True,
        **_review_meta(),
    }

    terminology_canonical_table_post_dryrun_review_readiness_decision = {
        "ready_for_terminology_canonical_table_roadmap_decision": boundary_ok,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_terminology_enforcement": False,
        "ready_for_canonical_table_generation": False,
        "ready_for_success_claim_gate_planning": False,
        "ready_for_permission_semantics_canonicalization_execution": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_debt_fix_execution": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_dryrun_review_completed": boundary_ok,
        "terminology_dryrun_completeness_review_pass": completeness_pass,
        "formal_table_non_generation_review_pass": formal_pass,
        "terminology_entry_simulation_review_pass": entry_pass,
        "terminology_verifier_non_modification_review_pass": verifier_pass,
        "terminology_forbidden_interpretation_non_enforcement_review_pass": forbidden_pass,
        "terminology_required_fields_simulation_review_pass": fields_pass,
        "terminology_registry_write_review_pass": registry_pass,
        "terminology_success_claim_dependency_review_pass": success_pass,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "terminology_canonical_table_dryrun_input_loaded": upstream["loaded"],
        "term_count": 24,
        "success_claim_topic_count": len(success_rows),
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_ready_for_post_review_observed": up_readiness.get(
            "ready_for_terminology_canonical_table_post_dryrun_review"
        )
        is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "terminology_canonical_table_dryrun",
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
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review pass; terminology not enforced; roadmap decision next; Route C not auto-started",
        **_review_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "terminology_canonical_table_post_dryrun_review_policy": terminology_canonical_table_post_dryrun_review_policy,
        "terminology_dryrun_completeness_review": terminology_dryrun_completeness_review,
        "terminology_formal_table_non_generation_review": terminology_formal_table_non_generation_review,
        "terminology_entry_simulation_review": terminology_entry_simulation_review,
        "terminology_verifier_non_modification_review": terminology_verifier_non_modification_review,
        "terminology_forbidden_interpretation_non_enforcement_review": terminology_forbidden_interpretation_non_enforcement_review,
        "terminology_required_fields_simulation_review": terminology_required_fields_simulation_review,
        "terminology_registry_write_review": terminology_registry_write_review,
        "terminology_success_claim_dependency_review": terminology_success_claim_dependency_review,
        "terminology_post_dryrun_review_non_claims_register": terminology_post_dryrun_review_non_claims_register,
        "terminology_canonical_table_post_dryrun_review_readiness_decision": terminology_canonical_table_post_dryrun_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
