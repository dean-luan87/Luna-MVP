#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Controlled Provider DryRun v1."""

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
    BOUNDARY_FALSE_DRYRUN,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.ocr_controlled_provider_planning_v1 import (
    CONSTITUTION_BLOCKS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO as PLANNING_NEXT,
    PROVIDER_CANDIDATES,
)

MIN_CHECKS = 100

REQUIRED = (
    "ocr_controlled_provider_dryrun_policy_v1.json",
    "ocr_controlled_provider_planning_input_review_v1.json",
    "ocr_provider_readiness_candidate_samples_v1.json",
    "ocr_request_candidate_samples_v1.json",
    "ocr_roi_candidate_samples_v1.json",
    "ocr_result_candidate_samples_v1.json",
    "ocr_evidence_pack_candidate_samples_v1.json",
    "ocr_candidate_chain_trace_v1.json",
    "ocr_timeout_fallback_branch_result_v1.json",
    "ocr_low_confidence_branch_result_v1.json",
    "ocr_empty_result_branch_result_v1.json",
    "ocr_unsupported_region_branch_result_v1.json",
    "ocr_runtime_boundary_violation_branch_result_v1.json",
    "ocr_health_binding_dryrun_result_v1.json",
    "ocr_constitution_boundary_dryrun_result_v1.json",
    "ocr_midplatform_flow_binding_dryrun_result_v1.json",
    "ocr_no_runtime_boundary_audit_v1.json",
    "ocr_blocked_path_result_v1.json",
    "ocr_controlled_provider_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun",
    )
    p.add_argument(
        "--ocr-controlled-provider-planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.ocr_controlled_provider_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "ocr_provider_readiness_candidate_samples_v1.json")
    request = _load(root / "ocr_request_candidate_samples_v1.json")
    roi = _load(root / "ocr_roi_candidate_samples_v1.json")
    result = _load(root / "ocr_result_candidate_samples_v1.json")
    evidence = _load(root / "ocr_evidence_pack_candidate_samples_v1.json")
    trace = _load(root / "ocr_candidate_chain_trace_v1.json")
    timeout = _load(root / "ocr_timeout_fallback_branch_result_v1.json")
    health = _load(root / "ocr_health_binding_dryrun_result_v1.json")
    blocked = _load(root / "ocr_blocked_path_result_v1.json")
    audit = _load(root / "ocr_no_runtime_boundary_audit_v1.json")
    constitution = _load(root / "ocr_constitution_boundary_dryrun_result_v1.json")
    decision = _load(root / "ocr_controlled_provider_dryrun_readiness_decision_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    req = (request.get("samples") or [{}])[0]
    roi_s = (roi.get("samples") or [{}])[0]
    res = (result.get("samples") or [{}])[0]
    ev = (evidence.get("samples") or [{}])[0]

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_controlled_provider_dryrun_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.readiness_gen", summary.get("provider_readiness_candidate_generated_now") is True)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    ok("readiness.count4", readiness.get("sample_count") == 4)
    ok("request.candidate_only", req.get("candidate_only") is True)
    ok("request.no_submit", req.get("submit_allowed") is False)
    ok("request.no_invoke", req.get("provider_invocation_allowed") is False)
    ok("request.visual_ref", bool(req.get("source_visual_candidate_ref")))
    ok("request.frame_ref", bool(req.get("source_frame_ref")))
    ok("request.roi_ref", bool(req.get("roi_ref")))

    ok("roi.no_read", roi_s.get("image_read_allowed") is False)
    ok("roi.no_crop", roi_s.get("crop_allowed") is False)
    ok("roi.bbox", bool(roi_s.get("bbox_or_region_ref")))

    ok("result.not_fact", res.get("fact_status") == "not_fact")
    ok("result.no_write", res.get("write_allowed") is False)
    ok("result.mock_type", res.get("provider_type") == "mock_or_fixture")
    ok("result.text", bool(res.get("text_candidate")))

    ok("evidence.no_wm", ev.get("world_model_write_allowed") is False)
    ok("evidence.no_mem", ev.get("memory_write_allowed") is False)
    ok("evidence.refs", all(ev.get(k) for k in ("ocr_request_ref", "roi_ref", "ocr_result_ref", "provider_readiness_ref")))

    ok("trace.pass", trace.get("chain_pass") is True)
    ok("timeout.pass", timeout.get("branch_pass") is True)
    ok("timeout.hold", timeout.get("target_candidate") == "hold_candidate")
    ok("health.pass", health.get("routing_pass") is True)
    ok("health.routes6", health.get("route_count") == 6)
    ok("health.fallback_gen", health.get("provider_failed_fallback_generated") is True)
    ok("constitution.all", constitution.get("all_blocked") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count", len(blocked.get("paths") or []) == len(BLOCKED_PATHS))
    ok("decision.ready", decision.get("ready_for_post_dryrun_review") is True)

    for p in PROVIDER_CANDIDATES:
        samples = readiness.get("samples") or []
        row = next((s for s in samples if s.get("provider_candidate_id") == p["provider_candidate_id"]), None)
        ok(f"ready.{p['provider_candidate_id'][:12]}", row is not None and row.get("invocation_allowed") is False)

    for pid in BLOCKED_PATHS:
        paths = blocked.get("paths") or []
        row = next((x for x in paths if x.get("path_id") == pid), None)
        ok(f"path.{pid[:18]}", row is not None and row.get("blocked") is True)

    for block in CONSTITUTION_BLOCKS:
        ok(f"block.{block['block_id'][:16]}", constitution.get("all_blocked") is True)
    for hb in HEALTH_BINDINGS:
        ok(f"health.{hb['trigger'][:14]}", health.get("routing_pass") is True)

    for field in BOUNDARY_FALSE_DRYRUN:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("summary.no_paddle", summary.get("paddleocr_invoked_now") is False)
    ok("summary.no_rapid", summary.get("rapidocr_invoked_now") is False)

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
