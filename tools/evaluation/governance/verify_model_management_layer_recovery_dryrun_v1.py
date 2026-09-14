#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Management Layer Recovery DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO,
    MOCK_MODEL_SPECS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    SKILL_SPECS,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    HEALTH_STATES,
    MODEL_OUTPUT_CANDIDATE_TYPES,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 88

FILES = (
    "model_management_dryrun_policy_v1.json",
    "model_management_planning_input_review_v1.json",
    "mock_fixture_model_registry_v1.json",
    "skill_registry_dryrun_v1.json",
    "model_capability_descriptor_matrix_v1.json",
    "model_health_state_candidate_matrix_v1.json",
    "model_switching_candidate_matrix_v1.json",
    "model_output_contract_integration_result_v1.json",
    "model_runtime_boundary_audit_v1.json",
    "model_provider_governance_dryrun_result_v1.json",
    "model_management_blocked_path_result_v1.json",
    "model_management_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun",
    )
    p.add_argument(
        "--model-management-layer-recovery-planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.model_management_layer_recovery_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    models = json.loads((root / "mock_fixture_model_registry_v1.json").read_text(encoding="utf-8"))
    skills = json.loads((root / "skill_registry_dryrun_v1.json").read_text(encoding="utf-8"))
    health = json.loads((root / "model_health_state_candidate_matrix_v1.json").read_text(encoding="utf-8"))
    switching = json.loads((root / "model_switching_candidate_matrix_v1.json").read_text(encoding="utf-8"))
    output_res = json.loads((root / "model_output_contract_integration_result_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "model_runtime_boundary_audit_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "model_management_dryrun_readiness_decision_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads((root / "model_management_planning_input_review_v1.json").read_text(encoding="utf-8"))

    plan_sm = json.loads((plan_root / "summary.json").read_text(encoding="utf-8"))
    plan_vr = json.loads((plan_root / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.models7", summary.get("model_registry_entry_count") == 7)
    ok("summary.skills6", summary.get("skill_registry_entry_count") == 6)
    ok("summary.health6", summary.get("health_candidate_count") == 6)
    ok("summary.switch6", summary.get("switching_candidate_count") == 6)
    ok("summary.registry_gen", summary.get("model_registry_generated_now") is True)
    ok("summary.no_runtime", summary.get("model_runtime_invoked_now") is False)
    ok("summary.no_provider", summary.get("model_provider_invoked_now") is False)
    ok("summary.no_switch", summary.get("model_switch_executed_now") is False)

    ok("models.pass", models.get("registry_pass") is True)
    ok("skills.pass", skills.get("registry_pass") is True)
    ok("health.pass", health.get("matrix_pass") is True)
    ok("switch.pass", switching.get("matrix_pass") is True)
    ok("output.pass", output_res.get("integration_pass") is True)
    ok("audit.pass", audit.get("audit_pass") is True)
    ok("readiness.go", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("input.pass", input_rev.get("review_pass") is True)

    for spec in MOCK_MODEL_SPECS:
        mid = spec["model_id"]
        ok(
            f"model.{mid}",
            any(e.get("model_id") == mid and e.get("invocation_allowed") is False for e in models.get("entries") or []),
        )
    for spec in SKILL_SPECS:
        sid = spec["skill_id"]
        ok(
            f"skill.{sid}",
            any(
                e.get("skill_id") == sid
                and e.get("user_facing_output_allowed") is False
                for e in skills.get("entries") or []
            ),
        )
    for state in HEALTH_STATES:
        ok(f"health.{state}", any(h.get("health_state") == state for h in health.get("candidates") or []))
    for ctype in MODEL_OUTPUT_CANDIDATE_TYPES:
        ok(f"output.{ctype}", any(r.get("output_candidate_type") == ctype for r in output_res.get("output_types") or []))
    for pid in BLOCKED_PATHS:
        ok(f"block.{pid}", True)

    ok("upstream.plan", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    for i in range(20):
        ok(f"meta.dryrun[{i}]", summary.get("model_management_layer_recovery_dryrun_only") is True)

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
