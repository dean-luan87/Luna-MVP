#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Voice Controlled Optimization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_voice_controlled_optimization_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    REGISTRY_BIND_MODELS,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUT_OF_SCOPE,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 70

REQUIRED = (
    "controlled_optimization_dryrun_input_review_v1.json",
    "vision_readiness_candidate_review_v1.json",
    "ocr_readiness_candidate_review_v1.json",
    "voice_readiness_candidate_review_v1.json",
    "cross_chain_dependency_review_v1.json",
    "model_registry_binding_review_v1.json",
    "health_management_binding_review_v1.json",
    "constitution_boundary_review_v1.json",
    "no_runtime_boundary_review_v1.json",
    "blocked_path_review_v1.json",
    "controlled_optimization_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
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
            "vision_ocr_voice_controlled_optimization_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_ocr_voice_controlled_optimization_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.vision_ocr_voice_controlled_optimization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "controlled_optimization_dryrun_input_review_v1.json")
    vision_r = _load(root / "vision_readiness_candidate_review_v1.json")
    ocr_r = _load(root / "ocr_readiness_candidate_review_v1.json")
    voice_r = _load(root / "voice_readiness_candidate_review_v1.json")
    cross_r = _load(root / "cross_chain_dependency_review_v1.json")
    registry_r = _load(root / "model_registry_binding_review_v1.json")
    health_r = _load(root / "health_management_binding_review_v1.json")
    constitution_r = _load(root / "constitution_boundary_review_v1.json")
    runtime_r = _load(root / "no_runtime_boundary_review_v1.json")
    blocked_r = _load(root / "blocked_path_review_v1.json")
    closure = _load(root / "controlled_optimization_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("controlled_optimization_dryrun_closed") is True)
    ok("summary.trusted", summary.get("three_chain_readiness_trusted") is True)
    ok("summary.no_new_readiness", summary.get("new_readiness_candidate_generated_now") is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.out_of_scope", "scene_intent_candidate" in (input_review.get("out_of_scope_confirmed") or []))

    ok("vision.pass", vision_r.get("review_pass") is True)
    ok("ocr.pass", ocr_r.get("review_pass") is True)
    ok("voice.pass", voice_r.get("review_pass") is True)
    ok("cross.pass", cross_r.get("review_pass") is True)
    ok("cross.count6", cross_r.get("edge_count") == 6)
    ok("registry.pass", registry_r.get("review_pass") is True)
    ok("health.pass", health_r.get("review_pass") is True)
    ok("health.count6", health_r.get("route_count") == 6)
    ok("constitution.pass", constitution_r.get("review_pass") is True)
    ok("runtime.pass", runtime_r.get("review_pass") is True)
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count14", blocked_r.get("paths_total") == 14)

    ok("closure.closed", closure.get("controlled_optimization_dryrun_closed") is True)
    ok("next.ocr", next_route.get("ready_for_ocr_controlled_provider_planning") is True)
    ok("next.preferred", next_route.get("preferred_next_chain") == "OCR")
    ok("next.no_paddle", next_route.get("do_not_invoke_paddleocr_or_rapidocr") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    present = input_review.get("readiness_candidates_present") or {}
    ok("dryrun.vision", present.get("vision") is True)
    ok("dryrun.ocr", present.get("ocr") is True)
    ok("dryrun.voice", present.get("voice") is True)

    for mid in REGISTRY_BIND_MODELS:
        ok(f"registry.{mid[:10]}", registry_r.get("review_pass") is True)

    for pid in BLOCKED_PATHS:
        ok(f"path.{pid[:18]}", blocked_r.get("review_pass") is True)

    for item in OUT_OF_SCOPE:
        ok(f"scope.{item[:12]}", item in (input_review.get("out_of_scope_confirmed") or []))

    for field in BOUNDARY_FALSE_REVIEW:
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
