# -*- coding: utf-8 -*-
"""Smoke: Case 1 OCR routing + Case 2 correction midplatform routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


_REPO = _detect_repo_root()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from capabilities.midplatform.model_test_lens.human_correction.correction_midplatform_analyzer_v1 import (  # noqa: E402
    analyze_correction,
    decide_post_correction_actions,
)
from capabilities.midplatform.model_test_lens.single_model_interaction_validation.result_to_midplatform_processor_v1 import (  # noqa: E402
    build_sample_attention_records,
    build_sample_case1_envelopes,
    process_segmentation_envelopes,
)


def _sample_correction(correction_id: str, region_id: str, types: list, note: str) -> dict:
    return {
        "correction_id": correction_id,
        "source_model_id": "mobile_sam",
        "source_model_category": "segmentation",
        "correction_types": types,
        "correction_type": types[0] if types else "",
        "manual_annotation": note,
        "user_note": note,
        "correction_target": {
            "target_id": region_id,
            "source_object_id": region_id,
            "target_type": "segmentation_mask",
            "target_display_name": region_id,
        },
        "candidate_only": True,
        "not_fact": True,
    }


def run_case1() -> dict:
    envelopes = build_sample_case1_envelopes()
    attention = build_sample_attention_records()
    trace_prefix = [
        {"stage": "image_input", "ref": "street_scene_v1"},
        {"stage": "segmentation_region", "ref": "region_001|region_002|region_003"},
        {"stage": "execution_candidate", "ref": "crec_case1_001"},
        {"stage": "runner_execution", "ref": "rex_mobile_sam_case1_001"},
        {"stage": "segmentation_result_envelope", "ref": "env_batch_case1"},
    ]
    out = process_segmentation_envelopes(
        envelopes,
        attention,
        task_context="street_navigation_test",
        trace_prefix=trace_prefix,
    )

    checks = {
        "attention_not_overwritten": out["attention_records_not_overwritten"],
        "has_observation_updates": len(out["observation_update_candidates"]) == 3,
        "region_002_ocr_route": any(
            r.get("region_id") == "region_002" and r.get("text_likely") for r in out["per_region_results"]
        ),
        "ocr_task_candidate_created": len(out["new_task_candidates"]) >= 1,
        "ocr_runner_forbidden": out["ocr_runner_forbidden"] is True,
        "no_pipeline_bypass": out["midplatform_schedules_not_pipeline"] is True,
        "trace_has_new_task": any(t.get("stage") == "new_task_candidate" for t in out["trace_chain"]),
    }
    failed = [k for k, v in checks.items() if not v]

    return {
        "smoke_id": "single_model_interaction_validation_case1_smoke_v1",
        "checks": checks,
        "failed_checks": failed,
        "ocr_task_count": len(out["new_task_candidates"]),
        "ocr_route_count": len(out["followup_model_route_candidates"]),
        "trace_chain": out["trace_chain"],
        "final_decision": "GO" if not failed else "BLOCKED",
    }


def run_case2() -> dict:
    boundary_corr = _sample_correction(
        "correction_case2_boundary", "region_002", ["boundary_inaccurate"], "区域少了一部分",
    )
    ignore_corr = _sample_correction(
        "correction_case2_ignore", "region_003", ["priority_wrong"], "这个区域不用看",
    )
    pref_corr = _sample_correction(
        "correction_case2_pref", "region_001", [], "我更关注公交站牌",
    )

    boundary_analysis = analyze_correction(boundary_corr)
    ignore_analysis = analyze_correction(ignore_corr)
    pref_analysis = analyze_correction(pref_corr)

    boundary_actions = decide_post_correction_actions(
        boundary_analysis, source_result_envelope={"region_id": "region_002"},
    )
    ignore_actions = decide_post_correction_actions(
        ignore_analysis, source_result_envelope={"region_id": "region_003"},
    )

    checks = {
        "boundary_is_model_error": boundary_analysis["attribution_id"] == "model_error",
        "boundary_training_pending": boundary_analysis["training_candidate"] == "pending_review",
        "boundary_has_rerun": boundary_analysis["model_rerun_candidate"] is True,
        "boundary_has_purified_signal": "purified_training_signal" in boundary_analysis,
        "ignore_is_attention": ignore_analysis["attribution_id"] == "attention_priority_error",
        "ignore_not_training": ignore_analysis["training_candidate"] == "not_applicable",
        "ignore_priority_action": any(
            a.get("action_type") == "priority_update_signal"
            for a in ignore_actions["post_correction_actions"]
        ),
        "pref_is_user_preference": pref_analysis["attribution_id"] == "user_preference",
        "no_modify_mask_in_actions": all(
            a.get("not_modify_mask", True) for a in boundary_actions["post_correction_actions"]
        ),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "smoke_id": "single_model_interaction_validation_case2_smoke_v1",
        "checks": checks,
        "failed_checks": failed,
        "final_decision": "GO" if not failed else "BLOCKED",
    }


def main() -> int:
    case1 = run_case1()
    case2 = run_case2()
    failed = case1.get("failed_checks", []) + case2.get("failed_checks", [])

    result = {
        "smoke_id": "single_model_interaction_validation_smoke_v1",
        "case_1": case1,
        "case_2": case2,
        "final_decision": "GO" if not failed else "BLOCKED",
    }

    out_dir = _REPO / "_tmp_eval_out" / "p1_midplatform_single_model_interaction_validation_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "single_model_interaction_validation_smoke_v1.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
