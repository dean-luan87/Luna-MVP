import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from luna_badge_v1_2.governance.risk_center.vo.evaluator import evaluate_vo
from luna_badge_v1_2.governance.risk_center.interfaces.snapshot import build_world_snapshot


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 tools/risk/run_vo_demo.py <system_snapshot.json>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r") as f:
        system_snapshot = json.loads(f.read())
    world_snapshot = build_world_snapshot(system_snapshot)
    projection = evaluate_vo(world_snapshot)
    print(
        json.dumps(
            {
                "time_to_risk": projection.time_to_risk,
                "min_distance": projection.min_distance,
                "level": projection.level,
                "schema_version": projection.schema_version,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
