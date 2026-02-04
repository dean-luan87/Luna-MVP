import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from c.controller import decide
from c.types import CDecision


def load_trace(path: Path) -> List[dict]:
    records = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def check_decision_rules() -> Dict[str, bool]:
    base = {
        "health": {"perception": "ok"},
        "perception_facts": {},
        "device_state": {},
    }
    snap_lost = dict(base)
    snap_lost["health"] = {"perception": "lost"}
    snap_obstacle = dict(base)
    snap_obstacle["perception_facts"] = {"obstacle_distance": 0.3}

    res_lost = decide(snap_lost)
    res_obstacle = decide(snap_obstacle)
    res_ok = decide(base)

    return {
        "perception_lost_is_hold": res_lost.decision == CDecision.HOLD,
        "obstacle_close_is_stop": res_obstacle.decision == CDecision.STOP,
        "no_risk_is_pass": res_ok.decision == CDecision.PASS,
    }


def check_trace_contains_c_decision(records: List[dict]) -> Dict[str, bool]:
    has_c_decision = False
    has_execution_intent = False
    has_reason = False
    for record in records:
        c_decision = record.get("c_decision")
        if isinstance(c_decision, dict):
            has_c_decision = True
            if "reason" in c_decision:
                has_reason = True
        if "execution_intent" in record:
            has_execution_intent = True
    return {
        "trace_has_c_decision": has_c_decision,
        "trace_has_execution_intent": has_execution_intent,
        "trace_has_reason": has_reason,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True, help="trace jsonl path")
    parser.add_argument("--out", help="optional output json path")
    args = parser.parse_args()

    records = load_trace(Path(args.trace))
    rule_checks = check_decision_rules()
    trace_checks = check_trace_contains_c_decision(records)

    result = {
        "trace_records": len(records),
        "checks": {**rule_checks, **trace_checks},
        "gate_pass": all([*rule_checks.values(), *trace_checks.values()]),
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    print(output)

    if not result["gate_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
