from core.logging import get_logger

log = get_logger("stress_nav_stuck_collector")
"""
从 telemetry / nav_stuck_events.jsonl 中统计 NAV_STUCK 次数，
写入 test_reports/stress_nav_metrics.json，
供 LNB 评分与 dashboard 使用。
"""

import json
from pathlib import Path
from typing import Dict, Any


def _safe_load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def collect_nav_stuck_metrics(
    telemetry_path: Path = Path("test_reports/telemetry.jsonl"),
    nav_stub_path: Path = Path("test_reports/nav_stuck_events.jsonl"),
    out_path: Path = Path("test_reports/stress_nav_metrics.json"),
) -> Dict[str, Any]:
    nav_stuck_count = 0

    # 1）从 nav_stuck_events.jsonl 读取
    if nav_stub_path.exists():
        with nav_stub_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                except Exception:
                    continue
                code = evt.get("code")
                if code == "NAV_STUCK":
                    nav_stuck_count += 1

    # 2）补充从 telemetry.jsonl 读取（如果有）
    if telemetry_path.exists():
        with telemetry_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                except Exception:
                    continue
                if evt.get("type") == "error" and evt.get("code") == "NAV_STUCK":
                    nav_stuck_count += 1

    out = {
        "nav_stuck_errors": nav_stuck_count,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    res = collect_nav_stuck_metrics()
    log.info("nav_stuck metrics:", res")


















