# -*- coding: utf-8 -*-
"""
最小 smoke：1 帧 DecisionMonitor JSONL，校验 environment_task_context_reserve 与关键摘要字段。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402


def main() -> int:
    stamp = os.environ.get("SMOKE_STAMP") or "smoke"
    out = ROOT / "logs" / f"smoke_environment_task_context_reserve_{stamp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    ctx = {
        "frame_seq": 1,
        "trace_anchor_id": f"smoke_etc_{stamp}",
        "current_ts": 0.0,
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
        "confirmation_input_raw_text": "找到了",
        "confirmation_input_type": "target_found",
    }

    b = DecisionMonitorBuilder()
    d = b.build(ctx).to_dict()

    etc = d.get("environment_task_context_reserve")
    ok = (
        isinstance(etc, dict)
        and bool(etc.get("context_premise_applied"))
        and bool(etc.get("context_premise_summary"))
        and isinstance(etc.get("environment_context"), dict)
        and isinstance(etc.get("task_chain_context"), dict)
    )
    ec = etc.get("environment_context") if isinstance(etc, dict) else {}
    tc = etc.get("task_chain_context") if isinstance(etc, dict) else {}
    ok = ok and bool(ec.get("environment_scene_type")) and bool(tc.get("task_chain_stage"))

    with out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("jsonl_path:", str(out))
    print("environment_task_context_reserve_ok:", ok)
    if isinstance(etc, dict):
        print("environment_scene_type:", (ec or {}).get("environment_scene_type"))
        print("task_chain_stage:", (tc or {}).get("task_chain_stage"))
        print("context_premise_summary:", (etc.get("context_premise_summary") or "")[:120] + "...")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
