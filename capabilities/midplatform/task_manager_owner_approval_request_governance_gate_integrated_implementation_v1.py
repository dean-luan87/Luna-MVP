# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Governance Gate Integrated Implementation v1.

Module-level governance closure before real issuance: integrated roadmap, authorization
preparation, missing conditions routing, closure boundary, slice test plan, precondition checklist.
No real execution. No fragmentary sub-phases.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
    MODULE_FIRST_CADENCE_RULE_DOC,
    MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.protocols.module_first_development_verification_cadence_rule_v1 import (
    DOC_REL_PATH as MODULE_FIRST_DOC,
    build_module_first_cadence_rule_document,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.protocols.top_level_objective_priority_rule_v1 import (
    DOC_REL_PATH as TOP_LEVEL_DOC,
    build_top_level_objective_priority_rule_document,
)
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES,
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_TERM_OVERRIDES,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FINAL_GATE_PLANNING_ROOT,
    FINAL_DECISION_GO as FINAL_GATE_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as FINAL_GATE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Implementation-v1-001"
)
SCOPE = "midplatform_task_manager_owner_approval_request_governance_gate_integrated_implementation_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_READY_FOR_AUTHORIZATION_PREPARATION_DRYRUN_OR_FUNCTIONAL_SLICE_PLANNING"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_BLOCKED_BY_UPSTREAM_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_INTEGRATED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_BLOCKED_BY_INTEGRATED_GAP"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_A = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Authorization-Preparation-DryRun-v1-001"
NEXT_PHASE_B = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-Test-Planning-v1-001"
NEXT_PHASE_C = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Missing-Conditions-Closure-Package-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Implementation-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1_smoke_v0"
)
GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

INTEGRATED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json",
    "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md",
    "integrated_roadmap_decision_v1.json",
    "issuance_authorization_preparation_package_v1.json",
    "missing_conditions_routing_v1.json",
    "real_issuance_precondition_checklist_v1.json",
    "record_approval_ack_evidence_closure_boundary_v1.json",
    "module_level_functional_slice_test_plan_v1.json",
    "governance_rule_reference_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_INDEX: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1.json",
)

SELECTED_ROUTE = "Owner Approval Request Issuance Authorization Preparation"

FUNCTIONAL_SLICE_CHAINS: Tuple[str, ...] = (
    "owner_approval_request_candidate_lifecycle",
    "authorization_preparation_lifecycle",
    "record_approval_ack_evidence_closure_lifecycle",
    "absence_and_rollback_safety_lifecycle",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "integrated_plan_complete",
    "integrated_roadmap_decision_complete",
    "issuance_authorization_preparation_package_complete",
    "missing_conditions_routing_complete",
    "real_issuance_precondition_checklist_complete",
    "record_approval_ack_evidence_boundary_complete",
    "module_level_functional_slice_test_plan_complete",
    "top_level_objective_priority_rule_ref_ok",
    "module_first_cadence_rule_ref_ok",
    "reuse_first_rule_ref_ok",
    "validate_once_rule_ref_ok",
    "file_size_governance_review_ok",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, post: Path, gate: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "integrated_implementation_only": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "post_review_root": str(post),
        "final_gate_planning_root": str(gate),
    }


def _build_governance_missing_conditions() -> List[Dict[str, Any]]:
    return [
        {
            "condition_id": "real_request_issuance",
            "category": "blocker",
            "resolved": False,
            "note": "Real owner approval request issuance requires governance gate integrated implementation GO.",
        },
        {
            "condition_id": "runtime_adapter_implementation",
            "category": "future_runtime",
            "resolved": False,
            "note": "Module adapter and runtime integration not implemented; governance debt carryover.",
        },
        {
            "condition_id": "whitebox_runtime_integration",
            "category": "future_runtime",
            "resolved": False,
            "note": "Whitebox runtime integration absent by design at this gate.",
        },
        {
            "condition_id": "module_level_functional_slice_tests",
            "category": "non_blocking",
            "resolved": False,
            "note": "Per Module-First cadence: complete module fill and slice tests before release gate.",
        },
        {
            "condition_id": "governance_debt_closure",
            "category": "governance_debt",
            "resolved": False,
            "note": "Governance debts preserved; must_not_implement_now flags remain.",
        },
        {
            "condition_id": "record_approval_closure_candidate_chain",
            "category": "non_blocking",
            "resolved": True,
            "note": "Planning, DryRun, and Post-DryRun Review GO achieved.",
        },
    ]


