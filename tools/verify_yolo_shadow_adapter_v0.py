#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-ModelPerception-002B

Verifier for YOLO Shadow Adapter v0, aligned with admission matrix A–L (subset/smoke).

Hard boundaries:
- Does not call real YOLO by default (uses mock detector).
- Can validate disable switch, fallback, forbidden probes, schema validation, and artifact presence.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_perception.yolo_shadow_adapter_v0 import (
    PhoneLocalSampleRefV0,
    YoloShadowAdapterConfigV0,
    run_yolo_shadow_adapter_on_sample_v0,
)


@dataclass
class VerifyCaseResult:
    case_id: str
    passed: bool
    details: Dict[str, Any]


class MockDetector:
    def __init__(self, mode: str):
        self.mode = mode

    def initialize(self, model_path: str) -> bool:
        if self.mode == "dependency_unavailable":
            raise RuntimeError("mock_dependency_unavailable")
        return True

    def detect(self, frame: Any) -> List[Dict[str, Any]]:
        if self.mode == "malformed_raw_output":
            return [{"bbox": [0, 0, 1, 1], "confidence": 0.9}]  # missing class_id/class_name
        if self.mode == "forbidden_execute_probe":
            return [{"bbox": [0, 0, 1, 1], "confidence": 0.9, "class_id": 0, "class_name": "execute_now"}]
        if self.mode == "forbidden_default_path_probe":
            return [{"bbox": [0, 0, 1, 1], "confidence": 0.9, "class_id": 0, "class_name": "enable_default_path"}]
        # valid default
        return [{"bbox": [10, 10, 20, 20], "confidence": 0.8, "class_id": 0, "class_name": "person"}]


def _exists(p: str) -> bool:
    return bool(p) and os.path.exists(p)


def _load_json(p: str) -> Any:
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _run_case(case_id: str, *, cfg: YoloShadowAdapterConfigV0, detector: Optional[MockDetector], tmp_out: str) -> VerifyCaseResult:
    # Use a known existing phone_local video to exercise the frame loop while still
    # keeping inference mocked via detector_override.
    fallback_video = "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_002/phone_local_001_clear_path.mp4"
    source_video = fallback_video if os.path.exists(fallback_video) else "__nonexistent__.mp4"
    sample = PhoneLocalSampleRefV0(
        sample_id=f"verify_{case_id}",
        source_video_path=source_video,
        archive_root="__none__",
        evidence_type="phone_local_controlled_capture",
        controlled_live_stream=False,
        phone_local_capture=True,
    )

    out = run_yolo_shadow_adapter_on_sample_v0(
        sample=sample,
        cfg=cfg,
        output_root=tmp_out,
        workspace_roots_for_media=[tmp_out, "/Users/luanlei/Desktop/Luna-Workspace-Min", "/Users/luanlei/Desktop/Luna-Core"],
        detector_override=detector,
    )

    # Per-sample artifact checks
    sample_dir = os.path.join(tmp_out, sample.sample_id)
    expected = {
        "trace": os.path.join(sample_dir, "yolo_shadow_trace.jsonl"),
        "replay": os.path.join(sample_dir, "yolo_shadow_replay.jsonl"),
        "whitebox": os.path.join(sample_dir, "yolo_shadow_whitebox.jsonl"),
        "result_json": os.path.join(sample_dir, "per_sample_yolo_shadow_results.json"),
    }

    artifacts_ok = all(_exists(p) for p in expected.values())
    details = {"adapter_out": out, "expected_artifacts": expected, "artifacts_ok": artifacts_ok}

    # Case-specific assertions (smoke-level)
    if case_id == "disable_switch_case":
        passed = (out.get("yolo_invoked") is False) and (out.get("fallback_used") is True) and (out.get("fallback_reason") == "yolo_disabled") and artifacts_ok
        return VerifyCaseResult(case_id=case_id, passed=passed, details=details)

    if case_id == "dependency_unavailable_case":
        passed = (out.get("fallback_used") is True) and (out.get("fallback_reason", "").startswith("detector_initialize_failed")) and artifacts_ok
        return VerifyCaseResult(case_id=case_id, passed=passed, details=details)

    if case_id == "forbidden_execute_probe_case":
        passed = (out.get("fallback_used") is True) and (out.get("fallback_reason") == "forbidden_output_blocked") and artifacts_ok
        return VerifyCaseResult(case_id=case_id, passed=passed, details=details)

    if case_id == "forbidden_default_path_probe_case":
        passed = (out.get("fallback_used") is True) and (out.get("fallback_reason") == "forbidden_output_blocked") and artifacts_ok
        return VerifyCaseResult(case_id=case_id, passed=passed, details=details)

    if case_id == "valid_yolo_shadow_case":
        passed = (out.get("fallback_used") is False) and (out.get("yolo_invoked") is True) and artifacts_ok
        return VerifyCaseResult(case_id=case_id, passed=passed, details=details)

    # Default: must at least be auditable and not executable.
    passed = artifacts_ok and (out.get("allows_execute_now") is False)
    return VerifyCaseResult(case_id=case_id, passed=passed, details=details)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default=None, help="Optional; if omitted, uses a temp dir.")
    args = ap.parse_args()

    out_root = args.output_root or os.path.join(tempfile.gettempdir(), f"yolo_shadow_verify_{int(time.time())}")
    os.makedirs(out_root, exist_ok=True)

    results: List[VerifyCaseResult] = []

    # A) disable switch (must not invoke)
    cfg_disable = YoloShadowAdapterConfigV0(disable_yolo=True, max_frames=1, frame_step=1)
    results.append(_run_case("disable_switch_case", cfg=cfg_disable, detector=None, tmp_out=out_root))

    # B) dependency unavailable (initialize raises)
    cfg_enabled = YoloShadowAdapterConfigV0(disable_yolo=False, max_frames=1, frame_step=1)
    results.append(_run_case("dependency_unavailable_case", cfg=cfg_enabled, detector=MockDetector("dependency_unavailable"), tmp_out=out_root))

    # C/D) forbidden probes
    results.append(_run_case("forbidden_execute_probe_case", cfg=cfg_enabled, detector=MockDetector("forbidden_execute_probe"), tmp_out=out_root))
    results.append(_run_case("forbidden_default_path_probe_case", cfg=cfg_enabled, detector=MockDetector("forbidden_default_path_probe"), tmp_out=out_root))

    # A) valid (mock)
    results.append(_run_case("valid_yolo_shadow_case", cfg=cfg_enabled, detector=MockDetector("valid"), tmp_out=out_root))

    # Write report
    report = {
        "phase": "Phase-ModelPerception-002B",
        "tool": "verify_yolo_shadow_adapter_v0.py",
        "generated_at_s": time.time(),
        "output_root": out_root,
        "cases": [{"case_id": r.case_id, "passed": r.passed, "details": r.details} for r in results],
        "passed": all(r.passed for r in results),
    }
    report_path = os.path.join(out_root, "yolo_shadow_verifier_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=False)

    print(report_path)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

