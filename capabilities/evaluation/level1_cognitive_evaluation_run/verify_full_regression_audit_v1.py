"""Fail-closed verifier for the read-only full-regression audit report."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Sequence


PHASE = "Phase-P1-Luna-Level1-Internal-Full-Regression-And-Data-Conformance-Audit-v1-001"


def verify_report_v1(report: Dict[str, Any]) -> Dict[str, Any]:
    findings = list(report.get("findings") or [])
    blockers = [item for item in findings if item.get("severity") == "BLOCKER"]
    majors = [item for item in findings if item.get("severity") == "MAJOR"]
    execution = report.get("execution_health") or {}
    runtime = report.get("runtime_data_conformance") or {}
    artifact = report.get("artifact_conformance") or {}
    session_evidence = report.get("session_evidence") or {}
    checks = {
        "phase_matches": report.get("phase") == PHASE,
        "execution_health_has_no_failed_checks": execution.get("failed", 0) == 0,
        "runtime_data_has_no_failed_checks": runtime.get("failed", 0) == 0,
        "artifact_data_has_no_failed_checks": artifact.get("failed", 0) == 0,
        "no_blocker_findings": not blockers,
        "no_major_findings": not majors,
        "session_evidence_provided": session_evidence.get("status") == "PROVIDED",
        "decision_candidate_not_blocked": not str(report.get("final_decision_candidate", "")).startswith("BLOCKED_"),
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {
        "phase": PHASE,
        "checks": checks,
        "issues": issues,
        "finding_counts": {
            "BLOCKER": len(blockers),
            "MAJOR": len(majors),
            "MINOR": sum(item.get("severity") == "MINOR" for item in findings),
            "INFO": sum(item.get("severity") == "INFO" for item in findings),
        },
        "all_checks_passed": not issues,
        "status": "WAITING_FOR_USER_TERMINAL_FULL_REGRESSION" if issues else "GO_CANDIDATE_PENDING_USER_REVIEW",
    }


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        raise SystemExit(
            "usage: python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_full_regression_audit_v1 <full_regression_audit_report_v1.json>"
        )
    path = Path(argv[0])
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        result: Dict[str, Any] = {
            "phase": PHASE,
            "checks": {"audit_report_readable": False},
            "issues": [f"audit_report_read_failed:{type(exc).__name__}"],
            "finding_counts": {},
            "all_checks_passed": False,
            "status": "WAITING_FOR_USER_TERMINAL_FULL_REGRESSION",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 1
    result = verify_report_v1(report if isinstance(report, dict) else {})
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
