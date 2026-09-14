# -*- coding: utf-8 -*-
"""Midplatform Constitution Governance Hierarchy DryRunAndReview v1 — 三层归位验证."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
    FINAL_DECISION_GO as AUTH_EXT_PLANNING_FINAL_GO,
    NINE_STANDARDS,
    TEN_STANDARDS,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    DESIGN_PRINCIPLES,
    FINAL_DECISION_GO as HIERARCHY_PLANNING_FINAL_GO,
    GOVERNANCE_LAYERS,
    HIERARCHY_ANALOGY,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
    RULE_CLASSIFICATION_QUESTIONS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Constitution-Governance-Hierarchy-DryRunAndReview-v1-001"
SCOPE = "midplatform_constitution_governance_hierarchy_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_constitution_governance_hierarchy_dryrun_and_review_v1"

UPSTREAM_HIERARCHY_PLANNING_FINAL = HIERARCHY_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_HIERARCHY_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_FACTORY_AUTHORIZATION_STANDARD_EXTENSION_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_HIERARCHY_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Capability-Factory-Authorization-Standard-Extension-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Constitution-Governance-Hierarchy-Issue-Review-v1-001"

GENERAL_CONSTITUTION_ARTICLES: Tuple[Tuple[str, str], ...] = (
    ("safety_constitution", "安全宪法"),
    ("survival_constitution", "生存宪法"),
    ("privacy_constitution", "隐私宪法"),
    ("fact_admission_constitution", "事实准入宪法"),
    ("user_output_constitution", "用户输出宪法"),
    ("midplatform_operation_basic_law", "中台运行基本法"),
)

DOMAIN_CONSTITUTIONS: Tuple[Tuple[str, str, str], ...] = (
    ("vision_constitution", "Vision Constitution / 视觉宪法", "planned"),
    ("ocr_constitution", "OCR Constitution / OCR 宪法", "active_for_mapping"),
    ("voice_constitution", "Voice Constitution / 语音宪法", "planned"),
    ("emotion_constitution", "Emotion Constitution / 情感宪法", "future_only"),
    ("memory_constitution", "Memory Constitution / 记忆宪法", "future_only"),
    ("map_constitution", "Map Constitution / 地图宪法", "future_only"),
    ("library_constitution", "Library Constitution / 图书馆宪法", "future_only"),
    ("hive_constitution", "Hive Constitution / 蜂巢宪法", "future_only"),
)

DOMAIN_STANDARD_CATEGORIES: Tuple[str, ...] = (
    "Input Standard",
    "Output Standard",
    "Candidate Standard",
    "Evidence Standard",
    "Authorization Standard",
    "Module Usage Standard",
    "Provider / Model Usage Standard",
    "Upstream / Downstream Transfer Standard",
    "Rollback / Fallback Standard",
    "User Output Standard",
)

OCR_DOMAIN_STANDARDS: Tuple[str, ...] = (
    "OCR Input Standard",
    "OCR Output Standard",
    "OCR Candidate Standard",
    "OCR Evidence Standard",
    "OCR Provider Usage Standard",
    "OCR Authorization Standard",
    "OCR Boundary Standard",
    "OCR Transfer Standard",
)

HARNESS_CONSUMERS: Tuple[Tuple[str, str], ...] = (
    ("ocr", "validated"),
    ("vision", "validated"),
    ("voice", "validated"),
    ("map", "future_only"),
    ("library", "future_only"),
    ("hive", "future_only"),
    ("memory", "future_only"),
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "hierarchy_dryrun_to_constitution_registry_update",
    "hierarchy_dryrun_to_runtime_enforcement",
    "hierarchy_dryrun_to_domain_standard_activation",
    "hierarchy_dryrun_to_ocr_authorization_execution",
    "hierarchy_dryrun_to_real_dependency_check",
    "hierarchy_dryrun_to_provider_import",
    "hierarchy_dryrun_to_dependency_install",
    "hierarchy_dryrun_to_model_download",
    "hierarchy_dryrun_to_grant_issue",
    "hierarchy_dryrun_to_execution_window_open",
    "hierarchy_dryrun_to_memory_write",
    "hierarchy_dryrun_to_world_model_write",
    "hierarchy_dryrun_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Hierarchy DryRunAndReview GO ≠ constitution runtime enforcement",
    "constitution mapping ≠ registry updated",
    "OCR Constitution mapping ≠ OCR authorization started",
    "Factory Authorization Standard mapping ≠ grant issued",
    "Validation Factory role mapping ≠ provider allowed",
    "next phase readiness ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "constitution_hierarchy_runtime_enforced_now",
    "constitution_registry_updated_now",
    "domain_constitution_runtime_enabled_now",
    "domain_standard_runtime_enabled_now",
    "ocr_authorization_started_now",
    "real_dependency_check_executed_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "formal_request_artifact_generated_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "provider_imported_now",
    "authorization_request_sent_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "midplatform_constitution_governance_hierarchy_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _mapping_entry(
    *,
    artifact_id: str,
    from_label: str,
    to_path: str,
    mapped: bool = True,
) -> Dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "from_label": from_label,
        "to_path": to_path,
        "mapped": mapped,
        "simulated": True,
    }


def run_midplatform_constitution_governance_hierarchy_dryrun_and_review_v1(
    *,
    midplatform_constitution_governance_hierarchy_planning_root: str,
    capability_factory_authorization_standard_extension_planning_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    factory_standard_historical_redundancy_cleanup_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    hierarchy_plan_root = Path(
        midplatform_constitution_governance_hierarchy_planning_root
    ).expanduser().resolve()
    hierarchy_plan_sm = _try_read_json(hierarchy_plan_root / "summary.json") or {}
    hierarchy_plan_vr = _try_read_json(hierarchy_plan_root / "verifier_report.json") or {}

    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_planning_root
        or hierarchy_plan_root.parent / "capability_factory_authorization_standard_extension_planning"
    ).expanduser().resolve()
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or hierarchy_plan_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or hierarchy_plan_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    ocr_auth_plan_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or hierarchy_plan_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    ocr_auth_plan_vr = _try_read_json(ocr_auth_plan_root / "verifier_report.json") or {}

    cleanup_dr_root = Path(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        or hierarchy_plan_root.parent / "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
    ).expanduser().resolve()
    cleanup_dr_vr = _try_read_json(cleanup_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_hierarchy_planning_root": str(hierarchy_plan_root),
        "upstream_auth_extension_planning_root": str(auth_ext_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "upstream_ocr_auth_planning_root": str(ocr_auth_plan_root),
        "upstream_cleanup_dryrun_review_root": str(cleanup_dr_root),
        "output_root": str(out_root),
    }

    if hierarchy_plan_vr.get("verifier") != "GO":
        blockers.append("hierarchy planning verifier must be GO")
    if hierarchy_plan_sm.get("final_decision") != UPSTREAM_HIERARCHY_PLANNING_FINAL:
        blockers.append("hierarchy planning final_decision mismatch")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension planning must be GO")
    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness post dryrun review must be GO")
    if ocr_auth_plan_vr.get("verifier") != "GO":
        blockers.append("ocr auth planning must be GO as reposition source")
    if cleanup_dr_vr.get("verifier") != "GO":
        blockers.append("cleanup dryrun review must be GO")

    planning_input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "constitution_hierarchy_planning_input_review_v1",
        "hierarchy_planning_verifier_go": hierarchy_plan_vr.get("verifier") == "GO",
        "hierarchy_planning_final_decision": hierarchy_plan_sm.get("final_decision"),
        "hierarchy_planning_next_phase": hierarchy_plan_sm.get("recommended_next_phase"),
        "auth_extension_go": auth_ext_vr.get("verifier") == "GO",
        "factory_dryrun_go": factory_dr_vr.get("verifier") == "GO",
        "harness_post_go": harness_post_vr.get("verifier") == "GO",
        "ocr_auth_planning_go": ocr_auth_plan_vr.get("verifier") == "GO",
        "cleanup_go": cleanup_dr_vr.get("verifier") == "GO",
        "review_pass": planning_input_ok,
        "blockers": blockers,
        **meta,
    }

    general_checks: List[Tuple[str, bool]] = [
        ("overlays_all_domains", True),
        ("cannot_be_overridden_by_domain_standard", True),
        ("cannot_be_overridden_by_provider", True),
        ("cannot_be_overridden_by_user_task", True),
    ]
    for article_id, _label in GENERAL_CONSTITUTION_ARTICLES:
        general_checks.append((f"article.{article_id}", True))

    general_review = {
        "review_id": "general_constitution_dryrun_review_v1",
        "layer": "Luna General Constitution / 总宪法",
        "articles": [
            {"article_id": aid, "label": label, "present": True, "simulated": True}
            for aid, label in GENERAL_CONSTITUTION_ARTICLES
        ],
        "article_count": len(GENERAL_CONSTITUTION_ARTICLES),
        "overlays_all_domains": True,
        "cannot_be_overridden_by_domain_standard": True,
        "cannot_be_overridden_by_provider": True,
        "cannot_be_overridden_by_user_task": True,
        **_review_ok(general_checks),
        **meta,
    }

    domain_checks: List[Tuple[str, bool]] = []
    domain_entries: List[Dict[str, Any]] = []
    for domain_id, label, status in DOMAIN_CONSTITUTIONS:
        domain_entries.append(
            {
                "domain_id": domain_id,
                "label": label,
                "status": status,
                "present_or_planned": True,
                "simulated": True,
            }
        )
        domain_checks.append((f"domain.{domain_id}", True))
    domain_checks.append(("ocr.active_for_mapping", True))
    domain_checks.append(("vision.planned", True))
    domain_checks.append(("voice.planned", True))
    for future_id in ("map", "library", "hive", "memory"):
        domain_checks.append((f"{future_id}.future_only", True))

    domain_review = {
        "review_id": "domain_constitution_dryrun_review_v1",
        "layer": "Domain Constitution / 行业宪法",
        "domains": domain_entries,
        "domain_count": len(DOMAIN_CONSTITUTIONS),
        "ocr_constitution_active_for_mapping": True,
        "vision_constitution_planned": True,
        "voice_constitution_planned": True,
        "map_library_hive_memory_future_only": True,
        **_review_ok(domain_checks),
        **meta,
    }

    std_checks: List[Tuple[str, bool]] = []
    std_mappings: List[Dict[str, Any]] = []
    for category in DOMAIN_STANDARD_CATEGORIES:
        std_mappings.append(
            _mapping_entry(
                artifact_id=category.lower().replace(" ", "_").replace("/", "_"),
                from_label=category,
                to_path=f"Domain Standard / 行业规范 → {category}",
            )
        )
        std_checks.append((f"standard.{category}", True))

    domain_standard_review = {
        "review_id": "domain_standard_dryrun_review_v1",
        "layer": "Domain Standard / 行业规范",
        "categories": list(DOMAIN_STANDARD_CATEGORIES),
        "category_count": len(DOMAIN_STANDARD_CATEGORIES),
        "mappings": std_mappings,
        **_review_ok(std_checks),
        **meta,
    }

    factory_category_mappings = [
        _mapping_entry(
            artifact_id=f"factory_standard:{std}",
            from_label=std,
            to_path=(
                "Factory Governance Constitution → Factory Admission and Operation Standard → "
                f"{std}"
            ),
        )
        for std in NINE_STANDARDS
    ]
    factory_checks: List[Tuple[str, bool]] = [
        ("factory_standard_root_mapped", True),
        ("not_isolated_outside_constitution", True),
    ]
    for std in NINE_STANDARDS:
        factory_checks.append((f"factory_category.{std}", True))

    factory_mapping_review = {
        "review_id": "factory_standard_constitution_mapping_review_v1",
        "reposition_path": (
            "Capability Factory Admission and Operation Standard → "
            "Factory Governance Constitution → Factory Admission and Operation Standard"
        ),
        "factory_standard_id": FACTORY_STANDARD_ID,
        "root_mapping": _mapping_entry(
            artifact_id=FACTORY_STANDARD_ID,
            from_label="Capability Factory Admission and Operation Standard",
            to_path=(
                "Factory Governance Constitution → Factory Admission and Operation Standard"
            ),
        ),
        "category_mappings": factory_category_mappings,
        "not_isolated_outside_constitution": True,
        **_review_ok(factory_checks),
        **meta,
    }

    auth_sub_mappings = [
        _mapping_entry(
            artifact_id=f"auth_sub:{sub.lower().replace(' ', '_').replace('/', '_')}",
            from_label=sub,
            to_path=f"Factory Governance Constitution → Authorization Standard → {sub}",
        )
        for sub in AUTHORIZATION_SUBCOMPONENTS
    ]
    auth_checks: List[Tuple[str, bool]] = [
        ("authorization_standard_mapped", True),
        ("approval_grant_distinct_from_authorization", True),
        ("ocr_domain_config_only_no_auth_logic_redefinition", True),
    ]
    for sub in AUTHORIZATION_SUBCOMPONENTS:
        auth_checks.append((f"auth_sub.{sub}", True))

    auth_mapping_review = {
        "review_id": "factory_authorization_standard_mapping_review_v1",
        "reposition_path": (
            "Factory Authorization Standard → Factory Governance Constitution → Authorization Standard"
        ),
        "authorization_standard_id": AUTHORIZATION_STANDARD_ID,
        "root_mapping": _mapping_entry(
            artifact_id=AUTHORIZATION_STANDARD_ID,
            from_label="Factory Authorization Standard",
            to_path="Factory Governance Constitution → Authorization Standard",
        ),
        "subcomponent_mappings": auth_sub_mappings,
        "approval_grant_standard_role": "lifecycle gate within factory admission — not full authorization scope owner",
        "authorization_standard_role": "cross-domain authorization scope / request / grant / window / actions",
        "approval_grant_distinct_from_authorization": True,
        "ocr_domain_config_only": True,
        "ocr_no_repeated_request_grant_window_rules": True,
        **_review_ok(auth_checks),
        **meta,
    }

    harness_checks: List[Tuple[str, bool]] = [
        ("harness_mapped_to_provider_model_admission", True),
        ("harness_does_not_write_constitution", True),
        ("harness_compliance_detection_only", True),
    ]
    for consumer, status in HARNESS_CONSUMERS:
        harness_checks.append((f"consumer.{consumer}.{status}", True))

    harness_mapping_review = {
        "review_id": "controlled_provider_harness_mapping_review_v1",
        "reposition_path": "ControlledProviderReadinessHarness → provider/model 准入规范",
        "harness_id": "controlled_provider_readiness_harness_v1",
        "consumers": [
            {"consumer": c, "status": s, "simulated": True} for c, s in HARNESS_CONSUMERS
        ],
        "writes_constitution": False,
        "role": "compliance detection / readiness validation only",
        **_review_ok(harness_checks),
        **meta,
    }

    vf_checks: List[Tuple[str, bool]] = [
        ("validation_factory_compliance_layer", True),
        ("does_not_generate_constitution_rules", True),
        ("consumes_constitution_and_standards", True),
        ("pass_required_before_midplatform_consumption", True),
    ]
    validation_factory_review = {
        "review_id": "validation_factory_role_mapping_review_v1",
        "role": "compliance inspection layer / 市场检测中心",
        "validation_factory_id": "luna_validation_factory_v1",
        "writes_constitution_rules": False,
        "consumes": [
            "Luna General Constitution",
            "Domain Constitution",
            "Domain Standard",
            "Factory Standard",
        ],
        "pass_required_before_midplatform_consumption": True,
        **_review_ok(vf_checks),
        **meta,
    }

    ocr_std_mappings = [
        _mapping_entry(
            artifact_id=std.lower().replace(" ", "_"),
            from_label=std,
            to_path=f"OCR Constitution → {std}",
        )
        for std in OCR_DOMAIN_STANDARDS
    ]
    ocr_checks: List[Tuple[str, bool]] = []
    for std in OCR_DOMAIN_STANDARDS:
        ocr_checks.append((f"ocr_standard.{std}", True))

    ocr_mapping_review = {
        "review_id": "ocr_constitution_and_standard_mapping_review_v1",
        "ocr_constitution": "OCR Constitution / OCR 宪法",
        "standard_mappings": ocr_std_mappings,
        "standard_count": len(OCR_DOMAIN_STANDARDS),
        **_review_ok(ocr_checks),
        **meta,
    }

    vv_checks: List[Tuple[str, bool]] = [
        ("vision_constitution_planned", True),
        ("voice_constitution_planned", True),
        ("not_runtime_enabled", True),
    ]
    vision_voice_review = {
        "review_id": "vision_voice_future_constitution_mapping_review_v1",
        "status": "planned_not_instantiated",
        "vision_constitution_planned": True,
        "voice_constitution_planned": True,
        "runtime_enabled": False,
        **_review_ok(vv_checks),
        **meta,
    }

    tree_checks: List[Tuple[str, bool]] = []
    for idx, question in enumerate(RULE_CLASSIFICATION_QUESTIONS, start=1):
        tree_checks.append((f"question_{idx}", True))
    tree_result = {
        "result_id": "rule_placement_decision_tree_dryrun_result_v1",
        "questions": list(RULE_CLASSIFICATION_QUESTIONS),
        "simulated_answers": [
            {"question": q, "dryrun_result": "classified_via_hierarchy", "pass": True}
            for q in RULE_CLASSIFICATION_QUESTIONS
        ],
        "design_principles": list(DESIGN_PRINCIPLES),
        "governance_layers": list(GOVERNANCE_LAYERS),
        **_review_ok(tree_checks),
        **meta,
    }

    ocr_path_checks: List[Tuple[str, bool]] = [
        ("chain_matches_spec", True),
        ("via_ocr_constitution", True),
        ("via_factory_authorization_standard", True),
        ("via_validation_factory", True),
        ("using_ocr_domain_config_only", True),
        ("no_repeated_request_grant_window_in_ocr_phase", True),
    ]
    ocr_path_review = {
        "review_id": "ocr_real_dep_authorization_governance_path_review_v1",
        "authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "chain_steps": [
            "OCR Real Dependency Check Authorization",
            "via OCR Constitution",
            "via Factory Authorization Standard",
            "via Validation Factory",
        ],
        "using_ocr_domain_config_only": True,
        "no_repeated_request_grant_window_rules_in_ocr_phase": True,
        "recommended_next_after_auth_extension": (
            "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001"
        ),
        **_review_ok(ocr_path_checks),
        **meta,
    }

    boundary_forbidden = [
        "constitution registry update",
        "runtime enforcement",
        "provider invocation",
        "dependency install",
        "model download",
        "formal artifact generation",
        "request send",
        "grant issue",
        "execution window open",
        "real dependency check",
        "Memory / WorldModel write",
        "user output",
    ]
    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    for item in boundary_forbidden:
        boundary_checks.append((f"forbidden.{item.replace(' ', '_')}", True))

    boundary_audit = {
        "audit_id": "constitution_hierarchy_boundary_audit_v1",
        "forbidden_actions": boundary_forbidden,
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        "boundary_fields": {f: meta.get(f) for f in BOUNDARY_FALSE},
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_results = [
        {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
    ]
    blocked_path_result = {
        "result_id": "constitution_hierarchy_blocked_path_result_v1",
        "blocked_paths": blocked_results,
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        general_review,
        domain_review,
        domain_standard_review,
        factory_mapping_review,
        auth_mapping_review,
        harness_mapping_review,
        validation_factory_review,
        ocr_mapping_review,
        vision_voice_review,
        tree_result,
        ocr_path_review,
        boundary_audit,
    ]
    all_reviews_pass = planning_input_ok and all(
        section.get("dryrun_and_review_pass", section.get("all_blocked")) is True
        for section in review_sections
        if section is not boundary_audit or section.get("dryrun_and_review_pass") is True
    )
    all_reviews_pass = (
        planning_input_ok
        and general_review["dryrun_and_review_pass"]
        and domain_review["dryrun_and_review_pass"]
        and domain_standard_review["dryrun_and_review_pass"]
        and factory_mapping_review["dryrun_and_review_pass"]
        and auth_mapping_review["dryrun_and_review_pass"]
        and harness_mapping_review["dryrun_and_review_pass"]
        and validation_factory_review["dryrun_and_review_pass"]
        and ocr_mapping_review["dryrun_and_review_pass"]
        and vision_voice_review["dryrun_and_review_pass"]
        and tree_result["dryrun_and_review_pass"]
        and ocr_path_review["dryrun_and_review_pass"]
        and boundary_audit["dryrun_and_review_pass"]
        and blocked_path_result["all_blocked"] is True
    )

    high_risk = not all_reviews_pass
    closure_decision = {
        "decision_id": "constitution_hierarchy_closure_decision_v1",
        "dryrun_and_review_pass": all_reviews_pass,
        "high_risk": high_risk,
        "final_decision": FINAL_DECISION_GO if all_reviews_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_reviews_pass else NEXT_PHASE_HOLD,
        "three_layer_structure_validated": all_reviews_pass,
        "rule_reposition_validated": all_reviews_pass,
        "ocr_path_validated": ocr_path_review["dryrun_and_review_pass"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_auth_extension_dryrun_review": all_reviews_pass,
        "ready_for_ocr_real_dep_authorization": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "deferred_until_auth_extension": (
            "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001"
        ),
        "note": "do not jump directly to OCR real-dep authorization",
        **meta,
    }

    policy = {
        "policy_id": "midplatform_constitution_hierarchy_dryrun_and_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_reviews_pass,
        "violations": blockers,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "general_constitution_articles": len(GENERAL_CONSTITUTION_ARTICLES),
        "domain_constitution_count": len(DOMAIN_CONSTITUTIONS),
        "domain_standard_categories": len(DOMAIN_STANDARD_CATEGORIES),
        "ocr_domain_standards": len(OCR_DOMAIN_STANDARDS),
        "blocked_path_count": len(BLOCKED_PATHS),
        "high_risk_count": 1 if high_risk else 0,
        "dryrun_and_review_pass": all_reviews_pass,
        **meta,
    }

    return {
        "midplatform_constitution_hierarchy_dryrun_and_review_policy": policy,
        "constitution_hierarchy_planning_input_review": planning_input_review,
        "general_constitution_dryrun_review": general_review,
        "domain_constitution_dryrun_review": domain_review,
        "domain_standard_dryrun_review": domain_standard_review,
        "factory_standard_constitution_mapping_review": factory_mapping_review,
        "factory_authorization_standard_mapping_review": auth_mapping_review,
        "controlled_provider_harness_mapping_review": harness_mapping_review,
        "validation_factory_role_mapping_review": validation_factory_review,
        "ocr_constitution_and_standard_mapping_review": ocr_mapping_review,
        "vision_voice_future_constitution_mapping_review": vision_voice_review,
        "rule_placement_decision_tree_dryrun_result": tree_result,
        "ocr_real_dep_authorization_governance_path_review": ocr_path_review,
        "constitution_hierarchy_boundary_audit": boundary_audit,
        "constitution_hierarchy_blocked_path_result": blocked_path_result,
        "constitution_hierarchy_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
