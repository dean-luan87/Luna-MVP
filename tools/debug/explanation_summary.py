import argparse
import json
from collections import Counter
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="jsonl file containing decision_trace")
    parser.add_argument("--last", type=int, default=50, help="number of recent snapshots")
    args = parser.parse_args()

    snapshots = load_snapshots(args.path)[-args.last :]
    reason_counter = Counter()
    blocked_counter = Counter()

    for snap in snapshots:
        reasons = snap.get("risk", {}).get("reason_codes", []) or []
        reason_counter.update(reasons)
        blocked_by = snap.get("authority", {}).get("blocked_by")
        if blocked_by:
            blocked_counter.update([blocked_by])

    print("Risk reason_codes:")
    for key, count in reason_counter.most_common():
        print(f"{key}: {count}")

    print("\nAuthority blocked_by:")
    for key, count in blocked_counter.most_common():
        print(f"{key}: {count}")


if __name__ == "__main__":
    main()
