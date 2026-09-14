# -*- coding: utf-8 -*-
"""Run controlled execution dryrun smoke v1."""

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

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_execution_dryrun_adapter_v1 import (  # noqa: E402
    FINAL_BLOCKED_BY_MISSING_FIXTURES,
    FINAL_GO,
    run_controlled_execution_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_smoke_v1 import (  # noqa: E402
    run_smoke_cases,
)


def main() -> int:
    run_controlled_execution_dryrun(repo_root=_REPO, write_outputs=True)
    result = run_smoke_cases()
    out_dir = _REPO / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "controlled_execution_dryrun_smoke_summary.json"
    summary = {k: v for k, v in result.items() if k != "smoke_cases"}
    summary["case_summaries"] = [{"case_id": c.get("case_id"), "passed": c.get("passed")} for c in result.get("smoke_cases", [])]
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fd = result.get("final_decision")
    print(json.dumps({
        "final_decision": fd,
        "dryrun_final_decision": result.get("dryrun_final_decision"),
        "smoke_passed": result.get("smoke_passed"),
        "real_execution_enabled": False,
        "failed_checks": result.get("failed_checks", []),
        "recommended_next_phase": result.get("recommended_next_phase"),
        "output": str(out_path),
    }, indent=2, ensure_ascii=False))
    ok = fd in (FINAL_GO, FINAL_BLOCKED_BY_MISSING_FIXTURES) and not result.get("failed_checks")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
