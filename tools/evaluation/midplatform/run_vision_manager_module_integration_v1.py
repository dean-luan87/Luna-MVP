#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.vision_manager.module import (
    run_vision_manager_module_api_v1,
)


def _base_request() -> Dict[str, Any]:
    return {
        "request_id": "vision_req_001",
        "capability": "luna.vision_manager",
        "observation_request": "observe_forward_path",
        "attention_target": "crosswalk",
        "frame_quality": "good",
        "model_test_lens": "default",
        "ownership_ok": True,
        "version_snapshot": {
            "capability_registry": "v1",
            "module_api": "v1",
        },
        "trace_context": {"scene": "synthetic"},
    }


def _merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in patch.items():
        merged[key] = value
    return merged


def _scenarios() -> List[Dict[str, Any]]:
    return [
        {"name": "valid_visual_input", "patch": {}},
        {"name": "frame_quality_good", "patch": {"frame_quality": "good"}},
        {
            "name": "frame_quality_insufficient",
            "patch": {"frame_quality": "insufficient"},
        },
        {
            "name": "invalid_observation_request",
            "patch": {"observation_request": "observe_unknown"},
        },
        {
            "name": "attention_target_available",
            "patch": {"attention_target": "signage"},
        },
        {"name": "no_attention_target", "patch": {"attention_target": ""}},
        {"name": "roi_candidate_generation", "patch": {}},
        {"name": "region_surface_candidate", "patch": {}},
        {"name": "detection_candidate_normalization", "patch": {}},
        {"name": "segmentation_candidate_normalization", "patch": {}},
        {"name": "tracking_candidate_normalization", "patch": {}},
        {"name": "multi_source_evidence_composition", "patch": {}},
        {"name": "model_handoff_blocked", "patch": {"model_test_lens": "blocked"}},
        {"name": "ownership_blocked", "patch": {"ownership_ok": False}},
        {"name": "degraded_without_model", "patch": {"attention_target": ""}},
        {
            "name": "human_correction_candidate",
            "patch": {"frame_quality": "insufficient"},
        },
        {"name": "deterministic_replay", "patch": {"request_id": "vision_req_det_001"}},
        {"name": "missing_version_snapshot", "patch": {"version_snapshot": {}}},
    ]


def run_integration() -> Dict[str, Any]:
    base = _base_request()
    cases: List[Dict[str, Any]] = []
    for scenario in _scenarios():
        req = _merge(base, scenario["patch"])
        result = run_vision_manager_module_api_v1(req)
        cases.append({"name": scenario["name"], "request": req, "result": result})

    det_req = _merge(base, {"request_id": "vision_req_det_001"})
    det_a = run_vision_manager_module_api_v1(det_req)
    det_b = run_vision_manager_module_api_v1(det_req)
    deterministic_replay_ok = det_a.get("trace_ref") == det_b.get(
        "trace_ref"
    ) and det_a.get("replay_key") == det_b.get("replay_key")

    boundary_flags_ok = all(
        case["result"].get("camera_invoked") is False
        and case["result"].get("visual_model_invoked") is False
        and case["result"].get("ocr_provider_invoked") is False
        and case["result"].get("segmentation_runtime_invoked") is False
        and case["result"].get("tracking_runtime_invoked") is False
        and case["result"].get("world_model_written") is False
        and case["result"].get("memory_written") is False
        and case["result"].get("fact_written") is False
        and case["result"].get("navigation_action_triggered") is False
        and case["result"].get("production_runtime_executed") is False
        for case in cases
    )

    required_fields_ok = all(
        "module_status" in case["result"]
        and "admitted_visual_input" in case["result"]
        and "frame_quality_status" in case["result"]
        and "attention_plan" in case["result"]
        and "roi_candidates" in case["result"]
        and "region_candidates" in case["result"]
        and "model_capability_request" in case["result"]
        and "model_handoff_candidate" in case["result"]
        and "detection_candidates" in case["result"]
        and "segmentation_candidates" in case["result"]
        and "tracking_candidates" in case["result"]
        and "scene_evidence_candidates" in case["result"]
        and "composed_visual_evidence" in case["result"]
        and "correction_candidates" in case["result"]
        and "degradation_plan" in case["result"]
        and "diagnostics" in case["result"]
        and "rejection_reasons" in case["result"]
        and bool(case["result"].get("trace_ref"))
        and bool(case["result"].get("replay_key"))
        for case in cases
    )

    integration_pass = (
        boundary_flags_ok and required_fields_ok and deterministic_replay_ok
    )

    return {
        "module": "luna.vision_manager",
        "runner": "run_vision_manager_module_integration_v1",
        "scenario_count": len(cases),
        "boundary_flags_ok": boundary_flags_ok,
        "required_fields_ok": required_fields_ok,
        "deterministic_replay_ok": deterministic_replay_ok,
        "integration_pass": integration_pass,
        "cases": cases,
    }


def main() -> int:
    out = run_integration()
    output_root = (
        REPO_ROOT / "_tmp_eval_out" / "vision_manager_module_integration_v1_smoke_v0"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    out_file = output_root / "vision_manager_module_integration_v1.json"
    out_file.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "integration_pass": out["integration_pass"],
                "scenario_count": out["scenario_count"],
                "boundary_flags_ok": out["boundary_flags_ok"],
                "required_fields_ok": out["required_fields_ok"],
                "deterministic_replay_ok": out["deterministic_replay_ok"],
                "output": str(out_file),
            },
            ensure_ascii=False,
        )
    )
    return 0 if out["integration_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
