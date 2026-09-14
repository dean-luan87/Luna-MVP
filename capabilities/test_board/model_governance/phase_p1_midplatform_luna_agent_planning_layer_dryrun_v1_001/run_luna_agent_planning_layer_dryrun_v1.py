# -*- coding: utf-8
"""Run Luna Agent Planning Layer dry-run v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


_REPO = _detect_repo_root()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (  # noqa: E402
    run_all_dryrun_cases,
)


def main() -> int:
    result = run_all_dryrun_cases()
    out_dir = _REPO / "_tmp_eval_out" / "p1_midplatform_luna_agent_planning_layer_dryrun_v1_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "dryrun_summary.json"

    summary = {
        "final_decision": result["final_decision"],
        "dryrun_cases_passed": result.get("dryrun_cases_passed"),
        "dryrun_case_count": result.get("dryrun_case_count"),
        "failed_checks": result.get("failed_checks", []),
        "core_validations": result.get("core_validations"),
        "job_564f1aa93983_l2_result": result.get("job_564f1aa93983_l2_result"),
        "case_summaries": [
            {
                "case_id": c.get("case_id"),
                "passed": c.get("passed"),
                "l1_scene": (c.get("result") or {})
                .get("situation_understanding_candidate", {})
                .get("scene_profile_candidate", {})
                .get("scene_type"),
                "l2_goal": ((c.get("result") or {}).get("selected_plan_candidate") or {})
                .get("plan_goal_candidate", {})
                .get("goal_type"),
                "tools": ((c.get("result") or {}).get("tool_plan_summary") or {}).get("active"),
                "noops": ((c.get("result") or {}).get("tool_plan_summary") or {}).get("noop"),
                "selected_slot": ((c.get("result") or {}).get("plan_competition") or {}).get("selected_slot"),
            }
            for c in result.get("dryrun_cases", [])
        ],
    }
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    full_path = out_dir / "dryrun_full_result.json"
    # Drop bulky nested plan objects for full dump size control — keep per-case assertions
    slim_cases = []
    for c in result.get("dryrun_cases", []):
        r = c.get("result") or {}
        slim_cases.append({
            "case_id": c.get("case_id"),
            "passed": c.get("passed"),
            "assertions": c.get("assertions"),
            "l1_scene": (r.get("situation_understanding_candidate") or {}).get("scene_profile_candidate", {}).get("scene_type"),
            "l2_goal": (r.get("selected_plan_candidate") or {}).get("plan_goal_candidate", {}).get("goal_type"),
            "tool_plan_summary": r.get("tool_plan_summary"),
            "handoff": r.get("tool_os_handoff_candidate"),
            "selection_trace": (r.get("plan_competition") or {}).get("selection_trace"),
            "l1_drives_l2": r.get("l1_drives_l2_assertion"),
            "l2_constrains_tools": r.get("l2_constrains_tools_assertion"),
        })
    full_path.write_text(json.dumps({
        **{k: v for k, v in result.items() if k != "dryrun_cases"},
        "dryrun_cases_slim": slim_cases,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "final_decision": result["final_decision"],
        "dryrun_cases_passed": result.get("dryrun_cases_passed"),
        "dryrun_case_count": result.get("dryrun_case_count"),
        "failed_checks": result.get("failed_checks", []),
        "core_validations": result.get("core_validations"),
        "job_564f1aa93983_l2_result": result.get("job_564f1aa93983_l2_result"),
        "output": str(out_path),
    }, indent=2, ensure_ascii=False))
    return 0 if result["final_decision"].endswith("_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
