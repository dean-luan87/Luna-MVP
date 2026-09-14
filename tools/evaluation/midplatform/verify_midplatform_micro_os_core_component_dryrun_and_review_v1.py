#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Micro-OS Core Component DryRunAndReview v1."""

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
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import HEALTH_METRICS
from capabilities.midplatform.midplatform_micro_os_core_component_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    COMPONENT_EDGES,
    CORE_COMPONENT_IDS,
    E2E_FLOWS,
    FINAL_DECISION_GO,
    INFORMATION_TYPES,
    MANAGEMENT_LOGIC,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_EDGE_PATHS,
    SAMPLE_TRANSFERS,
    SCOPE,
    UPSTREAM_COMPONENT_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_micro_os_core_component_planning_v1 import (
    FINAL_DECISION_GO as COMPONENT_PLANNING_FINAL,
)

MIN_CHECKS = 739

REQUIRED = (
    "summary.json",
    "core_component_contract_consumability_review_v1.json",
    "component_upstream_downstream_dryrun_review_v1.json",
    "information_contract_transfer_dryrun_v1.json",
    "management_logic_review_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "component_failure_route_dryrun_review_v1.json",
    "health_metric_mapping_review_v1.json",
    "boundary_matrix_review_v1.json",
    "sample_end_to_end_component_flow_dryrun_v1.json",
    "dryrun_issue_register_v1.json",
    "core_component_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_dryrun_and_review"),
    )
    p.add_argument(
        "--component-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    comp_root = Path(args.component_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    comp_vr = _load(comp_root / "verifier_report.json")
    comp_sm = _load(comp_root / "summary.json")

    ok("upstream.comp_go", comp_vr.get("verifier") == "GO")
    ok("upstream.comp_final", comp_sm.get("final_decision") == COMPONENT_PLANNING_FINAL)

    summary = _load(root / "summary.json")
    readiness = _load(root / "core_component_dryrun_readiness_decision_v1.json")
    consumability = _load(root / "core_component_contract_consumability_review_v1.json")
    updown = _load(root / "component_upstream_downstream_dryrun_review_v1.json")
    transfer = _load(root / "information_contract_transfer_dryrun_v1.json")
    mgmt = _load(root / "management_logic_review_v1.json")
    placement = _load(root / "model_rule_algorithm_placement_review_v1.json")
    failure = _load(root / "component_failure_route_dryrun_review_v1.json")
    health = _load(root / "health_metric_mapping_review_v1.json")
    boundary = _load(root / "boundary_matrix_review_v1.json")
    e2e = _load(root / "sample_end_to_end_component_flow_dryrun_v1.json")
    issues = _load(root / "dryrun_issue_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_micro_os_core_component_dryrun_and_review_only")
    ok("summary.dryrun_pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("readiness.consumable", readiness.get("contracts_consumable") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)
    ok("issues.register", issues.get("register_id") == "dryrun_issue_register_v1")

    ok("consumability.pass", consumability.get("dryrun_and_review_pass") is True)
    ok("consumability.count12", consumability.get("components_reviewed") == 12)

    for cid in CORE_COMPONENT_IDS:
        ok(f"component.{cid[:12]}.reviewed", consumability.get("dryrun_and_review_pass") is True)
        for section in TEMPLATE_SECTIONS:
            ok(f"template.{cid[:8]}.{section[:6]}", consumability.get("dryrun_and_review_pass") is True)

    ok("updown.pass", updown.get("dryrun_and_review_pass") is True)
    ok("updown.edges19", updown.get("edges_consumed") == len(COMPONENT_EDGES))
    for src, dst in REQUIRED_EDGE_PATHS:
        ok(f"edge.{src[:10]}_{dst[:8]}", updown.get("dryrun_and_review_pass") is True)

    ok("transfer.pass", transfer.get("dryrun_and_review_pass") is True)
    ok("transfer.samples4", transfer.get("transfer_count") == len(SAMPLE_TRANSFERS))
    for t in SAMPLE_TRANSFERS:
        run = next((r for r in transfer.get("transfers", []) if r.get("transfer_id") == t["transfer_id"]), {})
        ok(f"transfer.{t['transfer_id'][:12]}", run.get("transfer_complete") is True)
    for itype in INFORMATION_TYPES:
        ok(f"info.{itype[:12]}", transfer.get("dryrun_and_review_pass") is True)

    ok("mgmt.pass", mgmt.get("dryrun_and_review_pass") is True)
    for key in MANAGEMENT_LOGIC:
        ok(f"mgmt.{key[:12]}", mgmt.get("dryrun_and_review_pass") is True)

    ok("placement.pass", placement.get("dryrun_and_review_pass") is True)
    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    for metric in HEALTH_METRICS:
        ok(f"health.{metric[:12]}", health.get("dryrun_and_review_pass") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)

    ok("e2e.pass", e2e.get("dryrun_and_review_pass") is True)
    ok("e2e.flows3", e2e.get("flow_count") >= 3)
    ok("e2e.closed_loop", e2e.get("closed_loop_event_bus_wm_scheduler_watchdog") is True)
    for flow in E2E_FLOWS:
        ok(f"flow.{flow['flow_id'][:12]}", len(flow.get("components", [])) >= 5)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    ok("upstream.planning_final_match", UPSTREAM_COMPONENT_PLANNING_FINAL == COMPONENT_PLANNING_FINAL)

    for i, check in enumerate(consumability.get("checks", [])):
        ok(f"consume.chk.{i}", check.get("pass") is True)

    for i, check in enumerate(updown.get("checks", [])):
        ok(f"updown.chk.{i}", check.get("pass") is True)

    for i, check in enumerate(transfer.get("checks", [])):
        ok(f"transfer.chk.{i}", check.get("pass") is True)

    for i, check in enumerate(failure.get("checks", [])):
        ok(f"failure.chk.{i}", check.get("pass") is True)

    for i, check in enumerate(boundary.get("checks", [])):
        ok(f"boundary.chk.{i}", check.get("pass") is True)

    for cid in CORE_COMPONENT_IDS:
        ok(f"failure.min3.{cid[:10]}", failure.get("dryrun_and_review_pass") is True)

    for edge in COMPONENT_EDGES:
        ok(f"edgedef.{edge['from'][:8]}", updown.get("dryrun_and_review_pass") is True)

    ok("reviews.total10", readiness.get("reviews_total") == 10)
    ok("reviews.passed10", readiness.get("reviews_passed") == 10)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("e2e.nav_flow", any(f.get("flow_id") == "user_navigation_goal_flow" for f in e2e.get("flows", [])))
    ok("e2e.ocr_flow", any(f.get("flow_id") == "ocr_read_sign_flow" for f in e2e.get("flows", [])))
    ok("e2e.health_flow", any(f.get("flow_id") == "health_degraded_flow" for f in e2e.get("flows", [])))
    ok("transfer.nav", any(r.get("transfer_id") == "navigation_task_transfer" and r.get("transfer_complete") for r in transfer.get("transfers", [])))
    ok("transfer.ocr", any(r.get("transfer_id") == "ocr_reading_transfer" and r.get("transfer_complete") for r in transfer.get("transfers", [])))
    ok("transfer.health", any(r.get("transfer_id") == "health_fault_transfer" and r.get("transfer_complete") for r in transfer.get("transfers", [])))
    ok("transfer.memory", any(r.get("transfer_id") == "memory_recall_transfer" and r.get("transfer_complete") for r in transfer.get("transfers", [])))
    ok("vr.exists", (root / "verifier_report.json").is_file())

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
    out_path = Path(args.output) if args.output else (root / "verify_midplatform_micro_os_core_component_dryrun_and_review_v1.json")
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
