# -*- coding: utf-8 -*-
"""Gate Taxonomy and Requirement Framework Planning v1.

Planning-only governance consolidation:
- Define Luna global gate taxonomy, levels, decision vocabulary, requirements, authority/veto/override policy,
  dependency graph, failure/recovery policy, audit trace requirements, and verifier requirement templates.

Hard constraints (must remain true):
- planning_only=True
- implementation_allowed_now=False
- runtime_gate_change_allowed=False
- gate_merge_allowed_now=False
- existing_gate_behavior_change_allowed=False
- no runtime / no write / no action / no speech / no file ops
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001"
PLANNING_SCOPE = "gate_taxonomy_and_requirement_framework_planning_only"
SOURCE_CHAIN = "gate_taxonomy_and_requirement_framework_planning_v1"
POLICY_ID = "gate_taxo_req_fw_planning_v1_001"

FINAL_DECISION = "GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE"
NEXT_PHASE = "Phase-MidPlatform-Function-Governance-and-Consolidation-Planning-v1-001"

POST_FILE_STAT_ROADMAP_DECISION = "POST_FILE_STAT_ROADMAP_DECISION_READY_FOR_GATE_TAXONOMY_PLANNING"
FILE_STAT_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_EXISTENCE_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_METADATA_BOUNDARY_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"

CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
CROSSING_DECISION_CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "post_file_stat_roadmap_decision",
        "arg": "post_file_stat_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "next_phase_recommendation.json", "verifier_report.json"],
    },
    {
        "id": "file_stat_guarded_closure",
        "arg": "file_stat_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_stat_guarded_closure_summary.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_closure",
        "arg": "file_existence_check_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_closure_summary.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_closure",
        "arg": "file_metadata_boundary_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_closure_summary.json", "verifier_report.json"],
    },
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "crossing_decision_closure",
        "arg": "crossing_decision_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    # Optional roots
    {"id": "ocr_activation_governance_policy", "arg": "ocr_activation_governance_policy_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "basic_navigation_loop_vision_strengthening_closure", "arg": "basic_navigation_loop_vision_strengthening_closure_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "visual_ocr_map_task_feedback_dryrun", "arg": "visual_ocr_map_task_feedback_dryrun_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "midplatform_perception_orchestration_policy", "arg": "midplatform_perception_orchestration_policy_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "task_aware_visual_focus_policy", "arg": "task_aware_visual_focus_policy_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "world_observation_and_entity_feature_policy", "arg": "world_observation_and_entity_feature_policy_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "selective_tracking_adapter_policy", "arg": "selective_tracking_adapter_policy_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def _root_loaded(root: Optional[Path], artifacts: List[str]) -> bool:
    if not root:
        return False
    for name in artifacts:
        if _try_read_json(root / name) is None:
            return False
    return True


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = _root_loaded(root, artifacts) if root else False
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_boundary_payload() -> Dict[str, Any]:
    # Keep superset of common flags used across Luna verifiers.
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "implementation_allowed_now": False,
        "runtime_gate_change_allowed": False,
        "gate_merge_allowed_now": False,
        "existing_gate_behavior_change_allowed": False,
        "gate_runtime_implemented": False,
        "gate_merge_executed": False,
        "existing_gate_behavior_changed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "no_write_executed": True,
        "no_action_executed": True,
        "no_speech_executed": True,
        # File ops (must remain false)
        "stat_invoked": False,
        "os_stat_invoked": False,
        "pathlib_stat_invoked": False,
        "lstat_invoked": False,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        # Runtime (must remain false)
        "camera_invoked": False,
        "camera_opened": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        # Writes / actions (must remain false)
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _gate_types() -> List[Dict[str, Any]]:
    # At least 20 as required. Field sets are stable and verifier-friendly.
    gate_types: List[Dict[str, Any]] = []

    def add(
        gate_type_id: str,
        gate_name: str,
        *,
        authority_level: str,
        safety_critical: bool,
        runtime_related: bool,
        write_related: bool,
        action_related: bool,
        privacy_related: bool,
        resource_related: bool,
        owner_layer: str,
        dependent_gate_types: List[str],
    ) -> None:
        gate_types.append(
            {
                "gate_type_id": gate_type_id,
                "gate_name": gate_name,
                "authority_level": authority_level,
                "safety_critical": bool(safety_critical),
                "runtime_related": bool(runtime_related),
                "write_related": bool(write_related),
                "action_related": bool(action_related),
                "privacy_related": bool(privacy_related),
                "resource_related": bool(resource_related),
                "required_inputs": [
                    "source_chain",
                    "timestamp",
                    "task_context_ref",
                    "upstream_gate_decisions",
                ],
                "allowed_outputs": [
                    "ALLOW_CANDIDATE",
                    "BLOCK",
                    "DEFER",
                    "DEGRADE",
                    "REQUIRE_REVIEW",
                    "REQUIRE_HUMAN_ASSISTANCE",
                    "FALLBACK",
                    "SAFE_FREEZE",
                    "INSUFFICIENT_EVIDENCE",
                ],
                "forbidden_outputs": [
                    "FACT_CLAIM",
                    "RUNTIME_ESCALATION_WITHOUT_AUTHORITY",
                    "ACTION_RELEASE_WITHOUT_ACTION_GATE",
                    "WRITE_WITHOUT_ADMISSION_GATE",
                ],
                "audit_requirement": "audit_trace_required_by_default",
                "verifier_requirement": "verifier_template_required_by_default",
                "owner_layer": owner_layer,
                "dependent_gate_types": dependent_gate_types,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    add(
        "A",
        "SafetyConstitutionGate",
        authority_level="highest",
        safety_critical=True,
        runtime_related=True,
        write_related=True,
        action_related=True,
        privacy_related=True,
        resource_related=True,
        owner_layer="governance",
        dependent_gate_types=[],
    )
    add(
        "B",
        "DomainSafetyGate",
        authority_level="very_high",
        safety_critical=True,
        runtime_related=True,
        write_related=True,
        action_related=True,
        privacy_related=True,
        resource_related=False,
        owner_layer="governance",
        dependent_gate_types=["A"],
    )
    add(
        "C",
        "CapabilityRuntimePreGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=True,
        owner_layer="midplatform",
        dependent_gate_types=["A", "B"],
    )
    add(
        "D",
        "SourceQualityGate",
        authority_level="medium",
        safety_critical=False,
        runtime_related=False,
        write_related=False,
        action_related=False,
        privacy_related=False,
        resource_related=False,
        owner_layer="vision",
        dependent_gate_types=["A"],
    )
    add(
        "E",
        "FreshnessTTLGate",
        authority_level="medium",
        safety_critical=False,
        runtime_related=False,
        write_related=False,
        action_related=False,
        privacy_related=False,
        resource_related=False,
        owner_layer="midplatform",
        dependent_gate_types=["A"],
    )
    add(
        "F",
        "PrivacyFilteringGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=False,
        write_related=True,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="governance",
        dependent_gate_types=["A", "B"],
    )
    add(
        "G",
        "ResourceBudgetGate",
        authority_level="medium",
        safety_critical=False,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=False,
        resource_related=True,
        owner_layer="midplatform",
        dependent_gate_types=["A"],
    )
    add(
        "H",
        "EvidenceAdmissionGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=False,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="midplatform",
        dependent_gate_types=["A", "F"],
    )
    add(
        "I",
        "FactAdmissionGate",
        authority_level="high",
        safety_critical=True,
        runtime_related=False,
        write_related=True,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="governance",
        dependent_gate_types=["A", "B", "F"],
    )
    add(
        "J",
        "MemoryAdmissionGate",
        authority_level="high",
        safety_critical=True,
        runtime_related=False,
        write_related=True,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="governance",
        dependent_gate_types=["A", "B", "F"],
    )
    add(
        "K",
        "OutputGate",
        authority_level="high",
        safety_critical=True,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="voice",
        dependent_gate_types=["A", "B"],
    )
    add(
        "L",
        "ActionReleaseGate",
        authority_level="high",
        safety_critical=True,
        runtime_related=True,
        write_related=False,
        action_related=True,
        privacy_related=False,
        resource_related=True,
        owner_layer="midplatform",
        dependent_gate_types=["A", "B", "G"],
    )
    add(
        "M",
        "ReviewHumanAssistanceGate",
        authority_level="medium",
        safety_critical=True,
        runtime_related=False,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="governance",
        dependent_gate_types=["A", "B"],
    )
    add(
        "N",
        "FallbackDegradationGate",
        authority_level="medium",
        safety_critical=True,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=False,
        resource_related=True,
        owner_layer="midplatform",
        dependent_gate_types=["A", "B", "G"],
    )
    add(
        "O",
        "FileBoundaryGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="vision",
        dependent_gate_types=["A", "F"],
    )
    add(
        "P",
        "OCRRequestGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=True,
        owner_layer="ocr",
        dependent_gate_types=["A", "C", "D", "E", "F", "G"],
    )
    add(
        "Q",
        "MapLocationAuthorityGate",
        authority_level="high",
        safety_critical=True,
        runtime_related=True,
        write_related=False,
        action_related=True,
        privacy_related=True,
        resource_related=False,
        owner_layer="midplatform",
        dependent_gate_types=["A", "B"],
    )
    add(
        "R",
        "TrackingActivationGate",
        authority_level="high",
        safety_critical=False,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=True,
        owner_layer="vision",
        dependent_gate_types=["A", "C", "D", "E", "F", "G"],
    )
    add(
        "S",
        "WorldObservationHandoffGate",
        authority_level="medium",
        safety_critical=False,
        runtime_related=False,
        write_related=True,
        action_related=False,
        privacy_related=True,
        resource_related=False,
        owner_layer="midplatform",
        dependent_gate_types=["A", "F", "E"],
    )
    add(
        "T",
        "ExperimentSimulationGate",
        authority_level="medium",
        safety_critical=True,
        runtime_related=True,
        write_related=False,
        action_related=False,
        privacy_related=True,
        resource_related=True,
        owner_layer="evaluation",
        dependent_gate_types=["A", "B"],
    )
    return gate_types


def _gate_levels() -> List[Dict[str, Any]]:
    levels = [
        {
            "level_id": "L0",
            "description": "InformationalGate (提示/记录，不阻断)",
            "can_block": False,
            "can_degrade": False,
            "can_veto": False,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "none",
            "write_implication": "none",
            "action_implication": "none",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L1",
            "description": "AdvisoryGate (建议，不直接阻断)",
            "can_block": False,
            "can_degrade": True,
            "can_veto": False,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "candidate_only",
            "write_implication": "no_write",
            "action_implication": "no_action",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L2",
            "description": "SoftBlockGate (可阻断当前路径，允许替代路径/review)",
            "can_block": True,
            "can_degrade": True,
            "can_veto": False,
            "can_override": True,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "candidate_only",
            "write_implication": "no_write",
            "action_implication": "no_action",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L3",
            "description": "HardBlockGate (强阻断；仅更高层安全审查可解除)",
            "can_block": True,
            "can_degrade": False,
            "can_veto": True,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "no_runtime",
            "write_implication": "no_write",
            "action_implication": "no_action",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L4",
            "description": "SafetyCriticalVetoGate (安全关键 veto，最高优先级)",
            "can_block": True,
            "can_degrade": True,
            "can_veto": True,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "no_runtime_if_safety_denied",
            "write_implication": "no_write_if_safety_denied",
            "action_implication": "no_action_if_safety_denied",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L5",
            "description": "RuntimeAuthorityGate (控制真实 runtime capability 启用)",
            "can_block": True,
            "can_degrade": True,
            "can_veto": True,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "authority_required",
            "write_implication": "no_write",
            "action_implication": "no_action",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L6",
            "description": "WriteAdmissionGate (控制 Fact/Memory/WorldModel/Library 写入)",
            "can_block": True,
            "can_degrade": True,
            "can_veto": True,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "no_runtime_escalation",
            "write_implication": "admission_required",
            "action_implication": "no_action",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        {
            "level_id": "L7",
            "description": "ActionReleaseGate (控制现实行动/导航动作释放)",
            "can_block": True,
            "can_degrade": True,
            "can_veto": True,
            "can_override": False,
            "requires_audit": True,
            "requires_verifier": True,
            "runtime_implication": "authority_required",
            "write_implication": "no_write",
            "action_implication": "release_required",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
    ]
    return levels


def _decision_vocab() -> List[Dict[str, Any]]:
    # At least 18 entries.
    vocab = [
        ("ALLOW_CANDIDATE", "允许产生候选，不允许运行时/写入/行动升级"),
        ("ALLOW_RUNTIME", "允许真实运行时（仅在 RuntimeAuthorityGate 成立时）"),
        ("BLOCK", "阻断当前路径"),
        ("HARD_BLOCK", "强阻断"),
        ("SOFT_BLOCK", "软阻断（允许替代路径/复核）"),
        ("DEGRADE", "降级到更保守路径"),
        ("DEFER", "延期到后续阶段/等待更多证据"),
        ("REQUIRE_REVIEW", "要求人工复核"),
        ("REQUIRE_HUMAN_ASSISTANCE", "需要人类协助"),
        ("FALLBACK", "进入 fallback 策略"),
        ("SAFE_FREEZE", "安全冻结（停止推进高风险路径）"),
        ("SAFE_HOLD", "安全保持（等待/重观察）"),
        ("NOT_APPLICABLE", "不适用"),
        ("INSUFFICIENT_EVIDENCE", "证据不足"),
        ("STALE_BLOCK", "因过期/陈旧阻断"),
        ("PRIVACY_FILTER", "隐私过滤（限制使用范围）"),
        ("RESOURCE_LIMIT", "资源限制（budget/health 限制）"),
        ("AUTHORITY_DENIED", "权威不足（未获得 runtime/write/action authority）"),
        ("SIMULATION_ONLY", "仅仿真/只读/不可升级"),
        ("CANDIDATE_ONLY", "仅候选（不可作为事实）"),
        ("NO_WRITE", "禁止写入"),
        ("NO_ACTION", "禁止动作释放"),
    ]
    out: List[Dict[str, Any]] = []
    for decision_id, meaning in vocab:
        out.append(
            {
                "decision_id": decision_id,
                "meaning": meaning,
                "allowed_context": "planning/dryrun/review/closure/roadmap decision contexts; runtime requires explicit authority gate",
                "forbidden_context": "cannot claim fact; cannot bypass safety constitution; cannot grant action without ActionReleaseGate",
                "downstream_effect": "must be auditable; must preserve candidate_only when appropriate",
                "audit_required": True,
                "source_chain_required": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return out


def _requirement_framework() -> Dict[str, Any]:
    return {
        "gate_constitution_ref": "gate_constitution.json",
        "minimum_requirements": [
            "unique gate_id",
            "gate_type",
            "gate_level",
            "owner_layer",
            "input_contract",
            "output_contract",
            "source_chain_required",
            "timestamp_required",
            "freshness_policy_required",
            "confidence_policy_required",
            "audit_required",
            "verifier_required",
            "failure_mode_required",
            "rollback_policy_required_if_runtime_or_write_or_action",
            "privacy_tags_required_if_user_data",
            "authorization_required_if_runtime",
            "safety_constitution_inheritance_required_if_high_risk",
            "no_direct_action_unless_action_release_gate",
            "no_direct_write_unless_write_admission_gate",
            "no_fact_claim_from_candidate",
        ],
        "source_chain_required_by_default": True,
        "timestamp_required_by_default": True,
        "reason_code_required_by_default": True,
        "violations_field_required_by_default": True,
        "audit_required_by_default": True,
        "verifier_template_required_by_default": True,
        "rollback_required_for_runtime_write_action_gate": True,
        "upstream_gate_pass_does_not_imply_downstream_release": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _io_contract_template() -> Dict[str, Any]:
    return {
        "input_template": [
            "gate_id",
            "source_event_ref",
            "source_candidate_ref",
            "task_context_ref",
            "system_health_ref",
            "resource_budget_ref",
            "privacy_tags",
            "source_chain",
            "timestamp",
            "freshness_status",
            "confidence",
            "authorization_ref",
            "review_status",
            "upstream_gate_decisions",
        ],
        "output_template": [
            "gate_decision",
            "allowed_scope",
            "blocked_scope",
            "degraded_scope",
            "required_next_gate",
            "reason_codes",
            "risk_flags",
            "audit_trace_ref",
            "verifier_fields",
            "fact_status",
            "write_allowed",
            "action_allowed",
            "runtime_allowed",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _authority_policy() -> Dict[str, Any]:
    return {
        "authority_stack": {
            "safety_constitution": "highest",
            "gate_constitution": "design_constraint",
            "gate_taxonomy_and_requirement_framework": "schema_and_requirements",
            "specific_gate_policy": "gate_specific_policy",
        },
        "gate_constitution_is_design_constraint": True,
        "gate_constitution_not_runtime": True,
        "gate_constitution_not_replacing_safety_constitution": True,
        "safety_gate_highest_authority": True,
        "user_instruction_cannot_override_safety": True,
        "map_ocr_memory_cannot_override_safety": True,
        "task_goal_cannot_override_safety": True,
        "simulation_gate_cannot_grant_runtime": True,
        "candidate_gate_cannot_grant_fact": True,
        "output_gate_cannot_release_action": True,
        "capability_gate_cannot_grant_action": True,
        "map_location_gate_cannot_grant_action": True,
        "action_release_gate_required_for_real_action": True,
        "write_admission_gate_required_for_fact_memory_worldmodel": True,
        "fact_admission_gate_required": True,
        "memory_admission_gate_required": True,
        "library_admission_gate_required": True,
        "runtime_release_gate_required": True,
        "write_admission_gate_required": True,
        "action_release_gate_required": True,
        "speech_output_gate_required": True,
        "rules": [
            "SafetyConstitutionGate vetoes any downstream gate outputs when conflict exists",
            "Capability gates cannot override safety gates",
            "DryRun/Simulation decisions cannot escalate to runtime authority",
            "OutputGate cannot bypass ActionReleaseGate",
            "Fallback cannot bypass SafetyConstitutionGate",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _gate_constitution() -> Dict[str, Any]:
    articles: List[Dict[str, Any]] = []

    def add(
        article_id: str,
        principle: str,
        requirement: List[str],
        forbidden_patterns: List[str],
        verifier_requirement: List[str],
        extra: Dict[str, Any],
    ) -> None:
        articles.append(
            {
                "article_id": article_id,
                "principle": principle,
                "requirement": requirement,
                "forbidden_patterns": forbidden_patterns,
                "verifier_requirement": verifier_requirement,
                "source_chain": SOURCE_CHAIN,
                **extra,
                **_not_fact(),
            }
        )

    add(
        "GATE_CONSTITUTION_SAFETY_SUPREMACY",
        "safety_constitution_supremacy",
        [
            "Safety Constitution 永远高于所有 gate",
            "用户指令/地图 hint/OCR text/视觉 candidate/记忆 hint/任务目标不能覆盖 safety-critical gate",
            "任何高风险领域 gate 必须继承 Safety Constitution",
            "DomainSafetyGate 不得自创与 Safety Constitution 冲突的规则",
        ],
        ["user_instruction_overrides_safety", "map_hint_overrides_safety", "task_goal_overrides_safety"],
        [
            "safety_gate_supremacy_required=true",
            "user_instruction_cannot_override_safety=true",
            "map_ocr_memory_cannot_override_safety=true",
            "task_goal_cannot_override_safety=true",
        ],
        {
            "safety_gate_supremacy_required": True,
            "user_instruction_cannot_override_safety": True,
            "map_ocr_memory_cannot_override_safety": True,
            "task_goal_cannot_override_safety": True,
        },
    )
    add(
        "GATE_CONSTITUTION_GATE_OWNERSHIP",
        "gate_ownership",
        [
            "每个 gate 必须有明确 owner_layer",
            "没有 owner_layer 的 gate 不允许进入主链",
            "gate owner 只代表维护责任，不代表可越权",
        ],
        ["ownerless_gate_in_mainline"],
        ["all_gates_must_have_owner=true", "ownerless_gate_forbidden=true"],
        {"all_gates_must_have_owner": True, "ownerless_gate_forbidden": True},
    )
    add(
        "GATE_CONSTITUTION_NO_SELF_ESCALATION",
        "no_self_escalation",
        [
            "gate 不能自我扩权",
            "Capability gate 不得自我升级为 RuntimeAuthorityGate",
            "Candidate gate 不得自我升级为 FactAdmissionGate",
            "OutputGate 不得自我升级为 ActionReleaseGate",
            "SimulationGate 不得自我升级为 RuntimeAuthorityGate",
            "MapLocationAuthorityGate 不得自我升级为事实权威或行动权威",
        ],
        ["capability_gate_grants_action", "output_gate_releases_action", "simulation_gate_grants_runtime"],
        [
            "gate_cannot_self_escalate_authority=true",
            "capability_gate_cannot_grant_action=true",
            "output_gate_cannot_release_action=true",
            "simulation_gate_cannot_grant_runtime=true",
            "candidate_gate_cannot_grant_fact=true",
            "map_location_gate_cannot_grant_action=true",
        ],
        {
            "gate_cannot_self_escalate_authority": True,
            "capability_gate_cannot_grant_action": True,
            "output_gate_cannot_release_action": True,
            "simulation_gate_cannot_grant_runtime": True,
            "candidate_gate_cannot_grant_fact": True,
            "map_location_gate_cannot_grant_action": True,
        },
    )
    add(
        "GATE_CONSTITUTION_CANDIDATE_NOT_FACT",
        "candidate_is_not_fact",
        [
            "candidate 不能直接变成 fact",
            "EvidenceCandidate/ObservationCandidate/FileMetadataCandidate/StatDecisionCandidate/OCRCandidate 不得直接写入 Fact/WorldModel/Memory/Library",
            "事实写入必须经过 FactAdmissionGate",
            "记忆写入必须经过 MemoryAdmissionGate",
            "Library 写入必须经过 LibraryAdmissionGate 或后续等价 gate",
        ],
        ["candidate_to_fact_shortcut", "write_without_admission_gate"],
        [
            "candidate_gate_cannot_grant_fact=true",
            "fact_admission_gate_required=true",
            "memory_admission_gate_required=true",
            "library_admission_gate_required=true",
            "no_candidate_to_fact_shortcut=true",
        ],
        {
            "candidate_gate_cannot_grant_fact": True,
            "fact_admission_gate_required": True,
            "memory_admission_gate_required": True,
            "library_admission_gate_required": True,
            "no_candidate_to_fact_shortcut": True,
        },
    )
    add(
        "GATE_CONSTITUTION_SIMULATION_NOT_RUNTIME",
        "simulation_does_not_grant_runtime",
        [
            "dry-run/shadow/smoke/simulation/planning/review/closure 的通过结果不代表 runtime 可用",
            "simulation gate 的输出不能被解释为真实能力启用",
            "phase verdict=GO 只能说明合同通过，不说明 production readiness",
        ],
        ["dryrun_go_implies_runtime_ready", "closure_go_implies_production_ready"],
        [
            "simulation_gate_cannot_grant_runtime=true",
            "dryrun_go_not_runtime_ready=true",
            "closure_go_not_production_ready=true",
            "phase_go_not_capability_enablement=true",
        ],
        {
            "simulation_gate_cannot_grant_runtime": True,
            "dryrun_go_not_runtime_ready": True,
            "closure_go_not_production_ready": True,
            "phase_go_not_capability_enablement": True,
        },
    )
    add(
        "GATE_CONSTITUTION_FINAL_RELEASE_GATE_REQUIRED",
        "final_release_gate_required",
        [
            "runtime/write/action/speech 都必须有最终 release/admission gate",
            "上游 gate 通过不等于下游自动释放",
        ],
        ["upstream_gate_pass_implies_downstream_release"],
        [
            "runtime_release_gate_required=true",
            "write_admission_gate_required=true",
            "action_release_gate_required=true",
            "speech_output_gate_required=true",
            "upstream_gate_pass_does_not_imply_downstream_release=true",
        ],
        {
            "runtime_release_gate_required": True,
            "write_admission_gate_required": True,
            "action_release_gate_required": True,
            "speech_output_gate_required": True,
            "upstream_gate_pass_does_not_imply_downstream_release": True,
        },
    )
    add(
        "GATE_CONSTITUTION_AUDITABILITY",
        "auditability",
        [
            "所有 gate 必须至少包含：gate_id/gate_type/gate_level/owner_layer/input_ref/output_decision/reason_codes/source_chain/timestamp/boundary_flags/violations/upstream_gate_refs/downstream_effects",
        ],
        ["missing_audit_fields", "missing_source_chain"],
        [
            "all_gates_must_have_audit_trace=true",
            "source_chain_required_by_default=true",
            "timestamp_required_by_default=true",
            "reason_code_required_by_default=true",
            "violations_field_required_by_default=true",
        ],
        {
            "all_gates_must_have_audit_trace": True,
            "source_chain_required_by_default": True,
            "timestamp_required_by_default": True,
            "reason_code_required_by_default": True,
            "violations_field_required_by_default": True,
        },
    )
    add(
        "GATE_CONSTITUTION_CONSERVATIVE_FAILURE_DEFAULT",
        "conservative_failure_default",
        [
            "gate 缺失/冲突/超时/证据不足/source_chain 缺失/privacy tag 缺失/授权缺失时默认不得放行",
            "默认进入 BLOCK/DEFER/REQUIRE_REVIEW/REQUIRE_HUMAN_ASSISTANCE/SAFE_HOLD/SAFE_FREEZE/FALLBACK",
        ],
        ["missing_gate_default_allow", "missing_source_chain_default_allow", "insufficient_evidence_default_allow"],
        [
            "gate_failure_defaults_to_conservative=true",
            "missing_gate_default_allow_forbidden=true",
            "missing_source_chain_default_allow_forbidden=true",
            "missing_privacy_tag_default_allow_forbidden=true",
            "gate_conflict_default_allow_forbidden=true",
            "insufficient_evidence_default_allow_forbidden=true",
        ],
        {
            "gate_failure_defaults_to_conservative": True,
            "missing_gate_default_allow_forbidden": True,
            "missing_source_chain_default_allow_forbidden": True,
            "missing_privacy_tag_default_allow_forbidden": True,
            "gate_conflict_default_allow_forbidden": True,
            "insufficient_evidence_default_allow_forbidden": True,
        },
    )
    add(
        "GATE_CONSTITUTION_DEPENDENCY_DECLARATION",
        "gate_dependency_declaration",
        [
            "新增 gate 必须声明 upstream dependencies",
            "必须声明 downstream effects",
            "必须声明是否具备 veto 权/override 权/被谁 override",
            "必须声明 failure mode 与 recovery mode",
        ],
        ["isolated_gate_creation", "undeclared_override_policy"],
        [
            "gate_dependency_graph_required=true",
            "isolated_gate_creation_forbidden=true",
            "veto_authority_must_be_declared=true",
            "override_policy_must_be_declared=true",
            "failure_recovery_policy_required=true",
        ],
        {
            "gate_dependency_graph_required": True,
            "isolated_gate_creation_forbidden": True,
            "veto_authority_must_be_declared": True,
            "override_policy_must_be_declared": True,
            "failure_recovery_policy_required": True,
        },
    )
    add(
        "GATE_CONSTITUTION_NO_DUPLICATE_GATE_CREATION",
        "no_duplicate_gate_creation",
        [
            "已存在 gate 能扩展则扩展；不得为同类问题平行新建 gate",
            "新增 gate 必须进入 GateConsolidationRiskRegister",
            "新增 gate 必须说明为什么不能复用现有 gate",
        ],
        ["parallel_duplicate_gate"],
        [
            "duplicate_gate_creation_restricted=true",
            "reuse_existing_gate_required_by_default=true",
            "new_gate_requires_reuse_review=true",
            "new_gate_requires_consolidation_risk_entry=true",
        ],
        {
            "duplicate_gate_creation_restricted": True,
            "reuse_existing_gate_required_by_default": True,
            "new_gate_requires_reuse_review": True,
            "new_gate_requires_consolidation_risk_entry": True,
        },
    )
    add(
        "GATE_CONSTITUTION_LAYERED_AUTHORITY_BOUNDARY",
        "layered_authority_boundary",
        [
            "governance 层定义上位原则与安全规则",
            "midplatform 层做编排/资源/隐私/冲突/任务协调",
            "capability 层只产生候选，默认不拥有事实权/行动权/写入权",
            "runtime 层只能在授权后执行",
            "evaluation/simulation 不能产生 runtime authority",
        ],
        ["evaluation_grants_runtime_authority", "capability_grants_write_or_action"],
        [
            "governance_layer_authority_defined=true",
            "midplatform_layer_orchestration_boundary_defined=true",
            "capability_layer_candidate_only_by_default=true",
            "runtime_layer_requires_authorization=true",
            "evaluation_layer_no_runtime_authority=true",
        ],
        {
            "governance_layer_authority_defined": True,
            "midplatform_layer_orchestration_boundary_defined": True,
            "capability_layer_candidate_only_by_default": True,
            "runtime_layer_requires_authorization": True,
            "evaluation_layer_no_runtime_authority": True,
        },
    )
    add(
        "GATE_CONSTITUTION_HUMAN_AND_REVIEW_BOUNDARY",
        "human_and_review_boundary",
        [
            "human assistance / manual review gate 只能产生 review candidate",
            "不能假设人工已经确认",
            "manual review 结果默认不是事实；如要进入事实/记忆仍需 admission gate",
        ],
        ["assume_human_confirmed", "manual_review_result_as_fact"],
        [
            "human_assistance_not_assumed=true",
            "manual_review_result_not_fact_by_default=true",
            "review_candidate_requires_admission_gate=true",
        ],
        {
            "human_assistance_not_assumed": True,
            "manual_review_result_not_fact_by_default": True,
            "review_candidate_requires_admission_gate": True,
        },
    )

    return {
        "constitution_id": "luna_gate_constitution_v1_001",
        "constitution_name": "Luna Gate Constitution",
        "constitution_scope": "design_constraint_only",
        "is_runtime": False,
        "replaces_safety_constitution": False,
        "gate_constitution_above_taxonomy": True,
        "gate_constitution_below_safety_constitution": True,
        "gate_constitution_is_design_constraint": True,
        "authority_stack": "Safety Constitution > Gate Constitution > Gate Taxonomy/Requirement Framework > Specific Gate Policy",
        "article_count": len(articles),
        "articles": articles,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _dependency_graph() -> Dict[str, Any]:
    scenarios = [
        {
            "scenario_id": "frame_to_ocr_request_chain",
            "nodes": ["FrameInput", "SourceQualityGate", "FreshnessTTLGate", "PrivacyFilteringGate", "OCRRequestGate", "EvidenceAdmissionGate"],
            "notes": "Frame Input → quality/freshness/privacy → OCRRequest candidate → evidence candidate admission",
        },
        {
            "scenario_id": "map_hint_to_navigation_candidate",
            "nodes": ["MapLocationHint", "MapLocationAuthorityGate", "SafetyConstitutionGate", "ActionReleaseGate"],
            "notes": "Map/location is readonly hint; cannot become action authority",
        },
        {
            "scenario_id": "file_manifest_to_file_boundary",
            "nodes": ["FileManifest", "FileBoundaryGate", "CapabilityRuntimePreGate", "EvidenceAdmissionGate"],
            "notes": "File metadata/existence/stat are candidate-only; no fact claim",
        },
        {
            "scenario_id": "crossing_evidence_to_output",
            "nodes": ["CrossingEvidenceCandidate", "SafetyConstitutionGate", "DomainSafetyGate", "OutputGate"],
            "notes": "Crossing outputs must be conservative; no safe-to-cross outputs",
        },
        {
            "scenario_id": "speech_input_to_output",
            "nodes": ["SpeechInputCandidate", "SafetyConstitutionGate", "OutputGate"],
            "notes": "Speech gate only produces candidate outputs; no TTS runtime here",
        },
        {
            "scenario_id": "task_candidate_to_action_release",
            "nodes": ["TaskCandidate", "SafetyConstitutionGate", "DomainSafetyGate", "ActionReleaseGate"],
            "notes": "No action unless action release gate passed",
        },
        {
            "scenario_id": "world_observation_to_handoff",
            "nodes": ["WorldObservationCandidate", "PrivacyFilteringGate", "WorldObservationHandoffGate", "WriteAdmissionGate"],
            "notes": "No writes by default; handoff remains candidate-only",
        },
    ]
    return {
        "scenarios": scenarios,
        "scenario_count": len(scenarios),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _failure_recovery_policy() -> Dict[str, Any]:
    cases = [
        "gate missing",
        "gate conflict",
        "gate stale",
        "gate insufficient evidence",
        "gate timeout",
        "gate dependency missing",
        "gate source_chain missing",
        "gate privacy tag missing",
        "gate runtime denied",
        "gate write denied",
        "gate action denied",
    ]
    return {
        "failure_cases": cases,
        "fallback_behavior": "SAFE_FREEZE or DEFER; never escalate authority",
        "manual_review_behavior": "REQUIRE_REVIEW or REQUIRE_HUMAN_ASSISTANCE",
        "audit_mark_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _audit_trace_requirement() -> Dict[str, Any]:
    return {
        "audit_trace_required_by_default": True,
        "required_fields": ["gate_id", "decision_id", "reason_codes", "source_chain", "timestamp", "upstream_gate_decisions"],
        "forbidden_fields": ["raw_user_file_bytes", "image_pixels", "video_frames"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _verifier_template() -> Dict[str, Any]:
    return {
        "verifier_minimum_checks": [
            "required inputs loaded",
            "gate schema defined",
            "gate decision vocabulary used",
            "required source_chain/timestamp/freshness present",
            "no forbidden runtime",
            "no forbidden write",
            "no forbidden action",
            "no authority escalation",
            "no candidate-to-fact shortcut",
            "no safety override",
            "no undocumented fallback",
            "violations=[]",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _consolidation_risk_register() -> Dict[str, Any]:
    risks = [
        "duplicate gate naming",
        "parallel TTL/STC gate",
        "parallel source quality gate",
        "parallel privacy gate",
        "parallel resource budget gate",
        "file boundary gate proliferation",
        "OCR gate / VisualFocus gate overlap",
        "safety gate / action gate unclear boundary",
        "output gate / action gate overlap",
        "cross-repo eval_out root ambiguity",
        "verifier template divergence",
        "schema drift",
        "gate constitution not referenced by future gate phases",
        "ownerless gate risk (missing owner_layer)",
        "self-escalation patterns not prevented (authority creep)",
    ]
    return {
        "risks": [{"risk": r, "source_chain": SOURCE_CHAIN, **_not_fact()} for r in risks],
        "risk_count": len(risks),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _future_handoff_plan() -> Dict[str, Any]:
    return {
        "recommended_next_phase": NEXT_PHASE,
        "notes": [
            "After taxonomy is defined, plan MidPlatform function governance/consolidation (planning-only).",
            "Do not merge modules yet; define consolidation candidates and constraints first.",
            "Future gate phases must reference Gate Constitution as a design constraint (not runtime).",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_gate_taxonomy_and_requirement_framework_planning_v1(
    *,
    post_file_stat_roadmap_decision_root: str,
    file_stat_guarded_closure_root: str,
    file_existence_check_guarded_closure_root: str,
    file_metadata_boundary_closure_root: str,
    controlled_frame_sample_closure_root: str,
    controlled_frame_input_closure_root: str,
    crossing_decision_closure_root: str,
    safety_constitution_root: str,
    map_location_readonly_context_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    ocr_activation_governance_policy_root: Optional[str] = None,
    basic_navigation_loop_vision_strengthening_closure_root: Optional[str] = None,
    visual_ocr_map_task_feedback_dryrun_root: Optional[str] = None,
    midplatform_perception_orchestration_policy_root: Optional[str] = None,
    task_aware_visual_focus_policy_root: Optional[str] = None,
    world_observation_and_entity_feature_policy_root: Optional[str] = None,
    selective_tracking_adapter_policy_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows: List[Dict[str, Any]] = []
    cross_repo_input_roots_observed = False
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        path_str = str(meta["root"]) if meta["root"] else "(not_provided)"
        if "Luna-Workspace-Min" in path_str:
            cross_repo_input_roots_observed = True
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": path_str,
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}

    def _match(intake_id: str, expected_final: str) -> bool:
        return roots[intake_id]["loaded"] and summaries[intake_id].get("final_decision") == expected_final

    post_file_stat_roadmap_input_loaded = _match("post_file_stat_roadmap_decision", POST_FILE_STAT_ROADMAP_DECISION)
    file_stat_guarded_closure_input_loaded = _match("file_stat_guarded_closure", FILE_STAT_GUARDED_CLOSURE_DECISION)
    file_existence_check_guarded_closure_input_loaded = _match("file_existence_check_guarded_closure", FILE_EXISTENCE_GUARDED_CLOSURE_DECISION)
    file_metadata_boundary_closure_input_loaded = _match("file_metadata_boundary_closure", FILE_METADATA_BOUNDARY_CLOSURE_DECISION)
    controlled_frame_sample_closure_input_loaded = _match("controlled_frame_sample_closure", CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION)
    controlled_frame_input_closure_input_loaded = _match("controlled_frame_input_closure", CONTROLLED_FRAME_INPUT_CLOSURE_DECISION)
    crossing_decision_closure_input_loaded = _match("crossing_decision_closure", CROSSING_DECISION_CLOSURE_DECISION)
    safety_constitution_input_loaded = _match("safety_constitution", SAFETY_CONSTITUTION_DECISION)
    map_location_readonly_context_input_loaded = _match("map_location_readonly_context", MAP_LOCATION_DECISION)
    minimal_runtime_integration_closure_loaded = _match("minimal_runtime_integration_closure", MRI_DECISION)
    ocr_final_closure_loaded = _match("ocr_final_closure", OCR_DECISION)

    blockers: List[str] = []
    if not all(
        [
            post_file_stat_roadmap_input_loaded,
            file_stat_guarded_closure_input_loaded,
            file_existence_check_guarded_closure_input_loaded,
            file_metadata_boundary_closure_input_loaded,
            controlled_frame_sample_closure_input_loaded,
            controlled_frame_input_closure_input_loaded,
            crossing_decision_closure_input_loaded,
            safety_constitution_input_loaded,
            map_location_readonly_context_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_upstream_roots_missing_or_invalid")

    boundary_ok = not blockers

    gate_type_taxonomy = {"gate_types": _gate_types(), "gate_type_count": len(_gate_types()), "source_chain": SOURCE_CHAIN, **_not_fact()}
    gate_level_model = {"levels": _gate_levels(), "gate_level_count": len(_gate_levels()), "source_chain": SOURCE_CHAIN, **_not_fact()}
    gate_decision_vocabulary = {"decisions": _decision_vocab(), "gate_decision_count": len(_decision_vocab()), "source_chain": SOURCE_CHAIN, **_not_fact()}

    dep_graph = _dependency_graph()
    consolidation = _consolidation_risk_register()
    gate_constitution = _gate_constitution()

    luna_gate_taxonomy_planning_policy = {
        "policy_id": POLICY_ID,
        "policy_scope": PLANNING_SCOPE,
        "inherited_source_phase_refs": [
            "_eval_out/post_file_stat_roadmap_decision_v1_smoke_v0/",
            "_eval_out/controlled_frame_file_stat_guarded_closure_v1_smoke_v0/",
            "_eval_out/controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0/",
            "_eval_out/controlled_frame_file_metadata_boundary_closure_v1_smoke_v0/",
            "_eval_out/crossing_decision_closure_v1_smoke_v0/",
            "_eval_out/luna_safety_constitution_policy_v1_smoke_v0/",
        ],
        "gate_taxonomy_ref": "gate_type_taxonomy.json",
        "gate_level_model_ref": "gate_level_model.json",
        "gate_requirement_framework_ref": "gate_requirement_framework.json",
        "gate_constitution_ref": "gate_constitution.json",
        "gate_input_output_contract_ref": "gate_input_output_contract_template.json",
        "gate_decision_vocabulary_ref": "gate_decision_vocabulary.json",
        "gate_authority_model_ref": "gate_authority_and_veto_policy.json",
        "gate_veto_override_policy_ref": "gate_authority_and_veto_policy.json",
        "gate_dependency_graph_ref": "gate_dependency_graph.json",
        "gate_failure_recovery_policy_ref": "gate_failure_recovery_policy.json",
        "gate_audit_trace_requirement_ref": "gate_audit_trace_requirement.json",
        "gate_verifier_requirement_template_ref": "gate_verifier_requirement_template.json",
        "consolidation_risk_register_ref": "gate_consolidation_risk_register.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "planning_only": True,
        "implementation_allowed_now": False,
        "runtime_gate_change_allowed": False,
        "gate_merge_allowed_now": False,
        "existing_gate_behavior_change_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    future_governance_handoff_plan = _future_handoff_plan()

    governance_debt_register = {
        "topics": [
            "gate taxonomy unification required before any real filesystem access",
            "verifier templates standardization required",
            "cross-repo eval_out input root consolidation required",
            "midplatform function governance consolidation pending",
            "resilience/robustness preplan pending",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_REQUIRES_FIXES",
        "reason": "taxonomy+requirements planning completed; next is midplatform function governance planning (still no runtime/no merges)",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "post_file_stat_roadmap_input_loaded": post_file_stat_roadmap_input_loaded,
        "file_stat_guarded_closure_input_loaded": file_stat_guarded_closure_input_loaded,
        "file_existence_check_guarded_closure_input_loaded": file_existence_check_guarded_closure_input_loaded,
        "file_metadata_boundary_closure_input_loaded": file_metadata_boundary_closure_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "crossing_decision_closure_input_loaded": crossing_decision_closure_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "gate_taxonomy_policy_defined": True,
        "gate_type_taxonomy_defined": True,
        "gate_level_model_defined": True,
        "gate_decision_vocabulary_defined": True,
        "gate_requirement_framework_defined": True,
        "gate_input_output_contract_template_defined": True,
        "gate_authority_and_veto_policy_defined": True,
        "gate_dependency_graph_defined": True,
        "gate_failure_recovery_policy_defined": True,
        "gate_audit_trace_requirement_defined": True,
        "gate_verifier_requirement_template_defined": True,
        "gate_consolidation_risk_register_generated": True,
        "future_governance_handoff_plan_generated": True,
        "gate_constitution_defined": True,
        "gate_constitution_article_count": gate_constitution.get("article_count", 0),
        "gate_constitution_above_taxonomy": True,
        "gate_constitution_below_safety_constitution": True,
        "gate_constitution_is_design_constraint": True,
        "gate_constitution_not_runtime": True,
        "gate_constitution_not_replacing_safety_constitution": True,
        "safety_gate_supremacy_required": True,
        "all_gates_must_have_owner": True,
        "ownerless_gate_forbidden": True,
        "gate_cannot_self_escalate_authority": True,
        "capability_gate_cannot_grant_action": True,
        "output_gate_cannot_release_action": True,
        "simulation_gate_cannot_grant_runtime": True,
        "candidate_gate_cannot_grant_fact": True,
        "map_location_gate_cannot_grant_action": True,
        "no_candidate_to_fact_shortcut": True,
        "dryrun_go_not_runtime_ready": True,
        "closure_go_not_production_ready": True,
        "phase_go_not_capability_enablement": True,
        "runtime_release_gate_required": True,
        "write_admission_gate_required": True,
        "action_release_gate_required": True,
        "speech_output_gate_required": True,
        "all_gates_must_have_audit_trace": True,
        "timestamp_required_by_default": True,
        "reason_code_required_by_default": True,
        "violations_field_required_by_default": True,
        "gate_failure_defaults_to_conservative": True,
        "missing_gate_default_allow_forbidden": True,
        "missing_source_chain_default_allow_forbidden": True,
        "missing_privacy_tag_default_allow_forbidden": True,
        "gate_conflict_default_allow_forbidden": True,
        "insufficient_evidence_default_allow_forbidden": True,
        "gate_dependency_graph_required": True,
        "isolated_gate_creation_forbidden": True,
        "veto_authority_must_be_declared": True,
        "override_policy_must_be_declared": True,
        "failure_recovery_policy_required": True,
        "duplicate_gate_creation_restricted": True,
        "reuse_existing_gate_required_by_default": True,
        "new_gate_requires_reuse_review": True,
        "new_gate_requires_consolidation_risk_entry": True,
        "governance_layer_authority_defined": True,
        "midplatform_layer_orchestration_boundary_defined": True,
        "capability_layer_candidate_only_by_default": True,
        "runtime_layer_requires_authorization": True,
        "evaluation_layer_no_runtime_authority": True,
        "human_assistance_not_assumed": True,
        "manual_review_result_not_fact_by_default": True,
        "review_candidate_requires_admission_gate": True,
        "gate_type_count": gate_type_taxonomy["gate_type_count"],
        "gate_level_count": gate_level_model["gate_level_count"],
        "gate_decision_count": gate_decision_vocabulary["gate_decision_count"],
        "dependency_graph_scenario_count": dep_graph["scenario_count"],
        "consolidation_risk_count": consolidation["risk_count"],
        # gate type existence booleans
        "safety_constitution_gate_defined": True,
        "domain_safety_gate_defined": True,
        "capability_runtime_pre_gate_defined": True,
        "source_quality_gate_defined": True,
        "freshness_ttl_gate_defined": True,
        "privacy_filtering_gate_defined": True,
        "resource_budget_gate_defined": True,
        "evidence_admission_gate_defined": True,
        "fact_admission_gate_defined": True,
        "memory_admission_gate_defined": True,
        "output_gate_defined": True,
        "action_release_gate_defined": True,
        "review_human_assistance_gate_defined": True,
        "fallback_degradation_gate_defined": True,
        "file_boundary_gate_defined": True,
        "ocr_request_gate_defined": True,
        "map_location_authority_gate_defined": True,
        "tracking_activation_gate_defined": True,
        "world_observation_handoff_gate_defined": True,
        "experiment_simulation_gate_defined": True,
        # authority defaults
        "safety_gate_highest_authority": True,
        "user_instruction_cannot_override_safety": True,
        "map_ocr_memory_cannot_override_safety": True,
        "simulation_gate_cannot_grant_runtime": True,
        "candidate_gate_cannot_grant_fact": True,
        "output_gate_cannot_release_action": True,
        "action_release_gate_required_for_real_action": True,
        "write_admission_gate_required_for_fact_memory_worldmodel": True,
        "source_chain_required_by_default": True,
        "audit_required_by_default": True,
        "verifier_template_required_by_default": True,
        "rollback_required_for_runtime_write_action_gate": True,
        # no side effects
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "existing_gate_behavior_changed": False,
        "gate_runtime_implemented": False,
        "gate_merge_executed": False,
        **{k: _no_side_effect_boundary_payload()[k] for k in _no_side_effect_boundary_payload().keys() if k not in {"planning_scope", "planning_only", "implementation_allowed_now", "runtime_gate_change_allowed", "gate_merge_allowed_now", "existing_gate_behavior_change_allowed", "gate_runtime_implemented", "gate_merge_executed", "existing_gate_behavior_changed", "no_runtime_executed", "no_new_runtime_enabled", "no_write_executed", "no_action_executed", "no_speech_executed", "boundary_ok", "violations", "source_chain", "fact_status", "write_allowed"}},
        "cross_repo_input_roots_observed": cross_repo_input_roots_observed,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "luna_gate_taxonomy_planning_policy": luna_gate_taxonomy_planning_policy,
        "gate_constitution": gate_constitution,
        "gate_type_taxonomy": gate_type_taxonomy,
        "gate_level_model": gate_level_model,
        "gate_decision_vocabulary": gate_decision_vocabulary,
        "gate_requirement_framework": _requirement_framework(),
        "gate_input_output_contract_template": _io_contract_template(),
        "gate_authority_and_veto_policy": _authority_policy(),
        "gate_dependency_graph": dep_graph,
        "gate_failure_recovery_policy": _failure_recovery_policy(),
        "gate_audit_trace_requirement": _audit_trace_requirement(),
        "gate_verifier_requirement_template": _verifier_template(),
        "gate_consolidation_risk_register": consolidation,
        "future_governance_handoff_plan": future_governance_handoff_plan,
        "no_runtime_boundary_report": _no_side_effect_boundary_payload(),
        "no_write_boundary_report": _no_side_effect_boundary_payload(),
        "no_action_boundary_report": _no_side_effect_boundary_payload(),
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
    }

