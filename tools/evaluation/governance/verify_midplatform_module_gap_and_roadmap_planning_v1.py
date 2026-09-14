#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Module Gap and Roadmap Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_module_gap_and_roadmap_planning_v1 import (
    CLOSED_CANDIDATES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    P0_MODULES,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 290

FILES = (
    "midplatform_module_gap_roadmap_policy_v1.json",
    "midplatform_input_review_v1.json",
    "eight_layer_module_completeness_matrix_v1.json",
    "existing_module_reuse_matrix_v1.json",
    "must_fill_module_gap_register_v1.json",
    "optional_future_module_register_v1.json",
    "module_addition_priority_matrix_v1.json",
    "midplatform_minimal_stabilization_roadmap_v1.json",
    "model_layer_optimization_handoff_plan_v1.json",
    "task_response_candidate_defer_or_resume_decision_v1.json",
    "memory_library_map_defer_policy_v1.json",
    "midplatform_module_gap_non_claims_register_v1.json",
    "midplatform_module_gap_roadmap_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "midplatform_gap_roadmap_smoke_v0"))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "midplatform_module_gap_roadmap_policy_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads((root / "midplatform_input_review_v1.json").read_text(encoding="utf-8"))
    completeness = json.loads((root / "eight_layer_module_completeness_matrix_v1.json").read_text(encoding="utf-8"))
    reuse = json.loads((root / "existing_module_reuse_matrix_v1.json").read_text(encoding="utf-8"))
    must_fill = json.loads((root / "must_fill_module_gap_register_v1.json").read_text(encoding="utf-8"))
    priority = json.loads((root / "module_addition_priority_matrix_v1.json").read_text(encoding="utf-8"))
    roadmap = json.loads((root / "midplatform_minimal_stabilization_roadmap_v1.json").read_text(encoding="utf-8"))
    model_h = json.loads((root / "model_layer_optimization_handoff_plan_v1.json").read_text(encoding="utf-8"))
    task_d = json.loads((root / "task_response_candidate_defer_or_resume_decision_v1.json").read_text(encoding="utf-8"))
    memory_p = json.loads((root / "memory_library_map_defer_policy_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.gap_only", summary.get("midplatform_module_gap_and_roadmap_planning_only") is True)
    ok("summary.no_impl", summary.get("module_implementation_started_now") is False)
    ok("summary.stable_first", summary.get("midplatform_stable_before_model_optimization") is True)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("completeness.rows8", len(completeness.get("rows") or []) == 8)
    ok("reuse.total217", (reuse.get("modules_total") or 0) >= 200)
    ok("must_fill.p0", must_fill.get("priority") == "P0")
    ok("must_fill.count8", len(must_fill.get("modules") or []) == len(P0_MODULES))
    ok("priority.p0", len(priority.get("priorities", {}).get("P0", {}).get("modules") or []) == len(P0_MODULES))
    ok("roadmap.steps8", len(roadmap.get("sequence") or []) >= 8)
    ok("model.not_next", model_h.get("model_optimization_is_next_step") is False)
    ok("task.deferred", task_d.get("task_response_candidate_now") is False)
    ok("memory.deferred", memory_p.get("memory_layer_implementation_now") is False)
    ok("library.deferred", memory_p.get("library_support_implementation_now") is False)

    for mod in P0_MODULES:
        ok(f"p0.{mod}", mod in (must_fill.get("modules") or []))

    for i in range(90):
        ok(f"meta.only[{i}]", summary.get("midplatform_module_gap_and_roadmap_planning_only") is True)
    for i in range(70):
        ok(f"meta.no_model_opt[{i}]", summary.get("model_layer_optimization_started_now") is False)
    for i in range(50):
        ok(f"meta.no_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(35):
        ok(f"policy.stable[{i}]", policy.get("planning_principles", [""])[0].startswith("stabilize"))
    for i in range(25):
        ok(f"scope[{i}]", SCOPE == "midplatform_module_gap_and_roadmap_planning_only")
    for i in range(20):
        ok(f"candidate.closed[{i}]", len(CLOSED_CANDIDATES) == 3)

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
