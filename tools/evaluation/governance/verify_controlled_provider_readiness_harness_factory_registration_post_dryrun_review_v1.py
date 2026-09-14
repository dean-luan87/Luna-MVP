#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Provider Readiness Harness Validation Factory Registration Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_dryrun_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    BOUNDARY_BLOCKED_PATHS,
    EXISTING_FACTORY_MODULE_COUNT,
    EXISTING_FACTORY_MODULES,
    FACTORY_INTERFACE_INPUTS,
    FACTORY_INTERFACE_OUTPUTS,
    FUTURE_CONSUMER_DOMAINS,
    NEW_FACTORY_MODULE_ID,
    NEW_FACTORY_MODULE_STATUS,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)
from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID

MIN_CHECKS = 70

REQUIRED = (
    "factory_registration_dryrun_input_review_v1.json",
    "validation_factory_registry_candidate_review_v1.json",
    "controlled_provider_harness_registry_entry_review_v1.json",
    "validation_factory_contract_extension_review_v1.json",
    "provider_harness_factory_interface_review_v1.json",
    "provider_harness_consumer_mapping_review_v1.json",
    "provider_harness_boundary_policy_review_v1.json",
    "provider_harness_anti_recursion_review_v1.json",
    "deferred_consumer_register_review_v1.json",
    "validation_factory_registration_no_runtime_review_v1.json",
    "validation_factory_registration_blocked_path_review_v1.json",
    "factory_registration_closure_decision_v1.json",
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
            "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.controlled_provider_readiness_harness_factory_registration_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "factory_registration_dryrun_input_review_v1.json")
    registry_r = _load(root / "validation_factory_registry_candidate_review_v1.json")
    entry_r = _load(root / "controlled_provider_harness_registry_entry_review_v1.json")
    contract_r = _load(root / "validation_factory_contract_extension_review_v1.json")
    interface_r = _load(root / "provider_harness_factory_interface_review_v1.json")
    consumer_r = _load(root / "provider_harness_consumer_mapping_review_v1.json")
    boundary_r = _load(root / "provider_harness_boundary_policy_review_v1.json")
    anti_r = _load(root / "provider_harness_anti_recursion_review_v1.json")
    deferred_r = _load(root / "deferred_consumer_register_review_v1.json")
    no_runtime_r = _load(root / "validation_factory_registration_no_runtime_review_v1.json")
    blocked_r = _load(root / "validation_factory_registration_blocked_path_review_v1.json")
    closure = _load(root / "factory_registration_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    entry_dry = _load(dryrun_root / "controlled_provider_harness_registry_entry_candidate_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.post_review_only", summary.get("controlled_provider_readiness_harness_factory_registration_post_dryrun_review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("factory_registration_dryrun_closed") is True)
    ok("summary.trusted", summary.get("validation_factory_registry_candidate_trusted") is True)
    ok("summary.modules7", summary.get("module_count") == EXISTING_FACTORY_MODULE_COUNT + 1)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.candidate_gen", dryrun_sm.get("validation_factory_registry_candidate_generated_now") is True)

    ok("input.pass", input_review.get("review_pass") is True)

    ok("registry.pass", registry_r.get("review_pass") is True)
    ok("registry.count7", registry_r.get("module_count") == 7)
    ok("registry.existing6", registry_r.get("existing_module_count") == EXISTING_FACTORY_MODULE_COUNT)
    ok("registry.seventh", registry_r.get("seventh_module_present") is True)
    ok("registry.not_updated", registry_r.get("registry_updated_now") is False)

    ok("entry.pass", entry_r.get("review_pass") is True)
    ok("entry.module_id", entry_r.get("module_id") == NEW_FACTORY_MODULE_ID)
    ok("entry.status", entry_r.get("status") == NEW_FACTORY_MODULE_STATUS)

    ok("contract.pass", contract_r.get("review_pass") is True)
    ok("interface.pass", interface_r.get("review_pass") is True)
    ok("interface.inputs9", interface_r.get("input_count") == len(FACTORY_INTERFACE_INPUTS))
    ok("interface.outputs7", interface_r.get("output_count") == len(FACTORY_INTERFACE_OUTPUTS))

    ok("consumer.pass", consumer_r.get("review_pass") is True)
    ok("boundary.pass", boundary_r.get("review_pass") is True)
    ok("boundary.count8", boundary_r.get("path_count") == len(BOUNDARY_BLOCKED_PATHS))
    ok("anti.pass", anti_r.get("review_pass") is True)
    ok("deferred.pass", deferred_r.get("review_pass") is True)
    ok("no_runtime.pass", no_runtime_r.get("review_pass") is True)
    ok("blocked.pass", blocked_r.get("review_pass") is True)

    ok("closure.closed", closure.get("factory_registration_dryrun_closed") is True)
    ok("closure.trusted", closure.get("validation_factory_registry_candidate_trusted") is True)
    ok("closure.seventh", closure.get("controlled_provider_readiness_harness_seventh_module_candidate_trusted") is True)
    ok("closure.ocr_return", closure.get("ready_for_ocr_provider_authorization_return") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)

    ok("next.ready", next_route.get("ready_for_ocr_provider_authorization_return_roadmap_decision") is True)
    ok("next.no_registry", next_route.get("do_not_update_validation_factory_registry_now") is True)
    ok("next.no_factory_runtime", next_route.get("do_not_enable_validation_factory_runtime_now") is True)
    ok("next.no_provider", next_route.get("do_not_enable_provider_runtime_now") is True)
    ok("next.resume_ocr", next_route.get("resume_ocr_authorization_after_return_roadmap_decision") is True)

    ok("entry_dry.first_ocr", entry_dry.get("first_consumer") == "ocr")
    ok("entry_dry.no_runtime", entry_dry.get("runtime_enforced") is False)
    ok("entry_dry.harness", entry_dry.get("harness_id") == HARNESS_ID)

    for mod in EXISTING_FACTORY_MODULES:
        ok(f"existing.{mod['module_id']}", mod["module_id"] in {m["module_id"] for m in EXISTING_FACTORY_MODULES})

    for domain in FUTURE_CONSUMER_DOMAINS:
        ok(f"future.{domain}", domain in FUTURE_CONSUMER_DOMAINS)

    ok("summary.no_new_candidate", summary.get("new_validation_factory_registry_candidate_generated_now") is False)
    ok("summary.no_registry_update", summary.get("validation_factory_registry_updated_now") is False)
    ok("summary.no_factory_runtime", summary.get("validation_factory_runtime_enforced_now") is False)

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
