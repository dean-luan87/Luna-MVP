# -*- coding: utf-8 -*-
"""Run document surface detector post-review v1."""

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

from capabilities.midplatform.model_manager.runtime.document_surface.post_review.document_surface_detector_post_review_adapter_v1 import (  # noqa: E402
    run_document_surface_detector_post_review,
)


def main() -> int:
    result = run_document_surface_detector_post_review(repo_root=_REPO, write_outputs=True)
    print(json.dumps({
        "final_decision": result["final_decision"],
        "review_passed_count": result.get("review_passed_count"),
        "review_failed_count": result.get("review_failed_count"),
        "blocker_count": result.get("blocker_count"),
        "boundary_status": result.get("boundary_status"),
        "recommended_next_phase": result.get("recommended_next_phase"),
        "parallel_next_track": result.get("parallel_next_track"),
        "failed_checks": result.get("failed_checks", []),
        "output_dir": result.get("output_dir"),
    }, indent=2, ensure_ascii=False))
    return 0 if result["final_decision"].endswith("_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
