# -*- coding: utf-8 -*-
"""Upstream GO artifact chain bootstrap for SLAM P0 — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1 import (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_STOPPED,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1.py",
    "capabilities/midplatform/upstream_go_artifact_chain_bootstrap_for_slam_p0_lineage_v1.py",
    "capabilities/midplatform/upstream_go_artifact_chain_bootstrap_for_slam_p0_v1.py",
    "tools/evaluation/midplatform/run_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1.py",
    "tools/evaluation/midplatform/verify_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1.json",
    "upstream_blocked_chain_review_v1.json",
    "bootstrap_stage_run_registry_v1.json",
    "bootstrap_stage_verifier_registry_v1.json",
    "first_non_go_stage_review_v1.json",
    "slam_p0_upstream_readiness_review_v1.json",
    "slam_p0_revalidation_visibility_review_v1.json",
    "no_protocol_change_review_v1.json",
    "no_world_model_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_slam_p0_revalidation_blocked_by_upstream_gap",
    "blocked_chain_review_exists",
    "bootstrap_stage_run_registry_exists",
    "bootstrap_stage_verifier_registry_exists",
    "no_protocol_change",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_action_output",
    "no_field_simulation",
    "no_fake_go_artifacts",
    "no_forced_summary_mutation",
    "rerun_order_respects_dependency_chain",
    "stop_on_first_non_go",
    "slam_p0_smoke_io_go_or_blocked_with_reason",
    "slam_p0_adapter_skeleton_go_or_blocked_with_reason",
    "slam_p0_task_collaboration_go_or_blocked_with_reason",
    "p0_revalidation_visibility_review_exists",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_STOPPED,
)
