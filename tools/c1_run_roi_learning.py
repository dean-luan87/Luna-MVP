from __future__ import annotations

import json
import argparse
import sys
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from roi_learning_c1 import run_c1_from_timeline


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", required=True, help="timeline jsonl path")
    ap.add_argument("--out", required=True, help="output proposals json path")
    args = ap.parse_args()

    proposals = run_c1_from_timeline(args.timeline)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in proposals], f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(proposals)} proposals to {args.out}")


if __name__ == "__main__":
    main()
