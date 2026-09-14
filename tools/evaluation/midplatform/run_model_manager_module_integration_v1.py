#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _is_workspace_root(candidate: Path) -> bool:
    markers = (
        candidate / "AGENTS.md",
        candidate / "capabilities",
        candidate / "tools" / "evaluation" / "midplatform",
    )
    return all(marker.exists() for marker in markers)


def _find_ws_root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_workspace_root(cwd):
        return cwd

    script_path = Path(__file__).absolute()
    for candidate in (script_path.parent, *script_path.parents):
        if _is_workspace_root(candidate):
            return candidate

    raise RuntimeError(
        "Unable to locate Luna workspace root from cwd or non-resolved script path"
    )


REPO_ROOT = _find_ws_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.model_manager.module import (
    run_model_manager_module_api_v1,
)


def _base_request() -> Dict[str, Any]:
    return {
        "request_id": "req_base_001",
        "requested_capability": "unknown_scene_reasoning",
        "task_ref": "task_nav_001",
        "device_ref": "device_a",
        "region_ref": "region_001",
        "resource_snapshot": {
            "latency_ms": 900,
            "memory_available": 16384,
            "gpu_memory_required_gb": 4,
            "gpu_memory_available_gb": 12,
            "cpu_load_percent": 35,
            "concurrent_limit": 2,
            "concurrent_slots_used": 0,
            "api_quota_available": True,
            "runtime_status": "available",
            "network_available": True,
            "qwen_available": True,
            "gemini_available": True,
            "local_runtime_available": True,
            "cuda_available": True,
            "temperature_celsius": 62,
            "historical_performance": {"qwen_vl": 0.92, "internvl2_5": 0.86},
            "scoring_mode": "balanced",
        },
        "allowed_model_classes": [
            "teacher",
            "local_vlm",
            "tool",
            "vision_language_model",
        ],
        "forbidden_model_ids": [],
        "latency_requirement": 3000,
        "memory_budget": 8192,
        "offline_required": False,
        "privacy_requirement": "normal",
        "ownership_context": {
            "profile_key": "stacked_documents",
            "allowed_regions": ["region_001", "region_002"],
            "allowed_devices": ["device_a", "device_b"],
            "blocked_regions": [],
        },
        "version_snapshot": {
            "capability_registry": "v1",
            "model_registry": "v1",
            "module_api": "v1",
        },
        "trace_context": {
            "situation_understanding_candidate": {
                "scene_profile_candidate": {"scene_type": "unknown_scene"},
            },
            "agent_plan_candidate": {
                "plan_goal_candidate": {"goal_type": "complex_navigation"},
            },
            "decision_validation_candidate": {
                "validation_status_candidate": "candidate",
            },
        },
    }


def _scenarios() -> List[Dict[str, Any]]:
    base = _base_request()
    return [
        {"name": "happy_path", "patch": {}},
        {
            "name": "missing_required_field",
            "patch": {"request_id": "", "region_ref": ""},
        },
        {
            "name": "no_eligible_model",
            "patch": {"requested_capability": "non_existing_capability"},
        },
        {
            "name": "admission_rejected_by_class",
            "patch": {"allowed_model_classes": ["tool"]},
        },
        {"name": "ownership_blocked_region", "patch": {"region_ref": "region_999"}},
        {"name": "ownership_blocked_device", "patch": {"device_ref": "device_x"}},
        {
            "name": "resource_insufficient_memory",
            "patch": {
                "resource_snapshot": {
                    **base["resource_snapshot"],
                    "memory_available": 1024,
                }
            },
        },
        {
            "name": "latency_degraded",
            "patch": {
                "resource_snapshot": {**base["resource_snapshot"], "latency_ms": 5000}
            },
        },
        {
            "name": "offline_required_external_block",
            "patch": {"offline_required": True},
        },
        {
            "name": "forbidden_selected_model",
            "patch": {"forbidden_model_ids": ["qwen_vl"]},
        },
        {
            "name": "privacy_high_blocks_external",
            "patch": {"privacy_requirement": "high"},
        },
        {
            "name": "runtime_unavailable",
            "patch": {
                "resource_snapshot": {
                    **base["resource_snapshot"],
                    "local_runtime_available": False,
                    "qwen_available": False,
                    "gemini_available": False,
                }
            },
        },
        {
            "name": "network_unavailable",
            "patch": {
                "resource_snapshot": {
                    **base["resource_snapshot"],
                    "network_available": False,
                    "qwen_available": False,
                    "gemini_available": False,
                }
            },
        },
        {
            "name": "high_cpu_health_risk",
            "patch": {
                "resource_snapshot": {
                    **base["resource_snapshot"],
                    "cpu_load_percent": 96,
                    "temperature_celsius": 89,
                }
            },
        },
        {"name": "trace_determinism_pass_a", "patch": {"request_id": "req_det_001"}},
        {"name": "trace_determinism_pass_b", "patch": {"request_id": "req_det_001"}},
    ]


def _merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for k, v in patch.items():
        merged[k] = v
    return merged


def run_integration() -> Dict[str, Any]:
    base = _base_request()
    cases = []
    for s in _scenarios():
        req = _merge(base, s["patch"])
        result = run_model_manager_module_api_v1(req)
        cases.append({"name": s["name"], "request": req, "result": result})

    deterministic_ok = cases[-1]["result"].get("replay_key") == cases[-2]["result"].get(
        "replay_key"
    ) and cases[-1]["result"].get("trace_ref") == cases[-2]["result"].get("trace_ref")

    boundary_flags_ok = all(
        c["result"].get("model_inference_executed") is False
        and c["result"].get("model_load_executed") is False
        and c["result"].get("model_unload_executed") is False
        and c["result"].get("model_download_executed") is False
        and c["result"].get("model_training_executed") is False
        and c["result"].get("provider_call_executed") is False
        and c["result"].get("state_mutation_executed") is False
        and c["result"].get("fact_promotion_executed") is False
        and c["result"].get("action_trigger_executed") is False
        and c["result"].get("production_runtime_executed") is False
        for c in cases
    )

    status_coverage = sorted({c["result"].get("module_status") for c in cases})
    trace_replay_ok = all(
        bool(c["result"].get("trace_ref")) and bool(c["result"].get("replay_key"))
        for c in cases
    )

    passed = boundary_flags_ok and trace_replay_ok and deterministic_ok

    return {
        "module": "luna.model_manager",
        "runner": "run_model_manager_module_integration_v1",
        "scenario_count": len(cases),
        "status_coverage": status_coverage,
        "boundary_flags_ok": boundary_flags_ok,
        "trace_replay_ok": trace_replay_ok,
        "deterministic_replay_ok": deterministic_ok,
        "integration_pass": passed,
        "cases": cases,
    }


def main() -> int:
    out = run_integration()
    output_root = (
        REPO_ROOT / "_tmp_eval_out" / "model_manager_module_integration_v1_smoke_v0"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    out_file = output_root / "model_manager_module_integration_v1.json"
    out_file.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "integration_pass": out["integration_pass"],
                "scenario_count": out["scenario_count"],
                "status_coverage": out["status_coverage"],
                "boundary_flags_ok": out["boundary_flags_ok"],
                "trace_replay_ok": out["trace_replay_ok"],
                "deterministic_replay_ok": out["deterministic_replay_ok"],
                "output": str(out_file),
            },
            ensure_ascii=False,
        )
    )
    return 0 if out["integration_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
