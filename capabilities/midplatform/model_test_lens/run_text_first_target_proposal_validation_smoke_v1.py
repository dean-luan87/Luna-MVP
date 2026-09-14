# -*- coding: utf-8
"""Run text-first target proposal validation planning smoke v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


_REPO = _detect_repo_root()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from capabilities.midplatform.model_test_lens.target_proposal.text_first_target_proposal_validation_smoke_v1 import (  # noqa: E402
    run_smoke_cases,
)


def main() -> int:
    result = run_smoke_cases()
    out_dir = _REPO / "_tmp_eval_out" / "p1_midplatform_text_first_target_proposal_validation_planning_v1_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "text_first_target_proposal_validation_smoke_v1.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "final_decision": result["final_decision"],
        "smoke_passed": result.get("smoke_passed"),
        "smoke_case_count": result.get("smoke_case_count"),
        "failed_checks": result.get("failed_checks", []),
        "output": str(out_path),
    }, indent=2, ensure_ascii=False))
    return 0 if result["final_decision"].endswith("_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
