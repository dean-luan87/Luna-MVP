import argparse
import json
from typing import Any, Dict, List


def load_snapshots(path: str) -> List[Dict[str, Any]]:
    snapshots = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            bc_snapshot = record.get("decision_trace", {}).get("bc_snapshot")
            if bc_snapshot:
                snapshots.append(bc_snapshot)
    return snapshots


def format_line(index: int, snapshot: Dict[str, Any]) -> str:
    authority = snapshot.get("authority", {})
    risk = snapshot.get("risk", {})
    blocked_by = authority.get("blocked_by") or ""
    eff = authority.get("effective", "NA")
    risk_level = risk.get("level", "NONE")
    return f"T-{index:02d} | Authority {eff} | Risk {risk_level:<6} | BLOCKED_BY {blocked_by}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="jsonl file containing decision_trace")
    parser.add_argument("--last", type=int, default=30, help="number of recent snapshots")
    args = parser.parse_args()

    snapshots = load_snapshots(args.path)
    snapshots.sort(key=lambda s: s.get("authority", {}).get("since", 0.0))
    snapshots = snapshots[-args.last :]
    for idx, snap in enumerate(reversed(snapshots), start=1):
        print(format_line(idx, snap))


if __name__ == "__main__":
    main()
