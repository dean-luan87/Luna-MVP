import json
import sys
from typing import Any, Dict, List


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 tools/dump_debug_view.py <bc_snapshot_jsonl>")
        sys.exit(1)

    path = sys.argv[1]
    outputs: List[Dict[str, Any]] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            debug_view = record.get("decision_trace", {}).get("bc_snapshot", {}).get("debug_view")
            if debug_view is not None:
                outputs.append(debug_view)

    print(json.dumps(outputs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
