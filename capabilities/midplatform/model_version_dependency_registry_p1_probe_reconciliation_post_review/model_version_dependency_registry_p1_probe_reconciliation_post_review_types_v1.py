# -*- coding: utf-8 -*-
"""Midplatform Registry <-> P1 Probe Reconciliation Post-Review — types v1.

A pure post-review that reconciles, asset by asset, the midplatform model
version/dependency registry (Phase-Midplatform-Model-Version-Dependency-Registry-
Planning) against the P1 real-install local-availability probe results
(Phase-P1-Real-Install-Local-Availability-DryRun).

It only audits/aligns; it does NOT modify the registry, NOT modify the probe
results, NOT add capability, NOT install, NOT download, NOT run inference, NOT
enter runtime, NOT promote anything to runtime eligible, NOT enter the semantic
layer. Reconciliation success is NOT runtime/install/inference approval.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
SCOPE = "model_version_dependency_registry_p1_probe_reconciliation_post_review"
SOURCE_CHAIN = "model_version_dependency_registry_p1_probe_reconciliation_post_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "纯 post-review：逐条对齐中台模型版本/依赖 registry 与 P1 本地可用性探针结果。只做对账/对齐审计，"
    "不修改 registry、不修改探针结果、不新增能力、不安装、不下载、不推理、不进入 runtime、不把任何资产升为 "
    "runtime eligible、不进入语义层。对账成功不等于 runtime/install/inference 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "registry_p1_probe_reconciliation_is_post_review_only_no_mutation_no_runtime_no_inference_no_install"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
RECONCILIATION_ONLY = True
REGISTRY_MUTATION_ALLOWED = False
PROBE_MUTATION_ALLOWED = False
NEW_CAPABILITY_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True

REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF = "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001"
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"

TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding (post-review semantics).
TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "post_review"

# --------------------------------------------------------------------------- #
# Asset id alias map: registry_asset_id -> p1_probe_asset_id.
# Only sam2 differs (registry observation node naming vs probe id).
# --------------------------------------------------------------------------- #
REGISTRY_TO_P1_ASSET_ALIAS: Dict[str, str] = {
    "sam2_observation_node": "sam2",
}

# Divergence kinds.
DIV_MATCH = "MATCH"
DIV_ALIAS = "ALIAS"
DIV_EXPECTED = "EXPECTED_DIVERGENCE"
DIV_MISMATCH = "MISMATCH"

# Reconciled (non-blocking) divergence kinds.
RECONCILED_KINDS: Tuple[str, ...] = (DIV_MATCH, DIV_ALIAS, DIV_EXPECTED)

# P1 install-readiness "restricted" buckets (not currently executable).
P1_RESTRICTED_STATES: Tuple[str, ...] = (
    "BLOCKED_BY_LICENSE",
    "DEFERRED_RESOURCE_HEAVY",
    "RESERVED_ONLY",
)

# --------------------------------------------------------------------------- #
# Negative guards (12: A..L)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_registry_mutated", "go_key": "registry_not_modified", "depends_on": "registry_not_modified"},
    {"guard_id": "invalid_b_probe_results_mutated", "go_key": "p1_probe_not_modified", "depends_on": "p1_probe_not_modified"},
    {"guard_id": "invalid_c_reconciliation_promotes_runtime_eligible", "go_key": "no_runtime_eligible_promotion", "depends_on": "no_runtime_eligible_promotion"},
    {"guard_id": "invalid_d_package_visible_as_runtime_approval", "go_key": "package_visibility_not_runtime_approval", "depends_on": "package_visibility_not_runtime_approval"},
    {"guard_id": "invalid_e_weight_visible_as_inference_approval", "go_key": "weight_visibility_not_inference_approval", "depends_on": "weight_visibility_not_inference_approval"},
    {"guard_id": "invalid_f_agpl_unknown_as_commercial_runtime", "go_key": "agpl_unknown_not_commercial_runtime", "depends_on": "agpl_unknown_not_commercial_runtime"},
    {"guard_id": "invalid_g_reserved_deferred_promoted_executable", "go_key": "reserved_deferred_not_executable", "depends_on": "reserved_deferred_not_executable"},
    {"guard_id": "invalid_h_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_i_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_j_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_k_test_record_not_written_to_board", "go_key": "test_board_record_required_enforced", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_l_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (phase 16 + test board 6)
# --------------------------------------------------------------------------- #
RECONCILIATION_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_registry_p1_probe_reconciliation_post_review_only",
    "registry_must_not_be_modified",
    "p1_probe_results_must_not_be_modified",
    "no_new_capability_is_created",
    "reconciliation_does_not_promote_any_asset_to_runtime_eligible",
    "package_visibility_is_not_runtime_approval",
    "weight_visibility_is_not_inference_approval",
    "agpl_unknown_research_only_license_is_not_commercial_runtime",
    "reserved_only_and_deferred_families_are_not_executable",
    "runtime_trial_eligibility_remains_false_for_all_assets",
    "candidate_only_boundary_is_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "reconciliation_success_is_not_runtime_install_inference_semantic_approval",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    RECONCILIATION_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RegistryP1ReconciliationProfile",
    "AssetReconciliationRecord",
    "RestrictedBucketAgreement",
    "NonRuntimeEligibilityAudit",
    "ReconciliationDivergenceNote",
    "NegativeReconciliationGuard",
    "RegistryP1ReconciliationDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_planning_dryrun_readiness_recorded",
    },
)

FINAL_DECISION_GO = "MIDPLATFORM_REGISTRY_P1_PROBE_RECONCILIATION_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "MIDPLATFORM_REGISTRY_P1_PROBE_RECONCILIATION_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
}

POST_REVIEW_TRUE_INVARIANTS: Dict[str, bool] = {
    "registry_not_modified": True,
    "p1_probe_not_modified": True,
    "no_runtime_eligible_promotion": True,
    "package_visibility_not_runtime_approval": True,
    "weight_visibility_not_inference_approval": True,
    "agpl_unknown_not_commercial_runtime": True,
    "reserved_deferred_not_executable": True,
    "runtime_trial_eligibility_all_false": True,
    "candidate_only_boundary_preserved": True,
    "reconciliation_success_not_runtime_install_inference_approval": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_install_performed": False,
    "dependency_install_performed": False,
    "model_download_performed": False,
    "weight_download_performed": False,
    "dataset_download_performed": False,
    "real_inference_performed": False,
    "runtime_execution_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "semantic_promotion_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RegistryP1ReconciliationProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    reconciliation_only: bool
    registry_mutation_allowed: bool
    probe_mutation_allowed: bool
    new_capability_created: bool
    controlled_trial_template_reused: bool
    registry_planning_ref: str
    p1_real_install_local_availability_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class AssetReconciliationRecord:
    asset_id: str
    registry_asset_id: str
    id_alias_used: bool
    import_name_match: bool
    license_type_match: bool
    weight_required_match: bool
    reserved_match: bool
    restricted_in_registry: bool
    restricted_in_p1: bool
    restricted_agreement: bool
    registry_runtime_eligibility_level: int
    p1_can_enter_runtime_trial: bool
    runtime_eligibility_consistent_not_eligible: bool
    p1_install_readiness_state: str
    registry_risk_level: str
    divergence_kind: str
    divergence_note: str
    reconciled: bool


@dataclass(frozen=True)
class RestrictedBucketAgreement:
    asset_id: str
    registry_bucket: str
    p1_bucket: str
    agree_restricted: bool


@dataclass(frozen=True)
class NonRuntimeEligibilityAudit:
    asset_id: str
    registry_runtime_eligibility_level: int
    p1_can_enter_runtime_trial: bool
    not_runtime_eligible: bool


@dataclass(frozen=True)
class ReconciliationDivergenceNote:
    asset_id: str
    divergence_kind: str
    note: str
    is_blocker: bool


@dataclass
class NegativeReconciliationGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ReconciliationHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class RegistryP1ReconciliationDecision:
    decision_ref: str
    reconciliation_profile_count: int
    asset_reconciliation_record_count: int
    import_name_match_count: int
    license_type_match_count: int
    weight_required_match_count: int
    reserved_match_count: int
    restricted_agreement_count: int
    runtime_eligibility_consistent_count: int
    divergence_blocker_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
