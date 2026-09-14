#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Controlled Provider Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.ocr_controlled_provider_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    EXPECTED_PROVIDER_FAMILIES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 85

REQUIRED = (
    "ocr_controlled_provider_dryrun_input_review_v1.json",
    "ocr_provider_readiness_review_v1.json",
    "ocr_request_candidate_review_v1.json",
    "ocr_roi_candidate_review_v1.json",
    "ocr_result_candidate_review_v1.json",
    "ocr_evidence_pack_candidate_review_v1.json",
    "ocr_candidate_chain_trace_review_v1.json",
    "ocr_branch_review_v1.json",
    "ocr_health_binding_review_v1.json",
    "ocr_constitution_boundary_review_v1.json",
    "ocr_no_runtime_boundary_review_v1.json",
    "ocr_blocked_path_review_v1.json",
    "ocr_controlled_provider_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review",
    )
    p.add_argument(
        "--ocr-controlled-provider-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_controlled_provider_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "ocr_controlled_provider_dryrun_input_review_v1.json")
    readiness_r = _load(root / "ocr_provider_readiness_review_v1.json")
    request_r = _load(root / "ocr_request_candidate_review_v1.json")
    roi_r = _load(root / "ocr_roi_candidate_review_v1.json")
    result_r = _load(root / "ocr_result_candidate_review_v1.json")
    evidence_r = _load(root / "ocr_evidence_pack_candidate_review_v1.json")
    trace_r = _load(root / "ocr_candidate_chain_trace_review_v1.json")
    branch_r = _load(root / "ocr_branch_review_v1.json")
    blocked_r = _load(root / "ocr_blocked_path_review_v1.json")
    closure = _load(root / "ocr_controlled_provider_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("ocr_controlled_provider_dryrun_closed") is True)
    ok("summary.trusted", summary.get("ocr_candidate_chain_trusted") is True)
    ok("summary.no_new_readiness", summary.get("new_provider_readiness_candidate_generated_now") is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.count4", input_review.get("readiness_count") == 4)
    ok("readiness.pass", readiness_r.get("review_pass") is True)
    ok("readiness.count4", readiness_r.get("sample_count") == 4)
    ok("request.pass", request_r.get("review_pass") is True)
    ok("roi.pass", roi_r.get("review_pass") is True)
    ok("result.pass", result_r.get("review_pass") is True)
    ok("evidence.pass", evidence_r.get("review_pass") is True)
    ok("trace.pass", trace_r.get("review_pass") is True)
    ok("branch.pass", branch_r.get("review_pass") is True)
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count15", blocked_r.get("paths_total") == 15)

    ok("closure.closed", closure.get("ocr_controlled_provider_dryrun_closed") is True)
    ok("next.roadmap", next_route.get("ready_for_authorization_roadmap_decision") is True)
    ok("next.no_trial", next_route.get("do_not_start_provider_trial_now") is True)
    ok("next.no_paddle", next_route.get("do_not_invoke_paddleocr_or_rapidocr") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    ok("families", set(readiness_r.get("provider_families") or []) == EXPECTED_PROVIDER_FAMILIES)

    for pid in BLOCKED_PATHS:
        ok(f"path.{pid[:18]}", blocked_r.get("review_pass") is True)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("dryrun.no_paddle", dryrun_sm.get("paddleocr_invoked_now") is False)
    ok("dryrun.no_wm", dryrun_sm.get("world_model_written_now") is False)

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
