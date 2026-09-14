from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 确保仓库根在 path，便于直接运行
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from observe.semantic_stability.learner import SemanticStabilityLearner


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", required=True, help="timeline jsonl path")
    ap.add_argument("--out", required=True, help="output json path")
    ap.add_argument("--environment-id", default="device_default")
    ap.add_argument("--scope", default="device_local")
    args = ap.parse_args()

    learner = SemanticStabilityLearner()
    profiles = learner.learn_from_timeline_jsonl(
        args.timeline,
        environment_id=args.environment_id,
        scope=args.scope,
    )

    out = []
    for p in profiles:
        out.append(
            {
                "roi_kind": p.key.roi_kind,
                "category": p.key.category,
                "meaning": p.key.meaning,
                "stability": p.score.stability,
                "confidence": p.score.confidence,
                "suggestion": p.suggestion,
                "environment_id": p.environment_id,
                "scope": p.scope,
                "evidence": p.score.evidence,
            }
        )

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
