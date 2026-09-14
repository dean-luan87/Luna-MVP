#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Micro-OS Core Component Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.midplatform.midplatform_micro_os_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import HEALTH_METRICS
from capabilities.midplatform.midplatform_micro_os_core_component_planning_v1 import (
    BOUNDARY_FALSE,
    COMPONENT_EDGES,
    CORE_COMPONENT_IDS,
    FINAL_DECISION_GO,
    HEALTH_METRIC_COMPONENT_MAP,
    INFORMATION_TYPES,
    MANAGEMENT_LOGIC,
    MODEL_RULE_ALGORITHM_MAP,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 397

REQUIRED = (
    "summary.json",
    "midplatform_core_component_scope_v1.json",
    "midplatform_core_component_contract_collection_v1.json",
    "midplatform_core_component_upstream_downstream_matrix_v1.json",
    "midplatform_core_component_information_contract_v1.json",
    "midplatform_core_component_management_logic_v1.json",
    "midplatform_core_component_model_rule_algorithm_map_v1.json",
    "midplatform_core_component_failure_route_matrix_v1.json",
    "midplatform_core_component_health_metric_mapping_v1.json",
    "midplatform_core_component_boundary_matrix_v1.json",
    "midplatform_core_component_planning_readiness_decision_v1.json",
    "midplatform_core_component_non_claims_register_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"),
    )
    p.add_argument(
        "--planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"),
    )
    p.add_argument(
        "--dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    dr_vr = _load(Path(args.dryrun_root) / "verifier_report.json")
    dr_sm = _load(Path(args.dryrun_root) / "summary.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.dryrun_go", dr_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dr_sm.get("final_decision") == DRYRUN_FINAL)

    summary = _load(root / "summary.json")
    scope = _load(root / "midplatform_core_component_scope_v1.json")
    contracts = _load(root / "midplatform_core_component_contract_collection_v1.json")
    updown = _load(root / "midplatform_core_component_upstream_downstream_matrix_v1.json")
    info_contract = _load(root / "midplatform_core_component_information_contract_v1.json")
    mgmt = _load(root / "midplatform_core_component_management_logic_v1.json")
    mra = _load(root / "midplatform_core_component_model_rule_algorithm_map_v1.json")
    failure = _load(root / "midplatform_core_component_failure_route_matrix_v1.json")
    health_map = _load(root / "midplatform_core_component_health_metric_mapping_v1.json")
    boundary = _load(root / "midplatform_core_component_boundary_matrix_v1.json")
    readiness = _load(root / "midplatform_core_component_planning_readiness_decision_v1.json")
    nc = _load(root / "midplatform_core_component_non_claims_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_micro_os_core_component_planning_only")
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("scope.components12", scope.get("component_count") == 12)
    ok("contracts.count12", contracts.get("contract_count") == 12)
    ok("contracts.ten_sections", contracts.get("all_ten_sections") is True)
    ok("reuse.rule", scope.get("phase_governance_standard_reuse_rule") is True)
    ok("reuse.no_new_gov", scope.get("new_governance_need_proven") is False)

    for cid in CORE_COMPONENT_IDS:
        ok(f"component.{cid[:14]}.listed", cid in (scope.get("component_ids") or []))

    contract_list = contracts.get("contracts") or []
    for cid in CORE_COMPONENT_IDS:
        cdoc = next((c for c in contract_list if c.get("module_identity", {}).get("module_id") == cid), {})
        ok(f"contract.{cid[:12]}.exists", bool(cdoc))
        for section in TEMPLATE_SECTIONS:
            ok(f"contract.{cid[:8]}.{section[:8]}", section in cdoc)

    ok("wm.not_memory", any(
        "Working Memory ≠ Memory" in str(c.get("module_principles", {}).get("module_principles", []))
        for c in contract_list if c.get("module_identity", {}).get("module_id") == "working_memory"
    ))
    ok("wm.not_worldmodel", any(
        "Working Memory ≠ WorldModel" in str(c.get("module_principles", {}).get("module_principles", []))
        for c in contract_list if c.get("module_identity", {}).get("module_id") == "working_memory"
    ))

    ok("govgate.hard_boundary", updown.get("governance_gate_hard_boundary") is True)
    ok("watchdog.monitors", updown.get("watchdog_monitors_all") is True)
    ok("edges.count", updown.get("edge_count") == len(COMPONENT_EDGES))
    ok("edge.adapter_bus", any(e.get("from") == "module_adapter_layer" and e.get("to") == "event_bus" for e in updown.get("edges", [])))
    ok("edge.bus_wm", any(e.get("from") == "event_bus" and e.get("to") == "working_memory" for e in updown.get("edges", [])))

    for itype in INFORMATION_TYPES:
        ok(f"info.{itype[:14]}", itype in (info_contract.get("information_types") or []))

    for key, owner in MANAGEMENT_LOGIC.items():
        ok(f"mgmt.{key[:12]}", owner in str(mgmt.get("assignments", {})))

    ok("mra.no_gov_model", mra.get("no_model_in_governance_gate") is True)
    ok("mra.no_watchdog_model", mra.get("no_model_in_watchdog") is True)
    for cid in CORE_COMPONENT_IDS:
        ok(f"mra.{cid[:12]}", cid in (mra.get("components") or {}))

    for cid in CORE_COMPONENT_IDS:
        routes = (failure.get("components") or {}).get(cid) or []
        ok(f"failure.{cid[:10]}.min3", len(routes) >= 3)
        for route in routes[:3]:
            ok(f"failure.{cid[:8]}.detect", bool(route.get("detection_signal")))
            ok(f"failure.{cid[:8]}.recover", bool(route.get("recovery_candidate")))

    ok("health.all_mapped", health_map.get("all_metrics_mapped") is True)
    for metric in HEALTH_METRICS:
        ok(f"healthmap.{metric[:12]}", metric in (health_map.get("metric_to_component") or {}))

    for field in BOUNDARY_FALSE:
        ok(f"boundary.global.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)
        ok(f"summary.boundary.{field[:10]}", summary.get(field) is False)

    gov_contract = next((c for c in contract_list if c.get("module_identity", {}).get("module_id") == "governance_gate_manager"), {})
    ok("govgate.no_model", gov_contract.get("processing_scope", {}).get("provider_invocation_allowed") is False)
    wd_contract = next((c for c in contract_list if c.get("module_identity", {}).get("module_id") == "watchdog_recovery_manager"), {})
    ok("watchdog.no_real_recovery", "real recovery" in str(wd_contract.get("forbidden_actions", [])).lower() or "execute real recovery" in str(wd_contract.get("forbidden_actions", [])))

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))

    for cid in CORE_COMPONENT_IDS:
        rb = (boundary.get("components") or {}).get(cid, {})
        ok(f"compbound.{cid[:10]}.runtime", rb.get("runtime_enabled_now") is False)

    for metric, comp in HEALTH_METRIC_COMPONENT_MAP.items():
        ok(f"map.{metric[:10]}", health_map.get("metric_to_component", {}).get(metric) == comp)

    for cid, placement in MODEL_RULE_ALGORITHM_MAP.items():
        ok(f"place.{cid[:10]}.primary", bool(placement.get("primary")))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else (root / "verify_midplatform_micro_os_core_component_planning_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "verifier_report.json").write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
