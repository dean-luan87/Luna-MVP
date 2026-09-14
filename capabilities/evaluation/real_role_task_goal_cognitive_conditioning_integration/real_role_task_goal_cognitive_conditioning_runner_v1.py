"""User-terminal Runner for real OCR same-evidence conditioning contrasts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .case_definitions_v1 import build_conditioning_contrasts_v1
from .engine_v1 import PHASE, RealRoleTaskGoalConditioningEngineV1, _jsonable


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/real_role_task_goal_cognitive_conditioning_integration_v1"


def build_runner_summary_v1() -> dict:
    engine = RealRoleTaskGoalConditioningEngineV1(repository_root=ROOT)
    return engine.run(build_conditioning_contrasts_v1(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real OCR same-evidence Role/Task/Goal cognitive conditioning.")
    parser.parse_args()
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(_jsonable(summary), indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(_jsonable(summary), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
