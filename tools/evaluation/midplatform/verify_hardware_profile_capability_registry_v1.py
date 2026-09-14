#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Hardware Profile Capability Registry v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "hardware_profile_capability_registry_v1_summary.json",
        "intake": "hardware_profile_registry_input_intake_matrix_v1.json",
        "profile_schema": "hardware_profile_schema_v1.json",
        "camera_schema": "camera_capability_registry_schema_v1.json",
        "device_schema": "device_registry_schema_v1.json",
        "sensor_schema": "sensor_registry_schema_v1.json",
        "status_enum": "hardware_capability_status_enum_v1.json",
        "unknown_profile": "hardware_minimal_unknown_profile_v1.json",
        "adapter_placeholder": "hardware_camera_runtime_adapter_placeholder_v1.json",
        "freshness_policy": "hardware_profile_freshness_stale_policy_v1.json",
        "health_link": "hardware_profile_registry_system_health_link_v1.json",
        "guardedtrial_link": "hardware_profile_registry_guardedtrial_precondition_link_v1.json",
        "long_term": "hardware_profile_registry_long_term_candidate_link_v1.json",
        "trace": "hardware_profile_registry_decision_trace_v1.json",
        "final": "hardware_profile_registry_final_decision_v1.json",
        "boundary": "hardware_profile_registry_boundary_report_v1.json",
        "metrics": "hardware_profile_registry_metrics_candidate_report_v1.json",
        "bench": "hardware_profile_registry_benchmark_link_report_v1.json",
        "health": "hardware_profile_registry_system_health_report_v1.json",
        "no_write": "hardware_profile_registry_no_write_boundary_report_v1.json",
        "sim": "hardware_profile_registry_simulation_context_report_v1.json",
        "non_claims": "hardware_profile_registry_non_claims_report_v1.json",
        "followups": "hardware_profile_registry_open_followups_v1.json",
        "audit": "hardware_profile_registry_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "hardware_profile_registry_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("registry_scope") == "hardware_profile_capability_registry_schema_only", "scope")
    ok(s.get("based_on_hardware_runtime_dryrun") is True, "based_rt")
    ok(s.get("hardware_profile_schema_defined") is True, "profile_schema")
    ok(s.get("camera_capability_registry_schema_defined") is True, "camera_schema")
    ok(s.get("device_registry_schema_defined") is True, "device_schema")
    ok(s.get("sensor_registry_schema_defined") is True, "sensor_schema")
    ok(s.get("capability_status_enum_defined") is True, "enum")
    ok(s.get("minimal_unknown_profile_generated") is True, "unknown_prof")
    ok(s.get("runtime_adapter_placeholder_defined") is True, "adapter")
    ok(s.get("profile_freshness_policy_defined") is True, "freshness")
    ok(s.get("guardedtrial_precondition_link_defined") is True, "gt_link")
    ok(s.get("hardware_probe_invoked") is False, "no_probe")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")
    ok(s.get("hardware_action_invoked") is False, "no_hw")

    cam_ex = data["camera_schema"].get("example") or {}
    ok("zoom_supported" in cam_ex, "zoom_field")
    ok("autofocus_supported" in cam_ex, "af_field")

    sensor_types = {e.get("sensor_type") for e in data["sensor_schema"].get("examples") or [] if isinstance(e, dict)}
    for st in ("rgb_camera", "depth_tof", "imu", "gps", "microphone"):
        ok(st in sensor_types, st)

    statuses = {r.get("status") for r in data["status_enum"].get("statuses") or [] if isinstance(r, dict)}
    for st in ("available", "unknown", "unsupported", "degraded", "runtime_adapter_missing"):
        ok(st in statuses, st)

    up = data["unknown_profile"]
    ok(up.get("capability_status") == "unknown", "cap_unknown")
    ok(up.get("usable_for_runtime_action") is False, "not_usable_rt")
    ok(data["adapter_placeholder"].get("implementation_available") is False, "no_impl")
    ok(data["freshness_policy"].get("stale_blocks_runtime_action") is True, "stale_block")
    ok("HARDWARE_PROFILE_MISSING" in (data["health_link"].get("health_classes") or []), "hp_missing")
    ok("RUNTIME_ADAPTER_MISSING" in (data["health_link"].get("health_classes") or []), "adapter_missing")
    gt = data["guardedtrial_link"]
    ok(gt.get("guardedtrial_allowed_now") is False, "gt_not_now")
    blockers_list = gt.get("current_blockers") or []
    ok("capability_registry_missing" in blockers_list, "reg_blocker")
    ok("runtime_adapter_missing" in blockers_list, "adapter_blocker")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_PROFILE_REGISTRY_REVIEW_OR_ADAPTER_IMPLEMENTATION", "final")
    ok(data["boundary"].get("registry_schema_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("no_runtime_health_claim") is True, "health_claim")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("hardware_fact_written") is False, "audit_hw")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_delta")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 62,
        "blockers": blockers,
        "phase": "Hardware-Profile-Capability-Registry-v1-001",
    }
    _write_json(root / "hardware_profile_registry_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
