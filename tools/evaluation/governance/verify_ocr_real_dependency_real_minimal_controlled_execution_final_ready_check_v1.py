#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Minimal Controlled Execution Final Ready Check v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    FINAL_DECISION_GO as PREFLIGHT_FINAL,
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MINIMAL_DRYRUN_FINAL,
)
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    FORBIDDEN_READY_CHECK,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_AUTH_DECISION_FINAL,
)
from capabilities.governance.ocr_real_dependency_real_minimal_execution_authorization_decision_v1 import (
    SELECTED_ROUTE,
)

MIN_CHECKS = 55

REQUIRED = (
    "final_ready_check_policy_v1.json",
    "upstream_input_review_v1.json",
    "minimal_execution_scope_lock_review_v1.json",
    "final_ready_check_result_v1.json",
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
            "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
        ),
    )
    p.add_argument(
        "--authorization-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_real_minimal_execution_authorization_decision"
        ),
    )
    p.add_argument(
        "--minimal-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--final-preflight-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_final_preflight"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    auth_root = Path(args.authorization_decision_root)
    dryrun_root = Path(args.minimal_dryrun_root)
    preflight_root = Path(args.final_preflight_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    auth_vr = _load(auth_root / "verifier_report.json")
    auth_sm = _load(auth_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    preflight_vr = _load(preflight_root / "verifier_report.json")
    preflight_sm = _load(preflight_root / "summary.json")
    summary = _load(root / "summary.json")
    policy = _load(root / "final_ready_check_policy_v1.json")
    scope = _load(root / "minimal_execution_scope_lock_review_v1.json")
    result = _load(root / "final_ready_check_result_v1.json")

    ok("upstream.auth_go", auth_vr.get("verifier") == "GO")
    ok("upstream.auth_final", auth_sm.get("final_decision") == UPSTREAM_AUTH_DECISION_FINAL)
    ok("upstream.route_a", auth_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == MINIMAL_DRYRUN_FINAL)
    ok("upstream.preflight_go", preflight_vr.get("verifier") == "GO")
    ok("upstream.preflight_final", preflight_sm.get("final_decision") == PREFLIGHT_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.ready_only", summary.get("final_ready_check_only") is True)
    ok("summary.pass", summary.get("ready_check_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.compressed", summary.get("compressed_short_chain") is True)
    ok("summary.not_started", summary.get("real_execution_started_now") is False)

    ok("policy.short_chain", len(policy.get("short_chain") or []) == 3)
    ok("policy.cancelled", len(policy.get("cancelled_phases") or []) == 2)

    ok("scope.pass", scope.get("scope_lock_pass") is True)
    ok("scope.allowed5", scope.get("scope_lock_checks", {}).get("allowed_count_5") is True)
    ok("scope.sandbox", scope.get("scope_lock_checks", {}).get("sandbox_confirmed") is True)
    ok("scope.owner_req", scope.get("scope_lock_checks", {}).get("owner_confirmation_required") is True)

    ok("result.ready", result.get("ready_for_real_execution") is True)
    ok("result.owner_not_collected", result.get("owner_confirmation_collected_now") is False)

    ok("summary.scope_minimal", summary.get("execution_scope") == "minimal_real_dependency_check")
    ok("summary.sandbox", summary.get("sandbox_required") is True)
    ok("summary.evidence", summary.get("evidence_required") is True)
    ok("summary.rollback", summary.get("rollback_required") is True)
    ok("summary.post", summary.get("post_execution_review_required") is True)

    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        ok(f"allowed.{cid[:12]}", cid in (summary.get("allowed_checks") or []))

    for fb in FORBIDDEN_READY_CHECK:
        ok(f"forbidden.{fb[:12]}", fb in (summary.get("forbidden") or []))

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("provider.null", summary.get("selected_provider_for_execution") is None)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("ready_check_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "ready_check_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "compressed_short_chain": True,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
