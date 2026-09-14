# -*- coding: utf-8
"""Luna Situation Understanding Model — dry-run fixtures v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.situation_understanding.luna_situation_understanding_dryrun_adapter_v1 import (
    run_situation_understanding_dryrun,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_BLOCKED"

DRYRUN_CASE_IDS = (
    "case_a_job_564f1aa93983_shop_sign",
    "case_b_subway_jiahuihu",
    "case_c_street_crossing",
    "case_d_corridor",
    "case_e_unknown_scene",
    "case_f_teacher_case_ref_shopfront",
    "case_g_runner_scene_conflict",
)


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


def _generic_sam_regions() -> List[Dict[str, Any]]:
    return [
        {
            "prompt_id": f"generic_region_candidate_{i}",
            "prompt_target_label": f"generic_region_candidate_{i}",
            "display_task_semantic": "P1 静态区域候选",
            "ocr_route_candidate": False,
            "score": 0.85,
            "candidate_only": True,
        }
        for i in range(1, 6)
    ]


def _runner_result_unknown_generic() -> Dict[str, Any]:
    return {
        "scene_profile_candidate": {
            "scene_type_candidate": "unknown_scene",
            "confidence": 0.55,
            "candidate_only": True,
            "not_fact": True,
        },
        "segmentation_prompt_policy": {
            "prompt_set_id": "scene_prompt_set_generic_v1",
            "scene_type_candidate": "unknown_scene",
            "candidate_only": True,
            "not_fact": True,
        },
        "prompt_results": _generic_sam_regions(),
    }


def fixture_job_564f1aa93983_shop_sign() -> Dict[str, Any]:
    job_path = _repo_root() / "capabilities/midplatform/model_test_lens/local_runner_bridge/jobs/job_564f1aa93983.json"
    if job_path.is_file():
        envelope = json.loads(job_path.read_text(encoding="utf-8"))
    else:
        envelope = {
            "job_id": "job_564f1aa93983",
            "created_at": "2026-07-08T02:30:08.780633+00:00",
            "source": "replay",
            "asset_manifest": {
                "asset_id": "asset_d19f5fe2972f",
                "file_name": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
                "local_file_name": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
            },
            "runner_result": _runner_result_unknown_generic(),
            "prompt_set_id_optional": "scene_prompt_set_generic_v1",
            "runner_scene_hint_optional": "unknown_scene",
        }
    envelope.setdefault("job_id", "job_564f1aa93983")
    envelope.setdefault("dryrun_case_ref_key", "shopfront_sign_case")
    return envelope


def fixture_subway_jiahuihu_unknown_or_generic_runner() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_subway_jiahuihu",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {
            "asset_id": "asset_subway_jiahuihu",
            "file_name": "subway_direction_sign_jiahuihu.png",
        },
        "runner_scene_hint_optional": "unknown_scene",
        "prompt_set_id_optional": "scene_prompt_set_generic_v1",
        "runner_result": _runner_result_unknown_generic(),
        "user_goal_candidate_optional": {
            "goal_type": "find",
            "confidence": 0.75,
            "source": "user_command",
        },
        "dryrun_case_ref_key": "subway_platform_case",
    }


def fixture_street_crossing_generic_runner() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_street_crossing",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {"asset_id": "asset_street", "file_name": "street_crossing_fixture.png"},
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": _runner_result_unknown_generic(),
        "user_goal_candidate_optional": {"goal_type": "navigate", "confidence": 0.8, "source": "user_command"},
        "dryrun_extra_evidence": [
            {
                "evidence_id": "ev_st1", "source": "detection", "evidence_type": "scene_hint",
                "value": "crosswalk_hint", "confidence": 0.83, "source_trace_ref": "ev_st1",
                "candidate_only": True, "not_fact": True,
            },
            {
                "evidence_id": "ev_st2", "source": "detection", "evidence_type": "object_hint",
                "value": "vehicle_hint", "confidence": 0.8, "source_trace_ref": "ev_st2",
                "candidate_only": True, "not_fact": True,
            },
            {
                "evidence_id": "ev_st3", "source": "detection", "evidence_type": "object_hint",
                "value": "person_hint", "confidence": 0.78, "source_trace_ref": "ev_st3",
                "candidate_only": True, "not_fact": True,
            },
            {
                "evidence_id": "ev_st4", "source": "metadata", "evidence_type": "spatial_hint",
                "value": "open_road", "confidence": 0.76, "source_trace_ref": "ev_st4",
                "candidate_only": True, "not_fact": True,
            },
        ],
        "dryrun_case_ref_key": "street_crossing_case",
    }


def fixture_corridor_spatial_runner() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_corridor",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {"asset_id": "asset_corridor", "file_name": "corridor_fixture.png"},
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": _runner_result_unknown_generic(),
        "user_goal_candidate_optional": {"goal_type": "navigate", "confidence": 0.8, "source": "user_command"},
        "dryrun_extra_evidence": [
            {
                "evidence_id": "ev_co1", "source": "metadata", "evidence_type": "spatial_hint",
                "value": "corridor_lines", "confidence": 0.82, "source_trace_ref": "ev_co1",
                "candidate_only": True, "not_fact": True,
            },
            {
                "evidence_id": "ev_co2", "source": "depth", "evidence_type": "spatial_hint",
                "value": "indoor_path", "confidence": 0.8, "source_trace_ref": "ev_co2",
                "candidate_only": True, "not_fact": True,
            },
            {
                "evidence_id": "ev_co3", "source": "sam", "evidence_type": "spatial_hint",
                "value": "spatial_boundary", "confidence": 0.78, "source_trace_ref": "ev_co3",
                "candidate_only": True, "not_fact": True,
            },
        ],
        "dryrun_case_ref_key": "corridor_case",
    }


def fixture_unknown_scene_low_evidence() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_unknown",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {"asset_id": "asset_unknown", "file_name": "ambiguous_fixture.png"},
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": {
            "scene_profile_candidate": {"scene_type_candidate": "unknown_scene", "confidence": 0.3},
            "segmentation_prompt_policy": {"prompt_set_id": "scene_prompt_set_generic_v1"},
            "prompt_results": [],
        },
        "dryrun_extra_evidence": [
            {
                "evidence_id": "ev_weak", "source": "metadata", "evidence_type": "scene_hint",
                "value": "weak_hint", "confidence": 0.2, "source_trace_ref": "ev_weak",
                "candidate_only": True, "not_fact": True,
            },
        ],
    }


def fixture_teacher_case_ref_shopfront() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_teacher_case_ref",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {
            "asset_id": "asset_teacher_shop",
            "file_name": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        },
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": _runner_result_unknown_generic(),
        "situation_case_refs_optional": ["teacher_accepted_shopfront_case"],
        "dryrun_case_ref_key": "teacher_accepted_shopfront_case",
    }


def fixture_runner_scene_conflict() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_runner_conflict",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {
            "asset_id": "asset_conflict",
            "file_name": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        },
        "runner_scene_hint_optional": "street_crossing",
        "runner_result": {
            "scene_profile_candidate": {
                "scene_type_candidate": "street_crossing",
                "confidence": 0.6,
                "candidate_only": True,
                "not_fact": True,
            },
            "segmentation_prompt_policy": {"prompt_set_id": "scene_prompt_set_generic_v1"},
            "prompt_results": _generic_sam_regions(),
        },
        "situation_case_refs_optional": ["shopfront_sign_case"],
        "dryrun_case_ref_key": "shopfront_sign_case",
    }


def _caps(result: Dict[str, Any], bucket: str) -> List[str]:
    return result.get("model_need_hint_summary", {}).get(bucket, [])


def _task_types(candidate: Dict[str, Any]) -> List[str]:
    return [c["task_type"] for c in candidate.get("task_clue_candidates", [])]


def _info_types(candidate: Dict[str, Any]) -> List[str]:
    return [m["info_type"] for m in candidate.get("missing_information_candidates", [])]


def _has_conflict_stage(dryrun: Dict[str, Any], stage: str) -> bool:
    traces = dryrun.get("conflict_trace_optional") or []
    scene_traces = dryrun.get("scene_resolution_trace", {}).get("conflict_traces", [])
    all_traces = traces + scene_traces
    return any(t.get("stage") == stage for t in all_traces)


def dryrun_case_a_job_564f1aa93983() -> Dict[str, Any]:
    case_id = "case_a_job_564f1aa93983_shop_sign"
    dryrun = run_situation_understanding_dryrun(fixture_job_564f1aa93983_shop_sign())
    cand = dryrun["situation_understanding_candidate"]
    scene = cand["scene_profile_candidate"]
    passed = (
        dryrun["job_id"] == "job_564f1aa93983"
        and scene["scene_type"] == "shopfront_sign"
        and scene.get("owned_by") == "situation_understanding_layer"
        and _has_conflict_stage(dryrun, "runner_scene_hint_conflict")
        and "read_text" in _task_types(cand)
        and "identify_place" in _task_types(cand)
        and "text_content" in _info_types(cand)
        and "place_identity" in _info_types(cand)
        and "ocr" in _caps(dryrun, "likely_needed")
        and "slam" in _caps(dryrun, "not_needed")
        and "tracking" in _caps(dryrun, "not_needed")
        and "depth" in _caps(dryrun, "not_needed")
        and dryrun["no_runner_invocation_assertion"] is True
        and dryrun["no_fact_write_assertion"] is True
        and cand["candidate_only"] is True
        and cand["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def dryrun_case_b_subway() -> Dict[str, Any]:
    case_id = "case_b_subway_jiahuihu"
    dryrun = run_situation_understanding_dryrun(fixture_subway_jiahuihu_unknown_or_generic_runner())
    cand = dryrun["situation_understanding_candidate"]
    passed = (
        cand["scene_profile_candidate"]["scene_type"] == "subway_platform"
        and "find_direction" in _task_types(cand)
        and "read_text" in _task_types(cand)
        and "ocr" in _caps(dryrun, "likely_needed")
        and "slam" in _caps(dryrun, "not_needed")
        and cand["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def dryrun_case_c_street() -> Dict[str, Any]:
    case_id = "case_c_street_crossing"
    dryrun = run_situation_understanding_dryrun(fixture_street_crossing_generic_runner())
    cand = dryrun["situation_understanding_candidate"]
    likely = _caps(dryrun, "likely_needed")
    passed = (
        cand["scene_profile_candidate"]["scene_type"] == "street_crossing"
        and "assess_walkable" in _task_types(cand)
        and "avoid_obstacle" in _task_types(cand)
        and "detection" in likely
        and "depth" in likely
        and "tracking" in likely
        and "ocr" not in likely
        and cand["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def dryrun_case_d_corridor() -> Dict[str, Any]:
    case_id = "case_d_corridor"
    dryrun = run_situation_understanding_dryrun(fixture_corridor_spatial_runner())
    cand = dryrun["situation_understanding_candidate"]
    likely = _caps(dryrun, "likely_needed")
    not_needed = _caps(dryrun, "not_needed")
    passed = (
        cand["scene_profile_candidate"]["scene_type"] == "corridor"
        and cand["survival_context"]["mobility_relevance"] == "high"
        and "depth" in likely
        and "slam" in likely
        and "ocr" in not_needed
        and cand["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def dryrun_case_e_unknown() -> Dict[str, Any]:
    case_id = "case_e_unknown_scene"
    dryrun = run_situation_understanding_dryrun(fixture_unknown_scene_low_evidence())
    cand = dryrun["situation_understanding_candidate"]
    uncertainty = cand["uncertainty"]
    passed = (
        cand["scene_profile_candidate"]["scene_type"] == "unknown_scene"
        and (uncertainty["needs_manual_review"] is True or "ask_user" in uncertainty.get("fallback_suggestion", ""))
        and len(_caps(dryrun, "likely_needed")) == 0
        and dryrun["no_runner_invocation_assertion"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def dryrun_case_f_teacher_case_ref() -> Dict[str, Any]:
    case_id = "case_f_teacher_case_ref_shopfront"
    dryrun = run_situation_understanding_dryrun(fixture_teacher_case_ref_shopfront())
    cand = dryrun["situation_understanding_candidate"]
    scene = cand["scene_profile_candidate"]
    passed = (
        scene["scene_type"] == "shopfront_sign"
        and scene["candidate_only"] is True
        and scene["not_fact"] is True
        and "teacher_accepted_shopfront_case" in scene.get("case_refs", [])
        and cand["candidate_only"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun, "teacher_not_direct_owner": True}


def dryrun_case_g_runner_conflict() -> Dict[str, Any]:
    case_id = "case_g_runner_scene_conflict"
    dryrun = run_situation_understanding_dryrun(fixture_runner_scene_conflict())
    cand = dryrun["situation_understanding_candidate"]
    scene = cand["scene_profile_candidate"]
    passed = (
        scene["scene_type"] == "shopfront_sign"
        and scene["scene_type"] != "street_crossing"
        and _has_conflict_stage(dryrun, "runner_scene_hint_conflict")
        and dryrun["no_runner_invocation_assertion"] is True
        and dryrun["no_fact_write_assertion"] is True
    )
    return {"case_id": case_id, "passed": passed, "dryrun": dryrun}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_job_564f1aa93983,
        dryrun_case_b_subway,
        dryrun_case_c_street,
        dryrun_case_d_corridor,
        dryrun_case_e_unknown,
        dryrun_case_f_teacher_case_ref,
        dryrun_case_g_runner_conflict,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    passed_count = sum(1 for c in cases if c.get("passed"))

    job_recovery = next(
        (c for c in cases if c.get("case_id") == "case_a_job_564f1aa93983_shop_sign"),
        {},
    )
    recovery_dryrun = job_recovery.get("dryrun", {})
    recovery_scene = (
        recovery_dryrun.get("situation_understanding_candidate", {})
        .get("scene_profile_candidate", {})
        .get("scene_type")
    )
    runner_hint = recovery_dryrun.get("runner_scene_hint_evidence_record", {})
    runner_hint_val = runner_hint.get("value") if runner_hint else None

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-DryRun-v1-001",
        "deterministic_dryrun_only": True,
        "no_real_model_execution": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_cases_passed": passed_count,
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "job_564f1aa93983_recovery_result": {
            "job_id": "job_564f1aa93983",
            "runner_scene_hint": runner_hint_val,
            "situation_scene_corrected_to": recovery_scene,
            "recovered": recovery_scene == "shopfront_sign" and runner_hint_val == "unknown_scene",
        },
        "final_decision": decision,
    }
