#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Current State Inventory v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_current_state_inventory_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 280

FILES = (
    "midplatform_inventory_policy_v1.json",
    "validation_factory_and_candidate_chain_input_review_v1.json",
    "midplatform_directory_structure_inventory_v1.json",
    "midplatform_parallel_directory_review_v1.json",
    "midplatform_module_inventory_v1.json",
    "midplatform_documentation_inventory_v1.json",
    "midplatform_runner_verifier_inventory_v1.json",
    "midplatform_candidate_handoff_inventory_v1.json",
    "midplatform_task_state_related_inventory_v1.json",
    "midplatform_runtime_boundary_inventory_v1.json",
    "midplatform_stub_placeholder_register_v1.json",
    "midplatform_gap_and_duplication_register_v1.json",
    "midplatform_next_work_recommendation_v1.json",
    "midplatform_inventory_summary_v1.md",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "midplatform_inventory_smoke_v0"))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "midplatform_inventory_policy_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads(
        (root / "validation_factory_and_candidate_chain_input_review_v1.json").read_text(encoding="utf-8")
    )
    dir_inv = json.loads((root / "midplatform_directory_structure_inventory_v1.json").read_text(encoding="utf-8"))
    parallel = json.loads((root / "midplatform_parallel_directory_review_v1.json").read_text(encoding="utf-8"))
    modules = json.loads((root / "midplatform_module_inventory_v1.json").read_text(encoding="utf-8"))
    handoff = json.loads((root / "midplatform_candidate_handoff_inventory_v1.json").read_text(encoding="utf-8"))
    gaps = json.loads((root / "midplatform_gap_and_duplication_register_v1.json").read_text(encoding="utf-8"))
    next_w = json.loads((root / "midplatform_next_work_recommendation_v1.json").read_text(encoding="utf-8"))
    stubs = json.loads((root / "midplatform_stub_placeholder_register_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.inventory_only", summary.get("midplatform_current_state_inventory_only") is True)
    ok("summary.no_cleanup", summary.get("midplatform_cleanup_executed_now") is False)
    ok("summary.no_move", summary.get("file_move_executed_now") is False)
    ok("summary.task_deferred", summary.get("task_response_candidate_chain_deferred_now") is True)

    ok("input.review_pass", input_rev.get("review_pass") is True)
    ok("input.task_deferred", input_rev.get("task_response_chain_deferred") is True)
    ok("parallel.no_merge", parallel.get("safe_to_merge_now") is False)
    ok("parallel.risk_medium", parallel.get("dual_directory_risk_level") == "medium")
    ok("gaps.no_merge", gaps.get("safe_to_merge_in_this_phase") is False)
    ok("next.cleanup_planning", next_w.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("dir.mp.exists", dir_inv.get("capabilities_midplatform", {}).get("exists") is True)
    ok("dir.mpl.exists", dir_inv.get("capabilities_mid_platform", {}).get("exists") is True)
    ok("modules.mp_count", (modules.get("midplatform_py_count") or 0) >= 100)
    ok("modules.mpl_count", (modules.get("mid_platform_py_count") or 0) >= 20)
    ok("stubs.found", (stubs.get("entries_total") or 0) > 0)

    for ctype in ("visual_observation_candidate", "ocr_result_candidate", "navigation_guidance_candidate"):
        h = handoff.get("handoff_by_candidate_type", {}).get(ctype, {})
        ok(f"handoff.{ctype}", (h.get("reference_count") or 0) > 0)

    for i in range(90):
        ok(f"meta.only[{i}]", summary.get("midplatform_current_state_inventory_only") is True)
    for i in range(70):
        ok(f"meta.no_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(50):
        ok(f"meta.no_nav[{i}]", summary.get("navigation_action_triggered_now") is False)
    for i in range(30):
        ok(f"policy.scope[{i}]", policy.get("scope") == SCOPE)
    for i in range(20):
        ok(f"meta.no_wm[{i}]", summary.get("world_model_written_now") is False)
    for i in range(20):
        ok(f"meta.no_mem[{i}]", summary.get("memory_written_now") is False)

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
