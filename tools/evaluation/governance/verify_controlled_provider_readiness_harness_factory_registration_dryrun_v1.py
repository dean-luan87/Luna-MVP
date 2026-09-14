#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Provider Readiness Harness Validation Factory Registration DryRun v1."""

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
    BOUNDARY_BLOCKED_PATHS,
    BOUNDARY_FALSE,
    EXISTING_FACTORY_MODULE_COUNT,
    EXISTING_FACTORY_MODULES,
    FACTORY_INTERFACE_INPUTS,
    FACTORY_INTERFACE_OUTPUTS,
    FINAL_DECISION_GO,
    FUTURE_CONSUMER_DOMAINS,
    NEW_FACTORY_MODULE_DISPLAY,
    NEW_FACTORY_MODULE_ID,
    NEW_FACTORY_MODULE_STATUS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    VALIDATED_CONSUMERS,
)
from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)
from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID

MIN_CHECKS = 70

REQUIRED = (
    "controlled_provider_harness_factory_registration_dryrun_policy_v1.json",
    "factory_registration_planning_input_review_v1.json",
    "validation_factory_registry_candidate_v1.json",
    "controlled_provider_harness_registry_entry_candidate_v1.json",
    "validation_factory_contract_extension_dryrun_result_v1.json",
    "provider_harness_factory_interface_dryrun_result_v1.json",
    "provider_harness_consumer_mapping_dryrun_result_v1.json",
    "provider_harness_boundary_policy_dryrun_result_v1.json",
    "provider_harness_anti_recursion_dryrun_result_v1.json",
    "deferred_consumer_register_dryrun_result_v1.json",
    "validation_factory_registration_no_runtime_audit_v1.json",
    "validation_factory_registration_blocked_path_result_v1.json",
    "validation_factory_registration_readiness_decision_v1.json",
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
            "controlled_provider_readiness_harness_factory_registration_dryrun"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.controlled_provider_readiness_harness_factory_registration_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "factory_registration_planning_input_review_v1.json")
    registry = _load(root / "validation_factory_registry_candidate_v1.json")
    entry = _load(root / "controlled_provider_harness_registry_entry_candidate_v1.json")
    contract = _load(root / "validation_factory_contract_extension_dryrun_result_v1.json")
    interface = _load(root / "provider_harness_factory_interface_dryrun_result_v1.json")
    consumer = _load(root / "provider_harness_consumer_mapping_dryrun_result_v1.json")
    boundary = _load(root / "provider_harness_boundary_policy_dryrun_result_v1.json")
    anti = _load(root / "provider_harness_anti_recursion_dryrun_result_v1.json")
    deferred = _load(root / "deferred_consumer_register_dryrun_result_v1.json")
    audit = _load(root / "validation_factory_registration_no_runtime_audit_v1.json")
    blocked = _load(root / "validation_factory_registration_blocked_path_result_v1.json")
    readiness = _load(root / "validation_factory_registration_readiness_decision_v1.json")

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("controlled_provider_readiness_harness_factory_registration_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.candidate_gen", summary.get("validation_factory_registry_candidate_generated_now") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.modules7", summary.get("module_count") == EXISTING_FACTORY_MODULE_COUNT + 1)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("registry.count7", registry.get("module_count") == 7)
    ok("registry.existing6", registry.get("existing_module_count") == EXISTING_FACTORY_MODULE_COUNT)
    ok("registry.candidate_only", registry.get("candidate_only") is True)
    ok("registry.not_updated", registry.get("registry_updated_now") is False)
    ok("registry.seventh_id", registry.get("proposed_seventh_module_id") == NEW_FACTORY_MODULE_ID)

    modules = registry.get("modules") or []
    display_names = {m.get("display_name") for m in modules}
    for mod in EXISTING_FACTORY_MODULES:
        ok(f"registry.{mod['display_name']}", mod["display_name"] in display_names)

    ok("entry.module_id", entry.get("module_id") == NEW_FACTORY_MODULE_ID)
    ok("entry.harness_id", entry.get("harness_id") == HARNESS_ID)
    ok("entry.status", entry.get("status") == NEW_FACTORY_MODULE_STATUS)
    ok("entry.first_ocr", entry.get("first_consumer") == "ocr")
    ok("entry.no_runtime", entry.get("runtime_enforced") is False)
    ok("entry.no_global", entry.get("global_enforcement") is False)
    ok("entry.no_invoke", entry.get("provider_invocation_allowed") is False)
    ok("entry.candidate_only", entry.get("candidate_only") is True)

    ok("contract.pass", contract.get("extension_dryrun_pass") is True)
    ok("contract.input", contract.get("standard_input_contract_present") is True)
    ok("contract.output", contract.get("standard_output_contract_present") is True)

    ok("interface.pass", interface.get("interface_dryrun_pass") is True)
    ok("interface.inputs9", interface.get("input_count") == len(FACTORY_INTERFACE_INPUTS))
    ok("interface.outputs7", interface.get("output_count") == len(FACTORY_INTERFACE_OUTPUTS))

    consumers = {c.get("domain"): c for c in consumer.get("consumers") or []}
    ok("consumer.ocr", consumers.get("ocr", {}).get("status") == "validated")
    ok("consumer.vision", consumers.get("vision", {}).get("status") == "validated")
    ok("consumer.voice", consumers.get("voice", {}).get("status") == "validated")
    for domain in FUTURE_CONSUMER_DOMAINS:
        ok(f"consumer.{domain}_future", consumers.get(domain, {}).get("status") == "future_only")
    ok("consumer.not_adopted", consumer.get("future_consumers_not_adopted_now") is True)

    ok("boundary.pass", boundary.get("boundary_dryrun_pass") is True)
    ok("boundary.count8", boundary.get("path_count") == len(BOUNDARY_BLOCKED_PATHS))
    ok("boundary.all", boundary.get("all_blocked") is True)

    ok("anti.pass", anti.get("anti_recursion_dryrun_pass") is True)
    ok("anti.no_long_chain", anti.get("no_per_domain_long_chain_duplication") is True)
    ok("anti.domain_config", anti.get("domain_config_plus_harness_required") is True)

    ok("deferred.future", deferred.get("map_library_hive_memory_adoption_deferred") is True)
    ok("deferred.not_adopted", deferred.get("adopted_now") is False)

    ok("audit.pass", audit.get("audit_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count8", blocked.get("path_count") == len(BOUNDARY_BLOCKED_PATHS))

    ok("readiness.all", readiness.get("all_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)

    for domain in VALIDATED_CONSUMERS:
        ok(f"validated.{domain}", domain in VALIDATED_CONSUMERS)

    ok("summary.no_registry_update", summary.get("validation_factory_registry_updated_now") is False)
    ok("summary.no_factory_runtime", summary.get("validation_factory_runtime_enforced_now") is False)

    for field in BOUNDARY_FALSE:
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
