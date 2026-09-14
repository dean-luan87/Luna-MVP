#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Voice Controlled Optimization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.post_health_management_roadmap_decision_v1 import SELECTED_ROUTE
from capabilities.governance.vision_ocr_voice_controlled_optimization_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE_DRYRUN,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REGISTRY_BIND_MODELS,
    SCOPE,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    CONSTITUTION_BLOCKS,
    CROSS_CHAIN_DEPS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 90

REQUIRED = (
    "vision_ocr_voice_controlled_optimization_dryrun_policy_v1.json",
    "controlled_optimization_planning_input_review_v1.json",
    "vision_readiness_candidate_result_v1.json",
    "ocr_readiness_candidate_result_v1.json",
    "voice_readiness_candidate_result_v1.json",
    "cross_chain_dependency_dryrun_result_v1.json",
    "model_registry_binding_dryrun_result_v1.json",
    "health_management_binding_dryrun_result_v1.json",
    "constitution_boundary_dryrun_result_v1.json",
    "midplatform_candidate_flow_dryrun_result_v1.json",
    "controlled_provider_readiness_dryrun_matrix_v1.json",
    "no_runtime_boundary_audit_v1.json",
    "blocked_path_result_v1.json",
    "phased_optimization_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_ocr_voice_controlled_optimization_dryrun"
        ),
    )
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_ocr_voice_controlled_optimization_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_ocr_voice_controlled_optimization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    vision = _load(root / "vision_readiness_candidate_result_v1.json")
    ocr = _load(root / "ocr_readiness_candidate_result_v1.json")
    voice = _load(root / "voice_readiness_candidate_result_v1.json")
    cross = _load(root / "cross_chain_dependency_dryrun_result_v1.json")
    registry = _load(root / "model_registry_binding_dryrun_result_v1.json")
    health = _load(root / "health_management_binding_dryrun_result_v1.json")
    constitution = _load(root / "constitution_boundary_dryrun_result_v1.json")
    matrix = _load(root / "controlled_provider_readiness_dryrun_matrix_v1.json")
    audit = _load(root / "no_runtime_boundary_audit_v1.json")
    blocked = _load(root / "blocked_path_result_v1.json")
    readiness = _load(root / "phased_optimization_readiness_decision_v1.json")
    input_review = _load(root / "controlled_optimization_planning_input_review_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("vision_ocr_voice_controlled_optimization_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.readiness_gen", summary.get("controlled_optimization_readiness_candidate_generated_now") is True)
    ok("summary.no_provider", summary.get("controlled_provider_enabled_now") is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.ocr_p0", plan_sm.get("ocr_p0_first") is True)
    ok("upstream.route", summary.get("selected_route") == SELECTED_ROUTE)

    ok("vision.type", vision.get("candidate_type") == "vision_controlled_optimization_readiness_candidate")
    ok("vision.sample_scope", vision.get("source_scope") == "sample_or_controlled_frame_reference_only")
    ok("vision.no_real", vision.get("real_vision_model_allowed") is False)
    ok("vision.no_camera", vision.get("live_camera_allowed") is False)
    ok("vision.candidate_only", vision.get("candidate_only") is True)

    ok("ocr.type", ocr.get("candidate_type") == "ocr_controlled_provider_readiness_candidate")
    ok("ocr.mock_ready", ocr.get("mock_to_controlled_provider_planning_ready") is True)
    ok("ocr.no_paddle", ocr.get("paddleocr_allowed") is False)
    ok("ocr.no_real", ocr.get("real_ocr_provider_allowed") is False)
    ok("ocr.p0", ocr.get("p0_priority") == 1)

    ok("voice.type", voice.get("candidate_type") == "voice_boundary_readiness_candidate")
    ok("voice.partial", voice.get("controlled_provider_planning_allowed") == "partial")
    ok("voice.no_asr", voice.get("real_asr_allowed") is False)
    ok("voice.no_tts", voice.get("real_tts_allowed") is False)

    ok("cross.count6", cross.get("edge_count") == 6)
    ok("cross.pass", cross.get("routing_pass") is True)
    ok("registry.pass", registry.get("binding_pass") is True)
    ok("registry.count4", len(registry.get("bindings") or []) == 4)
    ok("health.pass", health.get("routing_pass") is True)
    ok("health.no_auto", health.get("no_automatic_fallback") is True)
    ok("constitution.all", constitution.get("all_blocked") is True)
    ok("matrix.all3", matrix.get("all_three_generated") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count14", len(blocked.get("paths") or []) == 14)
    ok("ready.review", readiness.get("ready_for_post_dryrun_review") is True)

    for mid in REGISTRY_BIND_MODELS:
        binds = registry.get("bindings") or []
        row = next((b for b in binds if b.get("model_id") == mid), None)
        ok(f"registry.{mid[:10]}", row is not None and row.get("invocation_allowed") is False)

    for edge in CROSS_CHAIN_DEPS:
        ok(f"edge.{edge['edge_id']}", cross.get("routing_pass") is True)
    for hb in HEALTH_BINDINGS:
        ok(f"health.{hb['trigger'][:14]}", health.get("routing_pass") is True)
    for block in CONSTITUTION_BLOCKS:
        ok(f"block.{block['block_id'][:16]}", constitution.get("all_blocked") is True)
    for pid in BLOCKED_PATHS:
        paths = blocked.get("paths") or []
        row = next((p for p in paths if p.get("path_id") == pid), None)
        ok(f"path.{pid[:20]}", row is not None and row.get("blocked") is True)

    for field in BOUNDARY_FALSE_DRYRUN:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
