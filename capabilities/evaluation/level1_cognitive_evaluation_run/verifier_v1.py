from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from .archive_v1 import read_evaluation_run_record_v1


FORBIDDEN_ARCHIVE_ROOTS = ("_tmp_eval_out", "_eval_out")


def verify_summary_v1(summary: Dict[str, Any], *, repository_root: Path | None = None) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    issues: List[str] = []
    checks["run_boundary_valid"] = summary.get("run_boundary_valid") is True
    checks["registry_case_linkage_clean"] = not summary.get("run_boundary_errors")
    checks["a_route_bridge_does_not_own_cognition"] = summary.get("a_route_bridge_status") in {"PARTIAL", "BLOCKED"}
    checks["whitebox_v1_attached"] = summary.get("whitebox_attachment_status") == "ATTACHED"
    checks["archive_record_created"] = summary.get("archive_record_created") is True
    checks["archive_immutable"] = summary.get("archive_record_immutable") is True
    archive_location = str(summary.get("archive_location", ""))
    checks["archive_not_execution_output"] = not any(root in archive_location for root in FORBIDDEN_ARCHIVE_ROOTS)
    checks["synthetic_cannot_claim_cognition"] = (
        summary.get("synthetic") is True
        and summary.get("cognition_execution") is False
        and summary.get("result_status") != "EXECUTION_OBSERVED"
    )
    checks["no_forbidden_execution"] = all(
        summary.get(key) is False
        for key in ("model_invocation", "provider_invocation", "observation_execution", "action_execution")
    )
    checks["no_truth_or_promotion"] = all(
        summary.get(key) is False
        for key in (
            "world_truth_declared",
            "field_mutation",
            "memory_promotion",
            "experience_promotion",
            "knowledge_promotion",
        )
    )
    checks["unavailable_metrics_not_zero_filled"] = summary.get("runtime_metrics_availability") in {
        "not_observed",
        "unavailable",
        "planned",
    }
    checks["comparison_is_not_runtime_policy"] = summary.get("comparison_eligibility") == "planned"
    checks["no_record_validation_errors"] = not summary.get("record_validation_errors")
    if repository_root is not None and archive_location:
        path = repository_root / archive_location
        checks["archive_readable_and_valid"] = path.is_file()
        if path.is_file():
            try:
                read_evaluation_run_record_v1(path)
            except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                issues.append(f"archive_record_invalid:{type(exc).__name__}")
                checks["archive_readable_and_valid"] = False
    for name, passed in checks.items():
        if not passed:
            issues.append(name)
    return {
        "phase": "Phase-P1-Luna-Level1-Cognitive-Evaluation-Run-Boundary-And-Durable-Archive-Bridge-v1-001",
        "checks": checks,
        "issues": list(dict.fromkeys(issues)),
        "all_checks_passed": not issues,
        "runtime_execution": False,
        "model_invocation": False,
        "provider_invocation": False,
        "observation_execution": False,
        "action_execution": False,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.evaluation.level1_cognitive_evaluation_run.verifier_v1 <runner_summary.json>")
    summary_path = Path(sys.argv[1])
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    result = verify_summary_v1(summary, repository_root=Path.cwd())
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

