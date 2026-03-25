# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from tools.real_scenario_pack import run_real_cases  # noqa: E402


def main() -> int:
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    out = ROOT / "logs" / f"smoke_real_scenario_pack_{stamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    # smoke: 至少跑 2 个真实 case
    results, summary = run_real_cases()
    payload = {"summary": summary, "results": [r.__dict__ for r in results]}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = True
    ok = ok and summary.get("total_cases", 0) >= 2
    ok = ok and "quality_grade_distribution" in summary
    ok = ok and all(getattr(r, "case_id", None) for r in results)
    ok = ok and all(getattr(r, "quality_grade", None) is not None for r in results)

    print("out_path:", str(out))
    print("summary:", json.dumps(summary, ensure_ascii=False))
    for r in results[:3]:
        print("case:", r.case_id, "grade:", r.quality_grade, "issue:", r.issue_type, "hint:", r.optimization_hint_type, "passed:", r.scenario_passed)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

