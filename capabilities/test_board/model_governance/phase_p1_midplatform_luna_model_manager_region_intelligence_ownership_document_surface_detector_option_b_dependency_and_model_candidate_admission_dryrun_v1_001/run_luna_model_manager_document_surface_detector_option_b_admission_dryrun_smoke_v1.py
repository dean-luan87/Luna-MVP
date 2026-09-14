# -*- coding: utf-8 -*-
"""Run Option B admission dryrun smoke v1."""

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

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_admission_dryrun_adapter_v1 import (  # noqa: E402
    FINAL_GO,
    run_option_b_admission_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1_001.luna_model_manager_document_surface_detector_option_b_admission_dryrun_smoke_v1 import (  # noqa: E402
    run_smoke_cases,
)


def main() -> int:
    run_option_b_admission_dryrun(repo_root=_REPO, write_outputs=True)
    result = run_smoke_cases()
    out_dir = _REPO / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "option_b_admission_dryrun_smoke_summary.json"
    summary = {k: v for k, v in result.items() if k != "smoke_cases"}
    summary["case_summaries"] = [{"case_id": c.get("case_id"), "passed": c.get("passed")} for c in result.get("smoke_cases", [])]
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({**summary, "output": str(out_path)}, indent=2, ensure_ascii=False))
    return 0 if result.get("final_decision") == FINAL_GO and not result.get("failed_checks") else 1


if __name__ == "__main__":
    raise SystemExit(main())
