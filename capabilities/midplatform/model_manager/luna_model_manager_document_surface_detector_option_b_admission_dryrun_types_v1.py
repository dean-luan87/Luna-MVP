# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B admission dryrun types v1."""

from __future__ import annotations

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Post-Review-v1-001"

SMOKE_CASE_IDS = (
    "case_a_candidate_fixtures_completeness",
    "case_b_admitted_to_preflight_only",
    "case_c_dependency_block",
    "case_d_license_weight_block",
    "case_e_output_contract_block",
    "case_f_wrapper_requirement",
    "case_g_abort_rollback",
    "case_h_protocol_compliance",
)

REQUIRED_FIXTURE_FIELDS = (
    "model_candidate_id",
    "family_type",
    "capability",
    "output_types_allowed",
    "output_types_forbidden",
    "dependency_profile",
    "weight_profile",
    "license_status_candidate",
    "execution_mode_candidate",
    "local_runtime_possible",
    "external_runtime_possible",
    "expected_input",
    "expected_output",
    "candidate_only",
    "not_fact",
    "active_status",
    "controlled_execution_required",
    "preflight_required",
    "validation_required",
)
