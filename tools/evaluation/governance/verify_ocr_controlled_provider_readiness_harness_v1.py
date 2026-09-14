#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Controlled Provider Readiness Harness extraction v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    BOUNDARY_BLOCKED_DEFAULT,
    BOUNDARY_FALSE,
    DEPENDENCY_READINESS_FIELDS,
    ENVIRONMENT_READINESS_FIELDS,
    EVIDENCE_SLOTS,
    FINAL_DECISION_GO,
    FUTURE_CONSUMERS,
    HARNESS_ID,
    HARNESS_PHASES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_CANDIDATE_FAMILIES,
    PHASE_ID,
    PROVIDER_CANDIDATE_FIELDS,
    SCOPE,
)
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REAL_POST_FINAL,
    NEXT_PHASE_GO as REAL_POST_NEXT,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    FAILURE_HANDLING,
    ROLLBACK_RULES,
)

MIN_CHECKS = 91

REQUIRED = (
    "controlled_provider_readiness_harness_policy_v1.json",
    "ocr_first_consumer_input_review_v1.json",
    "controlled_provider_readiness_harness_contract_v1.json",
    "provider_candidate_contract_v1.json",
    "dependency_readiness_contract_v1.json",
    "environment_readiness_contract_v1.json",
    "provider_comparison_matrix_contract_v1.json",
    "real_dependency_check_contract_v1.json",
    "provider_evidence_package_contract_v1.json",
    "provider_failure_route_contract_v1.json",
    "provider_rollback_contract_v1.json",
    "provider_boundary_guard_contract_v1.json",
    "provider_authorization_readiness_contract_v1.json",
    "ocr_first_consumer_mapping_v1.json",
    "future_consumer_adoption_plan_v1.json",
    "controlled_provider_readiness_harness_validation_result_v1.json",
    "controlled_provider_readiness_harness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
    "harness_usage_guide_v1.md",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.ocr_provider_real_dependency_check_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    harness = _load(root / "controlled_provider_readiness_harness_contract_v1.json")
    ocr_map = _load(root / "ocr_first_consumer_mapping_v1.json")
    future = _load(root / "future_consumer_adoption_plan_v1.json")
    validation = _load(root / "controlled_provider_readiness_harness_validation_result_v1.json")
    real_dep = _load(root / "real_dependency_check_contract_v1.json")
    evidence = _load(root / "provider_evidence_package_contract_v1.json")
    boundary = _load(root / "provider_boundary_guard_contract_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")
    next_route = _load(post_root / "next_route_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.extraction_only", summary.get("controlled_provider_readiness_harness_extraction_only") is True)
    ok("summary.contract_gen", summary.get("harness_contract_generated_now") is True)
    ok("summary.ocr_validated", summary.get("harness_first_consumer_validated_now") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.harness_id", summary.get("harness_id") == HARNESS_ID)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == REAL_POST_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == REAL_POST_NEXT)
    ok("next.harness_ready", next_route.get("ready_for_controlled_provider_readiness_harness") is True)
    ok("next.no_exec", next_route.get("do_not_execute_real_dependency_check_now") is True)

    ok("harness.phases13", harness.get("phase_count") == len(HARNESS_PHASES))
    for phase in HARNESS_PHASES:
        ok(f"harness.phase.{phase}", phase in (harness.get("phases") or []))

    ok("ocr.domain", ocr_map.get("provider_domain") == "ocr")
    ok("ocr.validated", ocr_map.get("first_consumer_status") == "validated")
    ok("ocr.output", ocr_map.get("output_contract") == "ocr_result_candidate")
    ok("ocr.evidence", ocr_map.get("evidence_pack_contract") == "ocr_evidence_pack_candidate")
    for fam in OCR_CANDIDATE_FAMILIES:
        ok(f"ocr.family.{fam}", fam in (ocr_map.get("provider_candidate_families") or []))

    ok("future.count", len(future.get("consumers") or []) >= len(FUTURE_CONSUMERS))
    ok("future.no_runtime", future.get("future_consumer_runtime_enabled_now") is False)
    ok("future.config", future.get("future_consumer_adoption_requires_config") is True)

    ok("validation.complete", validation.get("harness_contract_complete") is True)
    ok("validation.ocr", validation.get("ocr_first_consumer_validated") is True)
    ok("validation.no_global", validation.get("harness_global_enforcement_now") is False)

    ok("real_dep.steps9", real_dep.get("step_count") == 9)
    ok("evidence.slots10", evidence.get("slot_count") == len(EVIDENCE_SLOTS))
    ok("boundary.paths", boundary.get("path_count") == len(BOUNDARY_BLOCKED_DEFAULT))

    ok("provider.fields", len(_load(root / "provider_candidate_contract_v1.json").get("required_fields") or []) == len(PROVIDER_CANDIDATE_FIELDS))
    ok("dep.fields", len(_load(root / "dependency_readiness_contract_v1.json").get("required_fields") or []) == len(DEPENDENCY_READINESS_FIELDS))
    ok("env.fields", len(_load(root / "environment_readiness_contract_v1.json").get("required_fields") or []) == len(ENVIRONMENT_READINESS_FIELDS))
    ok("failure.routes", len(_load(root / "provider_failure_route_contract_v1.json").get("routes") or []) == len(FAILURE_HANDLING))
    ok("rollback.rules", len(_load(root / "provider_rollback_contract_v1.json").get("rules") or []) >= len(ROLLBACK_RULES))

    ok("summary.no_runtime_enforce", summary.get("harness_runtime_enforced_globally_now") is False)
    ok("summary.no_invoke", summary.get("provider_invoked_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    guide = (root / "harness_usage_guide_v1.md").read_text(encoding="utf-8")
    ok("guide.harness_id", HARNESS_ID in guide)
    ok("guide.anti_recursion", "Anti-recursion" in guide)

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
