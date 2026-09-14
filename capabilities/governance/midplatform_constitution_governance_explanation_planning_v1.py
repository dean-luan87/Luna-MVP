# -*- coding: utf-8 -*-
"""Midplatform Constitution Governance Explanation Planning v1 — 宪法治理说明."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL_GO,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    DOMAIN_CONSTITUTIONS,
    DOMAIN_STANDARD_CATEGORIES,
    GOVERNANCE_LAYERS,
    HIERARCHY_ANALOGY,
    LUNA_GENERAL_CONSTITUTION_ARTICLES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Constitution-Governance-Explanation-Planning-v1-001"
SCOPE = "constitution_governance_explanation_planning_only"
SOURCE_CHAIN = "midplatform_constitution_governance_explanation_planning_v1"

UPSTREAM_HIERARCHY_DR_FINAL = HIERARCHY_DR_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_EXPLANATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_EXPLANATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Constitution-Governance-Explanation-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Constitution-Governance-Explanation-Issue-Review-v1-001"

GOVERNANCE_ANALOGY = "国法 → 行业法 → 家规 / 操作规程 → 企业法 / 岗位手册 → 临时执行细则"

LAYER_PRIORITY: Tuple[str, ...] = (
    "Luna General Constitution",
    "Domain Constitution",
    "Domain Standard",
    "Factory Standard / Module Contract",
    "Phase-local Rule",
    "User instruction / Task instruction",
)

CONSTITUTION_LAYERS_EXPLAINED: Tuple[Dict[str, str], ...] = (
    {
        "layer_id": "luna_general_constitution",
        "label": "Luna General Constitution / 总宪法",
        "role": "最高层，管理 Luna 的安全、生存、隐私、事实准入、用户输出、中台基本运行规则",
        "analogy": "国法 / 总宪法",
    },
    {
        "layer_id": "domain_constitution",
        "label": "Domain Constitution / 行业宪法",
        "role": "管理 Vision、OCR、Voice、Emotion、Memory、Map、Library、Hive 等能力域的基本规则",
        "analogy": "行业法 / 部门基本法",
    },
    {
        "layer_id": "domain_standard",
        "label": "Domain Standard / 行业规范",
        "role": "管理某行业宪法下的输入、输出、候选、证据、授权、provider 使用、rollback、传输等执行规则",
        "analogy": "行业规范 / 操作规章",
    },
    {
        "layer_id": "factory_module_contract",
        "label": "Factory / Module / Provider Contract / 工厂与模块规章",
        "role": "管理具体模型、provider、runtime、工具、模块、工厂流水线、岗位职责、上下游交接",
        "analogy": "企业法 / 工厂规章 / 岗位手册",
    },
    {
        "layer_id": "phase_local_rule",
        "label": "Phase-local Rule / 临时执行细则",
        "role": "仅服务某个 phase 的局部验证，不得覆盖上位宪法与行业规范",
        "analogy": "临时执行细则",
    },
)

GENERAL_JURISDICTION: Tuple[str, ...] = (
    "safety",
    "survival",
    "privacy",
    "fact admission",
    "user output",
    "midplatform operation",
    "emergency degradation",
    "irreversible action prevention",
)

DOMAIN_JURISDICTION: Tuple[str, ...] = (
    "domain fundamental principles",
    "allowed/forbidden capability boundaries",
    "cross-domain interface boundaries",
    "evidence/candidate/authorization/output floor",
)

DOMAIN_STANDARD_JURISDICTION: Tuple[str, ...] = tuple(DOMAIN_STANDARD_CATEGORIES)

CONFLICT_RULES: Tuple[str, ...] = (
    "上位宪法优先于下位规则",
    "General Constitution 高于所有 Domain Constitution",
    "Domain Constitution 高于 Domain Standard",
    "Domain Standard 高于 module/provider contract",
    "module/provider contract 高于 phase-local rule",
    "user instruction / task instruction 不能覆盖任何宪法底线",
    "safety / survival / privacy / fact admission / user output 不可被 provider、task、domain、user 偏好覆盖",
    "规则冲突时默认选择更保守、更安全、更可审计、更可回滚的路径",
)

AMENDMENT_TRIGGERS: Tuple[str, ...] = (
    "repeated failure pattern",
    "safety incident",
    "privacy incident",
    "fact admission error",
    "provider boundary violation",
    "user output violation",
    "hardware degradation / lifespan risk",
    "environment change",
    "law/social rule change",
    "user long-term preference conflict",
    "survival mechanism pressure",
    "system robustness issue",
)

AMENDMENT_WORKFLOW: Tuple[str, ...] = (
    "issue detected",
    "evidence collected",
    "constitution_amendment_candidate generated",
    "impact analysis",
    "conflict analysis",
    "rollback plan",
    "Hive-side review",
    "owner/operator review if needed",
    "versioned approval",
    "staged rollout",
    "monitoring",
    "rollback if violation",
)

VIOLATION_LEVELS: Tuple[str, ...] = (
    "L0 warning",
    "L1 soft block",
    "L2 hard block",
    "L3 module quarantine",
    "L4 provider freeze",
    "L5 system degradation / safe mode",
    "L6 Hive escalation",
    "L7 owner/operator review required",
)

VIOLATION_TYPES: Tuple[str, ...] = (
    "safety violation",
    "privacy violation",
    "fact admission violation",
    "user output violation",
    "authorization violation",
    "provider boundary violation",
    "evidence chain violation",
    "memory/worldmodel write violation",
    "constitution override attempt",
    "Hive authority bypass attempt",
)

VIOLATION_ACTIONS: Tuple[str, ...] = (
    "block",
    "suppress output",
    "degrade",
    "quarantine module",
    "freeze provider",
    "revoke candidate",
    "require owner review",
    "generate violation report",
    "escalate to Hive",
    "rollback",
    "enter safe mode",
)

VIOLATION_EVIDENCE_FIELDS: Tuple[str, ...] = (
    "violation_id",
    "violated_constitution_ref",
    "source_module",
    "source_provider",
    "triggering_event",
    "evidence_ref",
    "severity",
    "action_taken",
    "rollback_status",
    "hive_report_required",
    "owner_review_required",
)

AMENDMENT_CANDIDATE_STATES: Tuple[str, ...] = (
    "issue_detected",
    "amendment_candidate_generated",
    "evidence_pack_ready",
    "impact_analysis_ready",
    "conflict_check_ready",
    "hive_review_pending",
    "owner_review_pending_later",
    "approved_later",
    "rejected_later",
    "staged_rollout_later",
    "active_later",
    "rollback_later",
    "closed",
)

DECISION_TREE_QUESTIONS: Tuple[str, ...] = (
    "是否属于 General Constitution？",
    "是否属于 Domain Constitution？",
    "是否属于 Domain Standard？",
    "是否属于 Factory / Module / Provider Contract？",
    "是否只是 Phase-local Rule？",
    "是否可能影响 safety / survival / privacy / fact / user output？",
    "是否需要 Hive review？",
    "是否允许 personalization overlay？",
    "是否存在上位规则冲突？",
    "是否需要 violation alarm / penalty？",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Explanation Planning GO ≠ constitution registry updated",
    "explanation defined ≠ constitution runtime enforced",
    "amendment logic defined ≠ amendment committed",
    "Hive authority rule defined ≠ Hive update executed",
    "violation penalty rule defined ≠ penalty executed now",
    "Explanation DryRunAndReview next ≠ OCR real-dep authorization allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "constitution_registry_updated_now",
    "constitution_runtime_enforced_now",
    "constitution_amendment_committed_now",
    "hive_constitution_update_requested_now",
    "local_constitution_override_now",
    "personalized_constitution_generated_now",
    "ocr_authorization_started_now",
    "grant_issued_now",
    "real_dependency_check_executed_now",
    "provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "amendment_candidate_generated_now",
    "hive_review_submitted_now",
    "approved_now",
    "active_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "constitution_governance_explanation_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "hierarchy_analogy": HIERARCHY_ANALOGY,
        "governance_analogy": GOVERNANCE_ANALOGY,
        "ocr_real_dep_authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["local_auto_amendment_allowed"] = False
    meta["hive_review_required"] = True
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_constitution_governance_explanation_planning_v1(
    *,
    midplatform_constitution_governance_hierarchy_dryrun_and_review_root: str,
    midplatform_constitution_governance_hierarchy_planning_root: Optional[str] = None,
    capability_factory_authorization_standard_extension_planning_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    hierarchy_dr_root = Path(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root
    ).expanduser().resolve()
    hierarchy_dr_sm = _try_read_json(hierarchy_dr_root / "summary.json") or {}
    hierarchy_dr_vr = _try_read_json(hierarchy_dr_root / "verifier_report.json") or {}

    hierarchy_plan_root = Path(
        midplatform_constitution_governance_hierarchy_planning_root
        or hierarchy_dr_root.parent / "midplatform_constitution_governance_hierarchy_planning"
    ).expanduser().resolve()
    hierarchy_plan_vr = _try_read_json(hierarchy_plan_root / "verifier_report.json") or {}

    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_planning_root
        or hierarchy_dr_root.parent / "capability_factory_authorization_standard_extension_planning"
    ).expanduser().resolve()
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or hierarchy_dr_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_hierarchy_dryrun_review_root": str(hierarchy_dr_root),
        "upstream_hierarchy_planning_root": str(hierarchy_plan_root),
        "upstream_auth_extension_planning_root": str(auth_ext_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "output_root": str(out_root),
    }

    if hierarchy_dr_vr.get("verifier") != "GO":
        blockers.append("hierarchy dryrun review verifier must be GO")
    if hierarchy_dr_sm.get("final_decision") != UPSTREAM_HIERARCHY_DR_FINAL:
        blockers.append("hierarchy dryrun final_decision mismatch")
    if hierarchy_dr_sm.get("dryrun_and_review_pass") is not True:
        blockers.append("hierarchy dryrun_and_review_pass must be true")
    if hierarchy_plan_vr.get("verifier") != "GO":
        blockers.append("hierarchy planning must be GO")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension planning should be GO for context")
    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    hierarchy_input_review = {
        "review_id": "constitution_hierarchy_input_review_v1",
        "hierarchy_dryrun_verifier_go": hierarchy_dr_vr.get("verifier") == "GO",
        "hierarchy_dryrun_final_decision": hierarchy_dr_sm.get("final_decision"),
        "three_layer_validated": hierarchy_dr_sm.get("dryrun_and_review_pass") is True,
        "validation_factory_compliance_only": True,
        "ocr_real_dep_path": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    layer_relationship = {
        "explanation_id": "constitution_layer_relationship_explanation_v1",
        "governance_analogy": GOVERNANCE_ANALOGY,
        "core_idea": (
            "宪法不是死规则，而是 Luna 的生存治理系统；"
            "类比社会治理：国法 → 行业法 → 家规 → 企业法 → 临时细则"
        ),
        "layers": list(CONSTITUTION_LAYERS_EXPLAINED),
        "layer_priority": list(LAYER_PRIORITY),
        "general_constitution_articles": list(LUNA_GENERAL_CONSTITUTION_ARTICLES),
        "domain_constitutions": list(DOMAIN_CONSTITUTIONS),
        "domain_standard_categories": list(DOMAIN_STANDARD_CATEGORIES),
        "governance_layers_from_hierarchy": list(GOVERNANCE_LAYERS),
        **meta,
    }

    jurisdiction_conflict = {
        "rule_id": "constitution_jurisdiction_and_conflict_rule_v1",
        "general_constitution_jurisdiction": list(GENERAL_JURISDICTION),
        "domain_constitution_jurisdiction": list(DOMAIN_JURISDICTION),
        "domain_standard_jurisdiction": list(DOMAIN_STANDARD_JURISDICTION),
        "conflict_rules": list(CONFLICT_RULES),
        "non_overridable_floors": [
            "safety",
            "survival",
            "privacy",
            "fact admission",
            "user output",
        ],
        "default_conflict_resolution": "更保守、更安全、更可审计、更可回滚",
        **meta,
    }

    generation_logic = {
        "logic_id": "constitution_generation_logic_v1",
        "initial_constitution": {
            "created_by": "human designers",
            "purpose": (
                "管理当前 Luna 模块功能、能力边界、候选、证据、授权、输出与 provider 准入"
            ),
            "applies_to": "current engineering phase",
            "not_final_form": True,
        },
        "future_constitution_generation": {
            "luna_may_propose": "constitution_candidate",
            "candidate_only": True,
            "local_auto_submit_forbidden": True,
            "required_reviews": ["Hive review", "owner review", "governance review"],
            "required_artifacts": [
                "source_chain",
                "evidence",
                "risk assessment",
                "rollback plan",
                "impact analysis",
            ],
            "version_preservation_required": True,
        },
        "generation_goals": [
            "提升 Luna 生存能力",
            "提升系统稳定性",
            "提升适应复杂环境的能力",
            "降低错误输出、错误动作、越权执行、事实污染风险",
            "保证长期自我治理能力",
        ],
        **meta,
    }

    amendment_logic = {
        "logic_id": "constitution_amendment_logic_v1",
        "amendment_triggers": list(AMENDMENT_TRIGGERS),
        "amendment_workflow": list(AMENDMENT_WORKFLOW),
        "constitution_amendment_committed_now": False,
        "local_auto_amendment_allowed": False,
        "hive_review_required": True,
        **meta,
    }

    system_vs_personalized = {
        "rule_id": "system_vs_personalized_constitution_rule_v1",
        "system_constitution": {
            "managed_by": "Hive",
            "scope": [
                "基础安全",
                "生存",
                "隐私",
                "事实",
                "输出",
                "授权",
                "provider",
                "运行边界",
            ],
            "local_modification_forbidden": True,
            "user_preference_override_forbidden": True,
            "personalized_override_forbidden": True,
        },
        "personalized_constitution": {
            "sources": [
                "用户长期偏好",
                "关系模式",
                "语言习惯",
                "交互风格",
                "本地生活环境",
            ],
            "must_stay_within_system_constitution": True,
            "cannot_relax": [
                "安全",
                "隐私",
                "事实",
                "授权",
                "输出底线",
                "provider 越权",
                "evidence 绕过",
                "Validation Factory 绕过",
                "Hive 最高宪法绕过",
            ],
            "status": "Domain Standard 下的 personalization overlay — 不得成为上位规则",
        },
        "priority_order": [
            "System Constitution",
            "Domain Constitution",
            "Domain Standard",
            "Personalized Constitution",
            "User Preference",
            "Phase-local Rule",
        ],
        **meta,
    }

    hive_authority = {
        "rule_id": "hive_constitution_authority_rule_v1",
        "hive_role": "最高宪法管理端",
        "hive_responsibilities": [
            "最高宪法发布",
            "版本管理",
            "审查",
            "撤销",
            "回滚",
            "审计",
        ],
        "local_luna_role": "消费、缓存、执行、校验、申请更新",
        "local_forbidden": [
            "私自修改 General Constitution",
            "绕过 Hive 发布最高宪法",
        ],
        "local_may_generate": [
            "constitution_update_request_candidate",
            "local_policy_candidate",
            "personalized_constitution_candidate",
        ],
        "local_generated_cannot_override_hive": True,
        "hive_constitution_authority": True,
        "local_override_of_general_constitution_allowed": False,
        "hive_review_required_for_general_constitution_change": True,
        **meta,
    }

    local_consumption = {
        "boundary_id": "local_luna_constitution_consumption_boundary_v1",
        "local_may": [
            "cache constitution",
            "validate constitution version",
            "enforce local copy",
            "detect conflict",
            "generate amendment candidate",
            "generate violation report",
            "request Hive update",
            "apply approved update",
            "rollback to safe previous version",
        ],
        "local_may_not": [
            "modify highest constitution locally",
            "silently change survival/safety/privacy/fact/user-output rules",
            "weaken provider boundary",
            "bypass authorization standard",
            "bypass Validation Factory",
            "override Hive-issued constitution",
            "erase constitution violation record",
        ],
        **meta,
    }

    survival_link = {
        "link_id": "constitution_survival_mechanism_link_v1",
        "core_principle": (
            "宪法不是单纯限制系统，而是 Luna 的生存机制之一；"
            "用于避免错误动作、事实污染、权限越界、隐私泄漏、provider 失控、"
            "硬件损伤、用户信任破裂导致系统死亡或失效"
        ),
        "supported_survival_capabilities": [
            "self-protection",
            "fault isolation",
            "risk suppression",
            "degradation mode",
            "provider quarantine",
            "evidence preservation",
            "rollback",
            "user trust preservation",
            "Hive coordination",
            "long-term adaptability",
        ],
        "candidate_sources": {
            "survival_drive": "constitution_amendment_candidate",
            "health_management": "constitution_review_candidate",
            "repeated_boundary_violation": "rule_hardening_candidate",
            "hardware_lifespan_risk": "hardware_constitution_candidate_later",
        },
        "all_amendments_require_hive_review": True,
        **meta,
    }

    violation_penalty = {
        "rule_id": "constitution_violation_alarm_and_penalty_rule_v1",
        "violation_levels": list(VIOLATION_LEVELS),
        "violation_types": list(VIOLATION_TYPES),
        "actions": list(VIOLATION_ACTIONS),
        "evidence_fields": list(VIOLATION_EVIDENCE_FIELDS),
        "hive_report_required_for_high_severity": True,
        **meta,
    }

    amendment_lifecycle = {
        "lifecycle_id": "constitution_change_candidate_lifecycle_v1",
        "states": list(AMENDMENT_CANDIDATE_STATES),
        "amendment_candidate_generated_now": False,
        "hive_review_submitted_now": False,
        "approved_now": False,
        "active_now": False,
        "current_phase_states_later_only": [
            "approved_later",
            "rejected_later",
            "staged_rollout_later",
            "active_later",
            "rollback_later",
        ],
        **meta,
    }

    decision_tree = {
        "tree_id": "constitution_governance_decision_tree_v1",
        "questions": list(DECISION_TREE_QUESTIONS),
        "rule_placement_flow": [
            "1. General Constitution?",
            "2. Domain Constitution?",
            "3. Domain Standard?",
            "4. Factory / Module / Provider Contract?",
            "5. Phase-local Rule only?",
            "6. Impacts safety/survival/privacy/fact/user output?",
            "7. Needs Hive review?",
            "8. Personalization overlay allowed?",
            "9. Upper-rule conflict?",
            "10. Violation alarm / penalty required?",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "constitution_explanation_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_decision = {
        "decision_id": "constitution_governance_explanation_planning_decision_v1",
        "planning_pass": boundary_ok,
        "explanation_complete": boundary_ok,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "constitution_governance_explanation_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "layer_count": len(CONSTITUTION_LAYERS_EXPLAINED),
        "decision_tree_questions": len(DECISION_TREE_QUESTIONS),
        "amendment_trigger_count": len(AMENDMENT_TRIGGERS),
        "violation_level_count": len(VIOLATION_LEVELS),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "constitution_governance_explanation_planning_policy": policy,
        "constitution_hierarchy_input_review": hierarchy_input_review,
        "constitution_layer_relationship_explanation": layer_relationship,
        "constitution_jurisdiction_and_conflict_rule": jurisdiction_conflict,
        "constitution_generation_logic": generation_logic,
        "constitution_amendment_logic": amendment_logic,
        "system_vs_personalized_constitution_rule": system_vs_personalized,
        "hive_constitution_authority_rule": hive_authority,
        "local_luna_constitution_consumption_boundary": local_consumption,
        "constitution_survival_mechanism_link": survival_link,
        "constitution_violation_alarm_and_penalty_rule": violation_penalty,
        "constitution_change_candidate_lifecycle": amendment_lifecycle,
        "constitution_governance_decision_tree": decision_tree,
        "constitution_explanation_non_claims_register": non_claims,
        "constitution_governance_explanation_planning_decision": planning_decision,
        "summary": summary,
    }
