from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path


if __package__ in {None, ""}:
    REPO_ROOT = Path(__file__).resolve().parents[4]
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_engine_v1 import (
    ContextPcnIntentMainlineEngineV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_fixture_v1 import (
    get_context_pcn_intent_fixture_cases_v1,
)


OUTPUT_DIR = (
    REPO_ROOT / "_eval_out/context_pcn_intent_mainline_controlled_integration_v1"
)


def run_controlled_integration() -> dict[str, object]:
    engine = ContextPcnIntentMainlineEngineV1()
    directives = tuple(
        item.directive for item in get_context_pcn_intent_fixture_cases_v1()
    )
    payload = engine.run_all(directives)
    return {
        "summary": asdict(payload.summary),
        "scenario_results": [asdict(item) for item in payload.scenario_results],
        "artifacts": payload.artifacts,
    }


def write_outputs(payload: dict[str, object]) -> dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUTPUT_DIR / "context_pcn_intent_summary_v1.json"
    scenario_path = OUTPUT_DIR / "context_pcn_intent_scenarios_v1.json"

    summary_path.write_text(
        json.dumps(payload["summary"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    scenario_path.write_text(
        json.dumps(payload["scenario_results"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {"summary": str(summary_path), "scenarios": str(scenario_path)}


def main() -> int:
    payload = run_controlled_integration()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
