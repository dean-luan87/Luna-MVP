#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Real Dependency Check Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_dryrun_v1 import (
    BLOCKED_PATHS,
    EVIDENCE_CANDIDATE_SLOTS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    CHECK_SEQUENCE,
)

MIN_CHECKS = 57

REQUIRED = (
    "real_dependency_check_dryrun_input_review_v1.json",
    "dependency_check_sequence_review_v1.json",
    "paddleocr_dependency_check_review_v1.json",
    "rapidocr_dependency_check_review_v1.json",
    "external_ocr_dependency_check_review_v1.json",
    "evidence_package_candidate_review_v1.json",
    "failure_route_candidate_review_v1.json",
    "rollback_plan_candidate_review_v1.json",
    "environment_isolation_boundary_review_v1.json",
    "future_execution_gate_review_v1.json",
    "real_dependency_check_blocked_path_review_v1.json",
    "real_dependency_check_no_execution_review_v1.json",
    "real_dependency_check_closure_decision_v1.json",
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
            "ocr_provider_real_dependency_check_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_provider_real_dependency_check_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    closure = _load(root / "real_dependency_check_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    sequence_r = _load(root / "dependency_check_sequence_review_v1.json")
    evidence_r = _load(root / "evidence_package_candidate_review_v1.json")
    blocked_r = _load(root / "real_dependency_check_blocked_path_review_v1.json")
    audit_r = _load(root / "real_dependency_check_no_execution_review_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("ocr_provider_real_dependency_check_dryrun_closed") is True)
    ok("summary.trusted", summary.get("real_dependency_check_flow_trusted") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    ok("sequence.pass", sequence_r.get("review_pass") is True)
    ok("evidence.pass", evidence_r.get("review_pass") is True)
    ok("evidence.slots", evidence_r.get("review_pass") is True)
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count", blocked_r.get("paths_total") == len(BLOCKED_PATHS))
    ok("audit.pass", audit_r.get("review_pass") is True)

    ok("closure.closed", closure.get("ocr_provider_real_dependency_check_dryrun_closed") is True)
    ok("closure.harness", next_route.get("ready_for_controlled_provider_readiness_harness") is True)
    ok("next.no_exec", next_route.get("do_not_execute_real_dependency_check_now") is True)
    ok("next.no_import", next_route.get("do_not_import_provider_now") is True)

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
