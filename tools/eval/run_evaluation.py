import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from luna_badge_v1_2.governance.risk_center.evaluation.evaluator import evaluate_metrics
from luna_badge_v1_2.governance.risk_center.evaluation.reader import read_timeline_from_jsonl


def _load_timeline(path: str) -> List[Dict[str, Any]]:
    return read_timeline_from_jsonl(path)


def _filter_window(timeline: List[Dict[str, Any]], window: str) -> List[Dict[str, Any]]:
    if window.startswith("last_") and window.endswith("min"):
        minutes = float(window.replace("last_", "").replace("min", ""))
        cutoff = time.time() - minutes * 60
        return [item for item in timeline if item.get("authority_panel", {}).get("since", 0.0) >= cutoff]
    if window.startswith("last_"):
        count = int(window.replace("last_", ""))
        return timeline[-count:]
    return timeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="jsonl file containing decision_trace")
    parser.add_argument("--window", default="last_100", help="window spec: last_5min or last_100")
    args = parser.parse_args()

    timeline = _load_timeline(args.input)
    timeline = _filter_window(timeline, args.window)
    report = evaluate_metrics(timeline, args.window)
    print(json.dumps(report.__dict__, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
