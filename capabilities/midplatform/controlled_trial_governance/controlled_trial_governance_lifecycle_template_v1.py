# -*- coding: utf-8 -*-
"""Controlled Trial Governance Lifecycle Template v1 — reusable midplatform baseline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

TEMPLATE_ID = "ControlledTrialGovernanceLifecycleTemplateV1"
TEMPLATE_PHASE_REF = "Phase-Midplatform-Controlled-Trial-Governance-Lifecycle-Template-v1-001"
SOURCE_CHAIN = "controlled_trial_governance_lifecycle_template_v1"

TEMPLATE_STAGES: Tuple[str, ...] = (
    "chain_closure",
    "trial_planning",
    "owner_approval_request",
    "owner_approval_issuance",
    "package_boundary",
    "pre_runtime_package_closure",
    "execution_planning",
)

TEMPLATE_STAGE_OUTPUTS: Dict[str, str] = {
    "chain_closure": "chain_status=sealed",
    "trial_planning": "trial_planning_go",
    "owner_approval_request": "owner_approval_request_go",
    "owner_approval_issuance": "owner_approval_issuance_go",
    "package_boundary": "package_boundary_go",
    "pre_runtime_package_closure": "pre_runtime_package_status=sealed",
    "execution_planning": "execution_planning_go",
}

TEMPLATE_POLICIES: Tuple[str, ...] = (
    "execution_planning_is_terminal_planning_stage_by_default",
    "no_further_gate_package_issuance_split_after_execution_planning",
    "future_capability_lines_reuse_template_by_default",
    "observation_offline_replay_may_compress_to_chain_closure_trial_planning_package_boundary_pre_runtime_closure",
    "owner_approval_not_required_requires_explicit_owner_approval_not_required_reason",
    "default_runtime_trial_requires_owner_approval",
    "live_runtime_live_sensor_direct_speech_action_fact_write_requires_activation_specific_governance",
    "planning_only_closure_cannot_authorize_runtime_activation",
)

COMPRESSED_MODE_STAGES: Tuple[str, ...] = (
    "chain_closure",
    "trial_planning",
    "package_boundary",
    "pre_runtime_package_closure",
)

FULL_MODE_STAGES: Tuple[str, ...] = TEMPLATE_STAGES

REUSE_TARGET_DOMAINS: Tuple[str, ...] = (
    "ocr",
    "vision_model",
    "slam",
    "asr",
    "tracking",
    "scene_graph",
    "phase_one_environment_cognition",
)

DEFAULT_REUSE_FLAGS: Dict[str, bool] = {
    "runtime_activation_allowed_default": False,
    "live_sensor_allowed_default": False,
    "direct_action_allowed_default": False,
    "direct_speech_allowed_default": False,
    "direct_fact_write_allowed_default": False,
}


@dataclass(frozen=True)
class ControlledTrialGovernanceStage:
    stage_id: str
    stage_zh: str
    expected_output: str
    source_chain: str


@dataclass(frozen=True)
class ControlledTrialGovernanceStagePolicy:
    policy_ref: str
    execution_planning_terminal_for_planning_only_chain: bool
    no_further_gate_package_issuance_split: bool
    future_governance_reuse_template_required: bool
    source_chain: str


@dataclass(frozen=True)
class ControlledTrialGovernanceCompressionPolicy:
    policy_ref: str
    compressed_mode_allowed: bool
    compressed_stages: Tuple[str, ...]
    full_stages: Tuple[str, ...]
    owner_approval_not_required_requires_reason: bool
    source_chain: str


@dataclass(frozen=True)
class ControlledTrialGovernanceReuseProfile:
    reuse_profile_id: str
    target_domain: str
    target_model_or_capability_family: str
    upstream_chain_ref: str
    governance_template_ref: str
    required_stages: Tuple[str, ...]
    optional_stages: Tuple[str, ...]
    compressed_mode_allowed: bool
    owner_approval_required: bool
    runtime_activation_allowed_default: bool = False
    live_sensor_allowed_default: bool = False
    direct_action_allowed_default: bool = False
    direct_speech_allowed_default: bool = False
    direct_fact_write_allowed_default: bool = False


@dataclass(frozen=True)
class ControlledTrialGovernanceLifecycleTemplate:
    template_id: str
    template_phase_ref: str
    stages: Tuple[ControlledTrialGovernanceStage, ...]
    stage_policy: ControlledTrialGovernanceStagePolicy
    compression_policy: ControlledTrialGovernanceCompressionPolicy
    reuse_profiles: Tuple[ControlledTrialGovernanceReuseProfile, ...]
    governance_policies: Tuple[str, ...]
    source_chain: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)


def build_controlled_trial_governance_stages_v1() -> Tuple[ControlledTrialGovernanceStage, ...]:
    stage_zh_map = {
        "chain_closure": "上游 candidate chain 已 sealed",
        "trial_planning": "定义 scenario admission level、blocked / observation-only / cautious / low-risk trial candidate",
        "owner_approval_request": "将 trial planning 转为 owner approval request",
        "owner_approval_issuance": "固化 request item 的 issuance status",
        "package_boundary": "封装 trial package，声明 allowed / blocked operations、rollback、observation log、failure handling",
        "pre_runtime_package_closure": "合并 planning / request / issuance / package boundary，封存 pre-runtime package",
        "execution_planning": "仅规划 controlled replay / execution plan，不启动 runtime",
    }
    return tuple(
        ControlledTrialGovernanceStage(
            stage_id=stage_id,
            stage_zh=stage_zh_map[stage_id],
            expected_output=TEMPLATE_STAGE_OUTPUTS[stage_id],
            source_chain=SOURCE_CHAIN,
        )
        for stage_id in TEMPLATE_STAGES
    )


def build_controlled_trial_governance_reuse_profiles_v1() -> Tuple[ControlledTrialGovernanceReuseProfile, ...]:
    profiles: Tuple[ControlledTrialGovernanceReuseProfile, ...] = ()
    for domain in REUSE_TARGET_DOMAINS:
        required = FULL_MODE_STAGES
        optional: Tuple[str, ...] = ()
        owner_required = True
        compressed_allowed = domain in ("ocr", "vision_model", "asr", "tracking", "scene_graph")
        if compressed_allowed:
            optional = (
                "owner_approval_request",
                "owner_approval_issuance",
            )
        profiles += (
            ControlledTrialGovernanceReuseProfile(
                reuse_profile_id=f"{domain}_controlled_trial_governance_reuse_v1",
                target_domain=domain,
                target_model_or_capability_family=domain,
                upstream_chain_ref=f"Phase-{domain.replace('_', '-').title()}-Chain-Closure-v1-001",
                governance_template_ref=TEMPLATE_ID,
                required_stages=required if not compressed_allowed else COMPRESSED_MODE_STAGES,
                optional_stages=optional,
                compressed_mode_allowed=compressed_allowed,
                owner_approval_required=owner_required,
                **DEFAULT_REUSE_FLAGS,
            ),
        )
    return profiles


def build_controlled_trial_governance_lifecycle_template_v1() -> ControlledTrialGovernanceLifecycleTemplate:
    return ControlledTrialGovernanceLifecycleTemplate(
        template_id=TEMPLATE_ID,
        template_phase_ref=TEMPLATE_PHASE_REF,
        stages=build_controlled_trial_governance_stages_v1(),
        stage_policy=ControlledTrialGovernanceStagePolicy(
            policy_ref="controlled_trial_governance_stage_policy_v1",
            execution_planning_terminal_for_planning_only_chain=True,
            no_further_gate_package_issuance_split=True,
            future_governance_reuse_template_required=True,
            source_chain=SOURCE_CHAIN,
        ),
        compression_policy=ControlledTrialGovernanceCompressionPolicy(
            policy_ref="controlled_trial_governance_compression_policy_v1",
            compressed_mode_allowed=True,
            compressed_stages=COMPRESSED_MODE_STAGES,
            full_stages=FULL_MODE_STAGES,
            owner_approval_not_required_requires_reason=True,
            source_chain=SOURCE_CHAIN,
        ),
        reuse_profiles=build_controlled_trial_governance_reuse_profiles_v1(),
        governance_policies=TEMPLATE_POLICIES,
        source_chain=SOURCE_CHAIN,
    )


def build_controlled_trial_governance_lifecycle_template_matrix_v1() -> Dict[str, Any]:
    template = build_controlled_trial_governance_lifecycle_template_v1()
    return {
        "template_id": TEMPLATE_ID,
        "template_phase_ref": TEMPLATE_PHASE_REF,
        "source_chain": SOURCE_CHAIN,
        "controlled_trial_governance_lifecycle_template": candidate_to_dict(template),
        "template_stages": [candidate_to_dict(s) for s in template.stages],
        "template_stage_count": len(template.stages),
        "governance_policies": list(TEMPLATE_POLICIES),
        "compressed_mode_stages": list(COMPRESSED_MODE_STAGES),
        "full_mode_stages": list(FULL_MODE_STAGES),
        "reuse_profiles": [candidate_to_dict(p) for p in template.reuse_profiles],
    }
