#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Controlled Provider Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_planning_v1 import (
    BOUNDARY_FALSE,
    CONSTITUTION_BLOCKS,
    EVIDENCE_PACK_FIELDS,
    FINAL_DECISION_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_FORBIDDEN,
    OCR_REQUEST_FIELDS,
    OCR_RESULT_FIELDS,
    PHASE_ID,
    PROVIDER_CANDIDATES,
    ROI_FIELDS,
    SCOPE,
)
from capabilities.governance.vision_ocr_voice_controlled_optimization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as VOV_POST_FINAL,
)

MIN_CHECKS = 85

REQUIRED = (
    "ocr_controlled_provider_planning_policy_v1.json",
    "upstream_controlled_optimization_review_input_review_v1.json",
    "ocr_controlled_provider_scope_v1.json",
    "ocr_provider_candidate_registry_plan_v1.json",
    "ocr_provider_admission_gate_plan_v1.json",
    "ocr_request_candidate_contract_v1.json",
    "ocr_roi_candidate_contract_v1.json",
    "ocr_result_candidate_contract_v1.json",
    "ocr_evidence_pack_candidate_contract_v1.json",
    "ocr_timeout_fallback_plan_v1.json",
    "ocr_health_binding_plan_v1.json",
    "ocr_constitution_boundary_plan_v1.json",
    "ocr_midplatform_flow_binding_plan_v1.json",
    "ocr_no_runtime_boundary_matrix_v1.json",
    "ocr_controlled_provider_dryrun_plan_v1.json",
    "ocr_controlled_provider_non_claims_register_v1.json",
    "ocr_controlled_provider_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning",
    )
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_ocr_voice_controlled_optimization_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.vision_ocr_voice_controlled_optimization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "upstream_controlled_optimization_review_input_review_v1.json")
    scope = _load(root / "ocr_controlled_provider_scope_v1.json")
    registry = _load(root / "ocr_provider_candidate_registry_plan_v1.json")
    request_c = _load(root / "ocr_request_candidate_contract_v1.json")
    roi_c = _load(root / "ocr_roi_candidate_contract_v1.json")
    result_c = _load(root / "ocr_result_candidate_contract_v1.json")
    evidence_c = _load(root / "ocr_evidence_pack_candidate_contract_v1.json")
    health = _load(root / "ocr_health_binding_plan_v1.json")
    constitution = _load(root / "ocr_constitution_boundary_plan_v1.json")
    flow = _load(root / "ocr_midplatform_flow_binding_plan_v1.json")
    boundary = _load(root / "ocr_no_runtime_boundary_matrix_v1.json")
    dryrun_plan = _load(root / "ocr_controlled_provider_dryrun_plan_v1.json")
    decision = _load(root / "ocr_controlled_provider_planning_decision_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_controlled_provider_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.no_paddle", summary.get("paddleocr_invoked_now") is False)
    ok("summary.no_rapid", summary.get("rapidocr_invoked_now") is False)
    ok("summary.no_real", summary.get("real_ocr_provider_invoked_now") is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.closed", input_review.get("controlled_optimization_dryrun_closed") is True)
    ok("input.trusted", input_review.get("three_chain_readiness_trusted") is True)
    ok("input.ocr_ready", input_review.get("ocr_readiness_ready") is True)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.final", post_sm.get("final_decision") == VOV_POST_FINAL)

    ok("scope.forbid_paddle", "paddleocr_invocation" in (scope.get("forbidden_now") or []))
    ok("registry.count4", registry.get("provider_count") == 4)
    ok("registry.all_invocation_false", registry.get("all_invocation_allowed_false") is True)

    for field in OCR_REQUEST_FIELDS:
        ok(f"request.{field[:14]}", field in (request_c.get("fields") or []))
    ok("request.no_submit", request_c.get("defaults", {}).get("submit_allowed") is False)
    ok("request.no_invoke", request_c.get("defaults", {}).get("provider_invocation_allowed") is False)

    for field in ROI_FIELDS:
        ok(f"roi.{field[:14]}", field in (roi_c.get("fields") or []))
    ok("roi.no_read", roi_c.get("defaults", {}).get("image_read_allowed") is False)

    for field in OCR_RESULT_FIELDS:
        ok(f"result.{field[:14]}", field in (result_c.get("fields") or []))
    ok("result.not_fact", result_c.get("defaults", {}).get("fact_status") == "not_fact")

    for field in EVIDENCE_PACK_FIELDS:
        ok(f"evidence.{field[:14]}", field in (evidence_c.get("fields") or []))
    ok("evidence.no_wm", evidence_c.get("defaults", {}).get("world_model_write_allowed") is False)

    ok("health.bind6", len(health.get("bindings") or []) == 6)
    ok("constitution.blocks7", len(constitution.get("blocks") or []) == 7)
    ok("flow.length6", len(flow.get("flow") or []) == 6)
    ok("boundary.pass", boundary.get("all_pass") is True)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)

    families = {p["provider_family"] for p in PROVIDER_CANDIDATES}
    ok("provider.mock", "mock_or_fixture" in families)
    ok("provider.paddle_later", "paddleocr_later" in families)
    ok("provider.rapid_later", "rapidocr_later" in families)

    for prov in registry.get("providers") or []:
        ok(f"prov.{prov.get('provider_candidate_id', 'x')[:16]}", prov.get("invocation_allowed") is False)

    for hb in HEALTH_BINDINGS:
        ok(f"health.{hb['trigger'][:14]}", True)
    for block in CONSTITUTION_BLOCKS:
        ok(f"block.{block['block_id'][:18]}", block.get("blocked") is True)
    for forbidden in OCR_FORBIDDEN:
        ok(f"forbid.{forbidden[:14]}", forbidden in (scope.get("forbidden_now") or []))

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "ocr_controlled_provider_non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
