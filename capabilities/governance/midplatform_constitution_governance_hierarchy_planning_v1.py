# -*- coding: utf-8 -*-
"""Midplatform Constitution Governance Hierarchy Planning v1 — 国法→行业法→家规归位."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DR_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    FINAL_DECISION_GO as AUTH_EXT_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as AUTH_EXT_PLANNING_NEXT,
    TEN_STANDARDS,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL_GO,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CLEANUP_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    FINAL_DECISION_GO as OCR_AUTH_PLANNING_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Constitution-Governance-Hierarchy-Planning-v1-001"
SCOPE = "midplatform_constitution_governance_hierarchy_planning_only"
SOURCE_CHAIN = "midplatform_constitution_governance_hierarchy_planning_v1"

UPSTREAM_AUTH_EXT_FINAL = AUTH_EXT_PLANNING_FINAL_GO
UPSTREAM_AUTH_EXT_NEXT = AUTH_EXT_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_HIERARCHY_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_HIERARCHY_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Constitution-Governance-Hierarchy-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Constitution-Governance-Hierarchy-Issue-Review-v1-001"

HIERARCHY_ANALOGY = "国法 → 行业法 → 家规 / 操作规程"

GOVERNANCE_LAYERS: Tuple[str, ...] = (
    "Luna Constitution Layer / 中台宪法管理层",
    "Luna General Constitution / 总宪法",
    "Domain Constitution / 行业宪法",
    "Domain Standard / 行业规范",
)

LUNA_GENERAL_CONSTITUTION_ARTICLES: Tuple[str, ...] = (
    "安全宪法",
    "生存宪法",
    "隐私宪法",
    "事实准入宪法",
    "用户输出宪法",
    "中台运行基本法",
)

DOMAIN_CONSTITUTIONS: Tuple[str, ...] = (
    "Vision Constitution / 视觉宪法",
    "OCR Constitution / OCR 宪法",
    "Voice Constitution / 语音宪法",
    "Emotion Constitution / 情感宪法",
    "Memory Constitution / 记忆宪法",
    "Map Constitution / 地图宪法",
    "Library Constitution / 图书馆宪法",
    "Hive Constitution / 蜂巢宪法",
)

DOMAIN_STANDARD_CATEGORIES: Tuple[str, ...] = (
    "输入规范",
    "输出规范",
    "候选规范",
    "证据规范",
    "授权规范",
    "模块使用规范",
    "provider / model 准入规范",
    "上下游传输规范",
    "rollback / fallback 规范",
    "用户输出规范",
)

DESIGN_PRINCIPLES: Tuple[str, ...] = (
    "最高层：决定什么绝对不能做",
    "行业宪法：决定某类能力域必须遵守什么基本原则",
    "行业规范：决定具体模块、模型、provider、输入输出、授权、证据怎么执行",
    "Validation Factory：负责检查是否合规",
    "Midplatform：负责按合规结果组装、调度、输出",
)

RULE_CLASSIFICATION_QUESTIONS: Tuple[str, ...] = (
    "它属于哪一层宪法？",
    "它属于哪个行业宪法？",
    "它属于哪条行业规范？",
    "是否应写进 phase 而不是 Standard/Constitution？",
)

DEFERRED_PHASES: Tuple[str, ...] = (
    "Phase-Capability-Factory-Authorization-Standard-Extension-DryRunAndReview-v1-001",
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001",
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-DryRunAndReview-v1-001",
)

OCR_REAL_DEP_AUTHORIZATION_CHAIN = (
    "OCR Real Dependency Check Authorization "
    "via OCR Constitution "
    "via Factory Authorization Standard "
    "via Validation Factory"
)

NON_CLAIMS: Tuple[str, ...] = (
    "Hierarchy Planning GO ≠ constitution runtime enforced",
    "reposition plan ≠ historical artifacts deleted",
    "reposition plan ≠ phase verdicts invalidated",
    "deferred phases ≠ phases skipped",
    "OCR Constitution planned ≠ real dependency check executed",
    "hierarchy defined ≠ Factory Authorization Extension DryRun executed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "constitution_runtime_enforced_now",
    "hierarchy_reposition_executed_now",
    "historical_rule_deleted_now",
    "phase_verdict_invalidated_now",
    "real_dependency_check_executed_now",
    "authorization_grant_issued_now",
    "provider_selection_finalized_now",
    "provider_imported_now",
    "provider_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "midplatform_constitution_governance_hierarchy_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _reposition_entry(
    *,
    artifact_id: str,
    artifact_type: str,
    current_label: str,
    layer: str,
    parent: str,
    repositioned_as: str,
    notes: str = "",
) -> Dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "current_label": current_label,
        "layer": layer,
        "parent": parent,
        "repositioned_as": repositioned_as,
        "physical_delete": False,
        "verdict_preserved": True,
        "notes": notes,
    }


def run_midplatform_constitution_governance_hierarchy_planning_v1(
    *,
    capability_factory_authorization_standard_extension_planning_root: str,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: Optional[str] = None,
    factory_standard_historical_redundancy_cleanup_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_planning_root
    ).expanduser().resolve()
    auth_ext_sm = _try_read_json(auth_ext_root / "summary.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or auth_ext_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        or auth_ext_root.parent / "compressed_ocr_authorization_lifecycle_dryrun_and_review"
    ).expanduser().resolve()
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}

    cleanup_dr_root = Path(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        or auth_ext_root.parent / "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
    ).expanduser().resolve()
    cleanup_dr_vr = _try_read_json(cleanup_dr_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or auth_ext_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    ocr_auth_plan_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or auth_ext_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    ocr_auth_plan_vr = _try_read_json(ocr_auth_plan_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_auth_extension_planning_root": str(auth_ext_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_cleanup_dryrun_review_root": str(cleanup_dr_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "upstream_ocr_auth_planning_root": str(ocr_auth_plan_root),
        "output_root": str(out_root),
    }

    if auth_ext_vr.get("verifier") != "GO" or auth_ext_vr.get("passed") is not True:
        blockers.append("authorization standard extension planning must be GO")
    if auth_ext_sm.get("final_decision") != UPSTREAM_AUTH_EXT_FINAL:
        blockers.append("auth extension final_decision mismatch")
    if auth_ext_sm.get("recommended_next_phase") != UPSTREAM_AUTH_EXT_NEXT:
        blockers.append("auth extension recommended_next_phase mismatch")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if lifecycle_dr_vr.get("verifier") != "GO":
        blockers.append("compressed lifecycle dryrun review must be GO")
    if cleanup_dr_vr.get("verifier") != "GO":
        blockers.append("cleanup dryrun review must be GO")
    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration must be GO")
    if ocr_auth_plan_vr.get("verifier") != "GO":
        blockers.append("ocr auth planning must exist as reposition source")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    upstream_review = {
        "review_id": "upstream_factory_standards_input_review_v1",
        "auth_extension_go": auth_ext_vr.get("verifier") == "GO",
        "factory_dryrun_go": factory_dr_vr.get("verifier") == "GO",
        "lifecycle_go": lifecycle_dr_vr.get("verifier") == "GO",
        "cleanup_go": cleanup_dr_vr.get("verifier") == "GO",
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    layer_outline = {
        "outline_id": "luna_constitution_layer_outline_v1",
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "layers": list(GOVERNANCE_LAYERS),
        "decision_rule": "所有规则先问属于哪一层宪法 / 哪个行业宪法 / 哪条行业规范，再决定是否写进 phase",
        **meta,
    }

    general_constitution = {
        "plan_id": "luna_general_constitution_plan_v1",
        "layer": "Luna General Constitution / 总宪法",
        "role": "决定什么绝对不能做",
        "articles": list(LUNA_GENERAL_CONSTITUTION_ARTICLES),
        "article_count": len(LUNA_GENERAL_CONSTITUTION_ARTICLES),
        **meta,
    }

    domain_constitution_registry = {
        "registry_id": "domain_constitution_registry_plan_v1",
        "layer": "Domain Constitution / 行业宪法",
        "role": "决定能力域必须遵守的基本原则",
        "domains": list(DOMAIN_CONSTITUTIONS),
        "domain_count": len(DOMAIN_CONSTITUTIONS),
        "future_domains_note": "Vision / Voice constitution planned — not yet fully instantiated",
        **meta,
    }

    domain_standard_registry = {
        "registry_id": "domain_standard_registry_plan_v1",
        "layer": "Domain Standard / 行业规范",
        "role": "决定模块、模型、provider、输入输出、授权、证据如何执行",
        "categories": list(DOMAIN_STANDARD_CATEGORIES),
        "category_count": len(DOMAIN_STANDARD_CATEGORIES),
        **meta,
    }

    factory_constitution_reposition = {
        "plan_id": "capability_factory_constitution_reposition_plan_v1",
        "reposition_path": (
            "中台宪法管理层 → 工厂治理宪法 / Capability Factory Constitution "
            "→ 工厂准入与运行规范"
        ),
        "entries": [
            _reposition_entry(
                artifact_id=FACTORY_STANDARD_ID,
                artifact_type="factory_admission_and_operation_standard",
                current_label="Capability Factory Admission and Operation Standard",
                layer="Domain Standard / 行业规范",
                parent="Capability Factory Constitution / 工厂治理宪法",
                repositioned_as="工厂准入与运行规范（九类标准 + 压缩 lifecycle）",
                notes=f"ten standards with pending {AUTHORIZATION_STANDARD_ID}",
            ),
            *[
                _reposition_entry(
                    artifact_id=f"factory_standard:{std}",
                    artifact_type="factory_standard_category",
                    current_label=std,
                    layer="Domain Standard / 行业规范",
                    parent="Capability Factory Constitution",
                    repositioned_as=f"工厂准入与运行规范 / {std}",
                )
                for std in TEN_STANDARDS
            ],
        ],
        **meta,
    }

    auth_standard_reposition = {
        "plan_id": "factory_authorization_standard_reposition_plan_v1",
        "reposition_path": (
            "中台宪法管理层 → 工厂治理宪法 → Factory Authorization Standard"
        ),
        "entries": [
            _reposition_entry(
                artifact_id=AUTHORIZATION_STANDARD_ID,
                artifact_type="factory_authorization_standard",
                current_label="Factory Authorization Standard",
                layer="Domain Standard / 行业规范",
                parent="Capability Factory Constitution / 工厂治理宪法",
                repositioned_as="授权规范（工厂级）",
                notes="not isolated OCR phase rules",
            ),
        ],
        "supersedes_duplicate_auth_in_ocr_phases": True,
        **meta,
    }

    harness_reposition = {
        "plan_id": "controlled_provider_readiness_harness_reposition_plan_v1",
        "reposition_path": (
            "中台宪法管理层 → 工厂治理宪法 → provider / model 准入规范"
        ),
        "entries": [
            _reposition_entry(
                artifact_id="controlled_provider_readiness_harness_v1",
                artifact_type="factory_module",
                current_label="ControlledProviderReadinessHarness",
                layer="Domain Standard / 行业规范",
                parent="Capability Factory Constitution",
                repositioned_as="provider / model 准入规范（工厂模块）",
            ),
        ],
        **meta,
    }

    validation_factory_reposition = {
        "plan_id": "validation_factory_reposition_plan_v1",
        "reposition_path": "中台宪法管理层 → Validation Factory → 合规检查层",
        "role": "负责检查是否合规 — not rule author",
        "entries": [
            _reposition_entry(
                artifact_id="luna_validation_factory_v1",
                artifact_type="validation_factory",
                current_label="Luna Validation Factory",
                layer="Midplatform compliance layer",
                parent="Luna Constitution Layer",
                repositioned_as="合规检查 — 不重复写字段级规则",
            ),
        ],
        **meta,
    }

    ocr_reposition = {
        "plan_id": "ocr_domain_constitution_reposition_plan_v1",
        "reposition_path": "中台宪法管理层 → OCR Constitution → OCR Domain Standards",
        "ocr_constitution": "OCR Constitution / OCR 宪法",
        "entries": [
            _reposition_entry(
                artifact_id="ocr_input_standard",
                artifact_type="domain_standard",
                current_label="OCR input rules scattered in phases",
                layer="Domain Standard / 行业规范",
                parent="OCR Constitution / OCR 宪法",
                repositioned_as="OCR Input Standard / OCR 输入规范",
            ),
            _reposition_entry(
                artifact_id="ocr_output_standard",
                artifact_type="domain_standard",
                current_label="OCR output / user-facing rules",
                layer="Domain Standard / 行业规范",
                parent="OCR Constitution",
                repositioned_as="OCR Output Standard / OCR 输出规范",
            ),
            _reposition_entry(
                artifact_id="ocr_evidence_standard",
                artifact_type="domain_standard",
                current_label="OCR evidence requirements",
                layer="Domain Standard / 行业规范",
                parent="OCR Constitution",
                repositioned_as="OCR Evidence Standard / OCR 证据规范",
            ),
            _reposition_entry(
                artifact_id="ocr_provider_usage_standard",
                artifact_type="domain_standard",
                current_label="OCR provider selection / readiness",
                layer="Domain Standard / 行业规范",
                parent="OCR Constitution",
                repositioned_as="OCR Provider Usage Standard / OCR provider 使用规范",
            ),
            _reposition_entry(
                artifact_id="ocr_authorization_standard",
                artifact_type="domain_standard",
                current_label="OCR authorization phase rules",
                layer="Domain Standard / 行业规范",
                parent="OCR Constitution",
                repositioned_as="OCR Authorization Standard / OCR 授权规范",
                notes="references Factory Authorization Standard + domain_config",
            ),
            _reposition_entry(
                artifact_id=OCR_AUTH_PLANNING_FINAL_GO,
                artifact_type="phase_evidence",
                current_label="OCR Real-Dep Authorization Planning",
                layer="phase_evidence",
                parent="OCR Authorization Standard",
                repositioned_as="absorption source — not standalone auth standard",
            ),
        ],
        "future_authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        **meta,
    }

    vision_voice_reposition = {
        "plan_id": "vision_voice_future_constitution_reposition_plan_v1",
        "status": "planned_not_instantiated",
        "entries": [
            _reposition_entry(
                artifact_id="vision_constitution",
                artifact_type="domain_constitution",
                current_label="Vision harness adoption evidence",
                layer="Domain Constitution / 行业宪法",
                parent="Luna Constitution Layer",
                repositioned_as="Vision Constitution / 视觉宪法（future）",
            ),
            _reposition_entry(
                artifact_id="voice_constitution",
                artifact_type="domain_constitution",
                current_label="Voice harness adoption evidence",
                layer="Domain Constitution / 行业宪法",
                parent="Luna Constitution Layer",
                repositioned_as="Voice Constitution / 语音宪法（future）",
            ),
        ],
        **meta,
    }

    decision_tree = {
        "tree_id": "governance_hierarchy_decision_tree_v1",
        "questions": list(RULE_CLASSIFICATION_QUESTIONS),
        "flow": [
            "1. Is it absolutely forbidden at platform level? → Luna General Constitution",
            "2. Is it domain principle? → Domain Constitution",
            "3. Is it module/provider/auth/evidence execution detail? → Domain Standard",
            "4. Is it factory-wide cross-domain? → Capability Factory Constitution → Domain Standard",
            "5. Is it compliance check only? → Validation Factory",
            "6. Is it assembly/scheduling? → Midplatform",
            "7. Only if none above → consider phase-local rule (minimize)",
        ],
        "design_principles": list(DESIGN_PRINCIPLES),
        **meta,
    }

    fragmentation_policy = {
        "policy_id": "rule_fragmentation_prevention_policy_v1",
        "forbidden_patterns": [
            "redefine authorization in each OCR phase",
            "duplicate request/grant/window in domain phases",
            "write provider readiness rules outside harness + constitution",
            "let single phase own cross-cutting boundary/evidence rules",
        ],
        "preferred_patterns": [
            "reference Factory Authorization Standard + domain_config",
            "reference OCR Constitution + OCR Domain Standards",
            "use Validation Factory for compliance",
            "use phase only for lifecycle simulation and evidence",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_phases_register_v1",
        "reason": "await hierarchy DryRunAndReview before downstream auth extension",
        "deferred_phases": [
            {
                "phase_id": p,
                "status": "deferred_until_hierarchy_dryrun_review",
                "note": "not skipped",
            }
            for p in DEFERRED_PHASES
        ],
        **meta,
    }

    dryrun_plan = {
        "plan_id": "hierarchy_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "validate reposition matrix for all major artifacts",
            "simulate rule classification decision tree",
            "verify deferred phases remain blocked",
            "no physical delete or verdict invalidation",
        ],
        **meta,
    }

    planning_decision = {
        "decision_id": "hierarchy_planning_decision_v1",
        "planning_pass": boundary_ok,
        "hierarchy_defined": boundary_ok,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "ocr_real_dep_authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_constitution_governance_hierarchy_planning_policy_v1",
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "general_constitution_articles": len(LUNA_GENERAL_CONSTITUTION_ARTICLES),
        "domain_constitution_count": len(DOMAIN_CONSTITUTIONS),
        "domain_standard_categories": len(DOMAIN_STANDARD_CATEGORIES),
        "deferred_phase_count": len(DEFERRED_PHASES),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "midplatform_constitution_governance_hierarchy_planning_policy": policy,
        "upstream_factory_standards_input_review": upstream_review,
        "luna_constitution_layer_outline": layer_outline,
        "luna_general_constitution_plan": general_constitution,
        "domain_constitution_registry_plan": domain_constitution_registry,
        "domain_standard_registry_plan": domain_standard_registry,
        "capability_factory_constitution_reposition_plan": factory_constitution_reposition,
        "factory_authorization_standard_reposition_plan": auth_standard_reposition,
        "controlled_provider_readiness_harness_reposition_plan": harness_reposition,
        "validation_factory_reposition_plan": validation_factory_reposition,
        "ocr_domain_constitution_reposition_plan": ocr_reposition,
        "vision_voice_future_constitution_reposition_plan": vision_voice_reposition,
        "governance_hierarchy_decision_tree": decision_tree,
        "rule_fragmentation_prevention_policy": fragmentation_policy,
        "deferred_phases_register": deferred_register,
        "hierarchy_dryrun_plan": dryrun_plan,
        "hierarchy_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
