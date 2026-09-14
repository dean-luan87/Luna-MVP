# -*- coding: utf-8 -*-
"""Test Board Planning-Mode Protocol Patch — types v1.

A lightweight patch to TestBoardProtectedArtifactRuleV1 that promotes "planning"
to a first-class, valid test_mode so later planning phases no longer borrow
"virtual_test" (with a test_mode_label="planning" workaround).

This phase patches the test board protocol enum / validation logic ONLY. It does
NOT change the protected / non-deletable rules, NOT migrate old records, NOT
delete old records, NOT rewrite existing test board records, and does NOT enter
model install / download / inference / runtime / semantic layer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.test_board.test_board_protocol_v1 import (
    PROTOCOL_ID,
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
SCOPE = "test_board_planning_mode_protocol_patch"
SOURCE_CHAIN = "test_board_planning_mode_protocol_patch_v1"

PLANNING_PRINCIPLE_ZH = (
    "对 TestBoardProtectedArtifactRuleV1 做轻量协议补丁，将 planning 正式纳入测试板块合法 test_mode。"
    "只修改测试板块协议枚举与验证逻辑，不改变 protected / non-deletable 规则，不迁移旧记录，不删除旧记录，"
    "不重写已有测试板块记录，不进入模型安装、不下载、不推理、不进入 runtime、不进入语义层。"
    "planning 不替代 virtual_test；dry_run / real_test / runtime_trial / post_review / closure_review 均保持兼容。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "test_board_planning_mode_protocol_patch_is_enum_and_validation_patch_only_no_migration_no_runtime_no_inference"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
PROTOCOL_PATCH_ONLY = True
PLANNING_TEST_MODE_ADDED = True
EXISTING_TEST_MODES_PRESERVED = True
PROTECTED_ARTIFACT_RULE_PRESERVED = True
NON_DELETABLE_RULE_PRESERVED = True
BACKWARD_COMPATIBILITY_PRESERVED = True
EXISTING_RECORDS_NOT_MODIFIED = True
EXISTING_RECORDS_NOT_DELETED = True
MIGRATION_NOT_PERFORMED = True

PLANNING_MODE = "planning"

# Upstream references.
TEST_BOARD_PROTOCOL_REF = PROTOCOL_ID
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF = "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001"

# Test board binding for THIS phase.
TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"  # this phase dogfoods the new mode.

# Expected post-patch allowed modes (>= 7).
EXPECTED_ALLOWED_TEST_MODES: Tuple[str, ...] = (
    "planning",
    "virtual_test",
    "dry_run",
    "real_test",
    "runtime_trial",
    "post_review",
    "closure_review",
)

LEGACY_TEST_MODES: Tuple[str, ...] = (
    "virtual_test",
    "dry_run",
    "real_test",
    "runtime_trial",
    "post_review",
    "closure_review",
)

# --------------------------------------------------------------------------- #
# Backfill notes (no migration; informational only).
# --------------------------------------------------------------------------- #
BACKFILL_NOTES: Dict[str, bool] = {
    "historical_virtual_test_planning_label_allowed": True,
    "planning_mode_available_for_future_records": True,
    "old_records_remain_valid": True,
    "future_planning_should_use_planning_mode": True,
}

# --------------------------------------------------------------------------- #
# Negative guards (11: A..K)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_planning_not_in_allowed_modes", "go_key": "planning_in_allowed_modes", "depends_on": "planning_in_allowed_modes"},
    {"guard_id": "invalid_b_planning_forced_to_virtual_test", "go_key": "planning_not_coerced_to_virtual_test", "depends_on": "planning_not_coerced_to_virtual_test"},
    {"guard_id": "invalid_c_planning_write_missing_six_records", "go_key": "planning_six_protected_records_present", "depends_on": "planning_six_protected_records_present"},
    {"guard_id": "invalid_d_planning_write_missing_manifest", "go_key": "planning_manifest_present", "depends_on": "planning_manifest_present"},
    {"guard_id": "invalid_e_planning_records_not_protected", "go_key": "planning_records_protected_non_deletable", "depends_on": "planning_records_protected_non_deletable"},
    {"guard_id": "invalid_f_planning_breaks_virtual_test", "go_key": "virtual_test_still_valid", "depends_on": "virtual_test_still_valid"},
    {"guard_id": "invalid_g_planning_breaks_other_modes", "go_key": "other_legacy_modes_still_valid", "depends_on": "other_legacy_modes_still_valid"},
    {"guard_id": "invalid_h_patch_migrates_or_deletes_existing_records", "go_key": "existing_records_untouched", "depends_on": "existing_records_untouched"},
    {"guard_id": "invalid_i_cleanup_deletes_planning_artifact", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
    {"guard_id": "invalid_j_phase_does_not_write_own_test_board", "go_key": "phase_writes_own_test_board", "depends_on": "phase_writes_own_test_board"},
    {"guard_id": "invalid_k_patch_used_to_approve_runtime_install_inference", "go_key": "patch_not_runtime_install_inference_approval", "depends_on": "patch_not_runtime_install_inference_approval"},
)

# --------------------------------------------------------------------------- #
# Governance rules (TestBoard 6 preserved + 17 phase patch rules)
# --------------------------------------------------------------------------- #
PATCH_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_test_board_protocol_patch_only",
    "planning_test_mode_must_be_supported",
    "planning_test_mode_must_not_replace_virtual_test",
    "existing_test_modes_must_remain_valid",
    "existing_records_must_not_be_modified",
    "existing_records_must_not_be_deleted",
    "no_migration_is_performed_in_this_phase",
    "planning_records_must_be_protected",
    "planning_records_must_be_non_deletable",
    "planning_records_must_include_manifest",
    "planning_records_must_include_test_process_record",
    "planning_records_must_include_test_conclusion_record",
    "cleanup_must_not_delete_planning_test_board_artifacts",
    "protocol_patch_success_is_not_runtime_approval",
    "protocol_patch_success_is_not_install_approval",
    "protocol_patch_success_is_not_inference_approval",
    "protocol_patch_success_is_not_semantic_layer_approval",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    PATCH_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)
REQUIRED_RECORD_TYPES_LOCAL: Tuple[str, ...] = tuple(REQUIRED_RECORD_TYPES)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "PlanningModeProtocolPatchProfile",
    "TestModeEnumPatchRecord",
    "PlanningWriteVerificationRecord",
    "ModeCompatibilityCheck",
    "BackfillNoteRecord",
    "NegativePatchGuard",
    "PlanningModeProtocolPatchDecision",
)

FINAL_DECISION_GO = "TEST_BOARD_PLANNING_MODE_PROTOCOL_PATCH_GO"
FINAL_DECISION_BLOCKED = "TEST_BOARD_PLANNING_MODE_PROTOCOL_PATCH_BLOCKED"

PATCH_FLAGS: Dict[str, bool] = {
    "protocol_patch_only": PROTOCOL_PATCH_ONLY,
    "planning_test_mode_added": PLANNING_TEST_MODE_ADDED,
    "existing_test_modes_preserved": EXISTING_TEST_MODES_PRESERVED,
    "protected_artifact_rule_preserved": PROTECTED_ARTIFACT_RULE_PRESERVED,
    "non_deletable_rule_preserved": NON_DELETABLE_RULE_PRESERVED,
    "backward_compatibility_preserved": BACKWARD_COMPATIBILITY_PRESERVED,
    "existing_records_not_modified": EXISTING_RECORDS_NOT_MODIFIED,
    "existing_records_not_deleted": EXISTING_RECORDS_NOT_DELETED,
    "migration_not_performed": MIGRATION_NOT_PERFORMED,
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
    "semantic_promotion_allowed": False,
    "vla_action_chain_allowed": False,
}


@dataclass(frozen=True)
class PlanningModeProtocolPatchProfile:
    profile_ref: str
    phase_id: str
    protocol_patch_only: bool
    planning_test_mode_added: bool
    existing_test_modes_preserved: bool
    protected_artifact_rule_preserved: bool
    non_deletable_rule_preserved: bool
    backward_compatibility_preserved: bool
    test_board_protocol_ref: str
    registry_planning_ref: str
    p1_real_install_local_availability_ref: str
    luna_core_principle: str
    expected_allowed_test_modes: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class TestModeEnumPatchRecord:
    planning_added: bool
    allowed_test_modes: Tuple[str, ...]
    allowed_test_mode_count: int
    planning_does_not_replace_virtual_test: bool
    legacy_modes_preserved: bool


@dataclass(frozen=True)
class PlanningWriteVerificationRecord:
    test_mode_used: str
    write_accepted: bool
    manifest_written: bool
    manifest_test_mode: str
    protected_record_count: int
    all_records_test_mode_planning: bool
    all_records_protected: bool
    all_records_non_deletable: bool
    all_records_deletion_forbidden: bool
    required_record_types_present: Tuple[str, ...]


@dataclass(frozen=True)
class ModeCompatibilityCheck:
    test_mode: str
    valid: bool
    semantics_preserved: bool
    note: str


@dataclass(frozen=True)
class BackfillNoteRecord:
    note_key: str
    value: bool


@dataclass
class NegativePatchGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PlanningModeProtocolPatchDecision:
    decision_ref: str
    protocol_patch_profile_count: int
    allowed_test_mode_count: int
    mode_compatibility_check_count: int
    planning_protected_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
