#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Management Layer Recovery Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_module_gap_and_roadmap_planning_v1 import P2_MODULES
from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import DEFERRED_ROUTE
from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    CAPABILITY_DESCRIPTORS,
    FINAL_DECISION_GO,
    HEALTH_STATES,
    MODEL_DOMAINS,
    MODEL_OUTPUT_CANDIDATE_TYPES,
    NEXT_PHASE_GO,
    PHASE_ID,
    RUNTIME_MODES,
    SCOPE,
    SWITCHING_RULES,
)
from capabilities.governance.task_response_candidate_midplatform_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as TR_REVIEW_FINAL,
    NEXT_PHASE_GO as TR_REVIEW_NEXT,
)

MIN_CHECKS = 85

REQUIRED_FILES = (
    "model_management_recovery_planning_policy_v1.json",
    "upstream_task_response_review_input_review_v1.json",
    "model_management_layer_scope_v1.json",
    "model_registry_contract_planning_v1.json",
    "skill_registry_contract_planning_v1.json",
    "model_capability_descriptor_contract_v1.json",
    "model_health_state_contract_v1.json",
    "model_switching_and_degradation_policy_v1.json",
    "model_output_contract_integration_plan_v1.json",
    "model_runtime_boundary_matrix_v1.json",
    "model_provider_governance_mapping_v1.json",
    "validation_factory_model_layer_integration_plan_v1.json",
    "model_management_recovery_dryrun_plan_v1.json",
    "model_management_non_claims_register_v1.json",
    "model_management_recovery_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_planning",
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    tr_root = Path(args.task_response_candidate_midplatform_integration_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "model_management_recovery_planning_policy_v1.json")
    input_rev = _load(root / "upstream_task_response_review_input_review_v1.json")
    scope = _load(root / "model_management_layer_scope_v1.json")
    registry = _load(root / "model_registry_contract_planning_v1.json")
    skill = _load(root / "skill_registry_contract_planning_v1.json")
    capability = _load(root / "model_capability_descriptor_contract_v1.json")
    health = _load(root / "model_health_state_contract_v1.json")
    switching = _load(root / "model_switching_and_degradation_policy_v1.json")
    output_plan = _load(root / "model_output_contract_integration_plan_v1.json")
    runtime = _load(root / "model_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "model_management_recovery_dryrun_plan_v1.json")
    decision = _load(root / "model_management_recovery_planning_decision_v1.json")

    tr_sm = _load(tr_root / "summary.json")
    tr_vr = _load(tr_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.planning_only", summary.get("model_management_layer_recovery_planning_only") is True)
    ok("summary.no_invoke", summary.get("model_runtime_invoked_now") is False)
    ok("summary.registry_not_created", summary.get("model_registry_created_now") is False)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.route_a_closed", input_rev.get("route_a_closed") is True)
    ok("input.route_b", input_rev.get("route_b_deferred_route") == DEFERRED_ROUTE)
    ok("scope.domains", len(scope.get("covers_domains") or []) >= 7)
    ok("registry.invocation_false", registry.get("invocation_allowed_default") is False)
    ok("registry.fields", "model_id" in (registry.get("required_fields") or []))
    ok("skill.safety", skill.get("safety_gate_required_default") is True)
    ok("skill.no_user_out", skill.get("user_facing_output_allowed_default") is False)
    ok("capability.no_fact", capability.get("defaults", {}).get("can_write_fact") is False)
    ok("capability.no_action", capability.get("defaults", {}).get("can_trigger_action") is False)
    ok("health.states6", len(health.get("states") or []) == len(HEALTH_STATES))
    ok("switching.rules6", len(switching.get("rules") or []) == len(SWITCHING_RULES))
    ok("output.candidate_only", output_plan.get("defaults", {}).get("candidate_only") is True)
    ok("runtime.rows", len(runtime.get("rows") or []) >= 5)
    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("ready_for_model_management_recovery_dryrun") is True)

    ok("upstream.tr_vr", tr_vr.get("verifier") == "GO")
    ok("upstream.tr_final", tr_sm.get("final_decision") == TR_REVIEW_FINAL)
    ok("upstream.tr_next", tr_sm.get("recommended_next_phase") == TR_REVIEW_NEXT)

    for domain in MODEL_DOMAINS[:6]:
        ok(f"scope.domain.{domain}", domain in (scope.get("covers_domains") or []))
    for mode in RUNTIME_MODES:
        ok(f"registry.mode.{mode}", mode in (registry.get("runtime_modes") or []))
    for ctype in MODEL_OUTPUT_CANDIDATE_TYPES:
        ok(f"output.{ctype}", ctype in (output_plan.get("candidate_output_types") or []))
    for desc in CAPABILITY_DESCRIPTORS:
        ok(f"cap.{desc}", desc in (capability.get("descriptors") or {}))
    for mod in P2_MODULES:
        ok(f"gap.p2.{mod}", mod in (input_rev.get("gap_p2_model_modules") or []))

    for i in range(15):
        ok(f"meta.planning[{i}]", summary.get("model_management_layer_recovery_planning_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
