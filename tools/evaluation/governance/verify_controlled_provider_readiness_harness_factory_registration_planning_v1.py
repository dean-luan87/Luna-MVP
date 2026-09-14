#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Provider Readiness Harness Validation Factory Registration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
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
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_ANTI_RECURSION,
    SCOPE,
    VALIDATED_CONSUMERS,
)
from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID
from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
    SELECTED_ROUTE,
)

MIN_CHECKS = 70

REQUIRED = (
    "controlled_provider_harness_factory_registration_planning_policy_v1.json",
    "provider_harness_generalization_roadmap_input_review_v1.json",
    "validation_factory_existing_registry_review_v1.json",
    "controlled_provider_harness_registry_entry_plan_v1.json",
    "validation_factory_contract_extension_plan_v1.json",
    "provider_harness_factory_interface_plan_v1.json",
    "provider_harness_consumer_mapping_plan_v1.json",
    "provider_harness_boundary_policy_plan_v1.json",
    "provider_harness_anti_recursion_rule_plan_v1.json",
    "validation_factory_registration_dryrun_plan_v1.json",
    "deferred_consumer_register_v1.json",
    "factory_registration_planning_decision_v1.json",
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
            "controlled_provider_readiness_harness_factory_registration_planning"
        ),
    )
    p.add_argument(
        "--provider-harness-generalization-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_harness_generalization_roadmap_decision"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    p.add_argument(
        "--luna-validation-factory-consolidation-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.provider_harness_generalization_roadmap_decision_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    factory_root = Path(args.luna_validation_factory_consolidation_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "provider_harness_generalization_roadmap_input_review_v1.json")
    registry_review = _load(root / "validation_factory_existing_registry_review_v1.json")
    entry_plan = _load(root / "controlled_provider_harness_registry_entry_plan_v1.json")
    contract_plan = _load(root / "validation_factory_contract_extension_plan_v1.json")
    interface_plan = _load(root / "provider_harness_factory_interface_plan_v1.json")
    consumer_plan = _load(root / "provider_harness_consumer_mapping_plan_v1.json")
    boundary_plan = _load(root / "provider_harness_boundary_policy_plan_v1.json")
    anti_plan = _load(root / "provider_harness_anti_recursion_rule_plan_v1.json")
    dryrun_plan = _load(root / "validation_factory_registration_dryrun_plan_v1.json")
    deferred = _load(root / "deferred_consumer_register_v1.json")
    decision = _load(root / "factory_registration_planning_decision_v1.json")

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    harness_vr = _load(harness_root / "verifier_report.json")
    factory_vr = _load(factory_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("controlled_provider_readiness_harness_factory_registration_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.modules6", summary.get("existing_factory_module_count") == EXISTING_FACTORY_MODULE_COUNT)
    ok("summary.seventh", summary.get("proposed_seventh_module") == NEW_FACTORY_MODULE_DISPLAY)
    ok("summary.three_consumer", summary.get("three_consumer_validated") is True)

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == ROADMAP_NEXT)
    ok("upstream.route_b", roadmap_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")
    ok("upstream.factory_go", factory_vr.get("verifier") == "GO")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.route_b", input_review.get("selected_route") == SELECTED_ROUTE)

    ok("registry.pass", registry_review.get("review_pass") is True)
    ok("registry.count6", registry_review.get("existing_module_count") == EXISTING_FACTORY_MODULE_COUNT)
    ok("registry.not_registered", registry_review.get("provider_harness_not_yet_registered") is True)

    proposed = entry_plan.get("proposed_module") or {}
    ok("entry.module_id", proposed.get("module_id") == NEW_FACTORY_MODULE_ID)
    ok("entry.harness_id", proposed.get("harness_id") == HARNESS_ID)
    ok("entry.first_ocr", proposed.get("first_consumer") == "ocr")
    ok("entry.no_runtime", proposed.get("runtime_enforced") is False)
    ok("entry.no_global", proposed.get("global_enforcement") is False)
    ok("entry.domain_config", proposed.get("domain_config_required") is True)
    ok("entry.no_invoke", proposed.get("provider_invocation_allowed") is False)
    ok("entry.no_install", proposed.get("dependency_install_allowed") is False)
    ok("entry.no_download", proposed.get("model_download_allowed") is False)
    ok("entry.evidence", proposed.get("evidence_package_required") is True)
    ok("entry.boundary", proposed.get("boundary_guard_required") is True)
    ok("entry.not_updated", entry_plan.get("registry_updated_now") is False)

    ok("contract.count6", contract_plan.get("existing_module_count") == EXISTING_FACTORY_MODULE_COUNT)
    ok("contract.seventh", contract_plan.get("proposed_seventh_module") == NEW_FACTORY_MODULE_DISPLAY)
    ok("contract.not_updated", contract_plan.get("contract_updated_now") is False)

    ok("interface.inputs9", len(interface_plan.get("standard_inputs") or []) == len(FACTORY_INTERFACE_INPUTS))
    ok("interface.outputs7", len(interface_plan.get("standard_outputs") or []) == len(FACTORY_INTERFACE_OUTPUTS))

    consumers = {c.get("domain"): c for c in consumer_plan.get("consumers") or []}
    ok("consumer.ocr", consumers.get("ocr", {}).get("status") == "validated")
    ok("consumer.vision", consumers.get("vision", {}).get("status") == "validated")
    ok("consumer.voice", consumers.get("voice", {}).get("status") == "validated")
    for domain in FUTURE_CONSUMER_DOMAINS:
        ok(f"consumer.{domain}_future", consumers.get(domain, {}).get("status") == "future_only")

    ok("boundary.count8", boundary_plan.get("path_count") == len(BOUNDARY_BLOCKED_PATHS))
    ok("boundary.all_blocked", boundary_plan.get("all_blocked_by_default") is True)

    ok("anti.count", anti_plan.get("rule_count") >= len(PLANNING_ANTI_RECURSION))
    ok("anti.no_long_chain", anti_plan.get("no_per_domain_long_chain_duplication") is True)
    ok("anti.domain_config", anti_plan.get("domain_config_plus_harness_required") is True)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)

    ok("deferred.future", deferred.get("map_library_hive_memory_adoption_deferred") is True)

    ok("decision.ready", decision.get("ready_for_dryrun") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for mod in EXISTING_FACTORY_MODULES:
        ok(f"existing.{mod['module_id']}", mod["display_name"] in [m["display_name"] for m in EXISTING_FACTORY_MODULES])

    for domain in VALIDATED_CONSUMERS:
        ok(f"validated.{domain}", domain in VALIDATED_CONSUMERS)

    ok("summary.no_registry_update", summary.get("validation_factory_registry_updated_now") is False)
    ok("summary.no_factory_runtime", summary.get("validation_factory_runtime_enforced_now") is False)
    ok("summary.no_harness_runtime", summary.get("controlled_provider_harness_runtime_enforced_now") is False)
    ok("summary.no_map_adopt", summary.get("map_library_hive_memory_adoption_started_now") is False)

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
