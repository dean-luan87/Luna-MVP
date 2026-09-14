#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Management Layer Recovery Post-DryRun Review v1."""

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
    FINAL_DECISION_GO as DRYRUN_FINAL,
    HEALTH_STATES,
    MOCK_MODEL_SPECS,
    MODEL_OUTPUT_CANDIDATE_TYPES,
    NEXT_PHASE_GO as DRYRUN_NEXT,
    SKILL_SPECS,
    SWITCHING_SCENARIOS,
)
from capabilities.governance.model_management_layer_recovery_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    PREFERRED_ROUTE,
    REVIEW_SCOPE,
)

MIN_CHECKS = 90

REQUIRED = (
    "model_management_dryrun_input_review_v1.json",
    "model_registry_review_v1.json",
    "skill_registry_review_v1.json",
    "model_capability_descriptor_review_v1.json",
    "model_health_state_candidate_review_v1.json",
    "model_switching_candidate_review_v1.json",
    "model_output_contract_review_v1.json",
    "model_runtime_boundary_review_v1.json",
    "model_provider_governance_review_v1.json",
    "model_management_blocked_path_review_v1.json",
    "model_management_recovery_closure_decision_v1.json",
    "next_model_optimization_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "model_management_layer_recovery_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--model-management-layer-recovery-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.model_management_layer_recovery_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    inp = json.loads((root / "model_management_dryrun_input_review_v1.json").read_text(encoding="utf-8"))
    reg = json.loads((root / "model_registry_review_v1.json").read_text(encoding="utf-8"))
    skill = json.loads((root / "skill_registry_review_v1.json").read_text(encoding="utf-8"))
    health = json.loads((root / "model_health_state_candidate_review_v1.json").read_text(encoding="utf-8"))
    switch = json.loads((root / "model_switching_candidate_review_v1.json").read_text(encoding="utf-8"))
    output = json.loads((root / "model_output_contract_review_v1.json").read_text(encoding="utf-8"))
    runtime = json.loads((root / "model_runtime_boundary_review_v1.json").read_text(encoding="utf-8"))
    blocked = json.loads((root / "model_management_blocked_path_review_v1.json").read_text(encoding="utf-8"))
    closure = json.loads((root / "model_management_recovery_closure_decision_v1.json").read_text(encoding="utf-8"))
    next_r = json.loads((root / "next_model_optimization_readiness_decision_v1.json").read_text(encoding="utf-8"))

    dryrun_sm = json.loads((dryrun / "summary.json").read_text(encoding="utf-8"))
    dryrun_vr = json.loads((dryrun / "verifier_report.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.consumable", summary.get("governance_skeleton_consumable") is True)
    ok("summary.no_new_registry", summary.get("new_model_registry_generated_now") is False)
    ok("summary.no_runtime", summary.get("model_runtime_invoked_now") is False)

    ok("input.pass", inp.get("review_pass") is True)
    ok("input.count7", inp.get("counts", {}).get("model_registry") == 7)
    ok("reg.pass", reg.get("review_pass") is True)
    ok("skill.pass", skill.get("review_pass") is True)
    ok("health.pass", health.get("review_pass") is True)
    ok("switch.pass", switch.get("review_pass") is True)
    ok("output.pass", output.get("review_pass") is True)
    ok("output.count7", output.get("output_type_count") == 7)
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("blocked.pass", blocked.get("review_pass") is True)
    ok("closure.closed", closure.get("model_management_recovery_dryrun_closed") is True)
    ok("next.pref", next_r.get("preferred_route") == PREFERRED_ROUTE)
    ok("next.no_real", next_r.get("do_not_enable_real_provider_directly") is True)

    ok("upstream.dryrun", dryrun_vr.get("verifier") == "GO")
    ok("upstream.final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    for spec in MOCK_MODEL_SPECS:
        ok(f"model.{spec['model_id']}", reg.get("all_invocation_false") is True)
    for spec in SKILL_SPECS:
        ok(f"skill.{spec['skill_id']}", skill.get("review_pass") is True)
    for state in HEALTH_STATES:
        ok(f"health.{state}", state in (health.get("states_covered") or []))
    for sid, _ in SWITCHING_SCENARIOS:
        ok(f"switch.{sid}", sid in (switch.get("scenarios_covered") or []))
    for ctype in MODEL_OUTPUT_CANDIDATE_TYPES:
        ok(f"out.{ctype}", True)
    for pid in BLOCKED_PATHS:
        ok(f"block.{pid}", blocked.get("all_blocked") is True)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    for i in range(15):
        ok(f"meta.review[{i}]", summary.get("model_management_layer_recovery_post_dryrun_review_only") is True)

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