def _route_missing_conditions(conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    bucket_map = {
        "real_request_issuance": "blocker_before_real_issuance",
        "runtime_adapter_implementation": "future_runtime_debt",
        "whitebox_runtime_integration": "future_runtime_debt",
        "module_level_functional_slice_tests": "non_blocking_follow_up",
        "governance_debt_closure": "governance_debt",
        "record_approval_closure_candidate_chain": "resolved",
    }
    return [
        {
            "condition_id": c.get("condition_id"),
            "source_category": c.get("category"),
            "source_resolved": c.get("resolved"),
            "routing_bucket": bucket_map.get(c.get("condition_id") or "", "unknown"),
        }
        for c in conditions
    ]


def run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1(
    *,
    post_review_root: str,
    final_gate_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post = Path(post_review_root).expanduser().resolve()
    gate = Path(final_gate_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post, gate)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    post_summary = _read_json(post / "summary.json")
    post_verifier = _read_json(post / "verifier_report.json")
    gate_summary = _read_json(gate / "summary.json")
    gate_verifier = _read_json(gate / "verifier_report.json")
    gate_file_size = _read_json(gate / "file_size_governance_review_v1.json")
    post_file_size = _read_json(post / "file_size_governance_review_v1.json")
    missing_doc = _read_json(gate / UPSTREAM_INDEX[2])

    post_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and post_summary.get("post_review_pass") is True
    )
    closure_result_accepted = (
        post_review_go
        and post_summary.get("dryrun_result_accepted") is True
    )
    if not post_review_go:
        issues.append("direct_upstream_not_go")
    if not closure_result_accepted:
        issues.append("closure_result_not_accepted")

    direct_upstream_ok = post_review_go and closure_result_accepted
    direct_upstream_ref_linked = post_review_go

    final_gate_go = (
        gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO
        and gate_summary.get("recommended_next_phase") == FINAL_GATE_PLANNING_NEXT_PHASE
        and gate_verifier.get("verifier") == "GO"
        and gate_summary.get("final_gate_planning_pass") is True
        and gate_summary.get("final_gate_plan_complete") is True
    )
    if not final_gate_go:
        downstream_readiness_gaps.append("final_gate_planning_not_go")

    governance_gate_node_linked = True
    evidence_paths_declared = direct_upstream_ok and governance_gate_node_linked
    downstream_readiness_refs = [
        "authorization_preparation_dryrun",
        "module_level_functional_slice_planning",
        "functional_slice_dryrun",
        "module_governance_closure",
        "module_handoff",
        "broader_midplatform_closure_roadmap",
    ]

    conditions = list(missing_doc.get("conditions") or _build_governance_missing_conditions())
    routed = _route_missing_conditions(conditions)
    missing_conditions_routing_complete = direct_upstream_ok and len(routed) >= 6 and all(r.get("routing_bucket") for r in routed)
    if not missing_conditions_routing_complete:
        issues.append("routing_incomplete")

    integrated_roadmap_decision_complete = (
        direct_upstream_ok
        and missing_conditions_routing_complete
        and any(r.get("routing_bucket") == "resolved" for r in routed)
        and any(r.get("routing_bucket") == "blocker_before_real_issuance" for r in routed)
    )
    if not integrated_roadmap_decision_complete:
        issues.append("roadmap_incomplete")

    auth_package = {
        "authorization_package_candidate": True,
        "authorization_precondition_candidate": True,
        "owner_operator_explicit_approval_required": True,
        "authorization_denial_reference": "candidate_only",
        "authorization_expiry_reference": "candidate_only",
        "authorization_revocation_reference": "candidate_only",
        "authorization_request_absent": True,
        "executes_real_authorization": False,
    }
    issuance_authorization_preparation_package_complete = (
        integrated_roadmap_decision_complete
        and auth_package.get("authorization_package_candidate") is True
        and auth_package.get("authorization_request_absent") is True
    )
    if not issuance_authorization_preparation_package_complete:
        issues.append("auth_prep_incomplete")

    closure_rows = [
        {
            "candidate_id": cid,
            "forbidden_final": forbidden,
            "forbidden_final_state": forbidden,
            "still_candidate": True,
            "record_created": False,
            "closure_executed": False,
        }
        for cid, forbidden in CANDIDATE_BOUNDARY_PAIRS
    ]
    record_approval_ack_evidence_boundary_complete = (
        direct_upstream_ok
        and len(closure_rows) == len(CORE_CANDIDATE_IDS)
        and all(r.get("still_candidate") for r in closure_rows)
    )
    if not record_approval_ack_evidence_boundary_complete:
        issues.append("closure_boundary_incomplete")

    slice_plan = [
        {
            "chain_id": chain,
            "test_type": "functional_slice",
            "executed": False,
            "blocking_real_issuance_now": False,
        }
        for chain in FUNCTIONAL_SLICE_CHAINS
    ]
    module_level_functional_slice_test_plan_complete = (
        direct_upstream_ok and len(slice_plan) == len(FUNCTIONAL_SLICE_CHAINS) and all(not t.get("executed") for t in slice_plan)
    )
    if not module_level_functional_slice_test_plan_complete:
        issues.append("slice_plan_incomplete")

    checklist_items = [
        {"item_id": "owner_operator_explicit_approval", "required": True, "satisfied": False},
        {"item_id": "authorization_request_readiness", "required": True, "satisfied": False},
        {"item_id": "record_readiness", "required": True, "satisfied": False},
        {"item_id": "evidence_readiness", "required": True, "satisfied": False},
        {"item_id": "rollback_expiry_revocation_readiness", "required": True, "satisfied": False},
        {"item_id": "runtime_boundary_readiness", "required": True, "satisfied": False},
        {"item_id": "record_approval_closure_candidate_chain", "required": True, "satisfied": True},
    ]
    real_issuance_precondition_checklist_complete = (
        direct_upstream_ok
        and len(checklist_items) >= 6
        and any(i.get("item_id") == "record_approval_closure_candidate_chain" and i.get("satisfied") for i in checklist_items)
        and any(not i.get("satisfied") for i in checklist_items if i.get("item_id") != "record_approval_closure_candidate_chain")
    )
    if not real_issuance_precondition_checklist_complete:
        issues.append("checklist_incomplete")

    top_level_doc = build_top_level_objective_priority_rule_document()
    module_first_doc = build_module_first_cadence_rule_document()
    top_level_objective_priority_rule_ref_ok = (
        top_level_doc.get("top_level_objective_priority_rule_complete") is True
        and (repo_root / TOP_LEVEL_DOC).is_file()
        and (repo_root / TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC).is_file()
    )
    module_first_cadence_rule_ref_ok = (
        module_first_doc.get("module_first_cadence_rule_complete") is True
        and (repo_root / MODULE_FIRST_DOC).is_file()
    )
    reuse_first_rule_ref_ok = REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF == "Reuse-First Protocol Engineering Rule"
    validate_once_rule_ref_ok = VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN == "Protocol Validate Once Per Module Rule"
    governance_refs_ok = (
        top_level_objective_priority_rule_ref_ok
        and module_first_cadence_rule_ref_ok
        and reuse_first_rule_ref_ok
        and validate_once_rule_ref_ok
        and (repo_root / FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC).is_file()
    )
    if not governance_refs_ok:
        issues.append("governance_ref_gap")

    absence_post = {k: post_summary.get(k) is True for k in ABSENCE_KEYS}
    absence_gate = {k: gate_summary.get(k) is True for k in ABSENCE_KEYS} if gate_summary else {}
    absence = {k: absence_post.get(k) for k in ABSENCE_KEYS}
    if not all(absence.values()) and final_gate_go:
        absence = {k: absence_post.get(k) and absence_gate.get(k) for k in ABSENCE_KEYS}
    non_execution_boundary_ok = direct_upstream_ok and all(absence.values())
    if final_gate_go and gate_summary.get("non_execution_boundary_ok") is not True:
        downstream_readiness_gaps.append("final_gate_non_execution_boundary_not_confirmed")
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if post_summary.get(flag) is True or gate_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Governance-Gate-Integrated-Planning-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Governance-Gate-Integrated-Implementation-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=(gate_file_size or post_file_size).get("previous_interruption_type"),
        previous_interruption_duration_seconds=(gate_file_size or post_file_size).get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=(gate_file_size or post_file_size).get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    integrated_plan_complete = (
        integrated_roadmap_decision_complete
        and issuance_authorization_preparation_package_complete
        and missing_conditions_routing_complete
        and real_issuance_precondition_checklist_complete
        and record_approval_ack_evidence_boundary_complete
        and module_level_functional_slice_test_plan_complete
        and governance_refs_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
    )

    has_blocker = any(r.get("routing_bucket") == "blocker_before_real_issuance" for r in routed)
    recommended_next_phase = NEXT_PHASE_A if has_blocker and integrated_plan_complete else NEXT_PHASE_C
    if integrated_plan_complete and not has_blocker:
        recommended_next_phase = NEXT_PHASE_A
    next_phase_candidates = [NEXT_PHASE_A, NEXT_PHASE_B, NEXT_PHASE_C]
    next_phase_readiness_ok = integrated_plan_complete and non_execution_boundary_ok and recommended_next_phase in next_phase_candidates

    evidence_chain_ok = (
        closure_result_accepted
        and direct_upstream_ref_linked
        and governance_gate_node_linked
        and evidence_paths_declared
    )
    governance_gate_pass = (
        direct_upstream_ok
        and evidence_chain_ok
        and integrated_plan_complete
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
    )

    if not direct_upstream_ok:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif not integrated_plan_complete:
        final_decision = FINAL_DECISION_INTEGRATED
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "integrated_plan_complete": integrated_plan_complete,
        "integrated_roadmap_decision_complete": integrated_roadmap_decision_complete,
        "issuance_authorization_preparation_package_complete": issuance_authorization_preparation_package_complete,
        "missing_conditions_routing_complete": missing_conditions_routing_complete,
        "real_issuance_precondition_checklist_complete": real_issuance_precondition_checklist_complete,
        "record_approval_ack_evidence_boundary_complete": record_approval_ack_evidence_boundary_complete,
        "module_level_functional_slice_test_plan_complete": module_level_functional_slice_test_plan_complete,
        "top_level_objective_priority_rule_ref_ok": top_level_objective_priority_rule_ref_ok,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "reuse_first_rule_ref_ok": reuse_first_rule_ref_ok,
        "validate_once_rule_ref_ok": validate_once_rule_ref_ok,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "real_request_issuance_authorized": False,
        "prior_post_review_go": post_review_go,
        "prior_final_gate_planning_go": final_gate_go,
        "closure_result_accepted": closure_result_accepted,
        "direct_upstream_ref_linked": direct_upstream_ref_linked,
        "governance_gate_node_linked": governance_gate_node_linked,
        "evidence_paths_declared": evidence_paths_declared,
        "evidence_chain_ok": evidence_chain_ok,
        "governance_gate_pass": governance_gate_pass,
        "governance_gate_integrated_implementation_complete": governance_gate_pass,
        "downstream_readiness_refs": downstream_readiness_refs,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "candidate_only": True,
        "no_execution_leakage": True,
        "no_protocol_change": True,
        "selected_route": SELECTED_ROUTE,
        "no_fragmentary_phase_expansion": True,
        "no_independent_roadmap_verifier": True,
        "no_independent_authorization_planning_phase": True,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    integrated_pass = (
        governance_gate_pass
        and len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_values[k] for k in GO_CONDITIONS_KEYS)
    )
    next_phase = recommended_next_phase if integrated_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(post_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_governance_gate_integrated_implementation"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    roadmap = {
        "decision_id": "integrated_roadmap_decision_v1",
        "integrated_roadmap_decision_complete": integrated_roadmap_decision_complete,
        "selected_route": SELECTED_ROUTE,
        "executes_real_issuance": False,
        "secondary_routes": [
            "Functional Slice Test Planning",
            "Missing Conditions Closure Package",
        ],
        **meta,
    }
    auth_prep_doc = {
        "package_id": "issuance_authorization_preparation_package_v1",
        "issuance_authorization_preparation_package_complete": issuance_authorization_preparation_package_complete,
        **auth_package,
        **meta,
    }
    routing_doc = {
        "routing_id": "missing_conditions_routing_v1",
        "missing_conditions_routing_complete": missing_conditions_routing_complete,
        "routes": routed,
        **meta,
    }
    checklist_doc = {
        "checklist_id": "real_issuance_precondition_checklist_v1",
        "real_issuance_precondition_checklist_complete": real_issuance_precondition_checklist_complete,
        "items": checklist_items,
        "real_request_issuance_authorized": False,
        **meta,
    }
    closure_doc = {
        "boundary_id": "record_approval_ack_evidence_closure_boundary_v1",
        "record_approval_ack_evidence_boundary_complete": record_approval_ack_evidence_boundary_complete,
        "rows": closure_rows,
        "core_candidate_ids": list(CORE_CANDIDATE_IDS),
        **meta,
    }
    slice_doc = {
        "plan_id": "module_level_functional_slice_test_plan_v1",
        "module_level_functional_slice_test_plan_complete": module_level_functional_slice_test_plan_complete,
        "chains": slice_plan,
        **meta,
    }
    governance_doc = {
        "reference_id": "governance_rule_reference_v1",
        "top_level_objective_priority_rule_ref": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
        "top_level_objective_priority_rule_doc": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        "module_first_cadence_rule_doc": MODULE_FIRST_CADENCE_RULE_DOC,
        "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "file_size_module_split_governance_rule_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        "top_level_objective_priority_rule_ref_ok": top_level_objective_priority_rule_ref_ok,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "reuse_first_rule_ref_ok": reuse_first_rule_ref_ok,
        "validate_once_rule_ref_ok": validate_once_rule_ref_ok,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **meta,
    }
    integrated_plan = {
        "plan_id": "task_manager_owner_approval_request_governance_gate_integrated_plan_v1",
        "integrated_plan_complete": integrated_plan_complete,
        "integrated_sections": [
            "roadmap_decision",
            "authorization_preparation",
            "missing_conditions_routing",
            "closure_boundary",
            "functional_slice_test_plan",
            "real_issuance_precondition_checklist",
        ],
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": next_phase,
        "next_phase_candidates": next_phase_candidates,
        **go_values,
        "final_decision": final_decision,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "integrated_implementation_pass": integrated_pass,
        "governance_gate_pass": governance_gate_pass,
        "governance_gate_integrated_implementation_complete": governance_gate_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    md = "\n".join(
        [
            "# Owner Approval Request Governance Gate Integrated Implementation v1",
            "",
            "Module-level governance closure before real issuance. No fragmentary sub-phases.",
            "",
            f"Selected route: `{SELECTED_ROUTE}`",
            f"Integrated plan complete: `{integrated_plan_complete}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_owner_approval_request_governance_gate_integrated_plan": integrated_plan,
        "task_manager_owner_approval_request_governance_gate_integrated_plan_md": md,
        "integrated_roadmap_decision": roadmap,
        "issuance_authorization_preparation_package": auth_prep_doc,
        "missing_conditions_routing": routing_doc,
        "real_issuance_precondition_checklist": checklist_doc,
        "record_approval_ack_evidence_closure_boundary": closure_doc,
        "module_level_functional_slice_test_plan": slice_doc,
        "governance_rule_reference": governance_doc,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
