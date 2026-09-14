"""Fail-closed verifier for Route-B admission-order adjudication."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from .engine_v1 import build_runtime_admission_order_summary_v1


OUTPUT_DIR = Path("_eval_out/perception_routing_admission_order_adjudication_v1")


def _check(checks: dict[str, bool], name: str, passed: bool) -> None:
    checks[name] = bool(passed)


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    proof = independent_case_proof(
        summary,
        build_runtime_admission_order_summary_v1,
        source="R11 canonical fixture + independent admission-order engine invocation",
        compare_top_level=("phase", "route"),
    )
    failed = sorted(name for name, passed in proof.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "checks": proof,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "proof_provenance": {
            "expected_source": "canonical fixture + independent admission-order engine invocation",
            "observed_source": "runner summary artifact",
            "recomputed_source": "fresh build_runtime_admission_order_summary_v1()",
        },
    }


def main() -> int:
    summary_path = OUTPUT_DIR / "runner_summary_v1.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    report = verify(summary)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "verifier_report_v1.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
