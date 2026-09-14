# -*- coding: utf-8
"""Network-Assisted Situation Learning — planning smoke v1 (deterministic stub)."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.network_assisted_learning.network_assisted_situation_learning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.network_assisted_learning.network_learning_candidate_builder_v1 import (
    build_from_human_correction,
    build_from_teacher_label,
    build_from_test_trace,
    build_from_web_reference,
)
from capabilities.midplatform.network_assisted_learning.network_learning_policy_reviewer_v1 import (
    review_learning_candidate,
)
from capabilities.midplatform.network_assisted_learning.situation_case_library_builder_v1 import (
    accept_candidate_as_case_record,
    build_training_dataset_candidate,
)

FINAL_SMOKE_GO = FINAL_GO.replace("_GO", "_SMOKE_GO")
FINAL_SMOKE_BLOCKED = FINAL_BLOCKED.replace("_BLOCKED", "_SMOKE_BLOCKED")


def smoke_case_a_teacher_shopfront() -> Dict[str, Any]:
    case_id = "case_a_teacher_shopfront_sign"
    built = build_from_teacher_label({
        "teacher_model_name": "third_party_vlm_teacher_stub",
        "input_ref": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        "scene": "shopfront_sign",
        "task_clues": ["read_text", "identify_place"],
        "needed_tools": ["OCR"],
        "noop_tools": ["SLAM", "Tracking", "Depth"],
        "reasoning_summary": "店招文字读取场景",
        "confidence": 0.86,
    })
    reviewed = review_learning_candidate(
        built["learning_candidate"],
        provenance=built["provenance"],
    )
    case = accept_candidate_as_case_record(
        reviewed["learning_candidate"],
        reviewed["review"],
        case_type="shopfront_sign",
        case_title="店招文字读取参考案例",
    )
    passed = (
        built.get("teacher_label")
        and reviewed["review"]["policy_decision"] == "accept_as_case_candidate"
        and case is not None
        and "OCR" in case.get("recommended_tools", [])
        and "SLAM" in case.get("noop_tools", [])
        and reviewed["learning_candidate"]["candidate_only"] is True
        and reviewed["learning_candidate"]["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "teacher_label": built.get("teacher_label"),
        "review": reviewed["review"],
        "case_record": case,
        "no_fact_write": True,
        "no_runner_execution": True,
    }


def smoke_case_b_teacher_bad_slam() -> Dict[str, Any]:
    case_id = "case_b_teacher_bad_slam_for_text"
    built = build_from_teacher_label({
        "teacher_model_name": "third_party_vlm_teacher_stub",
        "input_ref": "shop_sign.png",
        "scene": "shopfront_sign",
        "task_clues": ["read_text"],
        "needed_tools": ["SLAM"],
        "noop_tools": [],
    })
    reviewed = review_learning_candidate(
        built["learning_candidate"],
        provenance=built["provenance"],
    )
    case = accept_candidate_as_case_record(reviewed["learning_candidate"], reviewed["review"])
    passed = (
        reviewed["review"]["unsafe_rule_risk"] is True
        and reviewed["review"]["policy_decision"] in ("reject", "require_human_review")
        and case is None
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "review": reviewed["review"],
        "case_record": case,
        "no_case_library_entry": case is None,
    }


def smoke_case_c_web_reference() -> Dict[str, Any]:
    case_id = "case_c_web_reference_candidate"
    built = build_from_web_reference({
        "query_text": "店铺门头图像特征",
        "extracted_clues": ["signage panel", "large text block", "storefront facade"],
        "trust_tier": "unknown",
        "proposed_scene_type": "shopfront_sign",
    })
    reviewed = review_learning_candidate(
        built["learning_candidate"],
        provenance=built["provenance"],
        source=built["web_reference"],
    )
    passed = (
        built["web_reference"]["trust_tier"] == "unknown"
        and built["web_reference"]["review_status"] == "pending_policy_review"
        and reviewed["review"]["policy_decision"] in ("hold", "require_human_review", "reject")
        and reviewed["learning_candidate"]["candidate_only"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "web_reference": built["web_reference"],
        "review": reviewed["review"],
        "no_auto_train": True,
    }


def smoke_case_d_human_correction() -> Dict[str, Any]:
    case_id = "case_d_human_correction"
    built = build_from_human_correction({
        "correction_text": "这不是普通静态区域，是店招文字，应该读文字",
        "proposed_scene_type": "shopfront_sign",
        "proposed_task_clues": ["read_text"],
        "proposed_needed_tools": ["OCR"],
        "proposed_noop_tools": ["SLAM"],
    })
    reviewed = review_learning_candidate(
        built["learning_candidate"],
        provenance=built["provenance"],
    )
    passed = (
        built["learning_candidate"]["source_type"] == "human_correction"
        and built["learning_candidate"]["proposed_scene_type"] == "shopfront_sign"
        and "OCR" in built["learning_candidate"]["proposed_needed_tools"]
        and "SLAM" in built["learning_candidate"]["proposed_noop_tools"]
        and reviewed["review"]["policy_decision"] == "require_human_review"
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "learning_candidate": built["learning_candidate"],
        "review": reviewed["review"],
    }


def smoke_case_e_test_trace() -> Dict[str, Any]:
    case_id = "case_e_test_trace_regression"
    built = build_from_test_trace({
        "job_id": "job_564f1aa93983",
        "current_behavior": {
            "scene": "unknown_scene",
            "prompt_set": "scene_prompt_set_generic_v1",
            "needed_tools": [],
            "noop_tools": [],
        },
        "expected_behavior": {
            "scene": "shopfront_sign",
            "task_clues": ["read_text"],
            "needed_tools": ["OCR"],
            "noop_tools": ["SLAM"],
            "missing_information": ["text_region_candidate"],
        },
    })
    reviewed = review_learning_candidate(
        built["learning_candidate"],
        provenance=built["provenance"],
    )
    case = accept_candidate_as_case_record(
        reviewed["learning_candidate"],
        reviewed["review"],
        case_type="shopfront_sign",
        case_title="店招回归案例 job_564f1aa93983",
    )
    passed = (
        "current_behavior_mismatch" in built["learning_candidate"].get("risk_flags", [])
        and reviewed["review"]["policy_decision"] == "accept_as_case_candidate"
        and case is not None
        and case.get("canonical_scene_type") == "shopfront_sign"
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "case_record": case,
        "no_runner_mutation": True,
    }


def smoke_case_f_training_dataset() -> Dict[str, Any]:
    case_id = "case_f_training_dataset_candidate"
    cases = []
    for payload in (
        {
            "scene": "shopfront_sign",
            "task_clues": ["read_text"],
            "needed_tools": ["OCR"],
            "noop_tools": ["SLAM"],
        },
        {
            "scene": "subway_platform",
            "task_clues": ["read_text", "find_direction"],
            "needed_tools": ["OCR"],
            "noop_tools": ["SLAM"],
        },
    ):
        built = build_from_teacher_label({
            "teacher_model_name": "third_party_vlm_teacher_stub",
            "input_ref": f"fixture_{payload['scene']}.png",
            **payload,
        })
        reviewed = review_learning_candidate(built["learning_candidate"], provenance=built["provenance"])
        case = accept_candidate_as_case_record(reviewed["learning_candidate"], reviewed["review"])
        if case:
            cases.append(case)

    dataset = build_training_dataset_candidate(cases)
    passed = (
        len(cases) >= 2
        and dataset["review_status"] == "pending_human_approval"
        and dataset["requires_human_approval"] is True
        and "situation_understanding_model" in dataset["allowed_training_use"]
        and "direct_fact_prediction" in dataset["blocked_training_use"]
        and dataset.get("no_model_training_in_planning") is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "dataset_candidate": dataset,
        "case_count": len(cases),
        "no_model_training": True,
    }


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_a_teacher_shopfront,
    smoke_case_b_teacher_bad_slam,
    smoke_case_c_web_reference,
    smoke_case_d_human_correction,
    smoke_case_e_test_trace,
    smoke_case_f_training_dataset,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")

    for expected in SMOKE_CASE_IDS:
        if expected not in {c["case_id"] for c in cases}:
            failed.append(f"smoke.missing_case={expected}")

    decision = FINAL_SMOKE_GO if not failed else FINAL_SMOKE_BLOCKED
    return {
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_only": True,
        "no_network_call": True,
        "no_teacher_model_call": True,
        "no_model_training": True,
        "deterministic_smoke_only": True,
    }
