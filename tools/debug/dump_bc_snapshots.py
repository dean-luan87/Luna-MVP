import argparse
import json
from typing import Any, Dict, List

# === Alignment Note ===
# CLI name aligns with "dump_debug_view" in the issue spec.
# This file is the stable implementation.


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
    parser.add_argument("--last", type=int, default=20, help="number of recent snapshots")
    parser.add_argument("--format", choices=["json"], default="json")
    args = parser.parse_args()

    snapshots = load_snapshots(args.path)[-args.last :]
    print(json.dumps(snapshots, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
