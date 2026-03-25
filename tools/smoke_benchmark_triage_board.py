# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from tools.benchmark_triage_board import build_triage_board, load_results_from_input  # noqa: E402


def main() -> int:
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    inp = ROOT / "logs" / "real_scenario_pack_m0.json"
    out = ROOT / "logs" / f"smoke_benchmark_triage_board_{stamp}.json"

    results = load_results_from_input(str(inp))
    board = build_triage_board(results)
    payload = {
        "triage_summary": board.triage_summary,
        "next_focus_case_ids": board.next_focus_case_ids,
        "next_focus_modules": board.next_focus_modules,
        "next_focus_issue_types": board.next_focus_issue_types,
        "top_cases": [c.__dict__ for c in board.ranked_cases[:5]],
        "top_modules": [m.__dict__ for m in board.ranked_modules[:5]],
        "top_issues": [i.__dict__ for i in board.ranked_issues[:5]],
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = True
    ok = ok and bool(board.next_focus_case_ids)
    ok = ok and bool(board.next_focus_modules)
    ok = ok and bool(board.next_focus_issue_types)
    ok = ok and bool(board.triage_summary)

    print("out_path:", str(out))
    print("triage_summary:", board.triage_summary)
    print("next_focus_case_ids:", board.next_focus_case_ids[:3])
    print("next_focus_modules:", board.next_focus_modules[:3])
    print("next_focus_issue_types:", board.next_focus_issue_types[:3])
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

