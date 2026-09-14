# -*- coding: utf-8 -*-
"""Run controlled execution preflight smoke v1."""

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

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_preflight_adapter_v1 import (  # noqa: E402
    run_controlled_execution_preflight,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_001.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_smoke_v1 import (  # noqa: E402
    run_smoke_cases,
)


def main() -> int:
    run_controlled_execution_preflight(repo_root=_REPO, write_outputs=True)
    result = run_smoke_cases()
    out_dir = _REPO / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "controlled_execution_preflight_smoke_summary.json"
    summary = {k: v for k, v in result.items() if k != "smoke_cases"}
    summary["case_summaries"] = [{"case_id": c.get("case_id"), "passed": c.get("passed")} for c in result.get("smoke_cases", [])]
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "final_decision": result["final_decision"],
        "smoke_passed": result.get("smoke_passed"),
        "cv2_available_candidate": result.get("cv2_available_candidate"),
        "real_execution_enabled": False,
        "failed_checks": result.get("failed_checks", []),
        "recommended_next_phase": result.get("recommended_next_phase"),
        "output": str(out_path),
    }, indent=2, ensure_ascii=False))
    ok = result["final_decision"] in (
        "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO",
        "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO_WITH_DEPENDENCY_BLOCKED",
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
