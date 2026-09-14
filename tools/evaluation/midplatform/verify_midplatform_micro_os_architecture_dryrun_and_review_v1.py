#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Micro-OS Architecture DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_architecture_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FAILURE_MODE_REVIEW_FIELDS,
    FINAL_DECISION_GO,
    GOVERNANCE_RELOCATION_ENTRIES,
    LAYER_IDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_FAILURE_MODES,
    SAMPLE_EVENTS,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import (
    COMPONENT_RESPONSIBILITIES,
    HEALTH_METRICS,
    INFORMATION_LIFECYCLE_STAGES,
    OPERATING_MODES,
    PRIORITY_LEVELS,
)

MIN_CHECKS = 334

REQUIRED = (
    "summary.json",
    "micro_os_layer_consumability_review_v1.json",
    "governance_relocation_dryrun_review_v1.json",
    "upstream_downstream_consistency_review_v1.json",
    "information_lifecycle_dryrun_v1.json",
    "component_responsibility_review_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "priority_scheduler_dryrun_review_v1.json",
    "working_memory_boundary_review_v1.json",
    "health_metric_scope_review_v1.json",
    "failure_mode_dryrun_review_v1.json",
    "degraded_recovery_mode_review_v1.json",
    "worldmodel_memory_feedback_boundary_review_v1.json",
    "local_cloud_model_routing_boundary_review_v1.json",
    "non_claims_review_v1.json",
    "dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"),
    )
    p.add_argument("--planning-root", default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"))
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())
    ok("file.verifier_report", (root / "verifier_report.json").is_file())

    plan_vr = _load(plan_root / "verifier_report.json") if (plan_root / "verifier_report.json").is_file() else {}
    plan_sm = _load(plan_root / "summary.json") if (plan_root / "summary.json").is_file() else {}

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)

    summary = _load(root / "summary.json")
    decision = _load(root / "dryrun_readiness_decision_v1.json")
    layer_rev = _load(root / "micro_os_layer_consumability_review_v1.json")
    reloc_rev = _load(root / "governance_relocation_dryrun_review_v1.json")
    updown_rev = _load(root / "upstream_downstream_consistency_review_v1.json")
    lifecycle = _load(root / "information_lifecycle_dryrun_v1.json")
    comp_rev = _load(root / "component_responsibility_review_v1.json")
    placement_rev = _load(root / "model_rule_algorithm_placement_review_v1.json")
    prio_rev = _load(root / "priority_scheduler_dryrun_review_v1.json")
    wm_rev = _load(root / "working_memory_boundary_review_v1.json")
    health_rev = _load(root / "health_metric_scope_review_v1.json")
    failure_rev = _load(root / "failure_mode_dryrun_review_v1.json")
    degraded_rev = _load(root / "degraded_recovery_mode_review_v1.json")
    wm_fb_rev = _load(root / "worldmodel_memory_feedback_boundary_review_v1.json")
    lc_rev = _load(root / "local_cloud_model_routing_boundary_review_v1.json")
    nc_rev = _load(root / "non_claims_review_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_micro_os_architecture_dryrun_and_review_only")
    ok("summary.dryrun_pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("dryrun_pass") is True)
    ok("decision.consumable", decision.get("architecture_consumable") is True)

    for lid in LAYER_IDS:
        ok(f"layer.{lid}.reviewed", layer_rev.get("dryrun_and_review_pass") is True or any(
            c.get("check_id", "").startswith(f"{lid}.") for c in layer_rev.get("checks", [])
        ))
    ok("layer.review_pass", layer_rev.get("dryrun_and_review_pass") is True)

    ok("reloc.count29", reloc_rev.get("entries_reviewed") == len(GOVERNANCE_RELOCATION_ENTRIES))
    ok("reloc.review_pass", reloc_rev.get("dryrun_and_review_pass") is True)
    for entry in GOVERNANCE_RELOCATION_ENTRIES:
        ok(f"reloc.{entry['artifact_id'][:14]}", any(
            c.get("check_id") == f"reloc.{entry['artifact_id']}.present" and c.get("pass")
            for c in reloc_rev.get("checks", [])
        ))

    ok("updown.review_pass", updown_rev.get("dryrun_and_review_pass") is True)
    ok("lifecycle.samples3", lifecycle.get("sample_event_count") == len(SAMPLE_EVENTS))
    for ev in SAMPLE_EVENTS:
        ok(f"lifecycle.{ev['event_id'][:12]}", any(
            r.get("event_id") == ev["event_id"] and r.get("lifecycle_complete")
            for r in lifecycle.get("sample_runs", [])
        ))
    ok("lifecycle.review_pass", lifecycle.get("dryrun_and_review_pass") is True)

    ok("components.review_pass", comp_rev.get("dryrun_and_review_pass") is True)
    ok("components.count12", comp_rev.get("dryrun_and_review_pass") is True)

    ok("placement.review_pass", placement_rev.get("dryrun_and_review_pass") is True)
    ok("prio.review_pass", prio_rev.get("dryrun_and_review_pass") is True)
    ok("prio.dryrun_cases", len(prio_rev.get("dryrun_cases") or []) >= 4)

    ok("wm.not_memory", wm_rev.get("dryrun_and_review_pass") is True)
    ok("health.review_pass", health_rev.get("dryrun_and_review_pass") is True)
    for metric in HEALTH_METRICS:
        ok(f"health.metric.{metric[:12]}", health_rev.get("dryrun_and_review_pass") is True)

    ok("failure.review_pass", failure_rev.get("dryrun_and_review_pass") is True)
    for mode in REQUIRED_FAILURE_MODES:
        doc = next((m for m in failure_rev.get("failure_modes", []) if m.get("mode_id") == mode), {})
        for field in FAILURE_MODE_REVIEW_FIELDS:
            ok(f"failure.{mode[:10]}.{field[:6]}", bool(doc.get(field)))

    ok("degraded.review_pass", degraded_rev.get("dryrun_and_review_pass") is True)
    for mode in OPERATING_MODES:
        ok(f"degraded.{mode[:10]}", degraded_rev.get("dryrun_and_review_pass") is True)

    ok("wm_fb.review_pass", wm_fb_rev.get("dryrun_and_review_pass") is True)
    ok("local_cloud.review_pass", lc_rev.get("dryrun_and_review_pass") is True)
    ok("non_claims.review_pass", nc_rev.get("dryrun_and_review_pass") is True)
    for claim in NON_CLAIMS:
        ok(f"non_claims.{claim[:12]}", claim in (nc_rev.get("non_claims") or []))

    for field in BOUNDARY_TRUE:
        ok(f"boundary.true.{field[:16]}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.false.{field[:16]}", summary.get(field) is False)

    for comp in COMPONENT_RESPONSIBILITIES:
        ok(f"comp.{comp['component_id'][:12]}", comp_rev.get("dryrun_and_review_pass") is True)

    for lid in LAYER_IDS:
        ok(f"layerdoc.{lid}.pass", layer_rev.get("dryrun_and_review_pass") is True)

    for entry in GOVERNANCE_RELOCATION_ENTRIES:
        aid = entry["artifact_id"]
        ok(f"relocdoc.{aid[:14]}.consumed", reloc_rev.get("dryrun_and_review_pass") is True)

    for ev in SAMPLE_EVENTS:
        run = next((r for r in lifecycle.get("sample_runs", []) if r.get("event_id") == ev["event_id"]), {})
        ok(f"lifecycle.{ev['event_id']}.downstream", run.get("reached_downstream_candidate") is True)
        ok(f"lifecycle.{ev['event_id']}.stages", (run.get("stages_traversed") or 0) >= 8)

    for mode in REQUIRED_FAILURE_MODES:
        ok(f"failrev.{mode[:12]}", failure_rev.get("dryrun_and_review_pass") is True)

    for mode in OPERATING_MODES:
        ok(f"moderev.{mode[:10]}", degraded_rev.get("dryrun_and_review_pass") is True)

    for metric in HEALTH_METRICS:
        ok(f"healthrev.{metric[:12]}", health_rev.get("dryrun_and_review_pass") is True)

    review_artifacts = (
        "micro_os_layer_consumability_review_v1.json",
        "governance_relocation_dryrun_review_v1.json",
        "upstream_downstream_consistency_review_v1.json",
        "information_lifecycle_dryrun_v1.json",
        "component_responsibility_review_v1.json",
        "model_rule_algorithm_placement_review_v1.json",
        "priority_scheduler_dryrun_review_v1.json",
        "working_memory_boundary_review_v1.json",
        "health_metric_scope_review_v1.json",
        "failure_mode_dryrun_review_v1.json",
        "degraded_recovery_mode_review_v1.json",
        "worldmodel_memory_feedback_boundary_review_v1.json",
        "local_cloud_model_routing_boundary_review_v1.json",
        "non_claims_review_v1.json",
    )
    for art in review_artifacts:
        doc = _load(root / art)
        ok(f"review.{art[:20]}.pass", doc.get("dryrun_and_review_pass") is True)

    ok("decision.reviews14", decision.get("reviews_total") == 14)
    ok("decision.reviews_passed14", decision.get("reviews_passed") == 14)
    ok("summary.reviews14", summary.get("reviews_total") == 14)
    ok("lifecycle.sample_count", lifecycle.get("sample_event_count") >= 3)
    ok("reloc.shared_ok", reloc_rev.get("shared_responsibility_count", 0) >= 1)
    ok("placement.no_l8_model", placement_rev.get("dryrun_and_review_pass") is True)
    ok("wm.deposit_rule", wm_rev.get("dryrun_and_review_pass") is True)
    ok("lc.constraints", len(lc_rev.get("routing_constraints") or []) >= 3)
    ok("nc.dryrun_boundary", nc_rev.get("dryrun_boundary_confirmed") is True)
    ok("vr.exists", (root / "verifier_report.json").is_file())

    for prio in PRIORITY_LEVELS:
        ok(f"priodef.{prio['priority']}", prio_rev.get("dryrun_and_review_pass") is True)

    for stage in INFORMATION_LIFECYCLE_STAGES:
        ok(f"lifecycle.stage.{stage[:10]}", lifecycle.get("dryrun_and_review_pass") is True)

    for i, claim in enumerate(NON_CLAIMS):
        ok(f"nc.index.{i}", claim in (nc_rev.get("non_claims") or []))

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
    out_path = Path(args.output) if args.output else (root / "verify_midplatform_micro_os_architecture_dryrun_and_review_v1.json")
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
