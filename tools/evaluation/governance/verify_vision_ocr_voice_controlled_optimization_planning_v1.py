#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Voice Controlled Optimization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.post_health_management_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    SELECTED_ROUTE,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    BOUNDARY_FALSE,
    CONSTITUTION_BLOCKS,
    CROSS_CHAIN_DEPS,
    FINAL_DECISION_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_ALLOWED,
    OCR_FORBIDDEN,
    PHASE_ID,
    REGISTRY_BIND_MODELS,
    SCOPE,
    VISION_ALLOWED,
    VISION_FORBIDDEN,
    VOICE_ALLOWED,
    VOICE_FORBIDDEN,
)

MIN_CHECKS = 80

REQUIRED = (
    "vision_ocr_voice_controlled_optimization_planning_policy_v1.json",
    "post_health_roadmap_input_review_v1.json",
    "vision_controlled_optimization_scope_v1.json",
    "ocr_controlled_optimization_scope_v1.json",
    "voice_controlled_optimization_scope_v1.json",
    "cross_chain_dependency_matrix_v1.json",
    "model_registry_binding_plan_v1.json",
    "health_management_binding_plan_v1.json",
    "constitution_boundary_plan_v1.json",
    "midplatform_candidate_flow_binding_plan_v1.json",
    "controlled_provider_readiness_matrix_v1.json",
    "vision_controlled_provider_planning_v1.json",
    "ocr_controlled_provider_planning_v1.json",
    "voice_controlled_provider_planning_v1.json",
    "no_runtime_boundary_matrix_v1.json",
    "phased_optimization_roadmap_v1.json",
    "vision_ocr_voice_non_claims_register_v1.json",
    "vision_ocr_voice_planning_decision_v1.json",
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
            "vision_ocr_voice_controlled_optimization_planning"
        ),
    )
    p.add_argument(
        "--post-health-management-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "post_health_management_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.post_health_management_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "post_health_roadmap_input_review_v1.json")
    vision_scope = _load(root / "vision_controlled_optimization_scope_v1.json")
    ocr_scope = _load(root / "ocr_controlled_optimization_scope_v1.json")
    voice_scope = _load(root / "voice_controlled_optimization_scope_v1.json")
    cross = _load(root / "cross_chain_dependency_matrix_v1.json")
    registry = _load(root / "model_registry_binding_plan_v1.json")
    health = _load(root / "health_management_binding_plan_v1.json")
    constitution = _load(root / "constitution_boundary_plan_v1.json")
    readiness = _load(root / "controlled_provider_readiness_matrix_v1.json")
    ocr_plan = _load(root / "ocr_controlled_provider_planning_v1.json")
    boundary = _load(root / "no_runtime_boundary_matrix_v1.json")
    phased = _load(root / "phased_optimization_roadmap_v1.json")
    decision = _load(root / "vision_ocr_voice_planning_decision_v1.json")

    roadmap_sm = _load(roadmap_root / "summary.json")
    roadmap_vr = _load(roadmap_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("vision_ocr_voice_controlled_optimization_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.ocr_p0", summary.get("ocr_p0_first") is True)
    ok("summary.route", summary.get("selected_route") == SELECTED_ROUTE)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.health_closed", input_review.get("health_integration_closed") is True)
    ok("input.consumable", input_review.get("health_candidates_consumable") is True)
    ok("input.b_lite", input_review.get("b_lite_closed") is True)
    ok("input.task_closed", input_review.get("task_response_closed") is True)
    ok("input.backbone_closed", input_review.get("backbone_closed") is True)

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)

    ok("vision.allowed", len(vision_scope.get("allowed_now") or []) >= len(VISION_ALLOWED))
    ok("vision.forbidden", "live_camera" in (vision_scope.get("forbidden_now") or []))
    ok("ocr.p0", ocr_scope.get("p0_priority") == 1)
    ok("ocr.allowed", "ocr_mock_to_controlled_provider_planning" in (ocr_scope.get("allowed_now") or []))
    ok("ocr.no_paddle", "paddleocr_invocation" in (ocr_scope.get("forbidden_now") or []))
    ok("voice.no_tts", "tts_runtime" in (voice_scope.get("forbidden_now") or []))

    ok("cross.count6", cross.get("edge_count") == 6)
    ok("registry.bind4", len(registry.get("bindings") or []) == 4)
    ok("health.bind6", len(health.get("bindings") or []) == 6)
    ok("constitution.blocks7", len(constitution.get("blocks") or []) == 7)

    ocr_chain = readiness.get("chains", {}).get("OCR", {})
    ok("readiness.ocr_mock", ocr_chain.get("current_status") == "mock_result_candidate_ready")
    ok("readiness.ocr_plan", ocr_chain.get("controlled_provider_planning_allowed") is True)
    ok("readiness.ocr_no_real", ocr_chain.get("real_provider_allowed") is False)
    ok("readiness.vision", readiness.get("chains", {}).get("Vision", {}).get("real_runtime_allowed") is False)
    ok("readiness.voice_partial", readiness.get("chains", {}).get("Voice", {}).get("controlled_provider_planning_allowed") == "partial")

    ok("ocr_plan.p0", ocr_plan.get("p0_first") is True)
    ok("ocr_plan.no_real", ocr_plan.get("real_provider_invoked_now") is False)
    ok("boundary.all_pass", boundary.get("all_pass") is True)
    ok("decision.pass", decision.get("planning_pass") is True)

    ok("phased.p0_ocr", (phased.get("phases") or [{}])[0].get("items", [""])[0].startswith("OCR"))
    ok("phased.next_dryrun", phased.get("recommended_next_phase") == NEXT_PHASE_GO)

    for mid in REGISTRY_BIND_MODELS:
        binds = registry.get("bindings") or []
        row = next((b for b in binds if b.get("model_id") == mid), None)
        ok(f"registry.{mid[:12]}", row is not None and row.get("invocation_allowed") is False)

    for item in VISION_ALLOWED[:3]:
        ok(f"vision_allow.{item[:12]}", item in (vision_scope.get("allowed_now") or []))
    for item in OCR_FORBIDDEN[:2]:
        ok(f"ocr_forbid.{item[:12]}", item in (ocr_scope.get("forbidden_now") or []))
    for item in VOICE_ALLOWED[:2]:
        ok(f"voice_allow.{item[:12]}", item in (voice_scope.get("allowed_now") or []))

    for edge in CROSS_CHAIN_DEPS:
        ok(f"edge.{edge['edge_id']}", True)
    for hb in HEALTH_BINDINGS:
        ok(f"health.{hb['trigger'][:14]}", True)
    for block in CONSTITUTION_BLOCKS:
        ok(f"block.{block['block_id'][:16]}", True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("defer.metric", summary.get("defer_health_metric_baseline_planning") is True)
    ok("non_claims", len(_load(root / "vision_ocr_voice_non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
