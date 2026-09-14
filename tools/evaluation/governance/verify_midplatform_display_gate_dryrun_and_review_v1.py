#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Display Gate DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_display_gate_planning_v1 import (
    CHANNEL_ADMISSION_RULES,
    CONTENT_CONSTRAINT_RULES,
    DISPLAY_ACTION_TAXONOMY,
    DISPLAY_GATE_LAYER_POSITIONING,
    DISPLAY_GATE_RESULT_FIELDS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_RESULT_INTAKE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    LAYOUT_BOUNDARY_RULES,
    NO_RAW_CONSTITUTION_RULES,
    NOTIFICATION_BOUNDARY_RULES,
    PRIVACY_MASKING_RULES,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_DISCLOSURE_RULES,
    USER_OUTPUT_INTAKE_FIELDS,
)

MIN_CHECKS = 281

REQUIRED = (
    "display_gate_dryrun_review_policy_v1.json",
    "display_gate_planning_input_review_v1.json",
    "display_gate_model_candidate_v1.json",
    "sample_enforcement_result_intake_v1.json",
    "sample_user_output_candidate_intake_v1.json",
    "sample_display_gate_result_candidate_v1.json",
    "display_enforcement_layer_role_review_v1.json",
    "display_no_raw_constitution_binding_review_v1.json",
    "display_action_taxonomy_dryrun_review_v1.json",
    "display_channel_admission_dryrun_review_v1.json",
    "display_content_constraint_dryrun_review_v1.json",
    "display_uncertainty_disclosure_dryrun_review_v1.json",
    "display_privacy_masking_dryrun_review_v1.json",
    "display_layout_boundary_review_v1.json",
    "display_notification_boundary_review_v1.json",
    "display_refusal_hold_degrade_dryrun_review_v1.json",
    "display_downstream_handoff_review_v1.json",
    "display_execution_layer_boundary_review_v1.json",
    "display_gate_traceability_review_v1.json",
    "display_gate_boundary_audit_v1.json",
    "display_gate_blocked_path_result_v1.json",
    "display_gate_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review",
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    summary = _load(root / "summary.json")
    model = _load(root / "display_gate_model_candidate_v1.json")
    sample_enforcement = _load(root / "sample_enforcement_result_intake_v1.json")
    sample_user = _load(root / "sample_user_output_candidate_intake_v1.json")
    sample_result = _load(root / "sample_display_gate_result_candidate_v1.json")
    enforcement = _load(root / "display_enforcement_layer_role_review_v1.json")
    no_raw = _load(root / "display_no_raw_constitution_binding_review_v1.json")
    actions = _load(root / "display_action_taxonomy_dryrun_review_v1.json")
    channel = _load(root / "display_channel_admission_dryrun_review_v1.json")
    content = _load(root / "display_content_constraint_dryrun_review_v1.json")
    uncertainty = _load(root / "display_uncertainty_disclosure_dryrun_review_v1.json")
    privacy = _load(root / "display_privacy_masking_dryrun_review_v1.json")
    layout = _load(root / "display_layout_boundary_review_v1.json")
    notification = _load(root / "display_notification_boundary_review_v1.json")
    refusal = _load(root / "display_refusal_hold_degrade_dryrun_review_v1.json")
    handoff = _load(root / "display_downstream_handoff_review_v1.json")
    exec_boundary = _load(root / "display_execution_layer_boundary_review_v1.json")
    trace = _load(root / "display_gate_traceability_review_v1.json")
    blocked = _load(root / "display_gate_blocked_path_result_v1.json")
    closure = _load(root / "display_gate_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok(
        "upstream.enforcement",
        _load(plan_root / "display_gate_planning_policy_v1.json").get(
            "display_gate_is_enforcement_not_execution"
        )
        is True,
    )

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("display_gate_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.id", model.get("module_id") == "midplatform_display_gate_v1")
    ok("model.type", model.get("module_type") == "midplatform_user_output_gate_module")
    ok("model.role", model.get("role") == "display_output_enforcement_gate")
    ok("model.arch", model.get("architectural_layer") == "Enforcement")
    ok("model.layer", model.get("system_layer") == "Validation")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.consumes_enforcement", model.get("consumes_enforcement_result_candidate") is True)
    ok("model.consumes_user", model.get("consumes_user_output_candidate") is True)
    ok("model.emits_display", model.get("emits_display_gate_result_candidate") is True)
    ok("model.no_raw", model.get("reads_raw_constitution_clauses") is False)
    ok("model.no_display_out", model.get("invokes_display_output") is False)
    ok("model.no_ui", model.get("renders_ui") is False)
    ok("model.no_notification", model.get("sends_notification") is False)
    ok("model.no_push", model.get("triggers_app_push") is False)
    ok("model.no_bypass", model.get("bypasses_safety_gate") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)

    upstream_mods = model.get("upstream_modules") or []
    ok("model.up_safety", "safety_gate" in upstream_mods)
    ok("model.up_output", "output_plane_integration" in upstream_mods)
    ok("model.up_resolver", "constitution_resolver" in upstream_mods)

    downstream_mods = model.get("downstream_modules") or []
    ok("model.down_display", "display_output_later" in downstream_mods)
    ok("model.down_notification", "notification_gate_later" in downstream_mods)

    for field in ENFORCEMENT_RESULT_INTAKE_FIELDS:
        ok(f"enforcement.{field[:15]}", field in sample_enforcement)
    ok("enforcement.candidate", sample_enforcement.get("candidate_only") is True)

    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in sample_user)
    ok("user.no_facing", sample_user.get("user_facing_output_allowed") is False)
    ok("user.no_display", sample_user.get("display_output_allowed") is False)
    ok("user.not_fact", sample_user.get("fact_status") == "not_fact")

    for field in DISPLAY_GATE_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in sample_result)
    ok("result.no_display_out", sample_result.get("display_output_allowed") is False)
    ok("result.candidate", sample_result.get("candidate_only") is True)

    ok("enforcement_review.pass", enforcement.get("dryrun_and_review_pass") is True)
    for pos in DISPLAY_GATE_LAYER_POSITIONING:
        ok(f"enf_pos.{pos[:18]}", pos in (enforcement.get("display_gate_layer_positioning") or []))

    ok("no_raw.pass", no_raw.get("dryrun_and_review_pass") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("actions.pass", actions.get("dryrun_and_review_pass") is True)
    ok("actions.count13", actions.get("action_count") == 13)
    ok("actions.all13", actions.get("all_thirteen_actions_covered") is True)
    for action in DISPLAY_ACTION_TAXONOMY:
        ok(
            f"action.{action[:18]}",
            action in [a.get("display_gate_action") for a in (actions.get("actions") or [])],
        )

    ok("channel.pass", channel.get("dryrun_and_review_pass") is True)
    for rule in CHANNEL_ADMISSION_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))

    ok("content.pass", content.get("dryrun_and_review_pass") is True)
    for rule in CONTENT_CONSTRAINT_RULES:
        ok(f"content.{rule[:18]}", rule in (content.get("rules") or []))

    ok("uncertainty.pass", uncertainty.get("dryrun_and_review_pass") is True)
    for rule in UNCERTAINTY_DISCLOSURE_RULES:
        ok(f"uncertainty.{rule[:18]}", rule in (uncertainty.get("rules") or []))

    ok("privacy.pass", privacy.get("dryrun_and_review_pass") is True)
    for rule in PRIVACY_MASKING_RULES:
        ok(f"privacy.{rule[:18]}", rule in (privacy.get("rules") or []))

    ok("layout.pass", layout.get("dryrun_and_review_pass") is True)
    for rule in LAYOUT_BOUNDARY_RULES:
        ok(f"layout.{rule[:18]}", rule in (layout.get("rules") or []))

    ok("notification.pass", notification.get("dryrun_and_review_pass") is True)
    for rule in NOTIFICATION_BOUNDARY_RULES:
        ok(f"notification.{rule[:18]}", rule in (notification.get("rules") or []))

    ok("refusal.pass", refusal.get("dryrun_and_review_pass") is True)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_signal'][:16]}",
            any(
                x.get("safety_signal") == m["safety_signal"] and x.get("display_path") == m["display_path"]
                for x in (refusal.get("mappings") or [])
            ),
        )

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['display_action'][:16]}",
            any(
                x.get("display_action") == m["display_action"] and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("exec.pass", exec_boundary.get("dryrun_and_review_pass") is True)
    ok("exec.not_ui", exec_boundary.get("display_pass_not_display_output_or_ui") is True)
    for rule in EXECUTION_LAYER_BOUNDARY_RULES:
        ok(f"exec.{rule[:18]}", rule in (exec_boundary.get("rules") or []))

    ok("trace.pass", trace.get("dryrun_and_review_pass") is True)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("audit.pass", _load(root / "display_gate_boundary_audit_v1.json").get("dryrun_and_review_pass") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count17", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(x.get("blocked_path") == bp and x.get("blocked") is True for x in (blocked.get("blocked_paths") or [])),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.enforcement", closure.get("display_enforcement_layer_validated") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_health_enforcement_supervisor_planning") is True)
    ok("next.no_runtime", next_route.get("display_gate_runtime_enabled") is False)

    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed == total and pass_all and total > 0

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "HOLD",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
        "non_claims": list(NON_CLAIMS),
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
