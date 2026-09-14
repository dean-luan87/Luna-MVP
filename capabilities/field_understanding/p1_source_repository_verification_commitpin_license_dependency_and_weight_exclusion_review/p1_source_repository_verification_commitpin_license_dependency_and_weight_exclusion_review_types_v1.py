# -*- coding: utf-8 -*-
"""P1 Source Repository Verification / CommitPin / License / Dependency /
Weight-Exclusion Review — types v1 (NETWORK-ENABLED REVIEW, READONLY EVIDENCE).

Network-enabled review for byte_track and mobile_sam. This phase performs scoped,
readonly network lookups (repository metadata, file listings, license files,
dependency manifests, commit/tag metadata, large-file / git-lfs indicators) and
records evidence-backed findings. It executes NO git clone, NO source checkout, NO
source install, NO pip install, NO dependency install, NO model/weight/checkpoint/
dataset/example download, NO real import, NO model load, NO inference, NO runtime,
NO output adapter, NO semantic layer and NO registry mutation. All network access
is logged in a readonly evidence log. Vague evidence must never be marked verified.

License review is NOT commercial-runtime approval; dependency review is NOT
dependency-install approval; commit pin is NOT source-execution approval; and
mobile_sam weight-excluding checkout feasibility is NOT weight-download approval.
Source-execution retry must not execute in this phase even if readiness is reached.
Protected, non-deletable test board records are written in real_test mode.

The embedded EVIDENCE_* constants below were collected via real, scoped, readonly
GitHub REST API lookups (api.github.com, readonly GET) during this phase. No clone
or download of weight/checkpoint files was performed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Review-v1-001"
SCOPE = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review"
SOURCE_CHAIN = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_v1"

REVIEW_PRINCIPLE_ZH = (
    "byte_track 与 mobile_sam 的带网络检索 review：用 scoped、只读网络证据完成 repository verification、commit pin "
    "resolution、license review、dependency manifest review，以及 mobile_sam weight-excluding checkout 可行性复核。"
    "允许 scoped network lookup 与只读证据采集，但所有访问必须记录证据日志；不 clone、不 checkout、不源码安装、不 pip "
    "install、不安装依赖、不下载模型/权重/checkpoint/数据集/示例资产、不真实 import / model load / inference、不进入 "
    "runtime / output adapter / 语义层、不修改 registry。模糊证据不得伪造成 verified。license review 不等于 commercial "
    "runtime 批准；dependency review 不等于安装批准；commit pin 不等于执行批准；weight-excluding 可行性不等于权重下载批准。"
    "即使 readiness 达成，本阶段也不得执行 retry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_repository_review_is_scoped_readonly_network_evidence_only_no_clone_no_install_no_weight_download_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REVIEW_PHASE = True
SCOPED_NETWORK_LOOKUP_ALLOWED = True
READONLY_NETWORK_EVIDENCE_COLLECTION_ALLOWED = True
REPOSITORY_VERIFICATION_REVIEW = True
COMMIT_PIN_REVIEW = True
LICENSE_REVIEW = True
DEPENDENCY_REVIEW = True
WEIGHT_EXCLUSION_REVIEW = True

REGISTRY_MUTATION_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_CHECKOUT_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False
WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL = True
NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_SUCCESSFUL_SOURCE_EXECUTION_POST_REVIEW = True
SOURCE_EXECUTION_RETRY_NOT_ALLOWED_WITHOUT_READINESS_GATE = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PLANNING_REF = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Planning-v1-001"
UPSTREAM_PLANNING_EXPECTED_GO = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routing targets.
NEXT_PHASE_RETRY = "Phase-P1-Controlled-Source-Install-Execution-Retry-And-Post-Review-v1-001"
NEXT_PHASE_REVIEW_POST_REVIEW = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Review-Post-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Input scope.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

BLOCKED_WEIGHT_PATTERNS: Tuple[str, ...] = (
    "*.pth", "*.pt", "*.ckpt", "*.safetensors", "*.onnx", "*.bin", "*.h5", "*.pb",
)

ALLOWED_EVIDENCE_TYPES: Tuple[str, ...] = (
    "repository_metadata",
    "repository_file_listing",
    "license_file",
    "requirements_file",
    "pyproject_or_setup_file",
    "release_or_tag_metadata",
    "commit_metadata",
    "large_file_indicator",
    "git_lfs_indicator",
)

# Per-asset readiness fields evaluated by the gate (10 + mobile_sam extras).
RETRY_READINESS_FIELDS: Tuple[str, ...] = (
    "repository_url_verified",
    "commit_hash_pinned",
    "license_review_completed",
    "dependency_review_completed",
    "network_boundary_finalized",
    "source_checkout_strategy_finalized",
    "rollback_ready",
    "test_board_ready",
)

RISK_DIMENSIONS: Tuple[str, ...] = (
    "repository_identity_risk",
    "commit_drift_risk",
    "license_unknown_or_restrictive_risk",
    "dependency_unknown_risk",
    "build_or_compile_risk",
    "network_scope_risk",
    "weight_download_contamination_risk",
    "environment_contamination_risk",
    "rollback_complexity_risk",
    "runtime_misreadiness_risk",
)

# --------------------------------------------------------------------------- #
# Embedded REAL evidence collected via scoped readonly GitHub REST lookups.
# (api.github.com, readonly GET; no clone, no archive/weight download.)
# --------------------------------------------------------------------------- #
EVIDENCE_NETWORK_DOMAIN = "api.github.com"

EVIDENCE_REPOSITORY: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "repository_url": "https://github.com/FoundationVision/ByteTrack",
        "repository_owner": "FoundationVision",
        "repository_name": "ByteTrack",
        "redirected_from": "https://github.com/ifzhang/ByteTrack",
        "api_repo_id": 400476704,
        "default_branch": "main",
        "is_fork": False,
        "is_archived": False,
        "repository_url_verified": True,
        "repository_identity_confidence": "high",
        "repository_identity_rationale": (
            "api.github.com/repos/ifzhang/ByteTrack returned HTTP 301 -> repository id 400476704 -> "
            "FoundationVision/ByteTrack (canonical ByteTrack source, YOLOX-based, default_branch=main, not a fork, "
            "not archived). Root listing contains yolox/ source package, requirements.txt, setup.py, setup.cfg, LICENSE."
        ),
        "package_import_identity_unresolved_or_source_component": True,
        "package_import_identity_note": (
            "importable module is the in-repo `yolox` source package (+ tools), not a clean PyPI `byte_track` wheel; "
            "byte_track remains a source component, so code-only source checkout is required."
        ),
        "repository_may_contain_committed_checkpoint_weight": False,
        "root_listing": (
            ".gitignore", "Dockerfile", "LICENSE", "README.md", "assets", "datasets", "deploy", "exps",
            "requirements.txt", "setup.cfg", "setup.py", "tools", "tutorials", "videos", "yolox",
        ),
        "git_lfs_detected": False,
        "committed_weight_files_detected": False,
        "repository_verification_completed": True,
    },
    "mobile_sam": {
        "repository_url": "https://github.com/ChaoningZhang/MobileSAM",
        "repository_owner": "ChaoningZhang",
        "repository_name": "MobileSAM",
        "redirected_from": None,
        "api_repo_id": None,
        "default_branch": "master",
        "is_fork": False,
        "is_archived": False,
        "repository_url_verified": True,
        "repository_identity_confidence": "high",
        "repository_identity_rationale": (
            "api.github.com/repos/ChaoningZhang/MobileSAM returned canonical MobileSAM source (default_branch=master, "
            "not a fork, not archived). Root listing contains mobile_sam/ package, setup.py, setup.cfg, LICENSE and a "
            "weights/ directory."
        ),
        "package_import_identity_unresolved_or_source_component": True,
        "package_import_identity_note": (
            "setup.py declares name='mobile_sam' (find_packages); importable module is the in-repo `mobile_sam` source "
            "package, installed from source (not a maintained PyPI wheel)."
        ),
        "repository_may_contain_committed_checkpoint_weight": True,
        "root_listing": (
            ".gitignore", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "LICENSE", "Member.txt", "MobileSAMv2",
            "README.md", "app", "assets", "linter.sh", "mobile_sam", "notebooks", "scripts", "setup.cfg",
            "setup.py", "weights",
        ),
        "git_lfs_detected": False,
        "committed_weight_files_detected": True,
        "committed_weight_files": ("weights/mobile_sam.pt",),
        "committed_weight_total_bytes": 40728226,
        "committed_weight_note": (
            "weights/mobile_sam.pt is a ~40MB blob returned directly by the contents API (size=40728226, not a ~130B "
            "git-lfs pointer), and the repo has no .gitattributes (HTTP 404), so the checkpoint is a committed regular "
            "blob. A full clone of MobileSAM would therefore equal a weight download."
        ),
        "repository_verification_completed": True,
    },
}

EVIDENCE_COMMIT: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "branch_or_tag_candidate": "main",
        "commit_hash": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "commit_date": "2022-12-11T07:05:00Z",
        "commit_hash_resolved": True,
        "commit_pin_confidence": "high",
        "commit_pin_rationale": (
            "Latest commit on FoundationVision/ByteTrack default branch main resolved via "
            "api.github.com/repos/.../commits?sha=main&per_page=1."
        ),
        "commit_pin_completed": True,
    },
    "mobile_sam": {
        "branch_or_tag_candidate": "master",
        "commit_hash": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "commit_date": "2026-05-05T11:00:12Z",
        "commit_hash_resolved": True,
        "commit_pin_confidence": "high",
        "commit_pin_rationale": (
            "Latest commit on ChaoningZhang/MobileSAM default branch master resolved via "
            "api.github.com/repos/.../commits?sha=master&per_page=1."
        ),
        "commit_pin_completed": True,
    },
}

EVIDENCE_LICENSE: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "license_file_found": True,
        "license_type_candidate": "MIT",
        "license_review_confidence": "high",
        "license_review_rationale": (
            "GitHub repo metadata license.spdx_id=MIT and a root LICENSE file (1067 bytes) is present."
        ),
        "source_install_allowed_by_license_for_trial": True,
        "license_review_completed": True,
    },
    "mobile_sam": {
        "license_file_found": True,
        "license_type_candidate": "Apache-2.0",
        "license_review_confidence": "high",
        "license_review_rationale": (
            "GitHub repo metadata license.spdx_id=Apache-2.0 and a root LICENSE file (11357 bytes) is present "
            "(code derived from Meta segment-anything, Apache-2.0). Note: the committed checkpoint weight is a "
            "separate artifact whose distribution terms are NOT covered by code-license review here."
        ),
        "source_install_allowed_by_license_for_trial": True,
        "license_review_completed": True,
    },
}

EVIDENCE_DEPENDENCY: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "dependency_manifest_found": True,
        "dependency_manifest_refs": ("requirements.txt", "setup.py", "setup.cfg"),
        "torch_dependency_detected": True,
        "opencv_dependency_detected": True,
        "numpy_scipy_dependency_detected": True,
        "build_compile_risk_detected": True,
        "dependency_conflict_risk_detected": True,
        "dependency_risk_summary": (
            "requirements.txt requires numpy, torch>=1.7, torchvision>=0.10.0, opencv_python, plus lap/filterpy/"
            "motmetrics/thop/ninja and pinned onnx==1.8.1 / onnxruntime==1.8.0 / onnx-simplifier==0.3.5 (old pins -> "
            "conflict risk). HIGH build/compile risk: setup.py imports torch and builds C++ extensions via "
            "torch.utils.cpp_extension.CppExtension over yolox/layers/csrc (requires torch + a C++ toolchain at build "
            "time); lap typically needs compilation too."
        ),
        "dependency_review_completed": True,
    },
    "mobile_sam": {
        "dependency_manifest_found": True,
        "dependency_manifest_refs": ("setup.py", "setup.cfg"),
        "torch_dependency_detected": True,
        "opencv_dependency_detected": True,
        "numpy_scipy_dependency_detected": True,
        "build_compile_risk_detected": False,
        "dependency_conflict_risk_detected": True,
        "dependency_risk_summary": (
            "setup.py declares name='mobile_sam' with install_requires=[] (EMPTY) and extras_require['all']="
            "[matplotlib, pycocotools, opencv-python, onnx, onnxruntime]. torch/torchvision are UNDECLARED runtime "
            "dependencies (code is segment-anything-derived and requires torch), so a code-only install will import-"
            "fail without torch present -> undeclared-dependency risk. No C++ build extensions (pure-python packaging, "
            "low build/compile risk)."
        ),
        "dependency_review_completed": True,
    },
}

# mobile_sam weight-excluding checkout feasibility (evidence-backed).
EVIDENCE_MOBILE_SAM_WEIGHT_EXCLUSION: Dict[str, Any] = {
    "committed_weight_files_detected": True,
    "committed_weight_files": ("weights/mobile_sam.pt",),
    "committed_weight_total_bytes": 40728226,
    "git_lfs_detected": False,
    "sparse_checkout_feasible": True,
    "archive_filtering_feasible": True,
    "code_only_checkout_feasible": True,
    "full_clone_allowed_for_mobile_sam_next_execution": False,
    "mobile_sam_weight_exclusion_review_completed": True,
    "feasibility_rationale": (
        "weights/mobile_sam.pt (~40MB) is a committed regular blob (not git-lfs; no .gitattributes). A plain full "
        "clone WOULD pull the checkpoint (== weight download) and is therefore blocked. Code-only checkout is feasible "
        "via git sparse-checkout excluding weights/ and *.pt (cone or non-cone), or via a filtered archive/tarball that "
        "drops weights/*. The blocked file patterns (*.pth,*.pt,*.ckpt,*.safetensors,*.onnx,*.bin,*.h5,*.pb) must be "
        "enforced before any retry. This feasibility review is NOT weight-download approval."
    ),
}

# --------------------------------------------------------------------------- #
# Negative guards (21: Invalid A..U).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_git_clone_or_source_checkout", "go_key": "no_clone_checkout", "depends_on": "no_clone_checkout"},
    {"guard_id": "invalid_b_source_pip_dependency_install", "go_key": "no_install", "depends_on": "no_install"},
    {"guard_id": "invalid_c_model_weight_checkpoint_dataset_example_download", "go_key": "no_download", "depends_on": "no_download"},
    {"guard_id": "invalid_d_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_e_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_f_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_g_network_access_not_logged", "go_key": "network_access_logged", "depends_on": "network_access_logged"},
    {"guard_id": "invalid_h_repository_url_marked_verified_without_evidence", "go_key": "repo_verified_evidence_backed", "depends_on": "repo_verified_evidence_backed"},
    {"guard_id": "invalid_i_commit_hash_marked_pinned_without_resolution", "go_key": "commit_pin_evidence_backed", "depends_on": "commit_pin_evidence_backed"},
    {"guard_id": "invalid_j_license_marked_completed_without_check", "go_key": "license_evidence_backed", "depends_on": "license_evidence_backed"},
    {"guard_id": "invalid_k_dependency_marked_completed_without_check", "go_key": "dependency_evidence_backed", "depends_on": "dependency_evidence_backed"},
    {"guard_id": "invalid_l_mobile_sam_weight_risk_not_checked", "go_key": "weight_risk_checked", "depends_on": "weight_risk_checked"},
    {"guard_id": "invalid_m_mobile_sam_full_clone_allowed_on_weight_risk", "go_key": "full_clone_blocked_on_weight_risk", "depends_on": "full_clone_blocked_on_weight_risk"},
    {"guard_id": "invalid_n_license_review_as_commercial_runtime_approval", "go_key": "license_not_runtime_approval", "depends_on": "license_not_runtime_approval"},
    {"guard_id": "invalid_o_dependency_review_as_install_approval", "go_key": "dependency_not_install_approval", "depends_on": "dependency_not_install_approval"},
    {"guard_id": "invalid_p_commit_pin_as_source_execution_approval", "go_key": "commit_not_exec_approval", "depends_on": "commit_not_exec_approval"},
    {"guard_id": "invalid_q_weight_exclusion_feasibility_as_weight_download_approval", "go_key": "feasibility_not_download_approval", "depends_on": "feasibility_not_download_approval"},
    {"guard_id": "invalid_r_source_execution_retry_executed_in_this_phase", "go_key": "retry_not_executed", "depends_on": "retry_not_executed"},
    {"guard_id": "invalid_s_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_t_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_u_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (43 phase + 6 test board = 49).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_repository_verification_commit_pin_license_dependency_and_weight_exclusion_review_only",
    "only_byte_track_and_mobile_sam_are_in_scope",
    "scoped_network_lookup_is_allowed",
    "all_network_lookup_must_be_logged",
    "network_lookup_is_readonly_evidence_collection_only",
    "no_git_clone_is_allowed",
    "no_source_checkout_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_checkpoint_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_example_asset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "repository_verification_must_be_evidence_backed",
    "commit_pin_must_be_evidence_backed",
    "license_review_must_be_evidence_backed",
    "dependency_review_must_be_evidence_backed",
    "mobile_sam_weight_excluding_checkout_feasibility_must_be_reviewed",
    "mobile_sam_full_clone_is_blocked_when_weight_risk_is_true_or_unknown",
    "license_review_is_not_commercial_runtime_approval",
    "dependency_review_is_not_dependency_install_approval",
    "commit_pin_is_not_source_execution_approval",
    "weight_excluding_checkout_feasibility_is_not_weight_download_approval",
    "source_execution_retry_must_not_execute_in_this_phase",
    "weight_download_is_not_approved",
    "no_weight_download_phase_until_successful_source_execution_post_review",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "repository_verification_evidence_record",
    "commit_pin_resolution_record",
    "license_review_evidence_record",
    "dependency_manifest_review_record",
    "mobile_sam_weight_exclusion_feasibility_record",
    "network_evidence_log_record",
    "source_execution_retry_readiness_gate_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionReviewProfile",
    "ScopedNetworkEvidenceLog",
    "SourceRepositoryVerificationEvidence",
    "SourceCommitPinResolutionEvidence",
    "SourceLicenseReviewEvidence",
    "SourceDependencyManifestReviewEvidence",
    "MobileSAMWeightExclusionFeasibilityReview",
    "SourceExecutionRetryReadinessGateReview",
    "SourceRepositoryVerificationReviewDecisionRecord",
    "SourceRepositoryReviewRiskRecord",
    "NegativeSourceRepositoryVerificationCommitPinReviewGuard",
    "P1SourceRepositoryVerificationCommitPinReviewDecision",
)

FINAL_DECISION_GO = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "planning_phase_evidence_plan_reused": True,
}


@dataclass(frozen=True)
class P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionReviewProfile:
    profile_ref: str
    phase_id: str
    review_phase: bool
    scoped_network_lookup_allowed: bool
    readonly_network_evidence_collection_allowed: bool
    repository_verification_review: bool
    commit_pin_review: bool
    license_review: bool
    dependency_review: bool
    weight_exclusion_review: bool
    registry_mutation_allowed: bool
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    example_asset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ScopedNetworkEvidenceLog:
    evidence_id: str
    asset_id: str
    lookup_purpose: str
    target_domain: str
    target_url: str
    evidence_type: str
    timestamp: str
    readonly: bool
    no_clone: bool
    no_download_weight: bool
    no_source_checkout: bool
    no_install: bool
    evidence_saved_ref: str
    network_boundary_compliant: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationEvidence:
    asset_id: str
    source_family: str
    repository_candidate_required: bool
    repository_url_verified: bool
    repository_url: str
    repository_owner: str
    repository_name: str
    repository_metadata_evidence_ref: str
    repository_identity_confidence: str
    repository_identity_rationale: str
    package_import_identity_unresolved_or_source_component: bool
    repository_may_contain_committed_checkpoint_weight: bool
    git_lfs_detected: bool
    committed_weight_files_detected: bool
    repository_verification_completed: bool
    repository_verification_failure_reason: Optional[str]


@dataclass(frozen=True)
class SourceCommitPinResolutionEvidence:
    asset_id: str
    repository_url_ref: str
    branch_or_tag_candidate: str
    commit_hash_resolved: bool
    commit_hash: str
    commit_metadata_evidence_ref: str
    commit_pin_confidence: str
    commit_pin_rationale: str
    commit_pin_completed: bool
    commit_pin_failure_reason: Optional[str]
    commit_drift_check_required_before_execution: bool


@dataclass(frozen=True)
class SourceLicenseReviewEvidence:
    asset_id: str
    license_file_found: bool
    license_type_candidate: str
    license_file_evidence_ref: str
    license_review_completed: bool
    license_review_confidence: str
    license_review_rationale: str
    commercial_runtime_not_approved: bool
    source_install_allowed_by_license_for_trial: Any
    license_review_failure_reason: Optional[str]
    license_completion_does_not_approve_commercial_runtime: bool
    license_completion_does_not_approve_weight_download: bool
    license_completion_does_not_approve_inference_runtime: bool


@dataclass(frozen=True)
class SourceDependencyManifestReviewEvidence:
    asset_id: str
    dependency_manifest_found: bool
    dependency_manifest_refs: Tuple[str, ...]
    dependency_review_completed: bool
    dependency_risk_summary: str
    torch_dependency_detected: bool
    opencv_dependency_detected: bool
    numpy_scipy_dependency_detected: bool
    build_compile_risk_detected: bool
    dependency_conflict_risk_detected: bool
    dependency_review_failure_reason: Optional[str]
    dependency_review_is_not_install_approval: bool


@dataclass(frozen=True)
class MobileSAMWeightExclusionFeasibilityReview:
    asset_id: str
    mobile_sam_weight_excluding_checkout_required: bool
    committed_weight_files_detected: Any
    committed_weight_files: Tuple[str, ...]
    committed_weight_total_bytes: int
    git_lfs_detected: Any
    blocked_file_patterns: Tuple[str, ...]
    sparse_checkout_feasible: Any
    archive_filtering_feasible: Any
    code_only_checkout_feasible: Any
    full_clone_allowed_for_mobile_sam_next_execution: bool
    mobile_sam_weight_exclusion_review_completed: bool
    mobile_sam_weight_exclusion_failure_reason: Optional[str]
    feasibility_rationale: str
    weight_file_evidence_ref: str
    feasibility_is_not_weight_download_approval: bool


@dataclass(frozen=True)
class SourceExecutionRetryReadinessGateReview:
    asset_id: str
    repository_url_verified: bool
    commit_hash_pinned: bool
    license_review_completed: bool
    dependency_review_completed: bool
    network_boundary_finalized: bool
    command_whitelist_needs_update: bool
    source_checkout_strategy_finalized: bool
    rollback_ready: bool
    test_board_ready: bool
    mobile_sam_weight_excluding_checkout_plan_completed: Optional[bool]
    mobile_sam_full_clone_blocked_if_weight_risk: bool
    unresolved_blockers: Tuple[str, ...]
    can_enter_source_execution_retry_next: bool
    retry_must_not_execute_in_this_phase: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationReviewDecisionRecord:
    record_id: str
    ready_asset_ids: Tuple[str, ...]
    not_ready_asset_ids: Tuple[str, ...]
    both_assets_ready: bool
    partial_ready: bool
    none_ready: bool
    recommended_next_phase: str
    retry_scope_asset_ids: Tuple[str, ...]
    no_weight_download_phase_until_successful_source_execution_post_review: bool
    source_execution_retry_not_allowed_without_readiness_gate: bool
    retry_not_executed_in_this_phase: bool


@dataclass(frozen=True)
class SourceRepositoryReviewRiskRecord:
    asset_id: str
    risk_dimensions: Tuple[str, ...]
    all_risk_dimensions_recorded: bool
    highlighted_risks: Tuple[str, ...]


@dataclass
class NegativeSourceRepositoryVerificationCommitPinReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1SourceRepositoryVerificationCommitPinReviewDecision:
    decision_ref: str
    source_repository_verification_commitpin_review_profile_count: int
    scoped_network_evidence_log_count: int
    source_repository_verification_evidence_count: int
    source_commit_pin_resolution_evidence_count: int
    source_license_review_evidence_count: int
    source_dependency_manifest_review_evidence_count: int
    mobile_sam_weight_exclusion_feasibility_review_count: int
    source_execution_retry_readiness_gate_review_count: int
    source_repository_verification_review_decision_record_count: int
    source_repository_review_risk_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
