# -*- coding: utf-8 -*-
"""
最小 smoke：生成 1 帧 DecisionMonitor JSONL，并验证 confirmation_whitebox_trace 字段存在。

约束：
- 不跑视频、不跑长 trace
- 输出写入 logs/ 下独立文件
- 终端输出仅摘要
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.logger import DecisionMonitorLogger  # noqa: E402


def _read_first_line(jsonl_path: str) -> dict:
    p = Path(jsonl_path)
    if not p.exists():
        raise RuntimeError(f"JSONL 未生成: {jsonl_path}")
    first = p.read_text(encoding="utf-8").splitlines()[0]
    return json.loads(first)


def main() -> None:
    logs_dir = _ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    jsonl_path = str(logs_dir / f"smoke_confirmation_whitebox_trace_{stamp}.jsonl")

    # 用 env 模拟最小用户反馈（容器流：打开了）
    os.environ["CONFIRMATION_INPUT_TYPE"] = ""
    os.environ["CONFIRMATION_INPUT_RAW_TEXT"] = "打开了"

    ctx = {
        "trace_anchor_id": f"smoke_{stamp}",
        "input_source_type": "smoke",
        "input_source_path": str(_ROOT / "find_test.jpg"),
        "focus_object_label": "药瓶",
        "visual_audit_objects": [
            {"label": "cup", "bbox": [0.10, 0.10, 0.60, 0.70]},
            {"label": "bottle", "bbox": [0.25, 0.25, 0.45, 0.60]},
        ],
        "visual_audit_texts": [],
        "visual_audit_description": "smoke: confirmation opened_container mapping from raw text",
        "input_image_width": 640,
        "input_image_height": 480,
        "skip_human_check": True,
        "sampled": True,
        "route": "smoke",
    }

    builder = DecisionMonitorBuilder(trace_anchor_id_prefix="smoke")
    frame = builder.build(ctx)
    DecisionMonitorLogger(jsonl_path=jsonl_path, emit_console_summary=False).write(frame)

    d = _read_first_line(jsonl_path)
    has_cwb = "confirmation_whitebox_trace" in d
    cwb = d.get("confirmation_whitebox_trace") if isinstance(d, dict) else None
    has_steps = bool(isinstance(cwb, dict) and isinstance(cwb.get("reasoning_steps"), list) and len(cwb["reasoning_steps"]) >= 4)

    print(
        json.dumps(
            {
                "jsonl_path": jsonl_path,
                "has_confirmation_whitebox_trace": has_cwb,
                "reasoning_steps_ge_4": has_steps,
                "summary_preview": (cwb.get("whitebox_summary") if isinstance(cwb, dict) else "")[:100],
            },
            ensure_ascii=False,
        )
    )

    if not has_cwb:
        raise AssertionError("frame 中缺少 confirmation_whitebox_trace")
    if not has_steps:
        raise AssertionError("confirmation_whitebox_trace.reasoning_steps < 4")


if __name__ == "__main__":
    main()

