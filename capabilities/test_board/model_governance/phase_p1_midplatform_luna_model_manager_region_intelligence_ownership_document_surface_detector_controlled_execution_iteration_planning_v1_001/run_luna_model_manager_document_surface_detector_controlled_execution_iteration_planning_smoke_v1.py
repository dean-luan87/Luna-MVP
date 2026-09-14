# -*- coding: utf-8 -*-
"""Run iteration planning smoke v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _repo() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


_REPO = _repo()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_planning_adapter_v1 import (  # noqa: E402
    FINAL_GO,
    run_iteration_planning,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_v1_001.luna_model_manager_document_surface_detector_controlled_execution_iteration_planning_smoke_v1 import (  # noqa: E402
    run_smoke_cases,
)


def main() -> int:
    run_iteration_planning(repo_root=_REPO, write_outputs=True)
    result = run_smoke_cases()
    out = _REPO / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_v1_smoke_v0"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "iteration_planning_smoke_summary.json"
    summary = {k: v for k, v in result.items() if k != "smoke_cases"}
    summary["case_summaries"] = [{"case_id": c["case_id"], "passed": c["passed"]} for c in result.get("smoke_cases", [])]
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "final_decision": result.get("adapter_final_decision") or result.get("final_decision"),
        "smoke_passed": result.get("smoke_passed"),
        "failed_checks": result.get("failed_checks"),
        "recommended_next_phase": result.get("recommended_next_phase"),
        "output": str(path),
    }, indent=2, ensure_ascii=False))
    ok = (result.get("adapter_final_decision") == FINAL_GO or result.get("final_decision") == FINAL_GO) and not result.get("failed_checks")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
