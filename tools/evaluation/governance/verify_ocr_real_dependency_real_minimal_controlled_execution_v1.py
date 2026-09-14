#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Minimal Controlled Execution v1."""

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
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1 import (
    FINAL_DECISION_GO as READY_FINAL,
    NEXT_PHASE_GO as READY_NEXT,
)
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE_EXECUTED,
    FINAL_DECISION_FAIL,
    FINAL_DECISION_PASS,
    FINAL_DECISION_VIOLATION,
    NEXT_PHASE_POST_REVIEW,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 65

REQUIRED = (
    "real_minimal_controlled_execution_policy_v1.json",
    "final_ready_check_input_review_v1.json",
    "execution_environment_snapshot_v1.json",
    "package_presence_check_result_v1.json",
    "model_cache_path_check_result_v1.json",
    "model_file_existence_check_result_v1.json",
    "model_file_hash_check_result_v1.json",
    "provider_import_check_result_v1.json",
    "execution_boundary_audit_v1.json",
    "execution_failure_route_result_v1.json",
    "execution_rollback_result_v1.json",
    "execution_evidence_package_v1.json",
    "execution_non_claims_register_v1.json",
    "real_minimal_controlled_execution_decision_v1.json",
    "summary.json",
)

VALID_FINAL_DECISIONS = (
    FINAL_DECISION_PASS,
    FINAL_DECISION_FAIL,
    FINAL_DECISION_VIOLATION,
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_real_minimal_controlled_execution"
        ),
    )
    p.add_argument(
        "--final-ready-check-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    ready_root = Path(args.final_ready_check_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ready_vr = _load(ready_root / "verifier_report.json")
    ready_sm = _load(ready_root / "summary.json")
    summary = _load(root / "summary.json")
    pkg = _load(root / "package_presence_check_result_v1.json")
    cache = _load(root / "model_cache_path_check_result_v1.json")
    files = _load(root / "model_file_existence_check_result_v1.json")
    hashes = _load(root / "model_file_hash_check_result_v1.json")
    imp = _load(root / "provider_import_check_result_v1.json")
    audit = _load(root / "execution_boundary_audit_v1.json")
    evidence = _load(root / "execution_evidence_package_v1.json")
    decision = _load(root / "real_minimal_controlled_execution_decision_v1.json")

    ok("upstream.ready_go", ready_vr.get("verifier") == "GO")
    ok("upstream.ready_final", ready_sm.get("final_decision") == READY_FINAL)
    ok("upstream.ready_next", ready_sm.get("recommended_next_phase") == READY_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.real_phase", summary.get("real_minimal_controlled_execution_phase") is True)
    ok("summary.started", summary.get("real_execution_started_now") is True)
    ok("summary.completed", summary.get("execution_completed") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_valid", summary.get("final_decision") in VALID_FINAL_DECISIONS)
    ok("summary.post_review_next", summary.get("recommended_next_phase") == NEXT_PHASE_POST_REVIEW
       or summary.get("final_decision") == FINAL_DECISION_VIOLATION)

    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        ok(f"executed.{cid[:12]}", summary.get(f"{cid}_executed_now") is True)

    ok("pkg.executed", pkg.get("check_id") == "package_presence_check")
    ok("cache.executed", cache.get("check_id") == "model_cache_path_check")
    ok("files.executed", files.get("check_id") == "model_file_existence_check")
    ok("hash.executed", hashes.get("check_id") == "model_file_hash_check")
    ok("import.executed", imp.get("check_id") == "provider_import_check")
    ok("import.no_runtime", imp.get("runtime_invoked") is False)
    ok("import.no_ocr_init", imp.get("ocr_initialized") is False)

    ok("audit.ok", audit.get("boundary_ok") is True)
    ok("audit.smoke_blocked", audit.get("smoke_sample_ocr_blocked") is True)
    ok("evidence.count5", evidence.get("checks_executed_count") == 5)
    ok("decision.completed", decision.get("execution_completed") is True)

    for field in BOUNDARY_TRUE_EXECUTED:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("provider.null", summary.get("selected_provider_for_execution") is None)
    ok("no_finalize", summary.get("provider_selection_finalized_now") is False)
    ok("no_runtime_invoke", summary.get("provider_runtime_invoked_now") is False)

    ok("non_claims", len(_load(root / "execution_non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    execution_ok = (
        summary.get("execution_completed") is True
        and summary.get("boundary_ok") is True
        and summary.get("final_decision") in VALID_FINAL_DECISIONS
    )
    go = passed >= MIN_CHECKS and execution_ok and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "execution_completed": summary.get("execution_completed"),
        "checks_passed_all": summary.get("checks_passed"),
        "boundary_ok": summary.get("boundary_ok"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verifier": report["verifier"],
        "checks_passed": passed,
        "checks_total": total,
        "checks_passed_all": summary.get("checks_passed"),
        "final_decision": summary.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
